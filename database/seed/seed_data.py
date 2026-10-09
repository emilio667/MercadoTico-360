import subprocess
import sys
import os

print("=== CARGA DE DATOS MERCADOTICO360 ===")

python = sys.executable

ruta_actual = os.path.dirname(__file__)

scripts = [
    "seed_comercios.py",
    "seed_clientes.py",
    "seed_productos.py",
    "seed_pedidos.py"
]

for script in scripts:

    print(f"\nEjecutando {script}...")

    ruta_script = os.path.join(
        ruta_actual,
        script
    )

    subprocess.run(
        [python, ruta_script],
        check=True
    )

print("\nProceso finalizado correctamente")