import os

print("=== CARGA DE DATOS MERCADOTICO360 ===")

os.system("python seed_clientes.py")
os.system("python seed_productos.py")
os.system("python seed_pedidos.py")

print("Proceso finalizado")