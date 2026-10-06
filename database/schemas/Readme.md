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

Las categorías permitidas son:

- Alimentos
- Ropa
- Tecnología
- Artesanías
- Servicios
- Hogar
- Belleza
- Deportes

Ejemplo conceptual:

```python
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