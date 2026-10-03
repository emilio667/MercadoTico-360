# Schemas

Esta carpeta contiene los esquemas y reglas de validación de los documentos
utilizados en MongoDB para MercadoTico 360.

## ¿Qué debe incluir?

Se deben definir las estructuras correspondientes a las principales
colecciones de la base de datos:

- Productos
- Comercios
- Clientes
- Pedidos

## Productos

El catálogo debe permitir que diferentes categorías tengan atributos
diferentes. No se debe forzar que todos los productos tengan exactamente
los mismos atributos.

Cada producto debe estar asociado a un comercio mediante el campo
`comercio_id`, que referencia el identificador del comercio correspondiente.

Ejemplos de categorías:

- Alimentos
- Ropa
- Tecnología
- Artesanías
- Servicios
- Otras categorías

Ejemplo conceptual:

{
    "_id": "PROD-001",
    "nombre": "Camiseta Spiderman",
    "categoria": "Ropa",
    "precio": 18000.00,
    "comercio_id": "COM-102",
    "stock": 45,
    "atributos": {
        "talla": "M",
        "color": "Azul",
        "material": "Algodon"
    }
}

Los atributos específicos deben poder variar según la categoría.

## Comercios

Debe definirse la información necesaria para identificar y consultar
los comercios que forman parte del marketplace.

Cada comercio debe contar con un identificador único que pueda ser
referenciado desde los productos mediante el campo `comercio_id`.

La información del comercio puede incluir:

- nombre
- correo
- teléfono
- categoría
- estado
- dirección

La dirección puede representarse mediante una estructura anidada con:

- provincia
- cantón
- distrito
- dirección exacta

Los estados permitidos para un comercio pueden incluir:

- Activo
- Inactivo
- En remodelación

Ejemplo conceptual:

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

## Clientes

Debe definirse la información necesaria para identificar y consultar
los clientes del marketplace.

La información del cliente puede incluir datos personales y una dirección
embebida con provincia, cantón, distrito y dirección exacta.

Ejemplo conceptual:

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

Los pedidos deben contener información suficiente para reconstruir qué
compró el cliente aunque posteriormente cambie la información del producto.

Los detalles del pedido deben incluir información histórica del producto,
por ejemplo:

- producto_id
- nombre del producto
- precio al momento de la compra
- cantidad
- subtotal

Los productos que forman parte de un pedido pueden representarse mediante
estructuras anidadas.

Ejemplo conceptual:

{
    "_id": "PED-001",
    "fecha": datetime(2026, 10, 3, 10, 30),
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

## Validación

Cuando sea apropiado, se deben establecer reglas de validación para:

- Tipos de datos
- Campos requeridos
- Rangos de valores
- Valores permitidos

La estructura debe aprovechar la flexibilidad del modelo documental de
MongoDB.