#!/usr/bin/env python
"""
Benchmark de rendimiento - MercadoTico 360 

Mide, sobre la base MongoDB ya cargada (ver README de la raiz):
  1. Consultas frecuentes SIN indice y CON indice (tiempo, docs examinados, explain).
  2. Agregaciones (ventas por categoria, ticket promedio, mas vendidos).
  3. Lecturas concurrentes (10, 50 y 100 hilos).
  4. Carga masiva (insercion de los JSON en colecciones temporales).

Uso (desde la raiz del repositorio, con el entorno virtual activo):
    python Performance/scripts/benchmark.py

Opciones utiles:
    --reps 30            repeticiones por consulta (default 30)
    --agg-reps 5         repeticiones por agregacion (default 5)
    --skip-concurrency   omite la prueba de concurrencia
    --skip-load          omite la prueba de carga masiva
    --keep-indexes       deja los indices creados al terminar

Lee MONGODB_URI y MONGODB_DB del archivo .env de la raiz.
Resultados en Performance/resultados/ (CSV, entorno.json y capturas de explain).

AVISO: el script BORRA y RECREA los indices listados en INDICES. No lo apuntes a
una base compartida (por ejemplo el Atlas del grupo) si alguien mas la esta usando.
"""

import argparse
import csv
import json
import math
import os
import platform
import random
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient

RAIZ = Path(__file__).resolve().parents[2]
SALIDA_DEFECTO = RAIZ / "Performance" / "resultados"


# Indices a evaluar: (coleccion, nombre, claves)

INDICES = [
    ("productos", "idx_categoria_precio", [("categoria", 1), ("precio", 1)]),
    ("productos", "idx_precio", [("precio", 1)]),
    ("productos", "idx_atributos_talla", [("atributos.talla", 1)]),
    ("productos", "idx_comercio", [("comercio_id", 1)]),
    ("pedidos", "idx_cliente_fecha", [("cliente_id", 1), ("fecha", -1)]),
    ("pedidos", "idx_lineas_producto", [("lineas_detalle.producto_id", 1)]),
]


# Consultas a medir (equivalentes a database/queries/consultas_*.py)

CONSULTAS = [
    {
        "id": "Q1_categoria",
        "col": "productos",
        "filtro": {"categoria": "Tecnología"},
        "orden": None,
        "desc": "Productos de una categoria",
    },
    {
        "id": "Q2_rango_precio",
        "col": "productos",
        "filtro": {"precio": {"$gte": 100000, "$lte": 120000}},
        "orden": None,
        "desc": "Productos en un rango de precio",
    },
    {
        "id": "Q3_categoria_precio",
        "col": "productos",
        "filtro": {"categoria": "Tecnología",
                   "precio": {"$gte": 100000, "$lte": 150000}},
        "orden": None,
        "desc": "Productos por categoria y rango de precio",
    },
    {
        "id": "Q4_categoria_precio_talla",
        "col": "productos",
        "filtro": {"categoria": "Ropa",
                   "precio": {"$gte": 50000, "$lte": 250000},
                   "atributos.talla": "M"},
        "orden": None,
        "desc": "Categoria + rango de precio + atributo especifico (talla)",
    },
    {
        "id": "Q5_comercio",
        "col": "productos",
        "filtro": {"comercio_id": "COM-001"},
        "orden": None,
        "desc": "Productos de un comercio",
    },
    {
        "id": "Q6_pedidos_cliente",
        "col": "pedidos",
        "filtro": {"cliente_id": "CLI-00001"},
        "orden": [("fecha", -1)],
        "desc": "Pedidos de un cliente ordenados por fecha",
    },
    {
        "id": "Q7_pedidos_producto",
        "col": "pedidos",
        "filtro": {"lineas_detalle.producto_id": "PROD-00001"},
        "orden": None,
        "desc": "Pedidos que contienen un producto",
    },
]


# Agregaciones (equivalentes a database/queries/agregaciones.py)

AGREGACIONES = [
    {
        "id": "A1_ventas_por_categoria",
        "col": "pedidos",
        "pipeline": [
            {"$match": {"estado": {"$ne": "Cancelado"}}},
            {"$unwind": "$lineas_detalle"},
            {"$lookup": {"from": "productos",
                         "localField": "lineas_detalle.producto_id",
                         "foreignField": "_id", "as": "producto"}},
            {"$unwind": "$producto"},
            {"$group": {"_id": "$producto.categoria",
                        "total_ventas": {"$sum": "$lineas_detalle.subtotal"}}},
            {"$sort": {"total_ventas": -1}},
        ],
    },
    {
        "id": "A2_ticket_promedio",
        "col": "pedidos",
        "pipeline": [
            {"$match": {"estado": {"$ne": "Cancelado"}}},
            {"$group": {"_id": None,
                        "ticket_promedio": {"$avg": "$monto_total"},
                        "cantidad_pedidos": {"$sum": 1}}},
        ],
    },
    {
        "id": "A3_productos_mas_vendidos",
        "col": "pedidos",
        "pipeline": [
            {"$match": {"estado": {"$ne": "Cancelado"}}},
            {"$unwind": "$lineas_detalle"},
            {"$group": {"_id": "$lineas_detalle.producto_id",
                        "nombre_producto": {"$first": "$lineas_detalle.nombre_producto"},
                        "cantidad_vendida": {"$sum": "$lineas_detalle.cantidad"}}},
            {"$sort": {"cantidad_vendida": -1}},
            {"$limit": 10},
        ],
    },
]

CATEGORIAS = ["Alimentos", "Ropa", "Tecnología", "Artesanías",
              "Servicios", "Hogar", "Belleza", "Deportes"]



# Utilidades estadisticas

def percentil(valores, p):
    """Percentil p (0-100) por el metodo del rango mas cercano."""
    ordenados = sorted(valores)
    k = max(0, math.ceil(p / 100 * len(ordenados)) - 1)
    return ordenados[k]


def resumen(tiempos_ms):
    return {
        "n": len(tiempos_ms),
        "mediana_ms": round(statistics.median(tiempos_ms), 3),
        "p95_ms": round(percentil(tiempos_ms, 95), 3),
        "media_ms": round(statistics.mean(tiempos_ms), 3),
        "min_ms": round(min(tiempos_ms), 3),
        "max_ms": round(max(tiempos_ms), 3),
    }



# Indices

def nombres_indices_propios():
    return {nombre for _, nombre, _ in INDICES}


def indices_ajenos(db):
    """Indices (distintos de _id_ y de los propios) que podrian falsear la medicion."""
    propios = nombres_indices_propios()
    ajenos = []
    for col in {c for c, _, _ in INDICES}:
        for nombre in db[col].index_information():
            if nombre != "_id_" and nombre not in propios:
                ajenos.append(f"{col}.{nombre}")
    return ajenos


def borrar_indices(db):
    for col, nombre, _ in INDICES:
        if nombre in db[col].index_information():
            db[col].drop_index(nombre)


def crear_indices(db):
    """Crea los indices y devuelve el tiempo de construccion de cada uno (ms)."""
    tiempos = []
    for col, nombre, claves in INDICES:
        t0 = time.perf_counter()
        db[col].create_index(claves, name=nombre)
        tiempos.append({
            "coleccion": col,
            "indice": nombre,
            "claves": json.dumps(claves),
            "construccion_ms": round((time.perf_counter() - t0) * 1000, 3),
        })
    return tiempos



# Medicion de consultas

def cursor_de(col, consulta):
    cur = col.find(consulta["filtro"])
    if consulta["orden"]:
        cur = cur.sort(consulta["orden"])
    return cur


def recorrer_plan(nodo, etapas, indices):
    """Recorre el plan ganador de explain() y junta etapas e indices usados."""
    if isinstance(nodo, dict):
        etapa = nodo.get("stage")
        if isinstance(etapa, str) and etapa not in etapas:
            etapas.append(etapa)
        nombre = nodo.get("indexName")
        if isinstance(nombre, str) and nombre not in indices:
            indices.append(nombre)
        for valor in nodo.values():
            recorrer_plan(valor, etapas, indices)
    elif isinstance(nodo, list):
        for item in nodo:
            recorrer_plan(item, etapas, indices)


def explicar(col, consulta):
    explicacion = cursor_de(col, consulta).explain()
    stats = explicacion.get("executionStats", {})
    etapas, indices = [], []
    recorrer_plan(explicacion.get("queryPlanner", {}).get("winningPlan", {}),
                  etapas, indices)
    if "IXSCAN" in etapas:
        principal = "IXSCAN"
    elif "COLLSCAN" in etapas:
        principal = "COLLSCAN"
    else:
        principal = etapas[0] if etapas else "N/D"
    return explicacion, {
        "etapa_principal": principal,
        "etapas": ">".join(etapas),
        "indice_usado": ",".join(indices),
        "docs_examinados": stats.get("totalDocsExamined"),
        "claves_examinadas": stats.get("totalKeysExamined"),
        "docs_devueltos": stats.get("nReturned"),
        "explain_ms": stats.get("executionTimeMillis"),
    }


def medir_consulta(col, consulta, reps):
    list(cursor_de(col, consulta))  # calentamiento (se descarta)
    tiempos, devueltos = [], 0
    for _ in range(reps):
        t0 = time.perf_counter()
        devueltos = len(list(cursor_de(col, consulta)))
        tiempos.append((time.perf_counter() - t0) * 1000)
    return tiempos, devueltos


def fase_consultas(db, condicion, reps, dir_capturas, crudos):
    filas = []
    for consulta in CONSULTAS:
        col = db[consulta["col"]]
        tiempos, devueltos = medir_consulta(col, consulta, reps)
        explicacion, plan = explicar(col, consulta)
        with open(dir_capturas / f"{consulta['id']}_{condicion}.json", "w",
                  encoding="utf-8") as f:
            json.dump(explicacion, f, ensure_ascii=False, indent=2, default=str)
        for i, t in enumerate(tiempos, 1):
            crudos.append({"prueba": consulta["id"], "condicion": condicion,
                           "repeticion": i, "tiempo_ms": round(t, 3)})
        fila = {"consulta": consulta["id"], "descripcion": consulta["desc"],
                "condicion": condicion, "coleccion": consulta["col"],
                "devueltos": devueltos}
        fila.update(resumen(tiempos))
        fila.update(plan)
        filas.append(fila)
        print(f"  [{condicion:10}] {consulta['id']:28} "
              f"mediana={fila['mediana_ms']:9.3f} ms  p95={fila['p95_ms']:9.3f} ms  "
              f"examinados={plan['docs_examinados']}  {plan['etapa_principal']}")
    return filas



# Agregaciones

def fase_agregaciones(db, reps, crudos):
    filas = []
    for agg in AGREGACIONES:
        col = db[agg["col"]]
        list(col.aggregate(agg["pipeline"]))  # calentamiento
        tiempos, n_resultados = [], 0
        for _ in range(reps):
            t0 = time.perf_counter()
            n_resultados = len(list(col.aggregate(agg["pipeline"])))
            tiempos.append((time.perf_counter() - t0) * 1000)
        for i, t in enumerate(tiempos, 1):
            crudos.append({"prueba": agg["id"], "condicion": "agregacion",
                           "repeticion": i, "tiempo_ms": round(t, 3)})
        fila = {"agregacion": agg["id"], "resultados": n_resultados}
        fila.update(resumen(tiempos))
        filas.append(fila)
        print(f"  {agg['id']:28} mediana={fila['mediana_ms']:10.3f} ms  "
              f"p95={fila['p95_ms']:10.3f} ms")
    return filas



# Concurrencia

def trabajador(db, semilla, n_solicitudes, n_clientes):
    rnd = random.Random(semilla)
    latencias = []
    for _ in range(n_solicitudes):
        t0 = time.perf_counter()
        if rnd.random() < 0.5:
            cliente = f"CLI-{rnd.randint(1, n_clientes):05d}"
            list(db.pedidos.find({"cliente_id": cliente}).sort("fecha", -1))
        else:
            minimo = rnd.randint(1000, 400000)
            list(db.productos.find({"categoria": rnd.choice(CATEGORIAS),
                                    "precio": {"$gte": minimo,
                                               "$lte": minimo + 50000}}))
        latencias.append((time.perf_counter() - t0) * 1000)
    return latencias


def fase_concurrencia(uri, nombre_db, semilla, solicitudes_por_hilo=20):
    cliente = MongoClient(uri, maxPoolSize=200)
    db = cliente[nombre_db]
    n_clientes = db.clientes.count_documents({})
    trabajador(db, semilla, 5, n_clientes)  # calentamiento
    filas = []
    for hilos in (10, 50, 100):
        t0 = time.perf_counter()
        with ThreadPoolExecutor(max_workers=hilos) as pool:
            futuros = [pool.submit(trabajador, db, semilla + i,
                                   solicitudes_por_hilo, n_clientes)
                       for i in range(hilos)]
            latencias = [x for f in futuros for x in f.result()]
        duracion = time.perf_counter() - t0
        fila = {"hilos": hilos, "solicitudes": len(latencias),
                "duracion_s": round(duracion, 3),
                "solicitudes_por_s": round(len(latencias) / duracion, 1),
                "media_ms": round(statistics.mean(latencias), 3),
                "mediana_ms": round(statistics.median(latencias), 3),
                "p95_ms": round(percentil(latencias, 95), 3),
                "max_ms": round(max(latencias), 3)}
        filas.append(fila)
        print(f"  {hilos:3} hilos: {fila['solicitudes_por_s']:8.1f} sol/s  "
              f"media={fila['media_ms']:8.3f} ms  p95={fila['p95_ms']:8.3f} ms")
    cliente.close()
    return filas



# Carga masiva

def buscar_json(nombre):
    for carpeta in (RAIZ / "database" / "seed", RAIZ / "database" / "generadores"):
        ruta = carpeta / f"{nombre}.json"
        if ruta.exists():
            return ruta
    return None


def fase_carga(db):
    filas = []
    for nombre in ("comercios", "clientes", "productos", "pedidos"):
        ruta = buscar_json(nombre)
        if ruta is None:
            print(f"  {nombre}.json no encontrado, se omite")
            continue
        t0 = time.perf_counter()
        with open(ruta, "r", encoding="utf-8") as f:
            docs = json.load(f)
        lectura = time.perf_counter() - t0
        if nombre == "pedidos":
            for d in docs:
                d["fecha"] = datetime.fromisoformat(d["fecha"])
        temporal = db[f"bench_{nombre}"]
        temporal.drop()
        t0 = time.perf_counter()
        temporal.insert_many(docs, ordered=False)
        insercion = time.perf_counter() - t0
        temporal.drop()
        fila = {"coleccion": nombre, "documentos": len(docs),
                "lectura_json_s": round(lectura, 3),
                "insercion_s": round(insercion, 3),
                "docs_por_s": round(len(docs) / insercion, 1)}
        filas.append(fila)
        print(f"  {nombre:10} {len(docs):6} docs  insercion={insercion:7.3f} s  "
              f"({fila['docs_por_s']:.0f} docs/s)")
    return filas



# Entorno y salida

def info_entorno(client, db, args):
    ram = "N/D (instalar psutil para obtenerla)"
    try:
        import psutil
        ram = f"{psutil.virtual_memory().total / 1024 ** 3:.1f} GB"
    except ImportError:
        pass
    return {
        "fecha_ejecucion": datetime.now().isoformat(timespec="seconds"),
        "sistema_operativo": platform.platform(),
        "procesador": platform.processor(),
        "nucleos_logicos": os.cpu_count(),
        "ram": ram,
        "disco": "COMPLETAR A MANO (SSD/HDD)",
        "python": platform.python_version(),
        "pymongo": pymongo.version,
        "mongodb": client.server_info()["version"],
        "base_de_datos": db.name,
        "documentos": {c: db[c].count_documents({})
                       for c in ("comercios", "clientes", "productos", "pedidos")},
        "repeticiones_consultas": args.reps,
        "repeticiones_agregaciones": args.agg_reps,
        "semilla": args.seed,
    }


def guardar_csv(ruta, filas):
    if not filas:
        return
    campos = []
    for fila in filas:
        for k in fila:
            if k not in campos:
                campos.append(k)
    with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reps", type=int, default=30)
    ap.add_argument("--agg-reps", type=int, default=5)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=Path, default=SALIDA_DEFECTO)
    ap.add_argument("--skip-concurrency", action="store_true")
    ap.add_argument("--skip-load", action="store_true")
    ap.add_argument("--keep-indexes", action="store_true")
    ap.add_argument("--ignorar-indices-ajenos", action="store_true",
                    help="continua aunque existan indices de otros miembros")
    args = ap.parse_args()

    load_dotenv(RAIZ / ".env")
    uri = os.getenv("MONGODB_URI")
    nombre_db = os.getenv("MONGODB_DB")
    if not uri or not nombre_db:
        sys.exit("Faltan MONGODB_URI o MONGODB_DB en el archivo .env de la raiz")

    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[nombre_db]
    entorno = info_entorno(client, db, args)  # falla aqui si no hay conexion

    for coleccion, minimo in (("productos", 25000), ("clientes", 10000),
                              ("pedidos", 50000)):
        if entorno["documentos"][coleccion] < minimo:
            print(f"AVISO: {coleccion} tiene {entorno['documentos'][coleccion]} "
                  f"documentos (minimo del caso: {minimo})")

    borrar_indices(db)
    ajenos = indices_ajenos(db)
    if ajenos and not args.ignorar_indices_ajenos:
        sys.exit("Hay indices que no son del benchmark y falsearian la medicion "
                 f"'sin indice': {ajenos}\nBorralos o usa --ignorar-indices-ajenos")

    dir_capturas = args.out / "capturas"
    dir_capturas.mkdir(parents=True, exist_ok=True)
    crudos = []

    print(f"\nMongoDB {entorno['mongodb']} | {entorno['documentos']}")
    print("\n== Consultas SIN indice ==")
    sin = fase_consultas(db, "sin_indice", args.reps, dir_capturas, crudos)

    print("\n== Creando indices ==")
    construccion = crear_indices(db)
    for fila in construccion:
        print(f"  {fila['indice']:24} {fila['construccion_ms']:10.1f} ms")

    print("\n== Consultas CON indice ==")
    con = fase_consultas(db, "con_indice", args.reps, dir_capturas, crudos)

    print("\n== Agregaciones ==")
    agregaciones = fase_agregaciones(db, args.agg_reps, crudos)

    concurrencia = []
    if not args.skip_concurrency:
        print("\n== Concurrencia (con indices) ==")
        concurrencia = fase_concurrencia(uri, nombre_db, args.seed)

    carga = []
    if not args.skip_load:
        print("\n== Carga masiva (colecciones temporales bench_*) ==")
        carga = fase_carga(db)

    if not args.keep_indexes:
        borrar_indices(db)
        print("\nIndices del benchmark eliminados (use --keep-indexes para conservarlos)")

    # Tabla comparativa sin/con indice
    comparativa = []
    for a, b in zip(sin, con):
        mejora = (round((1 - b["mediana_ms"] / a["mediana_ms"]) * 100, 1)
                  if a["mediana_ms"] else None)
        comparativa.append({
            "consulta": a["consulta"], "descripcion": a["descripcion"],
            "devueltos": a["devueltos"],
            "mediana_sin_ms": a["mediana_ms"], "mediana_con_ms": b["mediana_ms"],
            "p95_sin_ms": a["p95_ms"], "p95_con_ms": b["p95_ms"],
            "mejora_mediana_pct": mejora,
            "docs_examinados_sin": a["docs_examinados"],
            "docs_examinados_con": b["docs_examinados"],
            "etapa_sin": a["etapa_principal"], "etapa_con": b["etapa_principal"],
            "indice_usado": b["indice_usado"],
        })

    guardar_csv(args.out / "consultas_detalle.csv", sin + con)
    guardar_csv(args.out / "comparativa_indices.csv", comparativa)
    guardar_csv(args.out / "construccion_indices.csv", construccion)
    guardar_csv(args.out / "agregaciones.csv", agregaciones)
    guardar_csv(args.out / "concurrencia.csv", concurrencia)
    guardar_csv(args.out / "carga_masiva.csv", carga)
    guardar_csv(args.out / "tiempos_crudos.csv", crudos)
    with open(args.out / "entorno.json", "w", encoding="utf-8") as f:
        json.dump(entorno, f, ensure_ascii=False, indent=2)

    print(f"\nResultados guardados en {args.out}")


if __name__ == "__main__":
    main()
