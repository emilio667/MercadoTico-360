# Modelo de Datos - MercadoTico 360

Este documento describe el modelo de datos utilizado en MercadoTico 360.
La solución utiliza MongoDB con un modelo orientado a documentos y está
compuesta por cuatro colecciones principales:

- Productos
- Comercios
- Clientes
- Pedidos

## Productos

La colección `productos` almacena el catálogo del marketplace. Cada producto pertenece a un comercio y puede tener atributos diferentes según su categoría.

Campos principales:

- `_id`: Identificador único del producto.
- `nombre`: Nombre del producto.
- `precio`: Precio actual del producto.
- `categoria`: Categoría a la que pertenece el producto.
- `comercio_id`: Identificador del comercio que ofrece el producto.
- `stock`: Cantidad disponible del producto.
- `atributos`: Características específicas del producto.

Las categorías permitidas son:

- Alimentos
- Ropa
- Tecnología
- Artesanías
- Servicios
- Hogar
- Belleza
- Deportes

Ejemplo:

{
    "_id": "PROD-001",
    "nombre": "Camiseta Spiderman",
    "precio": 18000.00,
    "categoria": "Ropa",
    "comercio_id": "COM-102",
    "stock": 45,
    "atributos": {
        "talla": "M",
        "color": "Azul",
        "material": "Algodon"
    }
}

El campo `atributos` se mantiene flexible debido a que las características pueden variar entre productos. Por ejemplo, un producto de ropa puede tener talla, color y material, mientras que un producto tecnológico puede tener garantía y voltaje. Los atributos se almacenan embebidos porque pertenecen directamente al producto y permite manejar características diferentes según la categoría, mientras que `comercio_id` se utiliza como referencia porque un comercio puede estar relacionado con varios productos.

## Comercios

La colección `comercios` almacena la información de los negocios que ofrecen productos dentro del marketplace.

Campos principales:

- `_id`: Identificador único del comercio.
- `nombre`: Nombre del comercio.
- `correo`: Correo electrónico del comercio.
- `telefono`: Número telefónico.
- `categoria`: Categoría general del comercio.
- `estado`: Estado actual del comercio.
- `direccion`: Objeto embebido con la ubicación del comercio.

Las categorías permitidas para los comercios son:

- Alimentos
- Ropa
- Tecnología
- Artesanías
- Servicios
- Hogar
- Belleza
- Deportes

La dirección contiene:

- `provincia`
- `canton`
- `distrito`
- `direccion_exacta`

Ejemplo:

{
    "_id": "COM-102",
    "nombre": "Disfraces Tiquicia",
    "correo": "contacto@disfracestiquicia.cr",
    "telefono": "2551-7788",
    "categoria": "Ropa",
    "estado": "Activo",
    "direccion": {
        "provincia": "Cartago",
        "canton": "Cartago",
        "distrito": "Oriental",
        "direccion_exacta": "100 metros norte del parque central"
    }
}

Los estados definidos para los comercios son:

- Activo
- Inactivo
- En remodelación

La dirección se almacena embebida porque forma parte directa de la información del comercio.

## Clientes

La colección `clientes` almacena la información de los usuarios que realizan pedidos dentro del marketplace.

Campos principales:

- `_id`: identificador único del cliente.
- `nombre`: nombre del cliente.
- `correo`: correo electrónico.
- `telefono`: número telefónico.
- `cedula`: número de identificación.
- `direccion`: objeto embebido con la dirección del cliente.

La dirección contiene:

- `provincia`
- `canton`
- `distrito`
- `direccion_exacta`

Ejemplo:

{
    "_id": "CLI-001",
    "nombre": "Ariel Rodriguez",
    "correo": "ariel.rodriguez@gmail.com",
    "telefono": "8888-1111",
    "cedula": "102340678",
    "direccion": {
        "provincia": "San Jose",
        "canton": "San Jose",
        "distrito": "Carmen",
        "direccion_exacta": "200 metros este de la iglesia"
    }
}

## Pedidos

La colección `pedidos` almacena el historial de compras realizadas por los clientes.

Campos principales:

- `_id`: identificador único del pedido.
- `fecha`: fecha y hora en la que se realizó el pedido.
- `cliente_id`: identificador del cliente que realizó el pedido.
- `estado`: estado actual del pedido.
- `monto_total`: monto total de la compra.
- `lineas_detalle`: arreglo embebido con los productos incluidos en el pedido.

Los estados definidos para un pedido son:

- Cancelado
- Pendiente
- Enviado
- Entregado

Cada elemento de `lineas_detalle` contiene:

- `producto_id`
- `nombre_producto`
- `precio_unitario`
- `cantidad`
- `subtotal`

Ejemplo:

{
    "_id": "PED-001",
    "fecha": "2026-10-03 10:30:00",
    "cliente_id": "CLI-001",
    "estado": "Pendiente",
    "monto_total": 36000.00,
    "lineas_detalle": [
        {
            "producto_id": "PROD-001",
            "nombre_producto": "Camiseta Spiderman",
            "precio_unitario": 18000.00,
            "cantidad": 2,
            "subtotal": 36000.00
        }
    ]
}

Las líneas de detalle se almacenan embebidas para conservar la información histórica de la compra, mientras que `cliente_id` y `producto_id` se utilizan como referencias a entidades independientes porque un pueden estar relacionados con varios pedidos.

## Relaciones entre colecciones

### Relación entre productos y comercios

La relación se realiza mediante:

productos.comercio_id -> comercios._id

Cada producto está asociado a un comercio mediante el campo `comercio_id`. Un comercio puede ofrecer varios productos, mientras que cada producto está asociado a un único comercio.

### Relación entre pedidos y clientes

La relación se realiza mediante:

pedidos.cliente_id -> clientes._id

Cada pedido está asociado a un cliente mediante el campo `cliente_id`. Un cliente puede realizar varios pedidos, mientras que cada pedido está asociado a un único cliente.

### Relación entre pedidos y productos

La relación se realiza mediante:

pedidos.lineas_detalle.producto_id -> productos._id

Cada línea de detalle contiene el campo `producto_id`, que permite identificar el producto correspondiente. Un producto puede aparecer en múltiples pedidos, mientras que cada línea de detalle hace referencia a un único producto.

## Uso de documentos embebidos y referencias

Se utilizan documentos embebidos cuando la información pertenece directamente al documento principal.

Ejemplos:

- Dirección dentro de clientes.
- Dirección dentro de comercios.
- Líneas de detalle dentro de pedidos.
- Atributos variables dentro de productos.

Se utilizan referencias cuando la información corresponde a una entidad independiente que puede relacionarse con varios documentos.

Ejemplos:

- `comercio_id` referencia un comercio desde un producto.
- `cliente_id` referencia un cliente desde un pedido.
- `producto_id` identifica el producto asociado a una línea de detalle.