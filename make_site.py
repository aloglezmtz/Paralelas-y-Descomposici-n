import json, math
R = json.load(open("resultados.json"))
t = {d["n"]: d for d in R["tamanos"]}
seq100 = t[100_000]["seq"]; c_elem = seq100 / 100_000
big = max(t); fixed = t[10_000]["par_con_pool"] - t[10_000]["seq"]
transfer = max(0.0, (t[big]["par_con_pool"] - t[big]["seq"] - fixed) / big) if R["cpu"] == 1 else 0
# con varios núcleos no se puede separar el costo de transferencia del cómputo paralelo: se usa un valor típico
if R["cpu"] != 1:
    transfer = max(0.0, (t[big]["par_con_pool"] - fixed - t[big]["seq"] / min(4, R["cpu"])) / big)
cor = R["corridas"]
rows = "".join(f"<tr><td>{c['n']}</td><td>{c['seq']*1000:.2f}</td><td>{c['par']*1000:.2f}</td><td>{c['seq']/c['par']:.2f}×</td></tr>" for c in cor)
rows_t = "".join(f"<tr><td>{d['n']:,}</td><td>{d['seq']*1000:.2f}</td><td>{d['par_con_pool']*1000:.2f}</td><td>{d['par_pool_listo']*1000:.2f}</td></tr>" for d in R["tamanos"])
html = open("index_template.html", encoding="utf-8").read()
for k, v in {"__CELEM__": repr(c_elem), "__CHEAVY__": repr(R["pesada"]["seq"] / 100_000), "__FIXED__": repr(fixed), "__TRANSFER__": repr(transfer), "__CPU__": str(R["cpu"]),
             "__ROWS__": rows, "__ROWS_T__": rows_t,
             "__SEQ_M__": f"{sum(c['seq'] for c in cor)/len(cor)*1000:.2f}", "__PAR_M__": f"{sum(c['par'] for c in cor)/len(cor)*1000:.2f}"}.items():
    html = html.replace(k, v)
open("index.html", "w", encoding="utf-8").write(html)
print("index.html", len(html), "bytes", c_elem, fixed, transfer)
