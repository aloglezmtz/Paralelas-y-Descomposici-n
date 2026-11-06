"""Práctica 6 · Tareas paralelas y descomposición de problemas.

Suma de una lista de 100,000 números aleatorios (1-100):
  1) versión SECUENCIAL
  2) versión PARALELA con multiprocessing.Pool(4) (descomposición de datos)

Uso: python sumas.py            (semilla por defecto 2025)
     python sumas.py --semilla 7
"""
import argparse
import multiprocessing as mp
import os
import random
import time

N = 100_000
PROCESOS = 4


def generar_lista(n=N, semilla=None):
    """Lista de n enteros aleatorios entre 1 y 100."""
    rng = random.Random(semilla)
    return [rng.randint(1, 100) for _ in range(n)]


def sumar_segmento(segmento):
    """Tarea paralela: recibe un segmento de la lista y devuelve su suma."""
    total = 0
    for x in segmento:
        total += x
    return total


def dividir(lista, partes=PROCESOS):
    """Descomposición de datos: 'partes' segmentos contiguos del mismo tamaño."""
    tam = len(lista) // partes
    return [lista[i * tam:(i + 1) * tam] for i in range(partes)]


def suma_secuencial(lista):
    t0 = time.perf_counter()
    total = sumar_segmento(lista)               # una sola tarea con todos los datos
    return total, time.perf_counter() - t0


def suma_paralela(lista, procesos=PROCESOS, pool=None):
    """Si se pasa un pool ya creado, no se cuenta el costo de crearlo."""
    t0 = time.perf_counter()
    segmentos = dividir(lista, procesos)
    if pool is None:
        with mp.Pool(procesos) as p:            # crear el pool SÍ cuenta
            parciales = p.map(sumar_segmento, segmentos)
    else:
        parciales = pool.map(sumar_segmento, segmentos)
    total = sum(parciales)                      # combinar resultados parciales
    return total, parciales, time.perf_counter() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--semilla", type=int, default=2025)
    args = ap.parse_args()

    lista = generar_lista(semilla=args.semilla)
    print(f"Elementos: {len(lista):,} | Núcleos disponibles: {os.cpu_count()} | Procesos: {PROCESOS}")
    print(f"Tamaño de cada segmento: {len(lista) // PROCESOS:,}\n")

    print("=== BLOQUE 1: ejecución SECUENCIAL ===")
    t_sec_total, t_sec = suma_secuencial(lista)
    print(f"Suma total: {t_sec_total:,}")
    print(f"--> Tiempo secuencial: {t_sec:.6f} s\n")

    print("=== BLOQUE 2: ejecución PARALELA (multiprocessing, 4 procesos) ===")
    t_par_total, parciales, t_par = suma_paralela(lista)
    for i, s in enumerate(parciales, 1):
        print(f"Proceso {i}: suma parcial = {s:,}")
    print(f"Suma total: {t_par_total:,}")
    print(f"--> Tiempo paralelo: {t_par:.6f} s\n")

    assert t_sec_total == t_par_total == sum(lista), "las sumas no coinciden"
    print("Verificación: ambas sumas coinciden con sum(lista).\n")

    print("=== TABLA COMPARATIVA ===")
    print(f"{'Versión':<24}{'Tiempo (s)':>14}")
    print(f"{'Secuencial':<24}{t_sec:>14.6f}")
    print(f"{'Paralelo (4 procesos)':<24}{t_par:>14.6f}")
    print(f"{'Aceleración':<24}{t_sec / t_par:>13.2f}x")


if __name__ == "__main__":
    main()
