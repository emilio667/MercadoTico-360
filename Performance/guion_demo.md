# Guion de la demostración en vivo — MercadoTico 360

Las pantallas y los nombres de botones de Compass pueden variar un poco según la versión instalada. Ensáyalo una vez con tu versión antes de la presentación.

## 1. Reparto del tiempo (15 min + 5 de preguntas)

Sigue el orden del "contenido mínimo" que pide el enunciado.

| Minutos | Bloque |
|---|---|
| 0:00 – 1:30 | Problema del cliente y qué pasa si no se resuelve |
| 1:30 – 3:00 | Propuesta de valor y por qué un modelo de documentos (MongoDB) |
| 3:00 – 4:30 | Arquitectura y modelo de datos (qué se embebe y qué se referencia) |
| 4:30 – 5:00 | Decisiones técnicas de la implementación |
| 5:00 – 10:00 | **Demostración en vivo** (sección 3) |
| 10:00 – 12:00 | Resultados y métricas (gráficos, tres corridas, tests) |
| 12:00 – 13:30 | Riesgos, limitaciones, costos y mejoras |
| 13:30 – 15:00 | Cierre comercial |
| 15:00 – 20:00 | Preguntas (pueden dirigirse a cualquier integrante) |

Repártanse los bloques para que **todos hablen**.

## 2. Antes de la demo

### La noche anterior
- [ ] `git pull --no-edit` y confirma que todo corre con lo último del repo.
- [ ] MongoDB corriendo: `Get-Service *mongo*` debe decir `Running`.
- [ ] Datos cargados: 500 comercios, 10 000 clientes, 25 000 productos, 50 000 pedidos.
- [ ] Ensayo completo con cronómetro: `python Performance/scripts/demo.py --auto` (corre todo sin pausas).
- [ ] Prueba de los tests: `python test/test_funcionales.py`.

### 30 minutos antes
- [ ] Terminal abierta en la raíz del repo, con `(venv)` activo, letra grande (`Ctrl` + `+`).
- [ ] Compass abierto y conectado a `mongodb://localhost:27017`, base `MercadoTico360`.
- [ ] Gráficos abiertos en otra ventana (`Performance/resultados_corrida3/graficos/`).
- [ ] Notificaciones silenciadas, computador conectado a la corriente.
- [ ] Revisar en Compass > `pedidos` > **Indexes** que no haya índices propios del grupo sobre `cliente_id` (el demo no los toca, pero conviene saberlo).

### Plan B (por si algo falla)
- Capturas de `explain` sin y con índice: `Performance/resultados*/capturas/`.
- Gráficos ya generados.
- Un video corto de la demo grabado en el ensayo.
- Copia de los JSON de datos fuera del repo.

## 3. La demostración (5 minutos)

**Recomendación:** haz los pasos 2 a 6 con `demo.py`, porque no modifica los datos reales, no se equivoca al escribir y trabaja con copias temporales. Usa Compass para **mostrar** los documentos y los índices.

```powershell
python Performance/scripts/demo.py --pasos 2,3,4,5,6 --mantener-indices
```

Cada paso se detiene hasta que presiones Enter, así controlas el ritmo.

### Paso 2 — Catálogo heterogéneo (45 s)
**Terminal:** el script muestra un producto de Ropa y uno de Tecnología.
**Compass:** `MercadoTico360` > `productos` > en el filtro escribe `{ "categoria": "Ropa" }` y **Find**. Cambia la vista con los íconos de la derecha (lista, JSON, tabla).
**Qué decir:** "Es una sola colección. La ropa tiene talla y color, la tecnología tiene garantía. En un modelo relacional serían muchas columnas vacías o tablas hijas."

### Paso 3 — Pedido anidado (45 s)
**Terminal:** busca un pedido por `_id` y lo muestra con sus líneas.
**Compass:** colección `pedidos`, filtro `{ "estado": "Entregado" }` (o el `_id` del pedido que muestre el script), despliega `lineas_detalle`.
**Qué decir:** "El pedido lleva sus líneas dentro, con el nombre y el precio del momento de la compra. Leerlo es una sola consulta, sin JOINs."

### Paso 4 — Índices: antes y después (1 min 45 s) — la evidencia principal
**Terminal:** para cada consulta muestra el recorrido completo (`COLLSCAN`, 50 000 documentos examinados), te deja pausar, crea el índice y repite (`IXSCAN`, pocos documentos).
**Compass (para que se vea visualmente):**
1. `pedidos` > pestaña **Documents**, escribe el filtro con el `cliente_id` que imprime el script (por ejemplo `{ "cliente_id": "CLI-07282" }`) y busca el botón **Explain** en la barra de consulta (junto a **Find**). En tu versión de Compass no existe la pestaña "Explain Plan" (las pestañas son Documents, Aggregations, Schema, Indexes y Validation), así que si no encuentras el botón, usa el atajo de la consola de comandos (**Open MongoDB shell**, arriba a la derecha) con el comando de abajo. Con el índice `demo_cliente_fecha` ya creado verás `IXSCAN`.
2. Pestaña **Indexes**: ahí aparece `demo_cliente_fecha` (por eso se usa `--mantener-indices`). Muéstralo y explica sus dos campos (`cliente_id` ascendente y `fecha` descendente).

Si prefieres escribirlo en la consola de comandos de Compass (`_MONGOSH`, abajo):
```javascript
db.pedidos.find({cliente_id: "CLI-07282"}).sort({fecha: -1}).explain("executionStats")   // usa el cliente que imprime demo.py
```
**Qué decir:** "Sin índice MongoDB revisó 50 000 pedidos para devolver 6. Con el índice, 6. Pasó de unos 100 ms a menos de 1 ms. Lo medimos 30 veces con mediana y percentil 95 en tres corridas."

### Paso 5 — Evolución del esquema (45 s)
**Terminal:** agrega el atributo `genero` a un solo producto y crea la categoría `Servicios`, en una colección temporal.
**Qué decir:** "Agregamos un atributo y una categoría sin ALTER TABLE ni migración. Solo cambia el documento que lo necesita."

### Paso 6 — El historial no cambia (45 s)
**Terminal:** sube el precio de un producto y muestra que el pedido anterior conserva el precio original.
**Qué decir:** "Es la integridad histórica que pedía el cliente: lo que compró hoy no cambia aunque el precio suba mañana."

### Paso 7 — Validación (opcional, 15 s)
Úsalo solo si les queda tiempo, o si ya agregaron `$jsonSchema` (entonces dirá "Activa"). Hoy el script muestra con honestidad que la validación vive en Python y que la de MongoDB está pendiente.

### Después de la demo
Para cerrar, desde la terminal: `python test/test_funcionales.py` (tarda segundos). Muestra que las pruebas pasan.

## 4. Preguntas probables y respuestas cortas

| Pregunta | Respuesta |
|---|---|
| ¿Por qué MongoDB y no un modelo relacional? | El catálogo tiene atributos distintos por categoría y los pedidos son estructuras anidadas; el modelo de documentos lo guarda sin columnas vacías ni JOINs. |
| ¿Qué embeben y qué referencian? | Las líneas van embebidas en el pedido (se leen juntas y deben quedar fijas); cliente y comercio se referencian por ID porque cambian de forma independiente. |
| ¿Cómo saben que usó el índice? | Con `explain()`: la etapa pasa de `COLLSCAN` a `IXSCAN` y baja el número de documentos examinados. |
| ¿Por qué mediana y no promedio? | Una medición lenta aislada distorsiona el promedio. Reportamos también el percentil 95. |
| ¿Por qué la consulta por categoría no mejoró? | Devuelve una octava parte del catálogo, así que el costo está en leer esos documentos, no en encontrarlos (es una hipótesis que reportamos como resultado). |
| ¿Por qué ventas por categoría tarda unos 40 s? | La línea del pedido no guarda la categoría y hace falta un `$lookup` a productos por cada línea. La mejora es guardar la categoría en la línea. |
| ¿Dónde midieron, Atlas o local? | En MongoDB 7.0.28 local, una instancia única, porque es reproducible sin credenciales. No se midió el rendimiento en Atlas. |
| ¿Qué pasa si cae el servicio? | En Atlas el clúster es un conjunto de réplicas con failover automático. En local es una sola instancia sin réplica, y es una limitación. |
| ¿Escala? | MongoDB permite réplicas y sharding, pero no lo medimos; está fuera del alcance. |
| ¿Los datos son reales? | No, son sintéticos (Faker), y es una limitación. |
| ¿Qué mejorarían? | Validación `$jsonSchema` en la base, categoría dentro de la línea del pedido, y datos con semilla fija para reproducibilidad. |

## 5. Qué NO hacer

- **No correr el benchmark completo en vivo:** tarda minutos y la agregación sola unos 40 s. Muestra los gráficos y di dónde están los CSV y el método.
- **No editar datos reales en Compass** durante la demo sin copiarlos antes. Para modificar, usa `demo.py` o una colección temporal.
- **No afirmar nada sobre el rendimiento en Atlas.**
- **No esconder limitaciones.** La defensa técnica vale 10 % y la rúbrica premia reconocer limitaciones y riesgos; es además el primer criterio de desempate.
- **No leer el paper.** El enunciado pide una venta técnica a un cliente, no una lectura.
