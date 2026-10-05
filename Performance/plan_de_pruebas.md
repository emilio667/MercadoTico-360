Plan de pruebas — MercadoTico 360 (MongoDB)

Responsable: Integrante 5 (QA & Performance) Estado: borrador inicial (Entregable 1)

1. Objetivo

Verificar que el modelo documental en MongoDB cumple los requisitos del caso MercadoTico 360 y demostrar con evidencia medible cómo mejoran los índices el desempeño de las consultas frecuentes.

2. Alcance
Colecciones: productos, clientes, pedidos.
Incluye pruebas funcionales, de desempeño (con y sin índice), de carga y de evolución del esquema.
Excluye interfaces de usuario, pasarelas de pago y logística.


4. Datos de prueba

Los datos son sintéticos y se generan de forma reproducible (semilla fija). Semilla utilizada: ___.

Productos: mínimo 25 000, en 8 o más categorías con atributos variables.
Clientes: mínimo 10 000, con dirección embebida (provincia, cantón, distrito).
Pedidos: mínimo 50 000, con varias líneas de detalle.


4. Entorno de pruebas

Completar al ejecutar las pruebas:

Sistema operativo:
CPU:
RAM:
Disco (SSD/HDD):
MongoDB (versión y modo: local, Docker o Atlas):
Python:
pymongo:


5. Pruebas de desempeño con y sin índice (prioridad)

Índices definidos por el grupo:

idx_categoria_precio (categoria: 1, precio: 1): debe acelerar la búsqueda por categoría y rango de precio.
idx_atributos_talla (atributos.talla: 1): debe acelerar el filtro por un atributo específico (talla).
idx_cliente_fecha (cliente_id: 1, fecha: -1): debe acelerar el historial de pedidos de un cliente.

Consultas a medir, cada una sin índice y con índice:

P1: productos por categoría y rango de precio.
P2: productos por categoría, rango de precio y talla.
P3: pedidos de un cliente ordenados por fecha.

Métricas por consulta (obtenidas con explain("executionStats") y con cronómetro en Python):

Tiempo de ejecución en ms: mediana y percentil 95.
Documentos examinados (totalDocsExamined).
Documentos devueltos (nReturned).
Etapa de ejecución: COLLSCAN (sin índice) frente a IXSCAN (con índice).


6. Otras pruebas de desempeño
P4. Carga masiva (seeding) del volumen mínimo. Métrica: tiempo total y documentos por segundo.
P5. Agregación de ventas por categoría. Métrica: tiempo de ejecución.
P6. Agregación de ticket promedio o productos más vendidos. Métrica: tiempo de ejecución.
P7. Lecturas concurrentes con 10, 50 y 100 hilos. Métrica: latencia media, percentil 95 y consultas por segundo.
P8. Actualización de estados de pedidos en lote. Métrica: tiempo y documentos modificados por segundo.


7. Pruebas funcionales
F1. Insertar productos de categorías distintas en la misma colección. Esperado: cada producto conserva sus atributos propios, sin campos nulos.
F2. Buscar por categoría, rango de precio y un atributo específico. Esperado: solo devuelve productos que cumplen los tres filtros.
F3. Recuperar todos los pedidos de un cliente. Esperado: pedidos completos con lineas_detalle anidadas.
F4. Actualizar el estado de un pedido. Esperado: cambia solo el campo estado.
F5. Cambiar el precio de un producto después de una compra. Esperado: el pedido histórico conserva el precio original.
F6. Agregación de ventas por categoría. Esperado: totales iguales a un cálculo manual.
F7. Agregación de ticket promedio o productos más vendidos. Esperado: resultado correcto y verificado.
F8. Agregar un atributo o categoría nueva. Esperado: se inserta sin migración y las consultas existentes siguen funcionando.


8. Metodología
Cargar los datos con la semilla fija.
Ejecutar una corrida de calentamiento y descartarla.
Repetir cada prueba 30 veces y registrar cada tiempo.
Medir primero sin índice, luego crear el índice y volver a medir, en el mismo entorno.
Reportar mediana y percentil 95 (no una sola medición).
Guardar los resultados crudos en resultados/*.csv y las capturas de explain() en resultados/capturas/.
Generar con esos CSV las tablas y gráficos de la sección de resultados del paper.


9. Criterios de aceptación
Todas las pruebas funcionales (F1 a F8) pasan.
Con índice, explain() muestra IXSCAN y examina menos documentos que sin índice.
Con índice, la mediana de tiempo baja respecto a la medición sin índice en las consultas P1 a P3.
Umbrales de tiempo aceptables: por acordar con el grupo tras las primeras mediciones.


10. Dependencias
Integrante 3: datos cargados con el volumen mínimo.
Integrante 4: consultas, agregaciones y operaciones CRUD a medir.


11. Entregables de esta etapa
Scripts en Performance/scripts/.
Resultados en Performance/resultados/.
Sección de pruebas y resultados del paper.




Parte resumida para la prueba iniical:


Plan de pruebas y riesgos técnicos
Plan de pruebas

Objetivo: verificar que el modelo documental en MongoDB cumple los requisitos del caso MercadoTico 360 y medir cómo los índices mejoran el desempeño de las consultas frecuentes.

Datos de prueba: datos sintéticos generados con semilla fija: 25 000 productos (8 o más categorías), 10 000 clientes y 50 000 pedidos con varias líneas de detalle.

Entorno: MongoDB [versión] con Python y pymongo. Se documentarán el hardware y las versiones utilizadas.

Pruebas de desempeño:

Búsqueda por categoría, rango de precio y atributo específico, sin y con índice. Se mide el tiempo, los documentos examinados y la etapa de ejecución (COLLSCAN vs IXSCAN).
Recuperación de los pedidos de un cliente ordenados por fecha, sin y con índice, con las mismas métricas.
Dos agregaciones: ventas por categoría y ticket promedio. Se mide el tiempo de ejecución.
Carga masiva de datos y lecturas concurrentes (10, 50 y 100 hilos). Se mide documentos por segundo, latencia media y percentil 95.

Pruebas funcionales:

Productos de distintas categorías conviven en una misma colección, con sus atributos propios y sin campos nulos.
Al cambiar el precio de un producto después de una compra, el pedido histórico conserva el precio original.
Agregar un atributo o una categoría nueva no requiere migración y no rompe las consultas existentes.

Metodología: cada prueba se ejecuta con una corrida de calentamiento y 30 repeticiones, y se reporta la mediana y el percentil 95. La medición sin índice se hace antes de crear el índice, sobre los mismos datos. Los resultados se guardan en CSV, junto con capturas de explain().
