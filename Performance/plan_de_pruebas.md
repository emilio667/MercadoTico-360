# Plan de pruebas — MercadoTico 360 (MongoDB)

**Responsable:** Integrante 5 (QA & Performance)  
**Estado:** Ejecutado y documentado

## 1. Objetivo

Verificar que el modelo documental en MongoDB cumple los requisitos del caso MercadoTico 360 y demostrar, mediante evidencia medible, cómo los índices mejoran el desempeño de las consultas frecuentes.

## 2. Alcance

Colecciones evaluadas: `productos`, `clientes`, `pedidos` y `comercios`.

El plan incluye pruebas funcionales, pruebas de desempeño con y sin índices, pruebas de carga, concurrencia y evolución del esquema.

Se excluyen interfaces de usuario, pasarelas de pago y procesos logísticos externos.

## 3. Datos de prueba

Los datos utilizados son sintéticos y fueron generados con Python de forma reproducible.

- Productos: 25 000 documentos distribuidos en 8 categorías, con atributos variables según la categoría.
- Comercios: 500 documentos.
- Clientes: 10 000 documentos con dirección embebida.
- Pedidos: 50 000 documentos con múltiples líneas de detalle.

En total, el conjunto principal contiene 85 500 documentos.

## 4. Entorno de pruebas

Las pruebas se ejecutan sobre el entorno documentado por el grupo para MercadoTico 360, utilizando MongoDB, Python y PyMongo.

Las versiones de software y las características del equipo utilizado para las mediciones se registran junto con los resultados, con el fin de permitir la reproducibilidad de las pruebas.

## 5. Pruebas de desempeño con y sin índice

Los índices utilizados fueron definidos a partir de los patrones de consulta más frecuentes del sistema.

Entre ellos se incluyen:

- Índice compuesto sobre `categoria` y `precio`, utilizado en búsquedas de productos por categoría y rango de precio.
- Índices sobre atributos variables dentro de `atributos`, utilizados para filtrar productos según características específicas de cada categoría.
- Índice compuesto sobre `cliente_id` y `fecha`, utilizado para recuperar el historial de pedidos de un cliente.
- Índices adicionales utilizados para otras consultas frecuentes evaluadas durante las pruebas.

Las consultas relevantes se ejecutaron primero sin los índices correspondientes y posteriormente con los índices creados.

Para cada consulta se registraron las siguientes métricas:

- Tiempo de ejecución en milisegundos.
- Mediana de las ejecuciones.
- Percentil 95.
- Documentos examinados (`totalDocsExamined`).
- Documentos devueltos (`nReturned`).
- Plan de ejecución obtenido mediante `explain("executionStats")`.
- Cambio de `COLLSCAN` a `IXSCAN` cuando corresponde.

## 6. Pruebas de desempeño realizadas

### P1. Consultas sobre productos

Se evaluaron diferentes patrones de búsqueda, entre ellos:

- Productos por categoría.
- Productos por rango de precio.
- Productos por categoría y rango de precio.
- Productos por atributos específicos.
- Combinaciones entre categoría, precio y atributos variables.

El objetivo fue comprobar la reducción del tiempo de ejecución y de los documentos examinados después de aplicar los índices correspondientes.

### P2. Consultas sobre pedidos

Se evaluaron consultas como:

- Recuperación de los pedidos de un cliente.
- Pedidos filtrados por estado.
- Pedidos asociados a un producto.
- Combinaciones entre cliente y estado.

Se verificó especialmente el comportamiento de las consultas sobre grandes cantidades de pedidos antes y después de aplicar índices.

### P3. Agregaciones

Se evaluaron operaciones analíticas utilizando el Aggregation Framework de MongoDB, entre ellas:

- Ventas por categoría.
- Productos más vendidos.
- Ticket promedio.
- Ventas por estado.
- Ventas de una categoría específica.

Para estas operaciones se registró el tiempo de ejecución.

### P4. Carga masiva

Se midió el proceso de carga de los datos sintéticos utilizados por el proyecto.

Las métricas consideradas incluyen:

- Tiempo total de carga.
- Cantidad de documentos procesados.
- Documentos insertados por segundo.

### P5. Concurrencia

Se realizaron pruebas de lectura concurrente utilizando diferentes cantidades de hilos.

Se evaluaron escenarios con:

- 10 hilos.
- 50 hilos.
- 100 hilos.

Las métricas utilizadas fueron:

- Latencia promedio.
- Percentil 95.
- Consultas ejecutadas por segundo.

## 7. Pruebas funcionales

### F1. Atributos variables

Se verifica que productos pertenecientes a diferentes categorías puedan convivir en la misma colección y mantener atributos específicos según su tipo.

**Resultado esperado:** los productos conservan únicamente los atributos que corresponden a su categoría, sin necesidad de utilizar una estructura idéntica para todos los documentos.

### F2. Consultas de productos

Se prueban búsquedas por categoría, rango de precio y atributos específicos.

**Resultado esperado:** únicamente se recuperan los productos que cumplen los filtros definidos.

### F3. Historial de pedidos

Se recuperan los pedidos asociados a un cliente.

**Resultado esperado:** cada pedido contiene sus líneas de detalle anidadas y mantiene la información correspondiente a la compra.

### F4. Actualización de estado

Se modifica el estado de un pedido mediante una actualización parcial.

**Resultado esperado:** únicamente cambia el campo `estado`, sin necesidad de reescribir el documento completo.

### F5. Integridad histórica

Se modifica el precio actual de un producto después de haber sido comprado.

**Resultado esperado:** el pedido histórico conserva el precio unitario registrado al momento de la compra.

### F6. Ventas por categoría

Se ejecuta la agregación de ventas por categoría.

**Resultado esperado:** los totales obtenidos coinciden con los datos almacenados en los pedidos.

### F7. Indicadores comerciales

Se ejecutan agregaciones como ticket promedio y productos más vendidos.

**Resultado esperado:** los resultados corresponden a los datos utilizados durante la prueba.

### F8. Evolución del esquema

Se agrega un atributo nuevo dentro del objeto `atributos` de un producto existente.

**Resultado esperado:** el nuevo atributo puede incorporarse sin realizar una migración tradicional sobre los demás documentos y sin afectar las consultas existentes.

## 8. Validación y consistencia

El proyecto utiliza validaciones implementadas en Python para controlar la estructura esperada de los documentos generados y utilizados por la aplicación.

Estas validaciones permiten verificar campos obligatorios, valores permitidos y reglas básicas de consistencia antes de construir los documentos.

Actualmente no se utiliza un esquema `$jsonSchema` obligatorio directamente en MongoDB, por lo que la consistencia depende principalmente de la lógica implementada en la aplicación.

## 9. Metodología

Para las pruebas de rendimiento se sigue el siguiente procedimiento:

1. Utilizar el mismo conjunto de datos para las comparaciones.
2. Ejecutar corridas de calentamiento antes de registrar las mediciones.
3. Repetir cada consulta 30 veces.
4. Registrar los tiempos obtenidos.
5. Calcular la mediana y el percentil 95.
6. Ejecutar las consultas sin índice.
7. Crear los índices correspondientes.
8. Repetir las mismas consultas.
9. Comparar los resultados antes y después.
10. Analizar los planes de ejecución mediante `explain("executionStats")`.

Los resultados se almacenan en archivos CSV y otros archivos de evidencia dentro del directorio de resultados del proyecto.

También se conservan capturas y salidas de `explain()` utilizadas para demostrar el comportamiento de las consultas con y sin índices.

## 10. Criterios de aceptación

Las pruebas se consideran satisfactorias cuando:

- Las pruebas funcionales principales se completan correctamente.
- Las consultas utilizan `IXSCAN` después de aplicar los índices correspondientes.
- Se reduce la cantidad de documentos examinados respecto a una ejecución con `COLLSCAN`.
- La mediana del tiempo de ejecución disminuye en las consultas donde el índice resulta aplicable.
- Los pedidos conservan correctamente la información histórica.
- La evolución del esquema puede realizarse sin una migración tradicional.
- Las agregaciones generan resultados coherentes con los datos almacenados.

## 11. Dependencias

- Generación y carga de los datos sintéticos.
- Consultas y operaciones CRUD implementadas para MercadoTico 360.
- Scripts de creación y eliminación de índices.
- Scripts de pruebas funcionales y de rendimiento.
- Entorno de MongoDB disponible durante las mediciones.

## 12. Evidencias generadas

Como resultado de este plan se generan:

- Archivos CSV con las mediciones de rendimiento.
- Resultados de las pruebas funcionales.
- Evidencias de consultas antes y después de utilizar índices.
- Salidas de `explain("executionStats")`.
- Resultados de pruebas de carga y concurrencia.
- Tablas y gráficos utilizados en el paper y en la presentación.