# Indexes

Esta carpeta contiene los índices utilizados para optimizar las consultas
frecuentes del marketplace.

## Requisito mínimo

Se deben implementar índices para al menos tres patrones de consulta
frecuentes.

## Patrones que se deben considerar

### 1. Búsqueda por categoría

Permitir consultar productos pertenecientes a una categoría específica.

Ejemplo:

categoria = "Tecnologia"

### 2. Búsqueda por rango de precio

Permitir consultar productos cuyo precio se encuentre dentro de un rango.

Ejemplo:

precio >= 100000
precio <= 500000

### 3. Búsqueda por categoría y precio

Permitir consultar productos de una categoría dentro de un determinado
rango de precios.

Ejemplo:

categoria = "Tecnologia"
precio entre 100000 y 500000

### 4. Pedidos de un cliente

Considerar un índice para recuperar eficientemente los pedidos asociados
a un cliente.

Ejemplo:

cliente_id = 12345

## Archivo

Los índices deben implementarse en archivos JavaScript (.js).

Ejemplo:

indexes.js

El archivo debe permitir crear los índices de forma reproducible.

## Evaluación

Se debe realizar al menos una comparación de una consulta antes y después
de crear un índice, registrando la evidencia y las métricas obtenidas.

También se debe justificar por qué cada índice es útil para el patrón de
consulta correspondiente.