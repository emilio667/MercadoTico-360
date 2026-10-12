# Script de demostración de consultas - MercadoTico 360
# Usa las funciones ya implementadas en database/queries

from pprint import pprint

from database.queries.consultas_productos import (
    buscar_por_categoria,
    buscar_por_rango_precio,
    buscar_por_atributo,
    buscar_por_categoria_y_precio,
    buscar_por_categoria_y_atributo,
    buscar_productos_disponibles,
    buscar_productos_por_comercio,
)

from database.queries.consultas_pedidos import (
    buscar_pedido_por_id,
    buscar_pedidos_por_cliente,
    buscar_pedidos_cliente_por_fecha,
    buscar_pedidos_por_estado,
    buscar_pedidos_cliente_por_estado,
    actualizar_estado_pedido,
    buscar_pedidos_por_producto,
    contar_pedidos_cliente,
)

from database.queries.agregaciones import (
    ventas_por_categoria,
    productos_mas_vendidos,
    ticket_promedio,
    ventas_por_estado,
    pedidos_con_cliente,
    ventas_categoria_especifica,
)


def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def mostrar_primeros(resultados, cantidad=3):
    print(f"Resultados encontrados: {len(resultados)}")
    for resultado in resultados[:cantidad]:
        pprint(resultado)


if __name__ == "__main__":

    #Consultas de productos

    titulo("1. PRODUCTOS POR CATEGORÍA")
    mostrar_primeros(
        buscar_por_categoria("Ropa")
    )

    titulo("2. PRODUCTOS POR RANGO DE PRECIO")
    mostrar_primeros(
        buscar_por_rango_precio(10000, 50000)
    )

    titulo("3. PRODUCTOS POR ATRIBUTO VARIABLE")
    mostrar_primeros(
        buscar_por_atributo("talla", "M")
    )

    titulo("4. PRODUCTOS POR CATEGORÍA Y PRECIO")
    mostrar_primeros(
        buscar_por_categoria_y_precio(
            "Tecnología",
            10000,
            200000,
        )
    )

    titulo("5. PRODUCTOS POR CATEGORÍA Y ATRIBUTO")
    mostrar_primeros(
        buscar_por_categoria_y_atributo(
            "Ropa",
            "talla",
            "M",
        )
    )

    titulo("6. PRODUCTOS DISPONIBLES")
    mostrar_primeros(
        buscar_productos_disponibles()
    )

    titulo("7. PRODUCTOS POR COMERCIO")
    mostrar_primeros(
        buscar_productos_por_comercio("COM-001")
    )

    #Consultas de pedidos

    titulo("8. PEDIDO POR ID")
    pedido = buscar_pedido_por_id("PED-00001")
    pprint(pedido)

    titulo("9. PEDIDOS DE UN CLIENTE")
    mostrar_primeros(
        buscar_pedidos_por_cliente("CLI-00001")
    )

    titulo("10. PEDIDOS DE UN CLIENTE ORDENADOS POR FECHA")
    mostrar_primeros(
        buscar_pedidos_cliente_por_fecha("CLI-00001")
    )

    titulo("11. PEDIDOS POR ESTADO")
    mostrar_primeros(
        buscar_pedidos_por_estado("Entregado")
    )

    titulo("12. PEDIDOS DE UN CLIENTE POR ESTADO")
    mostrar_primeros(
        buscar_pedidos_cliente_por_estado(
            "CLI-00001",
            "Entregado",
        )
    )

    titulo("13. PEDIDOS QUE CONTIENEN UN PRODUCTO")
    mostrar_primeros(
        buscar_pedidos_por_producto("PROD-00001")
    )

    titulo("14. CANTIDAD DE PEDIDOS DE UN CLIENTE")
    cantidad = contar_pedidos_cliente("CLI-00001")
    print("Cantidad de pedidos:", cantidad)

    #Actualización del estado de un pedido

    titulo("15. ACTUALIZACIÓN PARCIAL DEL ESTADO")

    id_pedido_demo = "PED-00001"
    pedido_actual = buscar_pedido_por_id(id_pedido_demo)

    if pedido_actual:
        estado_original = pedido_actual["estado"]

        nuevo_estado = (
            "Enviado"
            if estado_original != "Enviado"
            else "Pendiente"
        )

        print("Estado original:", estado_original)

        modificados = actualizar_estado_pedido(
            id_pedido_demo,
            nuevo_estado,
        )

        print("Documentos modificados:", modificados)

        pedido_actualizado = buscar_pedido_por_id(id_pedido_demo)
        print("Estado actualizado:", pedido_actualizado["estado"])

        #Restaurar el estado original

        actualizar_estado_pedido(
            id_pedido_demo,
            estado_original,
        )

        print("Estado restaurado:", estado_original)

    else:
        print("No se encontró el pedido de demostración.")

    #Agregaciones y consultas avanzadas
    
    titulo("16. VENTAS POR CATEGORÍA")
    pprint(
        ventas_por_categoria()
    )

    titulo("17. PRODUCTOS MÁS VENDIDOS")
    pprint(
        productos_mas_vendidos()
    )

    titulo("18. TICKET PROMEDIO")
    pprint(
        ticket_promedio()
    )

    titulo("19. VENTAS POR ESTADO")
    pprint(
        ventas_por_estado()
    )

    titulo("20. PEDIDOS CON INFORMACIÓN DEL CLIENTE")
    resultados = pedidos_con_cliente()
    mostrar_primeros(resultados)

    titulo("21. VENTAS DE UNA CATEGORÍA ESPECÍFICA")
    pprint(
        ventas_categoria_especifica("Ropa")
    )

    print("\nDemostración finalizada.")
