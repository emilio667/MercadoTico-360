#!/usr/bin/env python
"""
Pruebas funcionales - MercadoTico 360 (Integrante 5: QA & Performance)

Verifican, sobre MongoDB, los requisitos funcionales del caso. Corresponden a
las pruebas F1 a F10 del plan (Performance/plan_de_pruebas.md) y a las
comprobaciones V1 a V5 sobre la base ya cargada.

Uso (desde la raiz del repositorio, con el entorno virtual activo y MongoDB
corriendo):
    python test/test_funcionales.py

No requiere instalar nada adicional (usa unittest de la libreria estandar).

SEGURIDAD DE LOS DATOS
- Las pruebas F01-F10 usan una base APARTE llamada <MONGODB_DB>_test, que crean
  con datos minimos y borran al terminar. No tocan la base real.
- Las pruebas V1-V5 solo LEEN la base real (V5 intenta insertar un documento
  invalido y, si MongoDB lo acepta, lo elimina inmediatamente).

Resultado: Performance/resultados/pruebas_funcionales.csv

GUIA RAPIDA: QUE COMPRUEBA CADA PRUEBA
  F01  Que un mismo catalogo guarde productos con atributos distintos (esquema
       flexible) y sin campos vacios.
  F02  Que se pueda buscar por categoria + rango de precio + un atributo.
  F03  Que se recuperen los pedidos de un cliente con sus lineas anidadas.
  F04  Que cambiar el estado de un pedido no toque ningun otro campo.
  F05  Que cambiar el precio de un producto NO cambie los pedidos ya hechos.
  F06  Que "ventas por categoria" de MongoDB de el mismo total que un calculo manual.
  F07  Que "ticket promedio" de MongoDB de el mismo valor que un calculo manual.
  F08  Que se pueda agregar un atributo o una categoria nueva sin migrar nada.
  F09  Que el modelo rechace datos invalidos (precio negativo, etc.).
  F10  Que se puedan consultar los productos de un comercio.
  V1   Que la base real tenga el volumen minimo (25 000 / 10 000 / 50 000).
  V2   Que el catalogo real tenga al menos 8 categorias.
  V3   Que las categorias reales tengan atributos distintos entre si.
  V4   Que los pedidos reales conserven nombre, precio y subtotal coherentes.
  V5   Que MongoDB (no solo Python) rechace datos invalidos ($jsonSchema).

COMO LEER EL RESULTADO
  ok         la prueba paso: el requisito se cumple.
  FAIL       el requisito NO se cumple (o hay un error real en los datos/codigo).
  ERROR      la prueba no pudo ejecutarse (por ejemplo, fallo una consulta).
  skipped    se omitio (por ejemplo, V5 si no hay $jsonSchema todavia).
"""

import contextlib
import csv
import io
import os
import sys
import unittest
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import WriteError

# El modulo del grupo imprime ejemplos al importarse; se silencian.
with contextlib.redirect_stdout(io.StringIO()):
    from database.schemas.modelos_de_estructuras import (
        crear_estructura_cliente,
        crear_estructura_comercio,
        crear_estructura_pedido,
        crear_estructura_producto,
    )

load_dotenv(RAIZ / ".env")
URI = os.getenv("MONGODB_URI")
NOMBRE_DB = os.getenv("MONGODB_DB")


def conectar():
    """Conecta con MongoDB; si no se puede, omite las pruebas en lugar de fallar."""
    if not URI or not NOMBRE_DB:
        raise unittest.SkipTest("Faltan MONGODB_URI o MONGODB_DB en el .env")
    cliente = MongoClient(URI, serverSelectionTimeoutMS=3000)
    try:
        cliente.server_info()
    except Exception as error:  # noqa: BLE001
        raise unittest.SkipTest(f"No hay conexion con MongoDB: {error}")
    return cliente


# ----------------------------------------------------------------------------
# Datos de prueba minimos (construidos con las funciones del propio proyecto)
# ----------------------------------------------------------------------------
def linea(producto, cantidad):
    """Arma una linea de pedido copiando nombre y precio del producto en ese momento."""
    return {
        "producto_id": producto["_id"],
        "nombre_producto": producto["nombre"],
        "precio_unitario": producto["precio"],
        "cantidad": cantidad,
        "subtotal": producto["precio"] * cantidad,
    }


def construir_datos():
    """
    Mini tienda para las pruebas:
      Comercios: COM-T1 (ropa), COM-T2 (tecnologia/alimentos)
      Productos: P-ROPA-1 (20 000), P-ROPA-2 (30 000), P-TEC-1 (150 000), P-ALI-1 (2 500)
      Clientes:  CLI-T1, CLI-T2
      Pedidos:   PED-T1 (CLI-T1, Entregado, ropa x2 + audifonos x1 = 190 000)
                 PED-T2 (CLI-T1, Pendiente, cafe x3 = 7 500)
                 PED-T3 (CLI-T2, Cancelado, pantalon x1 = 30 000)
    Se usan numeros "redondos" para poder verificar los resultados a mano.
    """
    comercios = [
        crear_estructura_comercio(
            "COM-T1", "Tienda de Ropa", "ropa@test.cr", "22220001", "Ropa",
            "Activo", "San José", "Central", "Carmen", "Frente al parque"),
        crear_estructura_comercio(
            "COM-T2", "Tienda Tech", "tech@test.cr", "22220002", "Tecnología",
            "Activo", "Cartago", "Cartago", "Oriental", "Costado norte"),
    ]
    productos = [
        crear_estructura_producto("P-ROPA-1", "Camiseta", 20000.0, "Ropa",
                                  "COM-T1", 10, {"talla": "M", "color": "Azul"}),
        crear_estructura_producto("P-ROPA-2", "Pantalon", 30000.0, "Ropa",
                                  "COM-T1", 5, {"talla": "L", "material": "Lino"}),
        crear_estructura_producto("P-TEC-1", "Audifonos", 150000.0, "Tecnología",
                                  "COM-T2", 8, {"garantia_meses": 12}),
        crear_estructura_producto("P-ALI-1", "Cafe", 2500.0, "Alimentos",
                                  "COM-T2", 50, {"organico": True}),
    ]
    clientes = [
        crear_estructura_cliente("CLI-T1", "Ana Test", "ana@test.cr", "88880001",
                                 "1-1111-1111", "San José", "Central", "Carmen", "Casa 1"),
        crear_estructura_cliente("CLI-T2", "Beto Test", "beto@test.cr", "88880002",
                                 "2-2222-2222", "Alajuela", "Central", "Alajuela", "Casa 2"),
    ]
    p = {x["_id"]: x for x in productos}
    pedidos = [
        crear_estructura_pedido(
            "PED-T1", datetime(2026, 10, 1, 9, 0), "CLI-T1", "Entregado",
            [linea(p["P-ROPA-1"], 2), linea(p["P-TEC-1"], 1)]),
        crear_estructura_pedido(
            "PED-T2", datetime(2026, 10, 2, 10, 0), "CLI-T1", "Pendiente",
            [linea(p["P-ALI-1"], 3)]),
        crear_estructura_pedido(
            "PED-T3", datetime(2026, 10, 3, 11, 0), "CLI-T2", "Cancelado",
            [linea(p["P-ROPA-2"], 1)]),
    ]
    return comercios, productos, clientes, pedidos


# ----------------------------------------------------------------------------
# F01 - F10: sobre una base de pruebas aparte
# ----------------------------------------------------------------------------
class PruebasFuncionales(unittest.TestCase):
    """Cada prueba parte de la mini tienda de construir_datos(), recargada de cero."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = conectar()
        cls.nombre_db = f"{NOMBRE_DB}_test"
        assert cls.nombre_db != NOMBRE_DB, "La base de pruebas no puede ser la real"

    @classmethod
    def tearDownClass(cls):
        cls.cliente.drop_database(cls.nombre_db)
        cls.cliente.close()

    def setUp(self):
        self.cliente.drop_database(self.nombre_db)
        self.db = self.cliente[self.nombre_db]
        self.comercios, self.productos, self.clientes, self.pedidos = construir_datos()
        self.db.comercios.insert_many(self.comercios)
        self.db.productos.insert_many(self.productos)
        self.db.clientes.insert_many(self.clientes)
        self.db.pedidos.insert_many(self.pedidos)

    # --- F01 ---------------------------------------------------------------
    def test_F01_catalogo_heterogeneo(self):
        """F01 - Productos de categorias distintas conviven con atributos propios y sin nulos

        Requisito: "representar atributos diferentes por categoria sin forzar un
        esquema identico".
        Que hace: compara los atributos de una camiseta (talla, color) con los de
        unos audifonos (garantia_meses) y revisa que ningun atributo sea nulo.
        PASA si: los dos productos tienen conjuntos de atributos distintos y no
        hay valores vacios.
        FALLA si: todos los productos tuvieran los mismos campos o hubiera nulos
        de relleno (lo que pasaria en un modelo relacional de tabla unica).
        """
        ropa = self.db.productos.find_one({"_id": "P-ROPA-1"})
        tec = self.db.productos.find_one({"_id": "P-TEC-1"})
        self.assertNotEqual(set(ropa["atributos"]), set(tec["atributos"]))
        for producto in self.db.productos.find():
            self.assertNotIn(None, producto["atributos"].values())

    # --- F02 ---------------------------------------------------------------
    def test_F02_busqueda_categoria_precio_atributo(self):
        """F02 - Busqueda por categoria, rango de precio y atributo especifico

        Requisito: "resolver busquedas por categoria, rango de precio y al menos
        un atributo especifico de categoria".
        Que hace: busca ropa, de 10 000 a 25 000 colones, talla M.
        PASA si: devuelve solo la camiseta (P-ROPA-1). El pantalon cuesta 30 000 y
        es talla L, y los audifonos no son ropa, asi que deben quedar fuera.
        FALLA si: devuelve de mas (filtros ignorados) o de menos.
        """
        ids = {p["_id"] for p in self.db.productos.find({
            "categoria": "Ropa",
            "precio": {"$gte": 10000, "$lte": 25000},
            "atributos.talla": "M",
        })}
        self.assertEqual(ids, {"P-ROPA-1"})

    # --- F03 ---------------------------------------------------------------
    def test_F03_pedidos_de_un_cliente(self):
        """F03 - Recuperar los pedidos completos de un cliente, con lineas anidadas

        Requisito: "recuperar pedidos completos de un cliente".
        Que hace: pide los pedidos de CLI-T1 y revisa que cada pedido traiga sus
        lineas de detalle dentro, con todos sus campos.
        PASA si: devuelve PED-T1 y PED-T2 (y no el PED-T3, que es de otro
        cliente), PED-T1 trae 2 lineas, y cada linea tiene producto_id, nombre,
        precio_unitario, cantidad y subtotal.
        FALLA si: faltan pedidos, sobran pedidos ajenos o las lineas vienen
        incompletas.
        """
        pedidos = list(self.db.pedidos.find({"cliente_id": "CLI-T1"}))
        self.assertEqual({p["_id"] for p in pedidos}, {"PED-T1", "PED-T2"})
        ped1 = next(p for p in pedidos if p["_id"] == "PED-T1")
        self.assertEqual(len(ped1["lineas_detalle"]), 2)
        for campo in ("producto_id", "nombre_producto", "precio_unitario",
                      "cantidad", "subtotal"):
            self.assertIn(campo, ped1["lineas_detalle"][0])

    # --- F04 ---------------------------------------------------------------
    def test_F04_actualizar_estado_solo_cambia_estado(self):
        """F04 - Actualizar el estado de un pedido modifica unicamente ese campo

        Requisito: "actualizar estados del pedido sin reescribir informacion
        innecesaria".
        Que hace: guarda el pedido PED-T2 tal como esta, cambia su estado de
        Pendiente a Enviado, y compara el antes con el despues.
        PASA si: se modifico exactamente 1 documento, el estado es "Enviado", y
        todo lo demas (fecha, cliente, lineas, monto) es identico.
        FALLA si: el cambio altero otro campo o no modifico nada.
        """
        antes = self.db.pedidos.find_one({"_id": "PED-T2"})
        resultado = self.db.pedidos.update_one(
            {"_id": "PED-T2"}, {"$set": {"estado": "Enviado"}})
        despues = self.db.pedidos.find_one({"_id": "PED-T2"})
        self.assertEqual(resultado.modified_count, 1)
        self.assertEqual(despues["estado"], "Enviado")
        antes.pop("estado")
        despues.pop("estado")
        self.assertEqual(antes, despues)

    # --- F05 ---------------------------------------------------------------
    def test_F05_historial_conserva_precio_original(self):
        """F05 - Cambiar el precio de un producto no altera los pedidos ya hechos

        Requisito: "cada pedido debe conservar informacion suficiente para
        reconstruir que compro el cliente aunque posteriormente cambie el
        producto". Es la prueba mas importante del diseno de pedidos.
        Que hace: sube la camiseta de 20 000 a 99 999 despues de que se vendio en
        PED-T1, y revisa ese pedido.
        PASA si: el producto ya cuesta 99 999, pero la linea del pedido sigue en
        20 000 y el monto total del pedido no cambio.
        FALLA si: el pedido dependiera del precio actual del producto (lo que
        pasa cuando solo se guarda el ID del producto).
        """
        monto_antes = self.db.pedidos.find_one({"_id": "PED-T1"})["monto_total"]
        self.db.productos.update_one({"_id": "P-ROPA-1"}, {"$set": {"precio": 99999.0}})
        self.assertEqual(self.db.productos.find_one({"_id": "P-ROPA-1"})["precio"], 99999.0)
        pedido = self.db.pedidos.find_one({"_id": "PED-T1"})
        linea_ropa = next(l for l in pedido["lineas_detalle"]
                          if l["producto_id"] == "P-ROPA-1")
        self.assertEqual(linea_ropa["precio_unitario"], 20000.0)
        self.assertEqual(pedido["monto_total"], monto_antes)

    # --- F06 ---------------------------------------------------------------
    def test_F06_ventas_por_categoria(self):
        """F06 - Agregacion de ventas por categoria coincide con el calculo manual

        Requisito: "ejecutar al menos dos consultas de agregacion (ventas por
        categoria, ticket promedio...)".
        Que hace: calcula en Python, a mano y sin MongoDB, cuanto se vendio por
        categoria (sin contar pedidos cancelados), y lo compara con lo que
        devuelve el pipeline de MongoDB.
        PASA si: ambos coinciden (Ropa 40 000, Tecnologia 150 000, Alimentos 7 500).
        FALLA si: el pipeline suma de mas (cancelados), de menos, o agrupa mal.
        Nota: el pipeline es una copia del de database/queries/agregaciones.py.
        """
        categoria = {p["_id"]: p["categoria"] for p in self.productos}
        esperado = {}
        for pedido in self.pedidos:
            if pedido["estado"] == "Cancelado":
                continue
            for l in pedido["lineas_detalle"]:
                cat = categoria[l["producto_id"]]
                esperado[cat] = esperado.get(cat, 0) + l["subtotal"]
        pipeline = [
            {"$match": {"estado": {"$ne": "Cancelado"}}},
            {"$unwind": "$lineas_detalle"},
            {"$lookup": {"from": "productos",
                         "localField": "lineas_detalle.producto_id",
                         "foreignField": "_id", "as": "producto"}},
            {"$unwind": "$producto"},
            {"$group": {"_id": "$producto.categoria",
                        "total_ventas": {"$sum": "$lineas_detalle.subtotal"}}},
        ]
        obtenido = {r["_id"]: r["total_ventas"] for r in self.db.pedidos.aggregate(pipeline)}
        self.assertEqual(obtenido, esperado)

    # --- F07 ---------------------------------------------------------------
    def test_F07_ticket_promedio(self):
        """F07 - Agregacion de ticket promedio coincide con el calculo manual

        Requisito: igual que F06 (segunda agregacion).
        Que hace: calcula a mano el promedio de los montos de los pedidos no
        cancelados y lo compara con el $avg de MongoDB.
        PASA si: ambos dan 98 750 (promedio de 190 000 y 7 500).
        FALLA si: el promedio incluye cancelados o se calcula mal.
        """
        totales = [p["monto_total"] for p in self.pedidos if p["estado"] != "Cancelado"]
        esperado = sum(totales) / len(totales)
        resultado = list(self.db.pedidos.aggregate([
            {"$match": {"estado": {"$ne": "Cancelado"}}},
            {"$group": {"_id": None, "ticket_promedio": {"$avg": "$monto_total"}}},
        ]))
        self.assertAlmostEqual(resultado[0]["ticket_promedio"], esperado, places=2)

    # --- F08 ---------------------------------------------------------------
    def test_F08_evolucion_del_esquema_sin_migracion(self):
        """F08 - Agregar un atributo o una categoria nueva sin migrar lo existente

        Requisito: "demostrar una evolucion del esquema incorporando un nuevo
        atributo o categoria sin una migracion relacional tradicional".
        Que hace: (1) agrega el atributo "genero" a una sola camiseta, (2) crea
        la categoria nueva "Servicios" con atributos propios, (3) agrega un campo
        "nota" a un solo pedido.
        PASA si: solo el documento modificado tiene el campo nuevo (los demas no
        se rellenan con nulos), y las consultas de antes siguen devolviendo lo
        mismo.
        FALLA si: el cambio exigiera tocar los demas documentos o rompiera las
        consultas existentes.
        """
        # atributo nuevo solo en un producto existente
        self.db.productos.update_one({"_id": "P-ROPA-1"},
                                     {"$set": {"atributos.genero": "Unisex"}})
        # categoria nueva con atributos propios
        self.db.productos.insert_one(crear_estructura_producto(
            "P-SERV-1", "Clase de yoga", 15000.0, "Servicios", "COM-T1", 0,
            {"duracion_minutos": 60, "modalidad": "Virtual"}))
        self.assertEqual(self.db.productos.count_documents({"atributos.genero": "Unisex"}), 1)
        otra_ropa = self.db.productos.find_one({"_id": "P-ROPA-2"})
        self.assertNotIn("genero", otra_ropa["atributos"])  # no se rellena con nulos
        # las consultas existentes siguen funcionando
        self.assertEqual(self.db.productos.count_documents({"categoria": "Ropa"}), 2)
        self.assertEqual(self.db.productos.count_documents({"categoria": "Servicios"}), 1)
        # tambien en pedidos: un campo nuevo no afecta al resto
        self.db.pedidos.update_one({"_id": "PED-T1"}, {"$set": {"nota": "Regalo"}})
        self.assertEqual(self.db.pedidos.count_documents({"nota": {"$exists": True}}), 1)
        self.assertEqual(self.db.pedidos.count_documents({"cliente_id": "CLI-T1"}), 2)

    # --- F09 ---------------------------------------------------------------
    def test_F09_validaciones_rechazan_datos_invalidos(self):
        """F09 - Las validaciones del modelo rechazan datos invalidos

        Requisito: reglas de validacion (tipos, requeridos, rangos, valores
        permitidos) pedidas en el README de database/schemas.
        Que hace: intenta crear nueve documentos invalidos con las funciones de
        modelos_de_estructuras.py (precio negativo, stock negativo, categoria
        inexistente, atributos que no son un diccionario, estado de comercio
        invalido, pedido sin lineas, estado de pedido invalido, cantidad cero y
        subtotal que no cuadra).
        PASA si: los nueve intentos lanzan ValueError (se rechazan).
        FALLA si: alguno se acepta. El nombre del caso aparece en el detalle.
        Limite: esto prueba la validacion de PYTHON. Lo que hace MongoDB por su
        cuenta lo prueba V5.
        """
        p, c, cl, ped = construir_datos()
        lineas_ok = ped[0]["lineas_detalle"]
        casos = {
            "precio negativo": lambda: crear_estructura_producto(
                "X", "n", -1.0, "Ropa", "COM-T1", 1, {}),
            "stock negativo": lambda: crear_estructura_producto(
                "X", "n", 1.0, "Ropa", "COM-T1", -1, {}),
            "categoria invalida": lambda: crear_estructura_producto(
                "X", "n", 1.0, "Inexistente", "COM-T1", 1, {}),
            "atributos no diccionario": lambda: crear_estructura_producto(
                "X", "n", 1.0, "Ropa", "COM-T1", 1, "texto"),
            "estado de comercio invalido": lambda: crear_estructura_comercio(
                "X", "n", "a@b.cr", "2222", "Ropa", "Cerrado", "p", "c", "d", "e"),
            "pedido sin lineas": lambda: crear_estructura_pedido(
                "X", datetime.now(), "CLI-T1", "Pendiente", []),
            "estado de pedido invalido": lambda: crear_estructura_pedido(
                "X", datetime.now(), "CLI-T1", "Perdido", lineas_ok),
            "cantidad cero": lambda: crear_estructura_pedido(
                "X", datetime.now(), "CLI-T1", "Pendiente",
                [dict(lineas_ok[0], cantidad=0, subtotal=0.0)]),
            "subtotal incorrecto": lambda: crear_estructura_pedido(
                "X", datetime.now(), "CLI-T1", "Pendiente",
                [dict(lineas_ok[0], subtotal=1.0)]),
        }
        for nombre, construir in casos.items():
            with self.subTest(caso=nombre):
                with self.assertRaises(ValueError):
                    construir()

    # --- F10 ---------------------------------------------------------------
    def test_F10_productos_de_un_comercio(self):
        """F10 - Consultar los productos asociados a un comercio especifico

        Requisito: caso de uso "consulta de productos asociados a un comercio"
        (propuesta inicial).
        Que hace: pide los productos del comercio COM-T1.
        PASA si: devuelve exactamente la camiseta y el pantalon (los de COM-T2 no).
        FALLA si: mezcla productos de otros comercios o se deja alguno.
        """
        ids = {p["_id"] for p in self.db.productos.find({"comercio_id": "COM-T1"})}
        self.assertEqual(ids, {"P-ROPA-1", "P-ROPA-2"})


# ----------------------------------------------------------------------------
# V1 - V5: comprobaciones de solo lectura sobre la base real ya cargada
# ----------------------------------------------------------------------------
class PruebasBaseCargada(unittest.TestCase):
    """Revisan los datos REALES (los 85 500 documentos). Solo leen, no modifican."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = conectar()
        cls.db = cls.cliente[NOMBRE_DB]
        if cls.db.productos.estimated_document_count() == 0:
            raise unittest.SkipTest("La base real esta vacia: cargue los datos primero")

    @classmethod
    def tearDownClass(cls):
        cls.cliente.close()

    def test_V1_volumen_minimo(self):
        """V1 - La base cumple el volumen minimo del caso (25 000 / 10 000 / 50 000)

        Requisito: "minimo 25 000 productos, 10 000 clientes y 50 000 pedidos".
        PASA si: hay al menos esa cantidad en cada coleccion.
        FALLA si: algun seed no se ejecuto completo.
        """
        self.assertGreaterEqual(self.db.productos.count_documents({}), 25000)
        self.assertGreaterEqual(self.db.clientes.count_documents({}), 10000)
        self.assertGreaterEqual(self.db.pedidos.count_documents({}), 50000)

    def test_V2_ocho_categorias(self):
        """V2 - El catalogo tiene al menos 8 categorias

        Requisito: "distribuidos en al menos 8 categorias con atributos variables".
        PASA si: hay 8 o mas categorias distintas en los productos.
        """
        self.assertGreaterEqual(len(self.db.productos.distinct("categoria")), 8)

    def test_V3_atributos_variables_por_categoria(self):
        """V3 - Las categorias tienen conjuntos de atributos distintos

        Requisito: "atributos variables" por categoria.
        Que hace: toma un producto de cada categoria y compara los nombres de sus
        atributos.
        PASA si: existe mas de un conjunto distinto de atributos (no todas las
        categorias comparten los mismos campos).
        FALLA si: todos los productos tuvieran los mismos atributos (como cuando
        el generador solo ponia "marca").
        """
        conjuntos = set()
        for categoria in self.db.productos.distinct("categoria"):
            producto = self.db.productos.find_one({"categoria": categoria})
            conjuntos.add(frozenset(producto["atributos"]))
        self.assertGreater(len(conjuntos), 1)

    def test_V4_pedidos_conservan_historial(self):
        """V4 - Las lineas de pedido guardan nombre, precio y subtotal coherentes (muestra de 1 000)

        Requisito: el pedido debe poder reconstruirse aunque cambie el producto.
        Que hace: revisa 1 000 pedidos reales. En cada linea verifica que esten
        los cinco campos, que subtotal = precio_unitario x cantidad, y que el
        monto_total del pedido sea la suma de sus subtotales.
        PASA si: los 1 000 pedidos son coherentes.
        FALLA si: algun pedido tiene campos faltantes o cuentas que no cuadran.
        """
        campos = {"producto_id", "nombre_producto", "precio_unitario", "cantidad", "subtotal"}
        for pedido in self.db.pedidos.find().limit(1000):
            suma = 0
            for l in pedido["lineas_detalle"]:
                self.assertTrue(campos.issubset(l), pedido["_id"])
                self.assertAlmostEqual(l["subtotal"], l["precio_unitario"] * l["cantidad"], places=2)
                suma += l["subtotal"]
            self.assertAlmostEqual(pedido["monto_total"], suma, places=2)

    def test_V5_validacion_en_mongodb(self):
        """V5 - MongoDB rechaza un producto invalido (requiere $jsonSchema en la coleccion)

        Requisito: reglas de validacion en la base (README de database/schemas).
        Que hace: si la coleccion productos tiene un validador $jsonSchema, intenta
        insertar un producto con precio negativo y categoria inexistente.
        PASA si: MongoDB lo rechaza (y la prueba lo borra si por error entrara).
        OMITIDA si: la coleccion no tiene $jsonSchema todavia. Hoy esperable: es
        un pendiente real, porque la validacion existe solo en Python y no en la base.
        """
        info = list(self.db.list_collections(filter={"name": "productos"}))
        validador = info[0].get("options", {}).get("validator") if info else None
        if not validador:
            self.skipTest("La coleccion productos no tiene $jsonSchema (pendiente de P4)")
        invalido = {"_id": "TEST-INVALIDO", "nombre": "x", "precio": -5,
                    "categoria": "Inexistente"}
        try:
            with self.assertRaises(WriteError):
                self.db.productos.insert_one(invalido)
        finally:
            self.db.productos.delete_one({"_id": "TEST-INVALIDO"})


# ----------------------------------------------------------------------------
# Ejecucion y registro de resultados
# ----------------------------------------------------------------------------
class Resultado(unittest.TextTestResult):
    """Igual que el resultado normal, pero ademas guarda cada prueba para el CSV."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filas = []

    def _registrar(self, test, estado, detalle=""):
        self.filas.append({
            "prueba": test.id().split(".")[-1],
            # shortDescription() es solo la PRIMERA linea del docstring
            "descripcion": test.shortDescription() or "",
            "resultado": estado,
            "detalle": " ".join(str(detalle).split())[:200],
        })

    def addSuccess(self, test):
        super().addSuccess(test)
        self._registrar(test, "OK")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._registrar(test, "FALLA", err[1])

    def addError(self, test, err):
        super().addError(test, err)
        self._registrar(test, "ERROR", err[1])

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._registrar(test, "OMITIDA", reason)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2, resultclass=Resultado)
    resultado = runner.run(suite)

    salida = RAIZ / "Performance" / "resultados"
    salida.mkdir(parents=True, exist_ok=True)
    with open(salida / "pruebas_funcionales.csv", "w", newline="",
              encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(
            f, fieldnames=["prueba", "descripcion", "resultado", "detalle"])
        escritor.writeheader()
        escritor.writerows(resultado.filas)
    print(f"\nResultados guardados en {salida / 'pruebas_funcionales.csv'}")
    sys.exit(0 if resultado.wasSuccessful() else 1)
