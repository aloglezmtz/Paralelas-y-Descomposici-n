"""Repite las mediciones de la Práctica 6 y guarda resultados.json (lo usa generar_informe.py)."""
import argparse, csv, json, os, platform, re, statistics as st, subprocess, sys, time
import multiprocessing as mp
from sumas import generar_lista, sumar_segmento, dividir, suma_secuencial, suma_paralela, PROCESOS


def tarea_pesada(segmento):
    """Misma estructura que sumar_segmento, pero con más cálculo por elemento."""
    total = 0
    for x in segmento:
        for _ in range(100):
            total += (x * x) % 7
    return total


def medir_pesada(lista):
    t0 = time.perf_counter(); s = tarea_pesada(lista); t_sec = time.perf_counter() - t0
    t0 = time.perf_counter()
    with mp.Pool(PROCESOS) as p:
        par = sum(p.map(tarea_pesada, dividir(lista)))
    t_par = time.perf_counter() - t0
    assert s == par
    return t_sec, t_par


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Experimentos de la Práctica 6")
    ap.add_argument("--rapido", action="store_true", help="menos repeticiones y sin la lista de 10 millones (para probar)")
    args = ap.parse_args()
    REP = 2 if args.rapido else 5
    TAMS = (10_000, 100_000, 1_000_000) if args.rapido else (10_000, 100_000, 1_000_000, 10_000_000)

    # 0) corrida de referencia: ejecuta sumas.py y guarda su salida
    out = subprocess.run([sys.executable, "sumas.py", "--semilla", "2025"], capture_output=True, text=True, check=True).stdout
    open("salida.txt", "w", encoding="utf-8").write(out)
    t_ref_seq = float(re.search(r"Tiempo secuencial: ([\d.]+) s", out).group(1))
    t_ref_par = float(re.search(r"Tiempo paralelo: ([\d.]+) s", out).group(1))

    res = {"referencia": {"seq": t_ref_seq, "par": t_ref_par}, "cpu": os.cpu_count(), "python": platform.python_version(),
           "so": platform.system() + " " + platform.release()}

    # 1) 10 corridas con listas distintas (n = 100,000)
    corridas = []
    for i in range(10):
        lista = generar_lista(semilla=100 + i)
        ts, tp = suma_secuencial(lista)[1], suma_paralela(lista)[2]
        corridas.append({"n": i + 1, "seq": ts, "par": tp})
    res["corridas"] = corridas

    # 2) escalamiento con el tamaño de la lista (pool incluido / pool ya creado)
    tam = []
    for n in TAMS:
        lista = generar_lista(n, semilla=2025)
        rep = REP if n <= 1_000_000 else max(2, REP - 2)
        seq, par_c, par_w = [], [], []
        with mp.Pool(PROCESOS) as pool:
            suma_paralela(lista, pool=pool)            # calentamiento
            for _ in range(rep):
                seq.append(suma_secuencial(lista)[1])
                par_c.append(suma_paralela(lista)[2])
                par_w.append(suma_paralela(lista, pool=pool)[2])
        tam.append({"n": n, "seq": st.median(seq), "par_con_pool": st.median(par_c),
                    "par_pool_listo": st.median(par_w)})
        del lista
    res["tamanos"] = tam

    # 3) carga con más cálculo por elemento (100,000 elementos)
    lista = generar_lista(semilla=2025)
    pes = []
    for _ in range(3):
        a, b = medir_pesada(lista)
        pes.append({"seq": a, "par": b})
    res["pesada"] = {"seq": st.median(p["seq"] for p in pes), "par": st.median(p["par"] for p in pes)}

    json.dump(res, open("resultados.json", "w"), indent=1)

    def csv_out(nombre, campos, filas):
        with open(nombre, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(filas)
    csv_out("corrida_unica.csv", ["version", "tiempo_s"], [{"version": "secuencial", "tiempo_s": t_ref_seq}, {"version": "paralelo_4", "tiempo_s": t_ref_par}])
    csv_out("repeticiones.csv", ["n", "seq", "par"], res["corridas"])
    csv_out("tamanos.csv", ["n", "seq", "par_con_pool", "par_pool_listo"], res["tamanos"])
    csv_out("carga_pesada.csv", ["version", "tiempo_s"], [{"version": "secuencial", "tiempo_s": res["pesada"]["seq"]}, {"version": "paralelo_4", "tiempo_s": res["pesada"]["par"]}])
    seq_m = st.mean(c["seq"] for c in res["corridas"]); par_m = st.mean(c["par"] for c in res["corridas"])
    csv_out("resumen.csv", ["metrica", "valor"], [{"metrica": "nucleos", "valor": res["cpu"]}, {"metrica": "seq_promedio_s", "valor": seq_m},
            {"metrica": "par_promedio_s", "valor": par_m}, {"metrica": "aceleracion_promedio", "valor": st.mean(c["seq"]/c["par"] for c in res["corridas"])}])
    print(json.dumps(res, indent=1))
