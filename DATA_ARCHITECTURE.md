## MercadoTico-360
MercadoTico 360, Tecnología documentos

## Arquitectura de datos y justificación NoSQL

El caso de negocio MercadoTico 360 requiere solucionar las limitaciones de un modelo relacional tradicional al gestionar un catálogo con productos sumamente variados (alimentos, ropa, tecnología, artesanías y servicios).
El modelo orientado a documentos de MongoDB se justifica técnicamente por los siguientes factores:

1. **Esquema flexible (Catálogo heterogéneo):** Cada categoría de producto posee atributos distintos. En lugar de utilizar tablas relacionales con múltiples columnas nulas o tablas hijas para atributos dinámicos, el modelo de documentos (BSON/JSON) permite guardar productos con atributos personalizados según su categoría, eliminando campos vacíos y simplificando el almacenamiento.
2. **Documentos embebidos (Historial de pedidos):** Permite anidar las líneas de detalle directamente dentro del documento principal de cada pedido. Esto garantiza la inmutabilidad e integridad histórica de la compra sin depender de operaciones JOIN complejas entre múltiples tablas.
3. **Evolución del esquema sin interrupciones:** Permite incorporar nuevas categorías de productos o agregar nuevos datos a la estructura del pedido en tiempo real, facilitando la escalabilidad del marketplace a medida que crece.
4. **Capacidad de análisis:** MongoDB cuenta con un motor de agregaciones (*Aggregation Framework*) muy potente, idóneo para extraer reportes analíticos y métricas operativas requeridas por la plataforma.

## Estrategia de índices para optimización de lecturas
Para garantizar un rendimiento óptimo en la plataforma frente al volumen de datos, se definieron los siguientes índices estratégicos en el código (`docs/modelos-datos.py):
* **`idx_categoria_precio` (`categoria: 1, precio: 1`):** Optimiza las búsquedas frecuentes en el catálogo al filtrar por categoría y ordenar los productos por precio de forma ascendente.
* **`idx_atributos_talla` (`atributos.talla: 1`):** Acelera las consultas sobre el objeto embebido de atributos específicos (ej. filtrado por talla en prendas de vestir).
* **`idx_cliente_fecha` (`cliente_id: 1, fecha: -1`):** Permite recuperar de forma inmediata el historial de pedidos recientes de cualquier cliente en la plataforma.

