#!/usr/bin/env python
"""
Demostracion en vivo - MercadoTico 360 (Integrante 5: QA & Performance)

Muestra, paso a paso y con salida clara en pantalla, las evidencias que pide el
enunciado para el caso MercadoTico 360:
  1. Conexion y datos cargados
  2. Catalogo heterogeneo (atributos distintos por categoria)
  3. Pedido con estructura anidada y busqueda por _id
  4. Indices: antes y despues (con explain)
  5. Evolucion del esquema sin migracion
  6. Historial del pedido intacto aunque cambie el precio del producto
  7. Validacion de datos invalidos

Uso (desde la raiz del repositorio, con el entorno virtual activo):
    python Performance/scripts/demo.py                  # paso a paso (Enter)
    python Performance/scripts/demo.py --auto           # sin pausas (ensayo)
    python Performance/scripts/demo.py --pasos 4,6      # solo algunos pasos
    python Performance/scripts/demo.py --mantener-indices   # deja los indices del paso 4

SEGURIDAD DE LOS DATOS
- No modifica ni borra los datos reales.
- Los pasos 5 y 6 trabajan sobre copias en colecciones temporales demo_*,
  que se eliminan al terminar.
- El paso 4 crea dos indices con nombre demo_* y los elimina al terminar
  (salvo --mantener-indices). La medicion "sin indice" fuerza un recorrido
  completo con hint $natural, asi que no depende de borrar indices de nadie.
"""

import argparse
import contextlib
import io
import json
import os
import statistics
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from dotenv import load_dotenv
from pymongo import MongoClient

with contextlib.redirect_stdout(io.StringIO()):
    from database.schemas.modelos_de_estructuras import crear_estructura_producto

with contextlib.suppress(Exception):
    sys.stdout.reconfigure(encoding="utf-8")

TEMPORALES = ("demo_productos", "demo_pedidos")


# ----------------------------------------------------------------------------
# Utilidades de presentacion
# ----------------------------------------------------------------------------
def titulo(numero, texto):
    print("\n" + "=" * 74)
    print(f"PASO {numero} - {texto}")
    print("=" * 74)


def mostrar(documento):
    print(json.dumps(documento, ensure_ascii=False, indent=2, default=str))


def pausa(auto):
    if not auto:
        input("\n[Enter para continuar] ")


# ----------------------------------------------------------------------------
# Utilidades de medicion (mismas ideas que benchmark.py)
# ----------------------------------------------------------------------------
def recorrer_plan(nodo, etapas):
    if isinstance(nodo, dict):
        etapa = nodo.get("stage")
        if isinstance(etapa, str) and etapa not in etapas:
            etapas.append(etapa)
        for valor in nodo.values():
            recorrer_plan(valor, etapas)
    elif isinstance(nodo, list):
        for item in nodo:
            recorrer_plan(item, etapas)


def plan(cursor):
    explicacion = cursor.explain()
    stats = explicacion.get("executionStats", {})
    etapas = []
    recorrer_plan(explicacion.get("queryPlanner", {}).get("winningPlan", {}), etapas)
    return {
        "etapas": " > ".join(etapas),
        "examinados": stats.get("totalDocsExamined"),
        "devueltos": stats.get("nReturned"),
    }


def mediana_ms(fabrica, repeticiones=10):
    list(fabrica())  # calentamiento
    tiempos = []
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        list(fabrica())
        tiempos.append((time.perf_counter() - t0) * 1000)
    return statistics.median(tiempos)


def comparar_indice(descripcion, coleccion, filtro, orden, claves, nombre,
                    auto, mantener):
    def cursor(hint):
        c = coleccion.find(filtro)
        if orden:
            c = c.sort(orden)
        return c.hint(hint)

    print(f"\nConsulta: {descripcion}")
    print(f"Filtro:   {filtro}" + (f"   Orden: {orden}" if orden else ""))

    natural = [("$natural", 1)]
    p_sin = plan(cursor(natural))
    ms_sin = mediana_ms(lambda: cursor(natural))
    print("\n  SIN indice (recorrido completo de la coleccion)")
    print(f"    etapas:               {p_sin['etapas']}")
    print(f"    documentos examinados: {p_sin['examinados']}")
    print(f"    documentos devueltos:  {p_sin['devueltos']}")
    print(f"    tiempo mediano:        {ms_sin:.2f} ms")

    pausa(auto)
    print(f"  Creando el indice {nombre} sobre {claves} ...")
    t0 = time.perf_counter()
    coleccion.create_index(claves, name=nombre)
    print(f"  Indice creado en {(time.perf_counter() - t0) * 1000:.0f} ms")
    try:
        p_con = plan(cursor(nombre))
        ms_con = mediana_ms(lambda: cursor(nombre))
        print("\n  CON indice")
        print(f"    etapas:               {p_con['etapas']}")
        print(f"    documentos examinados: {p_con['examinados']}")
        print(f"    documentos devueltos:  {p_con['devueltos']}")
        print(f"    tiempo mediano:        {ms_con:.2f} ms")
    finally:
        if not mantener:
            coleccion.drop_index(nombre)

    if ms_con > 0:
        print(f"\n  => {p_sin['examinados']} -> {p_con['examinados']} documentos examinados; "
              f"{ms_sin:.2f} ms -> {ms_con:.2f} ms ({ms_sin / ms_con:.1f} veces).")


def pedido_demo(db):
    """Primer pedido entregado (no cancelado): sirve de ejemplo y su cliente tiene pedidos."""
    return (db.pedidos.find_one({"estado": "Entregado"}, sort=[("_id", 1)])
            or db.pedidos.find_one({}, sort=[("_id", 1)]))


# ----------------------------------------------------------------------------
# Pasos
# ----------------------------------------------------------------------------
def paso1(db, cliente, args):
    titulo(1, "Conexion y datos cargados")
    print(f"MongoDB {cliente.server_info()['version']}  |  base: {db.name}")
    for coleccion in ("comercios", "clientes", "productos", "pedidos"):
        print(f"  {coleccion:10} {db[coleccion].count_documents({}):>7} documentos")


def paso2(db, cliente, args):
    titulo(2, "Catalogo heterogeneo: mismos productos, atributos distintos")
    ropa = (db.productos.find_one({"categoria": "Ropa", "atributos.talla": {"$exists": True}})
            or db.productos.find_one({"categoria": "Ropa"}))
    tec = (db.productos.find_one({"categoria": "Tecnología",
                                  "atributos.garantia_meses": {"$exists": True}})
           or db.productos.find_one({"categoria": "Tecnología"}))
    print("\nProducto de la categoria Ropa:")
    mostrar(ropa)
    print("\nProducto de la categoria Tecnologia:")
    mostrar(tec)
    print("\n=> Misma coleccion, atributos distintos, sin columnas vacias.")


def paso3(db, cliente, args):
    titulo(3, "Pedido con estructura anidada y busqueda por _id")
    pedido = pedido_demo(db)
    t0 = time.perf_counter()
    encontrado = db.pedidos.find_one({"_id": pedido["_id"]})
    ms = (time.perf_counter() - t0) * 1000
    print(f"\nBusqueda por _id ({pedido['_id']}): {ms:.2f} ms\n")
    mostrar(encontrado)
    print(f"\n=> El pedido trae sus {len(encontrado['lineas_detalle'])} lineas dentro, "
          "con nombre y precio al momento de la compra.")


def paso4(db, cliente, args):
    titulo(4, "Indices: antes y despues")
    cliente_id = pedido_demo(db)["cliente_id"]
    comparar_indice("Pedidos de un cliente, del mas reciente al mas antiguo",
                    db.pedidos, {"cliente_id": cliente_id}, [("fecha", -1)],
                    [("cliente_id", 1), ("fecha", -1)], "demo_cliente_fecha",
                    args.auto, args.mantener_indices)
    pausa(args.auto)
    comparar_indice("Productos de una categoria dentro de un rango de precio",
                    db.productos,
                    {"categoria": "Tecnología", "precio": {"$gte": 100000, "$lte": 150000}},
                    None, [("categoria", 1), ("precio", 1)], "demo_categoria_precio",
                    args.auto, args.mantener_indices)
    if args.mantener_indices:
        print("\n(Indices demo_* conservados: se pueden ver en Compass > Indexes.)")


def paso5(db, cliente, args):
    titulo(5, "Evolucion del esquema sin migracion")
    demo = db["demo_productos"]
    demo.drop()
    for categoria in ("Ropa", "Tecnología"):
        demo.insert_one(db.productos.find_one({"categoria": categoria}))
    print("\nAntes (dos productos de categorias distintas):")
    for d in demo.find():
        print(f"  {d['_id']}  {d['categoria']:11} atributos: {d['atributos']}")

    primero = demo.find_one()
    # atributo que NO existe en ninguna categoria de los datos generados
    nuevo_atributo = "certificacion_sostenible"
    demo.update_one({"_id": primero["_id"]}, {"$set": {f"atributos.{nuevo_atributo}": True}})
    demo.insert_one(crear_estructura_producto(
        "PROD-DEMO", "Clase de yoga", 15000.0, "Servicios", primero["comercio_id"], 0,
        {"duracion_minutos": 60, "modalidad": "Virtual"}))
    print(f"\nDespues de agregar el atributo nuevo '{nuevo_atributo}' a UN producto y crear la categoria nueva 'Servicios':")
    for d in demo.find():
        print(f"  {d['_id']}  {d['categoria']:11} atributos: {d['atributos']}")
    print("\n=> Sin ALTER TABLE ni migracion: solo el documento cambiado tiene el campo nuevo.")
    demo.drop()


def paso6(db, cliente, args):
    titulo(6, "El historial del pedido no cambia aunque cambie el producto")
    pedido = pedido_demo(db)
    linea = pedido["lineas_detalle"][0]
    producto = db.productos.find_one({"_id": linea["producto_id"]})
    demo_p, demo_ped = db["demo_productos"], db["demo_pedidos"]
    demo_p.drop()
    demo_ped.drop()
    demo_p.insert_one(producto)
    demo_ped.insert_one(pedido)

    print(f"\nProducto {producto['_id']} ({producto['nombre']}): precio actual {producto['precio']}")
    print(f"Pedido {pedido['_id']}: linea con precio_unitario {linea['precio_unitario']}, "
          f"monto_total {pedido['monto_total']}")

    nuevo = round(producto["precio"] * 2, 2)
    demo_p.update_one({"_id": producto["_id"]}, {"$set": {"precio": nuevo}})
    print(f"\n>>> El comercio sube el precio del producto a {nuevo}\n")

    producto_ahora = demo_p.find_one({"_id": producto["_id"]})
    pedido_ahora = demo_ped.find_one({"_id": pedido["_id"]})
    linea_ahora = pedido_ahora["lineas_detalle"][0]
    print(f"Producto {producto['_id']}: precio ahora {producto_ahora['precio']}")
    print(f"Pedido {pedido['_id']}: precio_unitario {linea_ahora['precio_unitario']}, "
          f"monto_total {pedido_ahora['monto_total']}")
    print("\n=> El pedido conserva el precio con el que se vendio.")
    demo_p.drop()
    demo_ped.drop()


def paso7(db, cliente, args):
    titulo(7, "Validacion de datos invalidos")
    print("\nIntento de crear un producto con precio negativo (validacion del modelo en Python):")
    try:
        crear_estructura_producto("X", "Prueba", -100.0, "Ropa", "COM-001", 1, {})
        print("  !! se acepto (no deberia)")
    except ValueError as error:
        print(f"  Rechazado: {error}")
    print("\nIntento con una categoria inexistente:")
    try:
        crear_estructura_producto("X", "Prueba", 100.0, "Inexistente", "COM-001", 1, {})
        print("  !! se acepto (no deberia)")
    except ValueError as error:
        print(f"  Rechazado: {error}")

    info = list(db.list_collections(filter={"name": "productos"}))
    validador = info[0].get("options", {}).get("validator") if info else None
    print("\nValidacion dentro de MongoDB ($jsonSchema) en la coleccion productos:")
    print("  Activa." if validador else
          "  No configurada todavia (pendiente): hoy la validacion vive en el codigo Python.")


PASOS = {1: paso1, 2: paso2, 3: paso3, 4: paso4, 5: paso5, 6: paso6, 7: paso7}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--auto", action="store_true", help="sin pausas entre pasos")
    ap.add_argument("--pasos", default=",".join(map(str, PASOS)),
                    help="pasos a ejecutar, separados por coma (default: todos)")
    ap.add_argument("--mantener-indices", action="store_true")
    args = ap.parse_args()

    load_dotenv(RAIZ / ".env")
    uri, nombre_db = os.getenv("MONGODB_URI"), os.getenv("MONGODB_DB")
    if not uri or not nombre_db:
        sys.exit("Faltan MONGODB_URI o MONGODB_DB en el archivo .env de la raiz")
    cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = cliente[nombre_db]
    cliente.server_info()

    elegidos = [int(n) for n in args.pasos.split(",") if n.strip()]
    try:
        for n in elegidos:
            PASOS[n](db, cliente, args)
            pausa(args.auto)
    finally:
        for nombre in TEMPORALES:
            db[nombre].drop()
    print("\nDemostracion terminada. Colecciones temporales eliminadas.")


if __name__ == "__main__":
    main()
