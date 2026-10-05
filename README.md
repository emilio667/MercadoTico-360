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

4. Desarrollar un patrón de documentos para la colección de pedidos que encapsule las líneas de detalle de las compras, resguardando la integridad histórica de los precios y cantidades facturadas.


## 4. Tecnologías utilizadas

- MongoDB
- MongoDB Atlas
- Modelo de datos orientado a documentos


## 5. Modelo de datos

La base de datos está compuesta por tres colecciones principales.

### 5.1 Productos

Almacena el catálogo de productos de diferentes categorías y sus atributos específicos.

### 5.2 Clientes

Almacena la información de los clientes, incluyendo sus datos de contacto y ubicación.

### 5.3 Pedidos

Almacena las compras realizadas y sus líneas de detalle, conservando los precios y cantidades correspondientes al momento de cada transacción.


## 6. Prerrequisitos

Antes de ejecutar el proyecto es necesario contar con:

- Una cuenta de MongoDB Atlas.
- Acceso al clúster del proyecto.
- [PENDIENTE: verificar otros requisitos]


## 7. Instalación y configuración

### 7.1 Clonar el repositorio

[PENDIENTE: agregar URL y comando]

### 7.2 Configurar MongoDB Atlas

[PENDIENTE: agregar pasos de configuración]

### 7.3 Configurar la conexión

[PENDIENTE: agregar configuración definitiva]


## 8. Carga de datos

[PENDIENTE: agregar scripts, archivos y orden de carga]


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