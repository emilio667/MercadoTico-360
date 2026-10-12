# Performance — pruebas funcionales y de desempeño

Pruebas de MercadoTico 360 sobre MongoDB 7.0: verificación funcional de los
requisitos del caso y medición del rendimiento con y sin índices.

## Contenido

| Ruta | Qué es |
|---|---|
| `scripts/benchmark.py` | Mide consultas sin y con índice, agregaciones, concurrencia y carga masiva |
| `scripts/graficos.py` | Dibuja los gráficos a partir de los CSV del benchmark |
| `scripts/demo.py` | Demostración en vivo paso a paso (no modifica los datos reales) |
| `guion_demo.md` | Guion de la demostración en vivo |
| `plan_de_pruebas.md` | Plan de pruebas |
| `Riesgos` | Riesgos técnicos identificados |
| `resultados_final/` | **Corrida final** (datos con semilla): CSV, `entorno.json`, capturas de `explain()` y gráficos |
| `resultados_corrida2/`, `resultados_corrida3/` | Corridas preliminares (datos generados sin semilla fija) |
| `resultados/` | Resultado de las pruebas funcionales (`pruebas_funcionales.csv`) |

Relacionados fuera de esta carpeta: `../test/test_funcionales.py` (pruebas
funcionales) y `../database/Index/indexes.js` (índices evaluados).

## Cómo reproducir

### Prerrequisitos
- Python 3 y MongoDB 7.0 corriendo en local (`mongodb://localhost:27017`).
- Archivo `.env` en la raíz del repositorio (copiar `.env.example`) con:
  ```
  MONGODB_URI=mongodb://localhost:27017
  MONGODB_DB=MercadoTico360
  ```

### 1. Entorno virtual y dependencias
Desde la raíz del repositorio:

```powershell
python -m venv venv
venv\Scripts\activate            # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
pip install psutil               # opcional: el benchmark registra la RAM
```

### 2. Cargar los datos
Los datasets, generados con semilla fija (`Faker.seed(123)` y `random.seed(123)`),
están versionados en `database/seed/`. No hace falta regenerarlos:

```powershell
python -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017').drop_database('MercadoTico360')"
python -m database.seed.seed_data
```

Resultado esperado: 500 comercios, 10 000 clientes, 25 000 productos y
50 000 pedidos.

### 3. Pruebas funcionales
```powershell
python test/test_funcionales.py
```
Resultado esperado: 14 pruebas OK y 1 omitida (V5: la colección `productos` no
tiene validación `$jsonSchema`). Guarda `Performance/resultados/pruebas_funcionales.csv`.

Las pruebas F01–F10 usan una base aparte (`MercadoTico360_test`) que se crea y
se elimina sola. Las V1–V5 solo leen la base real.

### 4. Benchmark de rendimiento
```powershell
python Performance/scripts/benchmark.py --out Performance/resultados_final
```

Corrida corta de prueba: `--reps 5 --agg-reps 2 --skip-concurrency --skip-load`.
Para conservar los índices al terminar: `--keep-indexes`.

Mide, con una corrida de calentamiento descartada y 30 repeticiones (5 en las
agregaciones), mediana y percentil 95:
- 7 consultas sin y con índice (tiempo, documentos examinados y plan de `explain()`).
- 3 agregaciones.
- Lecturas concurrentes con 10, 50 y 100 hilos.
- Carga masiva en colecciones temporales `bench_*`, que se eliminan al terminar.

> **Importante:** el benchmark borra y recrea los índices `idx_categoria_precio`,
> `idx_precio`, `idx_atributos_talla`, `idx_comercio`, `idx_cliente_fecha` e
> `idx_lineas_producto`, y los elimina al terminar. Ejecutarlo solo sobre una
> base local, nunca sobre una base compartida. Si existen otros índices, se
> detiene para no falsear la medición "sin índice". Después de correrlo, volver a
> ejecutar `database/Index/indexes.js` si se necesitan los índices.

### 5. Índices
```powershell
mongosh "mongodb://localhost:27017" --file database/Index/indexes.js
```
O pegar el contenido de `indexes.js` en la consola de MongoDB Compass
(**Open MongoDB shell**).

### 6. Gráficos
```powershell
python Performance/scripts/graficos.py --entrada Performance/resultados_final
```
Genera `fig1_consultas_indices.png`, `fig2_docs_examinados.png`,
`fig3_concurrencia.png` y `fig4_agregaciones.png` en `resultados_final/graficos/`.

### 7. Demostración
```powershell
python Performance/scripts/demo.py                       # paso a paso (Enter)
python Performance/scripts/demo.py --auto                # sin pausas
python Performance/scripts/demo.py --pasos 3,4,5,6,7     # solo algunos pasos
python Performance/scripts/demo.py --agregacion-completa # paso 5 con los 50 000 pedidos (~40 s)
```

Los ocho pasos muestran: conexión y conteos, catálogo heterogéneo, pedido
anidado con cambio de estado, índices antes y después, agregaciones (funciones
de `database/queries/agregaciones.py`), evolución del esquema, historial intacto
y validación.

No modifica los datos reales: los pasos 3, 6 y 7 usan colecciones temporales
`demo_*`. El paso 4 fuerza el recorrido completo para medir "sin índice" y crea
índices `demo_*`; si ya existe un índice con las mismas claves (por ejemplo, el
de `indexes.js`), se retira un momento y se restaura al terminar.

## Resultados de la corrida final

Mediana de 30 repeticiones, MongoDB 7.0.28 local (`resultados_final/`):

| Consulta | Sin índice | Con índice | Docs. examinados |
|---|---|---|---|
| Q1 Categoría | 39.3 ms | 30.5 ms | 25 000 → 3 270 |
| Q2 Rango de precio | 62.4 ms | 10.4 ms | 25 000 → 990 |
| Q3 Categoría + precio | 47.1 ms | 4.9 ms | 25 000 → 329 |
| Q4 Categoría + precio + talla | 51.7 ms | 6.1 ms | 25 000 → 1 273 |
| Q5 Productos de un comercio | 48.0 ms | 1.0 ms | 25 000 → 54 |
| Q6 Pedidos de un cliente | 114.9 ms | 0.5 ms | 50 000 → 7 |
| Q7 Pedidos que contienen un producto | 234.8 ms | 0.5 ms | 50 000 → 5 |

Agregaciones: ventas por categoría 38.6 s, ticket promedio 259 ms, productos
más vendidos 757 ms. Concurrencia: entre 560 y 621 solicitudes por segundo con
10, 50 y 100 hilos. Carga masiva: 85 500 documentos en unos 2.1 s.

## Entorno de las mediciones
Windows 11, Intel (12 núcleos lógicos), 15.7 GB de RAM, SSD NVMe, Python 3.15,
pymongo 4.18.3, MongoDB 7.0.28 en una instancia única local. Los tiempos
dependen del equipo; ver `resultados_final/entorno.json`.

## Limitaciones
- Instancia única local: no se evaluaron replicación, sharding ni MongoDB Atlas.
- La concurrencia se simula con hilos de un solo proceso de Python.
- Los datos son sintéticos y caben en memoria.
- La validación de datos existe en Python; no hay `$jsonSchema` en MongoDB.
