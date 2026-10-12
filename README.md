# MercadoTico 360

MercadoTico 360 es una solución NoSQL orientada a documentos para un marketplace ficticio de comercios costarricenses. La propuesta utiliza MongoDB para manejar un catálogo de productos con atributos variables por categoría, pedidos con líneas de detalle anidadas e información histórica suficiente para reconstruir cada compra.

El proyecto fue desarrollado para el curso **XS-0131 Gestión de Bases de Datos y Análisis de Información**.

---

## Índice

1. [Descripción del proyecto](#1-descripción-del-proyecto)
2. [Problema de negocio](#2-problema-de-negocio)
3. [Objetivos](#3-objetivos)
4. [Tecnologías utilizadas](#4-tecnologías-utilizadas)
5. [Modelo de datos](#5-modelo-de-datos)
6. [Decisiones de diseño](#6-decisiones-de-diseño)
7. [Prerrequisitos](#7-prerrequisitos)
8. [Instalación y configuración](#8-instalación-y-configuración)
9. [Generación y carga de datos](#9-generación-y-carga-de-datos)
10. [Ejecución](#10-ejecución)
11. [Consultas y operaciones implementadas](#11-consultas-y-operaciones-implementadas)
12. [Índices](#12-índices)
13. [Evolución del esquema y consistencia](#13-evolución-del-esquema-y-consistencia)
14. [Pruebas y resultados](#14-pruebas-y-resultados)
15. [Guía de demostración](#15-guía-de-demostración)
16. [Riesgos y limitaciones](#16-riesgos-y-limitaciones)
17. [Estructura del repositorio](#17-estructura-del-repositorio)
18. [Autores](#18-autores)

---

## 1. Descripción del proyecto

MercadoTico 360 es una propuesta de almacenamiento NoSQL para un marketplace que agrupa productos y servicios de distintas categorías, entre ellas alimentos, ropa, tecnología, artesanías, servicios, hogar, belleza y deportes.

La solución utiliza MongoDB y documentos BSON para:

- almacenar productos con atributos variables;
- conservar pedidos con líneas de detalle anidadas;
- mantener información histórica de cada compra;
- ejecutar consultas operativas por categoría, precio, atributos, cliente y estado;
- realizar agregaciones útiles para el negocio;
- evaluar el efecto de índices sobre consultas frecuentes.

El repositorio incluye scripts de generación de datos sintéticos, carga de datos, operaciones CRUD, consultas, agregaciones, pruebas funcionales y pruebas de rendimiento.

---

## 2. Problema de negocio

MercadoTico 360 maneja productos de categorías con características muy diferentes. Un alimento puede requerir información como peso o tipo de empaque, mientras que una prenda puede manejar talla y material, y un producto tecnológico puede necesitar marca, almacenamiento u otras especificaciones.

En un modelo relacional rígido, esta heterogeneidad puede provocar numerosas tablas especializadas o una gran cantidad de campos opcionales. Además, los pedidos deben conservar la información histórica de la compra aunque posteriormente cambien el nombre o el precio del producto.

La propuesta utiliza un modelo documental para representar de forma flexible el catálogo y mantener las líneas históricas del pedido dentro del propio documento de compra.

---

## 3. Objetivos

### 3.1 Objetivo general

Diseñar e implementar una solución de base de datos NoSQL orientada a documentos utilizando MongoDB para satisfacer las necesidades operativas de MercadoTico 360.

### 3.2 Objetivos específicos

1. Diseñar colecciones que representen productos, comercios, clientes y pedidos de forma coherente con el modelo documental.
2. Representar atributos diferentes por categoría sin obligar a todos los productos a compartir exactamente los mismos campos.
3. Conservar dentro de cada pedido la información necesaria para reconstruir históricamente la compra.
4. Implementar consultas por categoría, rango de precio, atributos específicos, clientes, estados y productos incluidos en pedidos.
5. Implementar operaciones CRUD y actualizaciones parciales mediante operadores de MongoDB.
6. Ejecutar agregaciones para obtener información útil para el negocio.
7. Crear y evaluar índices para patrones de consulta frecuentes.
8. Demostrar que el esquema puede evolucionar incorporando nuevos atributos sin realizar una migración relacional tradicional.
9. Mantener un repositorio reproducible mediante variables de entorno, dependencias declaradas y scripts de generación, carga y prueba.

---

## 4. Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| MongoDB / MongoDB Atlas | Base de datos documental y alojamiento de la base utilizada por el proyecto |
| Python | Generación de datos, carga, consultas y pruebas |
| PyMongo (`pymongo`) | Driver de Python para MongoDB |
| `python-dotenv` | Lectura de variables de entorno desde `.env` |
| Faker (`faker`) | Generación de información sintética |
| Matplotlib | Generación de gráficos de resultados |
| NumPy | Apoyo en procesamiento de métricas |
| `unittest` | Pruebas funcionales |
| JSON / BSON | Representación de datos y documentos |
| Git / GitHub | Control de versiones y publicación del proyecto |

---

## 5. Modelo de datos

La base de datos está compuesta por cuatro colecciones principales:

- `comercios`
- `productos`
- `clientes`
- `pedidos`

### 5.1 Productos

Cada producto incluye un identificador, nombre, precio, categoría, comercio, existencias y un subdocumento `atributos`.

El contenido de `atributos` cambia según la categoría del producto.

Ejemplo:

```json
{
  "_id": "PROD-00001",
  "nombre": "Ejemplo de servicio",
  "precio": 154176.85,
  "categoria": "Servicios",
  "comercio_id": "COM-033",
  "stock": 500,
  "atributos": {
    "requiere_cita": true,
    "modalidad": "Presencial"
  }
}
```

Las categorías utilizadas son:

- Alimentos
- Ropa
- Tecnología
- Artesanías
- Servicios
- Hogar
- Belleza
- Deportes

### 5.2 Comercios

La colección `comercios` almacena los negocios asociados al catálogo.

Cada documento contiene información como:

- identificador;
- nombre;
- correo;
- teléfono;
- categoría;
- estado;
- dirección.

Los productos utilizan `comercio_id` para identificar el comercio al que pertenecen.

### 5.3 Clientes

La colección `clientes` almacena la información de los usuarios del marketplace.

Incluye:

- identificador;
- nombre;
- correo;
- teléfono;
- cédula;
- dirección con provincia, cantón, distrito y dirección exacta.

Los datos utilizados son sintéticos. Las localidades generadas por Faker no necesariamente representan combinaciones geográficas reales de Costa Rica.

### 5.4 Pedidos

La colección `pedidos` almacena las compras realizadas por los clientes.

Cada pedido incluye:

- `_id`;
- `fecha`;
- `cliente_id`;
- `estado`;
- `monto_total`;
- `lineas_detalle`.

Ejemplo simplificado:

```json
{
  "_id": "PED-00001",
  "fecha": "2026-01-01T12:00:00",
  "cliente_id": "CLI-00001",
  "estado": "Entregado",
  "monto_total": 25000,
  "lineas_detalle": [
    {
      "producto_id": "PROD-00001",
      "nombre_producto": "Producto de ejemplo",
      "precio_unitario": 12500,
      "cantidad": 2,
      "subtotal": 25000
    }
  ]
}
```

La línea del pedido conserva `producto_id`, `nombre_producto`, `precio_unitario`, `cantidad` y `subtotal`. De esta manera, la información relevante de la compra permanece en el pedido aunque posteriormente cambien datos del producto original.

---

Almacena los datos como identificación, nombre, correo, teléfono, cédula y dirección (`provincia`, `canton`, `distrito` y `direccion_exacta`). 

### 6.1 Información embebida

Se decidió embeber:

- `atributos` dentro de cada producto;
- `direccion` dentro de clientes y comercios;
- `lineas_detalle` dentro de cada pedido.

Estas estructuras forman parte natural del documento principal y normalmente se consultan junto con él.

En especial, `lineas_detalle` se mantiene embebido porque representa el estado histórico de la compra y permite recuperar un pedido completo en una sola estructura documental.

### 6.2 Información referenciada

Se decidió utilizar referencias lógicas mediante identificadores para:

- `productos.comercio_id`;
- `pedidos.cliente_id`;
- `pedidos.lineas_detalle.producto_id`.

Los datos completos de clientes, comercios y productos se mantienen en sus respectivas colecciones para evitar duplicar información que puede cambiar independientemente.

MongoDB no aplica estas referencias como llaves foráneas relacionales. La aplicación y los scripts del proyecto son responsables de utilizar identificadores válidos y mantener la consistencia esperada.

---

## 7. Prerrequisitos

Antes de ejecutar el proyecto se requiere:

- Git.
- Python 3.
- Una cuenta o instancia accesible de MongoDB.
- Credenciales válidas con permisos de lectura y escritura.
- Conexión a Internet si se utiliza MongoDB Atlas.
- Acceso de red autorizado al clúster.
- Espacio suficiente para los archivos JSON y los datos de prueba.

---
Para reproducir las pruebas de rendimiento, se recomienda utilizar un entorno aislado y mantener las versiones de las herramientas lo más cercanas posible a las empleadas en las mediciones originales. Las características específicas del entorno evaluado se encuentran documentadas en `Performance/resultados_final/entorno.json`

## 8. Instalación y configuración

### 8.1 Clonar el repositorio

```bash
git clone https://github.com/emilio667/MercadoTico-360.git
cd MercadoTico-360
```

### 8.2 Crear y activar un entorno virtual

#### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 8.3 Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

Las dependencias externas necesarias para ejecutar el proyecto están declaradas en `requirements.txt`.

### 8.4 Configurar variables de entorno

Crear un archivo `.env` en la raíz del repositorio a partir de `.env.example`.

#### Windows

```powershell
Copy-Item .env.example .env
```

#### Linux/macOS

```bash
cp .env.example .env
```

Contenido esperado:

```dotenv
MONGODB_URI=mongodb+srv://USUARIO:CONTRASENA@TU_CLUSTER.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=MercadoTico360
```

Reemplazar `USUARIO`, `CONTRASENA` y `TU_CLUSTER` por los valores correspondientes.

El archivo `.env` contiene información sensible y no debe subirse al repositorio.

---

## 9. Generación y carga de datos

El proyecto trabaja con las siguientes cantidades:

| Colección | Cantidad |
|---|---:|
| `comercios` | 500 |
| `clientes` | 10 000 |
| `productos` | 25 000 |
| `pedidos` | 50 000 |
| **Total** | **85 500** |

Los productos se distribuyen entre las ocho categorías definidas y los pedidos contienen múltiples líneas de detalle.

### 9.1 Archivos incluidos

```text
database/seed/
├── comercios.json
├── clientes.json
├── productos.json
└── pedidos.json
```

Si los archivos JSON ya existen, la forma más rápida de reproducir la base es cargar directamente esos datos.

### 9.2 Cargar los datos incluidos

Antes de ejecutar la carga se recomienda utilizar una base vacía para evitar conflictos por identificadores duplicados.

```bash
python database/seed/seed_data.py
```

El orquestador carga los datos en este orden:

1. comercios;
2. clientes;
3. productos;
4. pedidos.

También pueden ejecutarse individualmente:

```bash
python database/seed/seed_comercios.py
python database/seed/seed_clientes.py
python database/seed/seed_productos.py
python database/seed/seed_pedidos.py
```

Los scripts leen `MONGODB_URI` y `MONGODB_DB` desde `.env`.

### 9.3 Regenerar los datos sintéticos desde cero

Los generadores se encuentran en `database/generadores/`.

Los datos de comercios, clientes y productos pueden generarse primero:

```bash
python -m database.generadores.generar_comercios
python -m database.generadores.generar_clientes
python -m database.generadores.generar_productos
```

Luego se deben cargar esas tres colecciones:

```bash
python database/seed/seed_comercios.py
python database/seed/seed_clientes.py
python database/seed/seed_productos.py
```

Después se generan los pedidos:

```bash
python -m database.generadores.generar_pedidos
```

El generador de pedidos consulta clientes y productos ya cargados en MongoDB, por lo que este paso debe realizarse después de cargar esas colecciones.

Finalmente:

```bash
python database/seed/seed_pedidos.py
```

Los generadores utilizan una semilla fija para favorecer la reproducibilidad de los datos sintéticos.

### 9.4 Verificar la carga

En MongoDB Compass o `mongosh`:

```javascript
use MercadoTico360

db.comercios.countDocuments({})
db.clientes.countDocuments({})
db.productos.countDocuments({})
db.pedidos.countDocuments({})
```

En una base vacía cargada una sola vez con los datos del proyecto se esperan:

```text
comercios:   500
clientes:  10000
productos: 25000
pedidos:   50000
```

---

## 10. Ejecución

Los principales comandos deben ejecutarse desde la raíz del repositorio con el entorno virtual activo y el archivo `.env` configurado.

### Cargar datos

```bash
python database/seed/seed_data.py
```

### Ejecutar pruebas funcionales

```bash
python test/test_funcionales.py
```

### Ejecutar benchmark

```bash
python Performance/scripts/benchmark.py
```

### Generar gráficos

```bash
python Performance/scripts/graficos.py
```

---

## 11. Consultas y operaciones implementadas

### 11.1 Consultas de productos

Archivo:

```text
database/queries/consultas_productos.py
```

Incluye:

- búsqueda por categoría;
- búsqueda por rango de precio;
- búsqueda por un atributo específico;
- búsqueda por categoría y precio;
- búsqueda por categoría y atributo;
- productos disponibles en stock;
- productos pertenecientes a un comercio.

Ejemplos con `mongosh`:

```javascript
// Productos de tecnología
db.productos.find({
  categoria: "Tecnología"
}).limit(5)
```

```javascript
// Productos en un rango de precio
db.productos.find({
  precio: {
    $gte: 100000,
    $lte: 120000
  }
}).limit(5)
```

```javascript
// Productos de ropa con talla específica
db.productos.find({
  categoria: "Ropa",
  "atributos.talla": "M"
}).limit(5)
```

El uso de campos como `atributos.talla` demuestra que los atributos específicos pueden consultarse sin exigir que todas las categorías tengan la misma estructura.

### 11.2 Consultas de pedidos

Archivo:

```text
database/queries/consultas_pedidos.py
```

Incluye:

- búsqueda de pedido por ID;
- pedidos de un cliente;
- pedidos de un cliente ordenados por fecha;
- pedidos por estado;
- pedidos de un cliente por estado;
- actualización del estado de un pedido;
- pedidos que contienen un producto;
- conteo de pedidos por cliente.

Ejemplo:

```javascript
db.pedidos.find({
  cliente_id: "CLI-00001"
}).sort({
  fecha: -1
}).limit(5)
```

Para consultar un pedido con sus líneas anidadas:

```javascript
db.pedidos.findOne({
  _id: "PED-00001"
})
```

La actualización del estado se realiza mediante `$set`, por lo que no es necesario reescribir todo el documento:

```javascript
db.pedidos.updateOne(
  {
    _id: "PED-00001"
  },
  {
    $set: {
      estado: "Enviado"
    }
  }
)
```

### 11.3 Operaciones CRUD

Archivo:

```text
database/queries/crud.py
```

Incluye operaciones genéricas de:

- creación;
- lectura;
- actualización;
- eliminación;
- verificación de existencia;
- conteo.

También incluye funciones específicas para productos, comercios, clientes y pedidos.

Las actualizaciones utilizan `$set` y no permiten modificar el campo `_id`.

### 11.4 Agregaciones

Archivo:

```text
database/queries/agregaciones.py
```

Se implementaron, entre otras:

- ventas por categoría;
- productos más vendidos;
- ticket promedio;
- ventas por estado;
- pedidos asociados con información del cliente;
- ventas de una categoría específica.

Estas operaciones utilizan el Aggregation Framework de MongoDB con etapas como `$match`, `$unwind`, `$lookup`, `$group`, `$sort`, `$limit` y `$avg`, según corresponda.

---

## 12. Índices

El proyecto evalúa índices relacionados con patrones de consulta frecuentes.

| Índice | Colección | Campos |
|---|---|---|
| `idx_categoria_precio` | `productos` | `categoria` asc., `precio` asc. |
| `idx_precio` | `productos` | `precio` asc. |
| `idx_atributos_talla` | `productos` | `atributos.talla` asc. |
| `idx_comercio` | `productos` | `comercio_id` asc. |
| `idx_cliente_fecha` | `pedidos` | `cliente_id` asc., `fecha` desc. |
| `idx_lineas_producto` | `pedidos` | `lineas_detalle.producto_id` asc. |

Los índices fueron seleccionados a partir de patrones reales de consulta implementados en el proyecto, por ejemplo:

- categoría y rango de precio;
- precio;
- atributo específico;
- productos de un comercio;
- historial de pedidos de un cliente ordenado por fecha;
- pedidos que contienen un producto.

Para revisar el plan de ejecución:

```javascript
db.productos.find({
  categoria: "Tecnología"
}).explain("executionStats")
```

Las pruebas de rendimiento comparan planes sin índice y con índice para observar cambios como `COLLSCAN` e `IXSCAN`, además del tiempo de ejecución y la cantidad de documentos examinados.

---

## 13. Evolución del esquema y consistencia

### 13.1 Evolución del esquema

El modelo documental permite incorporar atributos nuevos sin alterar todos los documentos existentes.

Para demostrar la evolución del esquema durante la exposición, se puede incorporar un atributo nuevo a un producto mediante:

```javascript
db.productos.updateOne(
  {
    _id: "PROD-00001"
  },
  {
    $set: {
      "atributos.garantia_meses": 12
    }
  }
)
```

Los demás productos no necesitan incorporar ese campo. Esto permite demostrar que el catálogo puede evolucionar sin realizar una migración equivalente a modificar una tabla relacional completa.

También es posible incorporar nuevas categorías definiendo sus atributos específicos sin obligar a que el resto del catálogo comparta esos mismos campos.

### 13.2 Validación y consistencia

El proyecto aplica validaciones en la capa de Python mediante las funciones de construcción de documentos ubicadas en:

```text
database/schemas/modelos_de_estructuras.py
```

Entre las comprobaciones se incluyen:

- campos obligatorios;
- categorías permitidas;
- estados permitidos;
- valores numéricos no negativos;
- cantidad válida en líneas de pedido;
- coherencia de subtotales;
- estructura esperada de atributos y direcciones.

El proyecto define validaciones en Python para construir y verificar la estructura esperada de los documentos.

Como limitación, MongoDB continúa siendo una base de datos de esquema flexible y las referencias mediante identificadores no equivalen a restricciones de llave foránea de una base relacional.

---

## 14. Pruebas y resultados

### 14.1 Pruebas funcionales

Archivo:

```text
test/test_funcionales.py
```

Las pruebas verifican operaciones de inserción, consulta, actualización y comportamiento de las colecciones.

Ejecutar:

```bash
python test/test_funcionales.py
```

### 14.2 Benchmark de rendimiento

Archivo:

```text
Performance/scripts/benchmark.py
```

Ejemplo de ejecución:

```bash
python Performance/scripts/benchmark.py --reps 30 --agg-reps 5
```

El benchmark compara consultas sin índice y con índice, además de recopilar métricas de agregaciones, carga y concurrencia.

**Importante:** el script de benchmark puede eliminar y recrear índices definidos para la prueba. Debe ejecutarse únicamente sobre un entorno de pruebas.

### 14.3 Resultados observados

Resultados documentados en la tercera corrida:

| Consulta | Sin índice (ms) | Con índice (ms) | Mejora de mediana | Docs examinados sin/con |
|---|---:|---:|---:|---:|
| `Q1_categoria` | 47.59 | 29.84 | 37.3 % | 25000 / 3052 |
| `Q2_rango_precio` | 65.43 | 13.26 | 79.7 % | 25000 / 1029 |
| `Q3_categoria_precio` | 41.36 | 5.89 | 85.8 % | 25000 / 286 |
| `Q4_categoria_precio_talla` | 62.16 | 8.36 | 86.5 % | 25000 / 1180 |
| `Q5_comercio` | 50.70 | 1.53 | 97.0 % | 25000 / 54 |
| `Q6_pedidos_cliente` | 146.73 | 1.11 | 99.2 % | 50000 / 6 |
| `Q7_pedidos_producto` | 231.37 | 2.07 | 99.1 % | 50000 / 16 |

En estas consultas, los planes registrados pasan de exploraciones completas de colección (`COLLSCAN`) a planes que utilizan índices (`IXSCAN`), con reducción de documentos examinados y de la mediana observada.

Estos resultados corresponden al entorno y conjunto de datos utilizados en las pruebas y no garantizan los mismos porcentajes en otro equipo o servidor.

### 14.4 Concurrencia

| Hilos | Solicitudes | Solicitudes/s | Latencia media (ms) | p95 (ms) |
|---:|---:|---:|---:|---:|
| 10 | 200 | 353.8 | 24.273 | 47.595 |
| 50 | 1000 | 339.0 | 90.902 | 199.35 |
| 100 | 2000 | 304.8 | 143.815 | 347.905 |

En el entorno medido, la latencia aumentó conforme creció el número de hilos concurrentes.

### 14.5 Agregaciones

| Agregación | Resultados devueltos | Repeticiones | Mediana (ms) | p95 (ms) |
|---|---:|---:|---:|---:|
| `A1_ventas_por_categoria` | 8 | 5 | 33550.63 | 38602.80 |
| `A2_ticket_promedio` | 1 | 5 | 230.43 | 294.49 |
| `A3_productos_mas_vendidos` | 10 | 5 | 685.92 | 719.66 |

La agregación de ventas por categoría fue la más costosa de las tres en la corrida documentada.

### 14.6 Carga masiva

| Colección | Documentos | Tiempo de inserción (s) | Documentos/s |
|---|---:|---:|---:|
| `comercios` | 500 | 0.027 | 18585.8 |
| `clientes` | 10000 | 0.181 | 55142.4 |
| `productos` | 25000 | 0.518 | 48253.0 |
| `pedidos` | 50000 | 2.467 | 20270.8 |

### 14.7 Evidencias

Los resultados completos de las corridas de rendimiento se encuentran dentro de `Performance/`.

Entre los archivos generados se incluyen:

- comparativas de índices;
- mediciones detalladas;
- tiempos crudos;
- métricas de concurrencia;
- métricas de agregaciones;
- métricas de carga masiva;
- construcción de índices;
- información del entorno;
- planes de ejecución;
- gráficos.

Para generar los gráficos:

```bash
python Performance/scripts/graficos.py
```

---

## 15. Guía de demostración

La demostración puede realizarse siguiendo este orden.

### 15.1 Visualizar documentos reales y explicar el diseño

En MongoDB Compass:

1. abrir un documento de `productos`;
2. mostrar que `atributos` cambia según la categoría;
3. abrir un documento de `pedidos`;
4. mostrar el arreglo `lineas_detalle`.

Explicación esperada:

- los atributos variables se embeben dentro del producto;
- las líneas se embeben dentro del pedido para conservar la información histórica;
- clientes y comercios se relacionan mediante identificadores para evitar duplicar documentos completos.

### 15.2 Consultar producto y pedido

Ejemplo de producto con atributo específico:

```javascript
db.productos.find({
  categoria: "Ropa",
  "atributos.talla": "M"
}).limit(5)
```

Ejemplo de pedido anidado:

```javascript
db.pedidos.findOne({
  _id: "PED-00001"
})
```

### 15.3 Evidenciar el efecto de un índice

Ejecutar una consulta relevante antes y después del índice y revisar:

- plan de ejecución;
- tiempo observado;
- documentos examinados;
- cambio de `COLLSCAN` a `IXSCAN`, cuando corresponda.

Ejemplo de patrón:

```javascript
db.pedidos.find({
  cliente_id: "CLI-00001"
}).sort({
  fecha: -1
}).explain("executionStats")
```

### 15.4 Demostrar evolución del esquema

Agregar un atributo nuevo solamente a un producto:

```javascript
db.productos.updateOne(
  {
    _id: "PROD-00001"
  },
  {
    $set: {
      "atributos.garantia_meses": 12
    }
  }
)
```

Luego volver a consultar el producto y mostrar que el nuevo atributo existe sin haber modificado los demás documentos.

Finalmente, explicar que las validaciones principales del proyecto se realizan en la capa de Python y que la flexibilidad documental permite evolucionar la estructura sin una migración relacional tradicional.

---

## 16. Riesgos y limitaciones

### 16.1 Riesgos técnicos

- Exposición accidental de credenciales.
- Consultas lentas si no se utilizan índices adecuados.
- Inconsistencias si se insertan documentos fuera de las validaciones del proyecto.
- Interferencia entre pruebas y datos compartidos.
- Dependencia de conectividad cuando se utiliza MongoDB Atlas.
- Crecimiento de documentos si las estructuras embebidas aumentan sin control.
- Duplicación histórica intencional de nombre y precio dentro de las líneas de pedido.

### 16.2 Medidas aplicadas

- Uso de `.env` para credenciales.
- Archivo `.env.example` sin secretos.
- Uso de `requirements.txt`.
- Consultas e índices documentados.
- Pruebas funcionales y de rendimiento.
- Uso de una base separada o entorno controlado para benchmarks.
- Validaciones en Python antes de construir documentos.
- Conservación explícita de información histórica en `lineas_detalle`.

### 16.3 Limitaciones

- El proyecto no incluye una aplicación web, pasarela de pagos ni sistema logístico.
- Los datos son sintéticos.
- Los resultados de rendimiento dependen del hardware, red, servidor y carga durante la medición.
- Las referencias entre colecciones son lógicas y no llaves foráneas relacionales.
- La validación principal del esquema está implementada en Python.
- El benchmark modifica índices y debe ejecutarse en un entorno de pruebas.
- Las pruebas documentadas representan el entorno evaluado y no constituyen una garantía de rendimiento en producción.

---

## 17. Estructura del repositorio

```text
MercadoTico-360/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── DATA_ARCHITECTURE.md
├── LICENSE
├── database/
│   ├── generadores/
│   │   ├── generar_clientes.py
│   │   ├── generar_comercios.py
│   │   ├── generar_pedidos.py
│   │   └── generar_productos.py
│   ├── queries/
│   │   ├── agregaciones.py
│   │   ├── consultas_pedidos.py
│   │   ├── consultas_productos.py
│   │   └── crud.py
│   ├── schemas/
│   │   └── modelos_de_estructuras.py
│   ├── seed/
│   │   ├── comercios.json
│   │   ├── clientes.json
│   │   ├── productos.json
│   │   ├── pedidos.json
│   │   ├── seed_clientes.py
│   │   ├── seed_comercios.py
│   │   ├── seed_data.py
│   │   ├── seed_pedidos.py
│   │   └── seed_productos.py
│   └── Index/
├── Performance/
│   ├── plan_de_pruebas.md
│   ├── Riesgos
│   ├── scripts/
│   │   ├── benchmark.py
│   │   └── graficos.py
│   └── resultados/
├── test/
│   └── test_funcionales.py
├── docs/
└── Entregables/
```

La estructura exacta de carpetas de resultados puede variar según las corridas de benchmark conservadas en el repositorio.

---

## 18. Autores

- Adrián Quesada Jiménez
- Camila Alpízar Alfaro
- Emilio Calderón Jiménez
- Gustavo Jiménez Hidalgo
- Justin Zhu Fan
- Salma Capín Romero

---

## Reproducibilidad

Para reproducir la solución desde una copia limpia del repositorio:

```bash
git clone https://github.com/emilio667/MercadoTico-360.git
cd MercadoTico-360

python -m venv .venv
```

Activar el entorno virtual y luego:

```bash
python -m pip install -r requirements.txt
```

Crear `.env` a partir de `.env.example`, configurar las credenciales y cargar los datos:

```bash
python database/seed/seed_data.py
```

Verificar la implementación:

```bash
python test/test_funcionales.py
```

Opcionalmente ejecutar las pruebas de rendimiento en un entorno de pruebas:

```bash
python Performance/scripts/benchmark.py
```

Con estos pasos se dispone de la base, datos, consultas, pruebas y evidencia necesarias para revisar la implementación de MercadoTico 360.