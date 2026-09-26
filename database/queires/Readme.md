# Queries

Esta carpeta contiene las consultas utilizadas para demostrar el
funcionamiento de MercadoTico 360.

Las consultas deben estar organizadas según su propósito.

## 1. Productos

Archivo sugerido:

productos.js

Debe incluir consultas para:

- Buscar productos por categoría.
- Buscar productos por rango de precio.
- Buscar productos utilizando un atributo específico de una categoría.
- Combinar filtros cuando sea necesario.

## 2. Pedidos

Archivo sugerido:

pedidos.js

Debe incluir consultas para:

- Recuperar todos los pedidos de un cliente.
- Recuperar un pedido completo con sus líneas de detalle.
- Consultar información del estado de un pedido.
- Actualizar el estado de un pedido.

El pedido debe conservar la información necesaria para reconstruir
la compra realizada originalmente.

## 3. Agregaciones

Archivo sugerido:

agregaciones.js

Se deben implementar al menos dos consultas de agregación.

Ejemplos:

- Ventas por categoría.
- Ticket promedio.
- Productos más vendidos.

Cada agregación debe incluir una breve explicación de qué información
obtiene y para qué podría utilizarse en el marketplace.

## 4. Atributos variables

Debe existir al menos una consulta que demuestre que productos de
diferentes categorías pueden tener atributos específicos sin necesitar
un esquema idéntico para todos.

## Organización

Cada archivo .js debe contener consultas relacionadas con una misma
función y comentarios que permitan comprender qué hace cada consulta.
