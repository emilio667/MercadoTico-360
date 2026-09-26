# Schemas

Esta carpeta contiene los esquemas y reglas de validación de los documentos
utilizados en MongoDB para MercadoTico 360.

## ¿Qué debe incluir?

Se deben definir las estructuras correspondientes a las principales
colecciones de la base de datos:

- Productos
- Clientes
- Pedidos

## Productos

El catálogo debe permitir que diferentes categorías tengan atributos
diferentes. No se debe forzar que todos los productos tengan exactamente
los mismos atributos.

Ejemplos de categorías:

- Alimentos
- Ropa
- Tecnología
- Artesanías
- Servicios
- Otras categorías hasta completar al menos 8.

Ejemplo conceptual:

{
    nombre: "...",
    categoria: "...",
    precio: 0,
    stock: 0,
    atributos: {
        ...
    }
}

Los atributos específicos deben poder variar según la categoría.

## Pedidos

Los pedidos deben contener información suficiente para reconstruir qué
compró el cliente aunque posteriormente cambie la información del producto.

Los detalles del pedido deben incluir información histórica del producto,
por ejemplo:

- producto_id
- nombre del producto
- precio al momento de la compra
- cantidad
- otros datos necesarios

Los productos que forman parte de un pedido pueden representarse mediante
estructuras anidadas.

## Clientes

Debe definirse la información necesaria para identificar y consultar
los clientes del marketplace.

## Validación

Cuando sea apropiado, se deben establecer reglas de validación para:

- Tipos de datos
- Campos requeridos
- Rangos de valores
- Valores permitidos

La estructura debe aprovechar la flexibilidad del modelo documental de
MongoDB.
