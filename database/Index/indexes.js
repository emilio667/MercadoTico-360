// =============================================================================
// indexes.js - Indices de MercadoTico 360 (MongoDB 7.0)
//
// Crea de forma reproducible los indices que optimizan las consultas frecuentes.
// Es seguro ejecutarlo varias veces: si un indice ya existe con la misma
// definicion, MongoDB no lo vuelve a crear.
//
// COMO EJECUTARLO (con los datos ya cargados, ver README de la raiz)
//   Opcion A - mongosh:
//     mongosh "mongodb://localhost:27017" --file database/Index/indexes.js
//   Opcion B - MongoDB Compass: boton "Open MongoDB shell", pegar este archivo.
//
// COMO VERIFICAR
//   db.productos.getIndexes()
//   db.pedidos.getIndexes()
//
// EVIDENCIA ANTES/DESPUES (Performance/resultados_final/, 30 repeticiones,
// mediana, MongoDB 7.0.28 local, 25 000 productos y 50 000 pedidos):
//   Consulta                           sin indice   con indice   docs examinados
//   Categoria                            39.3 ms      30.5 ms     25 000 -> 3 270
//   Rango de precio                      62.4 ms      10.4 ms     25 000 -> 990
//   Categoria + rango de precio          47.1 ms       4.9 ms     25 000 -> 329
//   Categoria + precio + talla           51.7 ms       6.1 ms     25 000 -> 1 273
//   Productos de un comercio             48.0 ms       1.0 ms     25 000 -> 54
//   Pedidos de un cliente (por fecha)   114.9 ms       0.5 ms     50 000 -> 7
//   Pedidos que contienen un producto   234.8 ms       0.5 ms     50 000 -> 5
//
// NOTA: Performance/scripts/benchmark.py borra y recrea estos mismos indices
// (mismos nombres) durante su ejecucion y los elimina al terminar, salvo que se
// use --keep-indexes. Si se corre el benchmark, volver a ejecutar este archivo.
// =============================================================================

db = db.getSiblingDB("MercadoTico360");

// -----------------------------------------------------------------------------
// PATRONES REQUERIDOS POR EL ENUNCIADO (productos)
// -----------------------------------------------------------------------------

// 1) Busqueda por categoria y 3) busqueda por categoria + rango de precio
//    Indice compuesto (categoria, precio): la categoria (igualdad) va primero y
//    el precio (rango) despues. Un solo indice cubre las dos consultas, porque
//    el prefijo "categoria" sirve para filtrar solo por categoria.
//    Ejemplo: { categoria: "Tecnologia", precio: { $gte: 100000, $lte: 500000 } }
db.productos.createIndex(
  { categoria: 1, precio: 1 },
  { name: "idx_categoria_precio" }
);

// 2) Busqueda por rango de precio (sin categoria)
//    El indice compuesto anterior no sirve cuando no se filtra por categoria,
//    porque el precio no es su prefijo.
//    Ejemplo: { precio: { $gte: 100000, $lte: 500000 } }
db.productos.createIndex(
  { precio: 1 },
  { name: "idx_precio" }
);

// -----------------------------------------------------------------------------
// PATRON REQUERIDO POR EL ENUNCIADO (pedidos)
// -----------------------------------------------------------------------------

// 4) Pedidos de un cliente, del mas reciente al mas antiguo
//    (cliente_id, fecha descendente): filtra por cliente y devuelve los pedidos
//    ya ordenados por fecha, sin ordenar en memoria.
//    Ejemplo: db.pedidos.find({ cliente_id: "CLI-00001" }).sort({ fecha: -1 })
db.pedidos.createIndex(
  { cliente_id: 1, fecha: -1 },
  { name: "idx_cliente_fecha" }
);

// -----------------------------------------------------------------------------
// INDICES ADICIONALES (atributos variables, comercios y lineas de pedido)
// -----------------------------------------------------------------------------

// Atributo especifico de una categoria (ejemplo: talla de la ropa)
//    Indexa un campo del objeto embebido "atributos". Solo incluye los
//    documentos que tienen ese atributo, por lo que es pequeno.
//    Ejemplo: { categoria: "Ropa", "atributos.talla": "M" }
db.productos.createIndex(
  { "atributos.talla": 1 },
  { name: "idx_atributos_talla" }
);

// Productos de un comercio
//    Ejemplo: { comercio_id: "COM-001" }
db.productos.createIndex(
  { comercio_id: 1 },
  { name: "idx_comercio" }
);

// Pedidos que contienen un producto
//    Indice multikey sobre el arreglo embebido "lineas_detalle": genera una
//    entrada por cada linea de pedido, por lo que es el mas costoso de crear
//    (alrededor de 1.4 s con 50 000 pedidos).
//    Ejemplo: { "lineas_detalle.producto_id": "PROD-00001" }
db.pedidos.createIndex(
  { "lineas_detalle.producto_id": 1 },
  { name: "idx_lineas_producto" }
);

// -----------------------------------------------------------------------------
// RESUMEN
// -----------------------------------------------------------------------------
print("Indices de productos:");
db.productos.getIndexes().forEach(function (i) { print("  " + i.name); });
print("Indices de pedidos:");
db.pedidos.getIndexes().forEach(function (i) { print("  " + i.name); });

// Para eliminarlos (por ejemplo, antes de una demostracion "sin indice"):
//   ["idx_categoria_precio", "idx_precio", "idx_atributos_talla", "idx_comercio"]
//     .forEach(function (n) { db.productos.dropIndex(n); });
//   ["idx_cliente_fecha", "idx_lineas_producto"]
//     .forEach(function (n) { db.pedidos.dropIndex(n); });
