#!/usr/bin/env python
"""
Genera los graficos del paper a partir de los CSV que produce benchmark.py.
(Integrante 5: QA & Performance)

Uso (desde la raiz del repositorio, con el entorno virtual activo):
    pip install matplotlib
    python Performance/scripts/graficos.py

Lee   Performance/resultados/*.csv
Crea  Performance/resultados/graficos/*.png

No consulta MongoDB: solo dibuja lo que ya midio benchmark.py.
"""

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # sin ventana: solo guarda archivos
import matplotlib.pyplot as plt
import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
ENTRADA = RAIZ / "Performance" / "resultados"
GRIS, AZUL, NARANJA = "#9aa5b1", "#1f6fb2", "#e08a1e"


def leer_csv(ruta):
    if not ruta.exists():
        print(f"  (no existe {ruta.name}, se omite)")
        return []
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def etiqueta(consulta_id):
    """'Q3_categoria_precio' -> 'Q3\\ncategoria precio'"""
    codigo, _, resto = consulta_id.partition("_")
    return f"{codigo}\n{resto.replace('_', ' ')}"


def rotular(ax, barras, formato="{:.1f}"):
    for b in barras:
        ax.annotate(formato.format(b.get_height()),
                    (b.get_x() + b.get_width() / 2, b.get_height()),
                    ha="center", va="bottom", fontsize=7,
                    xytext=(0, 2), textcoords="offset points")


def barras_sin_con(filas, col_sin, col_con, titulo, ylabel, salida, formato="{:.1f}"):
    etiquetas = [etiqueta(f["consulta"]) for f in filas]
    sin = [float(f[col_sin]) for f in filas]
    con = [float(f[col_con]) for f in filas]
    x = np.arange(len(filas))
    w = 0.38
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=200)
    b1 = ax.bar(x - w / 2, sin, w, label="Sin índice", color=GRIS)
    b2 = ax.bar(x + w / 2, con, w, label="Con índice", color=AZUL)
    ax.set_yscale("log")
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas, fontsize=8)
    rotular(ax, b1, formato)
    rotular(ax, b2, formato)
    ax.set_ylim(min(con + sin) * 0.5, max(con + sin) * 2.5)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(salida)
    plt.close(fig)
    print(f"  {salida.name}")


def fig_concurrencia(filas, salida):
    hilos = [f["hilos"] for f in filas]
    rendimiento = [float(f["solicitudes_por_s"]) for f in filas]
    media = [float(f["media_ms"]) for f in filas]
    p95 = [float(f["p95_ms"]) for f in filas]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=200)
    barras = a1.bar(hilos, rendimiento, color=AZUL)
    rotular(a1, barras, "{:.0f}")
    a1.set_xlabel("Hilos concurrentes")
    a1.set_ylabel("Solicitudes por segundo")
    a1.set_title("Rendimiento")
    a1.set_ylim(0, max(rendimiento) * 1.2)
    a1.grid(axis="y", alpha=0.3)
    a1.set_axisbelow(True)
    x = np.arange(len(hilos))
    w = 0.38
    rotular(a2, a2.bar(x - w / 2, media, w, label="Media", color=AZUL), "{:.0f}")
    rotular(a2, a2.bar(x + w / 2, p95, w, label="Percentil 95", color=NARANJA), "{:.0f}")
    a2.set_xticks(x)
    a2.set_xticklabels(hilos)
    a2.set_xlabel("Hilos concurrentes")
    a2.set_ylabel("Latencia (ms)")
    a2.set_title("Latencia por solicitud")
    a2.legend()
    a2.grid(axis="y", alpha=0.3)
    a2.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(salida)
    plt.close(fig)
    print(f"  {salida.name}")


def fig_agregaciones(filas, salida):
    nombres = [f["agregacion"].partition("_")[0] + "\n" +
               f["agregacion"].partition("_")[2].replace("_", " ") for f in filas]
    medianas = [float(f["mediana_ms"]) / 1000 for f in filas]  # segundos
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=200)
    barras = ax.bar(nombres, medianas, color=AZUL)
    ax.set_yscale("log")
    ax.set_ylabel("Tiempo mediano (s, escala logarítmica)")
    ax.set_title("Tiempo de las agregaciones")
    rotular(ax, barras, "{:.2f}")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(salida)
    plt.close(fig)
    print(f"  {salida.name}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrada", type=Path, default=ENTRADA)
    ap.add_argument("--salida", type=Path, default=None)
    args = ap.parse_args()
    salida = args.salida or args.entrada / "graficos"
    salida.mkdir(parents=True, exist_ok=True)

    print(f"Leyendo {args.entrada}")
    comparativa = leer_csv(args.entrada / "comparativa_indices.csv")
    if comparativa:
        barras_sin_con(comparativa, "mediana_sin_ms", "mediana_con_ms",
                       "Tiempo mediano por consulta, sin y con índice",
                       "Tiempo mediano (ms, escala logarítmica)",
                       salida / "fig1_consultas_indices.png")
        barras_sin_con(comparativa, "docs_examinados_sin", "docs_examinados_con",
                       "Documentos examinados por consulta, sin y con índice",
                       "Documentos examinados (escala logarítmica)",
                       salida / "fig2_docs_examinados.png", "{:.0f}")
    concurrencia = leer_csv(args.entrada / "concurrencia.csv")
    if concurrencia:
        fig_concurrencia(concurrencia, salida / "fig3_concurrencia.png")
    agregaciones = leer_csv(args.entrada / "agregaciones.csv")
    if agregaciones:
        fig_agregaciones(agregaciones, salida / "fig4_agregaciones.png")
    print(f"Graficos guardados en {salida}")


if __name__ == "__main__":
    main()