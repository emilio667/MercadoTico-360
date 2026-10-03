# Decisiones de Diseño - MercadoTico 360

Este documento describe las principales decisiones tomadas para el diseño
del modelo de datos de MercadoTico 360, utilizando MongoDB como tecnología
orientada a documentos.

## Diseño del catálogo de productos

Se utiliza un modelo orientado a documentos debido a que el catálogo de
MercadoTico 360 incluye productos de categorías muy diferentes, como
alimentos, ropa, tecnología, artesanías y servicios. Cada categoría puede requerir atributos distintos, 
por lo que se decidió utilizar el campo `atributos` como un objeto embebido flexible dentro de
cada producto.

De esta forma, un producto de ropa puede almacenar atributos como talla,
color y material, mientras que un producto tecnológico puede almacenar
garantía o voltaje, sin obligar a todos los productos a compartir exactamente
la misma estructura.

## Relación entre productos y comercios

Los comercios se almacenan en una colección independiente de la colección
`productos`. Cada producto contiene el campo `comercio_id`, que permite identificar el
comercio que ofrece ese producto.

La relación se establece de la siguiente forma:

productos.comercio_id -> comercios._id

Se decidió utilizar una referencia debido a que un mismo comercio puede
ofrecer varios productos. De esta manera se evita repetir en cada producto
información como el nombre, correo, teléfono, categoría, estado y dirección
del comercio.

## Dirección embebida en comercios y clientes

La dirección se almacena como un objeto embebido dentro de los documentos
de las colecciones `comercios` y `clientes`. La estructura de dirección contiene:

- provincia
- canton
- distrito
- direccion_exacta

Se decidió utilizar una estructura embebida porque la dirección forma parte
directa de la información de cada comercio o cliente y se consulta
junto con los demás datos del documento.

## Relación entre pedidos y clientes

Cada pedido contiene el campo `cliente_id`, que permite identificar al cliente
que realizó la compra. La relación se establece de la siguiente forma:

pedidos.cliente_id -> clientes._id

Se utiliza una referencia porque un mismo cliente puede realizar varios
pedidos y no es necesario repetir toda su información personal dentro de
cada documento de pedido.

## Líneas de detalle embebidas en pedidos

Las líneas de detalle de los pedidos se almacenan como un arreglo embebido dentro del
documento de cada pedido. Cada línea de detalle contiene:

- producto_id
- nombre_producto
- precio_unitario
- cantidad
- subtotal

Esta estructura permite conservar la información necesaria para reconstruir
qué compró el cliente aunque posteriormente cambie la información del producto
en el catálogo.

## Relación entre pedidos y productos

Dentro de cada línea de detalle se almacena el campo `producto_id`. La relación se establece de la siguiente forma:

pedidos.lineas_detalle.producto_id -> productos._id

Esta referencia permite identificar el producto asociado a cada línea del
pedido, mientras que la información histórica permanece embebida dentro del
pedido.

## Uso de referencias y documentos embebidos

El modelo combina referencias y estructuras embebidas según el tipo de
información.

Se utilizan referencias en:

- `productos.comercio_id` para relacionar productos con comercios.
- `pedidos.cliente_id` para relacionar pedidos con clientes.
- `pedidos.lineas_detalle.producto_id` para identificar los productos
  incluidos en un pedido.

Se utilizan estructuras embebidas en:

- `productos.atributos`
- `comercios.direccion`
- `clientes.direccion`
- `pedidos.lineas_detalle`

