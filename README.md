# MercadoTico 360

## Índice

1. [Descripción del proyecto](#1-descripción-del-proyecto)
2. [Problema de negocio](#2-problema-de-negocio)
3. [Objetivos](#3-objetivos)
4. [Tecnologías utilizadas](#4-tecnologías-utilizadas)
5. [Modelo de datos](#5-modelo-de-datos)
6. [Prerrequisitos](#6-prerrequisitos)
7. [Instalación y configuración](#7-instalación-y-configuración)
8. [Generación y carga de datos (seed)](#8-generación-y-carga-de-datos-seed)
9. [Ejecución](#9-ejecución)
10. [Consultas y comandos de demostración](#10-consultas-y-comandos-de-demostración)
11. [Pruebas y resultados](#11-pruebas-y-resultados)
12. [Riesgos y limitaciones](#12-riesgos-y-limitaciones)
13. [Estructura del repositorio](#13-estructura-del-repositorio)
14. [Autores](#14-autores)

## 1. Descripción del proyecto

MercadoTico 360 es una propuesta de almacenamiento NoSQL para un marketplace el cual llegar a abarcar alimentos, ropa, tecnología, artesanías, servicios y otros. Se utilizo MongoDB y documentos BSON para almacenar atributos de los producto, tambien la informacion historica de pedidos. Se trabajo con scripts de python para generar datos de prueba, insertarlos, consultarlos y medir su comportamiento.

## 2. Problema de negocio

MercadoTico 360 maneja productos de distintas categorías, como alimentos, ropa, tecnología, artesanías y servicios. Esta variedad requiere una estructura de datos flexible que permita almacenar diferentes atributos y conservar correctamente el historial de los pedidos.

## 3. Objetivos

### 3.1 Objetivo general

Diseñar e implementar un modelo de base de datos no relacional orientado a documentos utilizando MongoDB Atlas para la plataforma MercadoTico 360.

### 3.2 Objetivos específicos

1. Configurar la arquitectura de almacenamiento en la nube a través de clústeres distribuidos en MongoDB Atlas para asegurar la alta disponibilidad, el aislamiento de consultas y la tolerancia a fallos de la plataforma.

2. Evaluar las limitantes del modelo relacional frente a las ventajas del modelo NoSQL orientado a documentos para entornos transaccionales de alta velocidad y volumen.

3. Estructurar un esquema de datos flexible que consolide en una única colección un catálogo de productos heterogéneo (alimentos, ropa, tecnología, artesanías y servicios) sin incurrir en redundancias ni campos nulos.

4. Desarrollar un patrón de documentos para la colección de pedidos que encapsule las lineas de detalle de las compras, resguardando la integridad historica de los precios y cantidades facturadas.


## 4. Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| MongoDB / MongoDB Atlas | Base de datos documental y alojamiento en la nube |
| Python | Generación de datos, carga, consultas y pruebas |
| PyMongo (`pymongo`) | Conexión y operaciones con MongoDB |
| `python-dotenv` | Lectura de variables de conexión desde `.env` |
| Faker (`faker`) | Generación de información sintética |
| Matplotlib y NumPy | Elaboración de gráficos de rendimiento |
| `unittest` | Pruebas funcionales (biblioteca estándar de Python) |
| JSON / BSON | Datos de entrada y representación de documentos |
| Git y GitHub | Versionado y publicación del proyecto |


## 5. Modelo de datos

La base de datos esta compuesta por cautro colecciones
- Comercios
- Productos
- Clientes
- Pedidos

### 5.1 Productos

Cada documento incluye identificador, nombre, categoría, precio, comercio, existencias y un subdocumento `atributos` que varía según la categoria.

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

### 5.2 Clientes

La colección `clientes` almacena la información de los usuarios de la plataforma, incluyendo sus datos de contacto y ubicación.

ALmacena los datos como identificación, nombre, correo, teléfono, cédula y dirección (`provincia`, `canton`, `distrito` y `direccion_exacta`). 

Los datos son sintéticos: las localidades producidas por Faker no necesariamente representan combinaciones geográficas reales de Costa Rica

### 5.3 Pedidos

La coleccion `pedidos` almacena las compras realizadas por los clientes.

Los pedidos incluyen datos como: fecha, cliente, estado, monto total y el arreglo `lineas_detalle` la cual almacena (`producto_id`, `nombre_producto`, `precio_unitario`, `cantidad` y `subtotal`).

### 5.4 Comercios

La colección  `comercios` almacena los negocios asociados al catálogo, el cual tiene datos de contacto, categoría, estado y dirección. `productos.

Tenemos `comercio_id` que identifica el comercio correspondiente.

## 6. Prerrequisitos

Antes de ejecutar el proyecto es necesario contar con:

- Git, para clonar el repositorio
- Python 
- Una cuenta de MongoDB Atlas
- Acceso al cluster de MongoDB Atlas utilizado por el proyecto y conexion a Internet para tener acceso
- Credenciales válidas y permisos de lectura/escritura en la base de datos de trabajo
- PyMongo instalado
- Acceso de red al servidor; en Atlas, configurar el usuario de base de datos y la lista de direcciones IP permitidas
- Espacio suficiente para los archivos JSON y las colecciones de prueba

## 7. Instalación y configuración

### 7.1 Clonar el repositorio

Clonar el repositorio de MercadoTico 360 en el equipo:

```bash

git clone https://github.com/emilio667/MercadoTico-360.git 

```

Ingresar a la carpeta:

```bash

cd MercadoTico-360

```

### 7.2 Crear y activar un entorno virtual (recomendado)

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 7.3 Instalar dependencias

```bash
python -m pip install pymongo python-dotenv faker matplotlib numpy
```

Estas son las dependencias externas observadas en los scripts del repositorio; `unittest`, `json`, `csv` y otras bibliotecas estándar ya vienen con Python.

### 7.4 Configurar MongoDB Atlas

1. Crear o seleccionar un clúster de MongoDB Atlas.
2. Crear un usuario de base de datos con los permisos apropiados.
3. Autorizar la IP desde la que se conectará el equipo, aplicando el acceso más restrictivo posible.
4. Copiar la URI de conexión desde la opción **Connect** de Atlas.
5. Crear un archivo `.env` en la **raíz del repositorio**, a partir de `.env.example`.

**Windows:**

```powershell
Copy-Item .env.example .env
```

**Linux/macOS:**

```bash
cp .env.example .env
```

Editar `.env` con valores propios:

```dotenv
MONGODB_URI=mongodb+srv://USUARIO:CONTRASENA@TU_CLUSTER.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=MercadoTico360
```


## 8. Carga de datos
La carga de datos utilizara generadores independientes para las principales colecciones del proyecto:

- Productos
- Clientes
- Pedido
- Comercios

### 8.1 La semilla de datos

Los generadores usan `Faker.seed(123)`.

### 8.2 Datos incluidos

| Colección | Documentos en los JSON de `database/seed/` |
|---|---:|
| `comercios` | 500 |
| `clientes` | 10.000 |
| `productos` | 25.000 |
| `pedidos` | 50.000 |
| **Total** | **85.500** |

Los archivos de datos incluidos en el repositorio son:

```text
database/seed/
├── comercios.json
├── clientes.json
├── productos.json
└── pedidos.json
```

### 8.3 Datos sintéticos

Desde la raíz del proyecto, los generadores se encuentran en `database/generadores/`:

```bash
python -m database.generadores.generar_comercios
python -m database.generadores.generar_clientes
python -m database.generadores.generar_productos
python -m database.generadores.generar_pedidos
```




## 9. Ejecución

Actualmente el repositorio contiene scripts en Python para comprobar PyMongo, conectarse con MongoDB Atlas y realizar una insercion basica en la coleccion de clientes.

Para verificar PyMongo:

```bash

python database/integrante3/test_atlas.py

```

Para probar la conexion con MongoDB Atlas:

```bash

python database/integrante3/conexion.py

```

Para ejecutar la prueba de creación e inserción de un documento:

```bash

python database/integrante3/crear_db.py

```
[PENDIENTE: actualizar comandos de ejecución, falta info]


## 10. Comandos de demostración

### 10.1 Consultas de productos

Se implementará consultas para:

- Buscar productos por categoría.

- Buscar productos por rango de precio.

- Buscar productos utilizando atributos específicos.

- Combinar filtros de categoría y precio.

### 10.2 Consultas de pedidos

Se implementará consultas para:

- Recuperar los pedidos de un cliente.

- Consultar un pedido con sus líneas de detalle.

- Consultar el estado de un pedido.

- Actualizar el estado de un pedido.

### 10.3 Agregaciones

Se incorporaran consultas de agregación para obtener información útil para el negocio, como:

- Ventas por categoría.

- Ticket promedio.

- Productos más vendidos.

### 10.4 Índices

El proyecto contempla índices para optimizar consultas frecuentes, entre ellos:

- Categoría y precio.

- Atributos específicos de productos.

- Cliente y fecha de los pedidos.

[PENDIENTE: agregar los comandos definitivos de demostracion cuando los archivos de consultas e indices esten implementados]


## 11. Pruebas y resultados

### 11.1 Plan de pruebas

Descripción de las pruebas que se realizarán para verificar el funcionamiento de la base de datos.

### 11.2 Pruebas funcionales

Validación de inserciones, consultas, actualizaciones y operaciones sobre las colecciones.

### 11.3 Pruebas de rendimiento

Evaluación de los tiempos de respuesta de las consultas y comparación del rendimiento con y sin índices.

### 11.4 Resultados obtenidos

Presentación de los resultados reales de las pruebas, incluyendo evidencias y observaciones

## 12. Riesgos y limitaciones

### 12.1 Riesgos del proyecto
- Conexión a MongoDB Atlas: posibles interrupciones del servicio o problemas de conectividad.
- Seguridad de los datos: riesgo de acceso no autorizado si las credenciales no se protegen adecuadamente.
- Rendimiento: posibles tiempos de respuesta elevados cuando aumente el volumen de información.
- Integridad de los datos: riesgo de inconsistencias si no se validan correctamente los documentos y las operaciones.

### 12.2 Limitaciones del proyecto

- Alcance funcional: el proyecto se enfoca en el diseño e implementación de la base de datos, sin desarrollar una aplicación completa de comercio electrónico.
- Interfaz de usuario: no se contempla el desarrollo de interfaces gráficas para clientes o administradores.
- Procesamiento de pagos: no se incluyen pasarelas de pago ni transacciones financieras reales.
Logística: no se implementan procesos de envio o distribución de productos.
- Dependencia de MongoDB Atlas: el acceso a la base de datos requiere conectividad y disponibilidad del servicio en la nube.

## 13. Estructura del repositorio

```text

MercadoTico-360/

├── data/

│   └── README.md

│

├── database/

│   ├── Index/

│   ├── integrante3/

│   ├── queires/

│   └── schemas/

│

├── docs/

├── Performance/

├── test/

├── Entregables/

├── Paper técnico/

│

├── DATA_ARCHITECTURE.md

├── LICENSE

└── README.md

```

### Descripción de las carpetas principales

- `data/`: generación y carga de los datos utilizados por el proyecto.

- `database/`: archivos relacionados con la implementación de la base de datos.

- `database/Index/`: definición de índices para optimizar las consultas.

- `database/integrante3/`: scripts actuales de conexión y pruebas con MongoDB Atlas.

- `database/queires/`: consultas y agregaciones del proyecto.

- `database/schemas/`: definición de las estructuras de datos.

- `docs/`: documentación sobre arquitectura, modelo de datos y decisiones de diseño.

- `Performance/`: evidencia de las pruebas de rendimiento de los índices.

- `test/`: pruebas del proyecto.

- `Entregables/`: documentos correspondientes a las entregas del proyecto.

- `Paper técnico/`: archivos relacionados con el paper técnico.


## 14. Autores

- Adrián Quesada Jiménez
- Camila Alpízar Alfaro
- Emilio Calderón Jiménez
- Gustavo Jiménez Hidalgo
- Justin Zhu Fan
- Salma Capín Romero