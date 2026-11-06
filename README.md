# Práctica 6 · Tareas paralelas y descomposición de problemas

Suma de una lista de **100,000 números aleatorios (1–100)** comparando una versión **secuencial** con una versión **paralela** que divide la lista en **4 segmentos** y los suma con `multiprocessing.Pool(4)`. Incluye una página interactiva que muestra cuándo conviene paralelizar.

**Alumna:** Alondra Goretti González Martínez (218534681) · **Materia:** Programación Paralela y Concurrente · CUCEI · **Profesor:** Mtro. Zeus Emanuel Gutiérrez Cobián

## Contenido

| Archivo | Descripción |
|---|---|
| `index.html` | Página interactiva (se publica con GitHub Pages) |
| `sumas.py` | **Código de la práctica**: lista aleatoria, `sumar_segmento`, versión secuencial, versión paralela y tabla comparativa |
| `experimento.py` | Corrida de referencia, 10 repeticiones, efecto del tamaño y carga pesada; genera los CSV y `resultados.json` |
| `graficas.py` | Gráficas y captura de la terminal |
| `generar_informe.py` | Genera `Practica6_Paralelismo_Informe.pdf` con los datos de `resultados.json` |
| `make_site.py` + `index_template.html` | Regeneran `index.html` con tus mediciones |
| `*.csv`, `*.png`, `salida.txt` | Resultados y figuras |
| `.github/workflows/paralelo.yml` | Ejecuta todo en GitHub Actions |
| `.nojekyll` | Indica a GitHub Pages que sirva los archivos tal cual |

## Ejecutar en tu computadora

```
pip install -r requirements.txt
python sumas.py                 # lo que pide la práctica
python sumas.py --semilla 7     # otra lista, reproducible
python experimento.py           # mediciones (~1-2 min); --rapido para probar
python graficas.py
python generar_informe.py       # PDF
python make_site.py             # index.html con tus datos
```

`sumas.py` solo usa la biblioteca estándar. En Windows y macOS `multiprocessing` usa *spawn*, por eso el código está protegido con `if __name__ == "__main__":`; no lo quites.

> **Importante:** los resultados incluidos se midieron en un equipo con **1 núcleo**, donde la versión paralela es más lenta. Vuelve a correr `experimento.py` en tu computadora (idealmente con 4 o más núcleos) y regenera el informe y la página para entregar tus propios tiempos.

## Publicar en GitHub Pages

1. Crea un repositorio **Public** (por ejemplo `Tareas-Paralelas`).
2. **Add file → Upload files**, arrastra **todo el contenido** de esta carpeta (incluida `.github`) y **Commit changes**.
3. **Settings → Pages**: *Deploy from a branch*, rama `main`, carpeta `/ (root)`, guardar.
4. En uno o dos minutos queda en `https://TU-USUARIO.github.io/Tareas-Paralelas/`.

Con Git:

```
git init
git add .
git commit -m "Practica 6 tareas paralelas"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/Tareas-Paralelas.git
git push -u origin main
```

## Ejecutar Python en GitHub (Actions)

Cada `push` lanza la pestaña **Actions**, que corre todos los scripts y guarda CSV, gráficas, PDF e `index.html` como artefacto (*resultados-paralelo*). Los ejecutores de GitHub suelen tener varios núcleos, así que ahí puedes ver el paralelismo funcionando; descarga el artefacto, copia los archivos al repositorio y súbelos para actualizar la página y el informe.

## Idea principal

La descomposición por datos reparte la lista en segmentos independientes que se suman a la vez y luego se combinan. Solo conviene si cada tarea tiene suficiente cálculo para compensar crear los procesos y enviar los datos, y si hay núcleos disponibles.
