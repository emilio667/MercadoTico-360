# MercadoTico 360

## Índice

1. [Descripción del proyecto](#1-descripción-del-proyecto)
2. [Problema de negocio](#2-problema-de-negocio)
3. [Objetivos](#3-objetivos)
4. [Tecnologías utilizadas](#4-tecnologías-utilizadas)
5. [Modelo de datos](#5-modelo-de-datos)
- [5.1 Productos](#51-productos)
- [5.2 Clientes](#52-clientes)
- [5.3 Pedidos](#53-pedidos)
6. [Prerrequisitos](#6-prerrequisitos)
7. [Instalación y configuración](#7-instalación-y-configuración)
8. [Carga de datos](#8-carga-de-datos)
9. [Ejecución](#9-ejecución)
10. [Comandos de demostración](#10-comandos-de-demostración)
11. [Resultados](#11-resultados)
12. [Estructura del repositorio](#12-estructura-del-repositorio)
13. [Autores](#13-autores)


## 1. Descripción del proyecto

MercadoTico 360 es un proyecto de base de datos NoSQL orientado a documentos para una plataforma de comercio electrónico.

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

- MongoDB
- MongoDB Atlas
- Modelo de datos orientado a documentos


## 5. Modelo de datos

La base de datos esta compuesta por tres colecciones principales.

### 5.1 Productos

La colección `productos` almacena el catálogo de MercadoTico 360. Cada producto puede tener atributos diferentes segun su categoria mediante el campo `atributos`.

Ejemplo:

```json

{

  "_id": "PROD-001",

  "nombre": "Camiseta Tipica",

  "precio": 18000,

  "categoria": "Ropa",

  "comercio_id": "COM-102",

  "stock": 45,

  "atributos": {

    "talla": "M",

    "color": "Azul",

    "material": "Algodon"

  }

}

```

### 5.2 Clientes

La colección `clientes` almacena la información de los usuarios de la plataforma, incluyendo sus datos de contacto y ubicación.

La dirección puede almacenarse como una estructura embebida con información como provincia, cantón y distrito.

### 5.3 Pedidos

La coleccion `pedidos` almacena las compras realizadas por los clientes.

Cada pedido contiene sus lineas de detalle, permitiendo conservar los productos, cantidades y precios correspondientes al momento en que se realizo la compra.

El monto total del pedido se obtiene a partir de los subtotales incluidos en las lineas de detalle.


## 6. Prerrequisitos

Antes de ejecutar el proyecto es necesario contar con:

- Python instalado.

- Una cuenta de MongoDB Atlas.

- Acceso al cluster de MongoDB Atlas utilizado por el proyecto.

- PyMongo instalado.

- Conexion a Internet para acceder al cluster alojado en MongoDB Atlas.


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



### 7.2 Instalar PyMongo

Ejecutar:

```bash

pip install pymongo

```

### 7.3 Configurar MongoDB Atlas

Para utilizar el proyecto es necesario contar con acceso al cluster correspondiente en MongoDB Atlas y configurar la conexion utilizando una URI valida.

Por seguridad, las credenciales de acceso no deben publicarse directamente en el repositorio.

### 7.4 Verificar PyMongo

Se puede comprobar la instalación ejecutando:

```bash

python database/integrante3/test_atlas.py

```

El resultado esperado es:

```text

PyMongo instalado correctamente

```

## 8. Carga de datos
La carga de datos utilizara generadores independientes para las principales colecciones del proyecto:

- Productos.

- Clientes.

- Pedidos.

La estructura prevista dentro de `data/` es:

```text

data/

├── generate_products.js

├── generate_customers.js

└── generate_orders.js

```
[PENDIENTE: incorporar los generadores y documentar los comandos definitivos para realizar la carga de datos]


## 9. Ejecución

[PENDIENTE: agregar instrucciones y comandos de ejecución]


## 10. Comandos de demostración

### 10.1 Consultas de productos

[PENDIENTE]

### 10.2 Consultas de clientes

[PENDIENTE]

### 10.3 Consultas de pedidos

[PENDIENTE]

### 10.4 Consultas analíticas

[PENDIENTE]


## 11. Resultados

[PENDIENTE: agregar resultados obtenidos durante las pruebas]


## 12. Estructura del repositorio

[PENDIENTE: agregar estructura final del repositorio]


## 13. Autores

- Adrián Quesada Jiménez
- Camila Alpízar Alfaro
- Emilio Calderón Jiménez
- Gustavo Jiménez Hidalgo
- Justin Zhu Fan
- Salma Capín Romero