# Plan de pruebas — MercadoTico 360 (MongoDB)

**Responsable:** Integrante 5 (QA & Performance)
**Estado:** borrador inicial (Entregable 1)

## 1. Objetivo

Verificar que el modelo documental en MongoDB cumple los requisitos del caso MercadoTico 360 y **demostrar con evidencia medible cómo mejoran los índices el desempeño** de las consultas frecuentes.

## 2. Alcance

- Colecciones: `productos`, `clientes`, `pedidos`.
- Incluye pruebas funcionales, de desempeño (con y sin índice), de carga y de evolución del esquema.
- Excluye interfaces de usuario, pasarelas de pago y logística.

## 3. Datos de prueba

| Colección | Mínimo exigido | Notas |
|---|---|---|
| productos | 25 000 | 8 o más categorías con atributos variables |
| clientes | 10 000 | Con dirección embebida (provincia, cantón, distrito) |
| pedidos | 50 000 | Con varias líneas de detalle |

Los datos son sintéticos y se generan de forma reproducible (semilla fija). Semilla utilizada: `___`.

## 4. Entorno de pruebas

Completar al ejecutar las pruebas.

| Componente | Valor |
|---|---|
| Sistema operativo | |
| CPU | |
| RAM | |
| Disco (SSD/HDD) | |
| MongoDB (versión y modo: local/Docker/Atlas) | |
| Python | |
| pymongo | |

## 5. Pruebas de desempeño con y sin índice (prioridad)

Índices definidos por el grupo:

| Índice | Campos | Consulta que debe acelerar |
|---|---|---|
| `idx_categoria_precio` | `categoria: 1, precio: 1` | Búsqueda por categoría y rango de precio |
| `idx_atributos_talla` | `atributos.talla: 1` | Filtro por atributo específico (talla) |
| `idx_cliente_fecha` | `cliente_id: 1, fecha: -1` | Historial de pedidos de un cliente |

| ID | Consulta | Sin índice | Con índice |
|---|---|---|---|
| P1 | Productos por categoría + rango de precio | Medir | Medir |
| P2 | Productos por categoría + rango de precio + talla | Medir | Medir |
| P3 | Pedidos de un cliente ordenados por fecha | Medir | Medir |

**Métricas por consulta** (obtenidas con `explain("executionStats")` y con cronómetro en Python):

- Tiempo de ejecución (ms): mediana y percentil 95.
- Documentos examinados (`totalDocsExamined`).
- Documentos devueltos (`nReturned`).
- Etapa de ejecución: `COLLSCAN` (sin índice) vs `IXSCAN` (con índice).

## 6. Otras pruebas de desempeño

| ID | Prueba | Métrica |
|---|---|---|
| P4 | Carga masiva (seeding) del volumen mínimo | Tiempo total y documentos por segundo |
| P5 | Agregación: ventas por categoría | Tiempo de ejecución |
| P6 | Agregación: ticket promedio o productos más vendidos | Tiempo de ejecución |
| P7 | Lecturas concurrentes (10, 50 y 100 hilos) | Latencia media, p95 y consultas por segundo |
| P8 | Actualización de estados de pedidos en lote | Tiempo y documentos modificados por segundo |

## 7. Pruebas funcionales

| ID | Prueba | Resultado esperado |
|---|---|---|
| F1 | Insertar productos de categorías distintas en la misma colección | Cada producto conserva sus atributos propios, sin campos nulos |
| F2 | Buscar por categoría + rango de precio + un atributo específico | Solo devuelve productos que cumplen los tres filtros |
| F3 | Recuperar todos los pedidos de un cliente | Pedidos completos con `lineas_detalle` anidadas |
| F4 | Actualizar el estado de un pedido | Cambia solo el campo `estado` |
| F5 | Cambiar el precio de un producto después de una compra | El pedido histórico conserva el precio original |
| F6 | Agregación de ventas por categoría | Totales iguales a un cálculo manual |
| F7 | Agregación de ticket promedio o productos más vendidos | Resultado correcto y verificado |
| F8 | Agregar un atributo o categoría nueva | Se inserta sin migración y las consultas existentes siguen funcionando |

## 8. Metodología

1. Cargar los datos con la semilla fija.
2. Ejecutar una corrida de calentamiento y descartarla.
3. Repetir cada prueba **N = 30** veces y registrar cada tiempo.
4. Medir primero **sin índice** y después crear el índice y volver a medir, en el mismo entorno.
5. Reportar mediana y percentil 95 (no una sola medición).
6. Guardar los resultados crudos en `resultados/*.csv` y las capturas de `explain()` en `resultados/capturas/`.
7. Generar con esos CSV las tablas y gráficos de la Sección 6 del paper.

## 9. Criterios de aceptación

- Todas las pruebas funcionales (F1 a F8) pasan.
- Con índice, `explain()` muestra `IXSCAN` y examina menos documentos que sin índice.
- Con índice, la mediana de tiempo baja respecto a la medición sin índice en las consultas P1 a P3.
- Umbrales de tiempo aceptables: por acordar con el grupo tras las primeras mediciones.

## 10. Dependencias

- **Integrante 3:** datos cargados con el volumen mínimo.
- **Integrante 4:** consultas, agregaciones y operaciones CRUD a medir.

## 11. Entregables de esta etapa

- Scripts en `Performance/scripts/`.
- Resultados en `Performance/resultados/`.
- Sección 6 (Pruebas y Resultados) del paper.
