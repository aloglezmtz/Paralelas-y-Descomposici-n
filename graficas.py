import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
r = json.load(open("resultados.json"))
OR, GR = "#d95f02", "#1b9e77"

# Fig: 10 corridas
c = r["corridas"]; x = [d["n"] for d in c]
plt.figure(figsize=(6.2, 2.9))
plt.plot(x, [d["seq"]*1000 for d in c], "o-", color=OR, label="Secuencial")
plt.plot(x, [d["par"]*1000 for d in c], "s-", color=GR, label="Paralelo (4 procesos)")
plt.xlabel("Corrida"); plt.ylabel("Tiempo (ms)"); plt.title("10 corridas con 100,000 elementos")
plt.grid(alpha=.3); plt.legend(); plt.tight_layout(); plt.savefig("fig_corridas.png", dpi=200); plt.close()

# Fig: tamaños (log-log)
t = r["tamanos"]; n = [d["n"] for d in t]
plt.figure(figsize=(6.2, 3.0))
plt.plot(n, [d["seq"]*1000 for d in t], "o-", color=OR, label="Secuencial")
plt.plot(n, [d["par_con_pool"]*1000 for d in t], "s-", color=GR, label="Paralelo (creando el pool)")
plt.plot(n, [d["par_pool_listo"]*1000 for d in t], "^--", color="#7570b3", label="Paralelo (pool ya creado)")
plt.xscale("log"); plt.yscale("log"); plt.xlabel("Número de elementos"); plt.ylabel("Tiempo (ms)")
plt.title("Escalamiento con el tamaño de la lista"); plt.grid(alpha=.3, which="both"); plt.legend(fontsize=8)
plt.tight_layout(); plt.savefig("fig_tamanos.png", dpi=200); plt.close()

# Fig: diagrama de descomposición
fig, ax = plt.subplots(figsize=(6.4, 2.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 4)
def box(x, y, w, h, txt, col):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=col, ec="#1f3a5f", lw=1)); ax.text(x+w/2, y+h/2, txt, ha="center", va="center", fontsize=7.5)
box(0.2, 3.0, 9.6, 0.8, "Lista de 100,000 enteros (1-100)", "#e6ecf8")
for i in range(4):
    box(0.2+i*2.4, 1.9, 2.4, 0.7, f"Segmento {i+1}\n25,000 elementos", "#fde9d9")
    box(0.2+i*2.4, 0.9, 2.4, 0.7, f"Proceso {i+1}\nsumar_segmento()", "#d9f0e6")
    ax.annotate("", xy=(1.4+i*2.4, 2.6), xytext=(1.4+i*2.4, 3.0), arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xy=(1.4+i*2.4, 1.6), xytext=(1.4+i*2.4, 1.9), arrowprops=dict(arrowstyle="->"))
box(2.6, 0.0, 4.8, 0.55, "sum(parciales) = suma total", "#e6ecf8")
for i in range(4): ax.annotate("", xy=(5.0, 0.55), xytext=(1.4+i*2.4, 0.9), arrowprops=dict(arrowstyle="->", color="#555"))
plt.tight_layout(); plt.savefig("fig_descomp.png", dpi=200); plt.close()

# Captura de terminal
lines = open("salida.txt").read().rstrip().split("\n")
fig = plt.figure(figsize=(7.4, 0.28*(len(lines)+3)), facecolor="#161b2b")
fig.text(0.02, 1-0.5/(len(lines)+3), "$ python sumas.py --semilla 2025", color="#9ece6a", family="monospace", fontsize=7.5, va="top")
for i, l in enumerate(lines):
    col = "#7aa2f7" if l.startswith("===") else "#9ece6a" if l.startswith("-->") else "#d6deeb"
    fig.text(0.02, 1-(i+1.7)/(len(lines)+3), l, color=col, family="monospace", fontsize=7.5, va="top")
plt.savefig("captura.png", dpi=200, facecolor="#161b2b"); plt.close()
