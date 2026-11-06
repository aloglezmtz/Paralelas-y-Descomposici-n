import json, statistics as st
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, Preformatted, KeepTogether)

R = json.load(open("resultados.json"))
NAVY, LIGHT, SAND = colors.HexColor("#1f3a5f"), colors.HexColor("#e6ecf8"), colors.HexColor("#fdebd0")
W = letter[0] - 4*cm

body = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.2, leading=14, alignment=TA_JUSTIFY, spaceAfter=6)
small = ParagraphStyle("s", parent=body, fontSize=7.8, leading=10, alignment=0, spaceAfter=0)
cap = ParagraphStyle("c", parent=body, fontName="Helvetica", fontSize=8, textColor=colors.HexColor("#555555"), alignment=TA_CENTER)
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15, textColor=colors.white, leading=19)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.5, textColor=colors.HexColor("#2f6fd0"), spaceBefore=8, spaceAfter=5)
cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.6, leading=11)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")
code = ParagraphStyle("code", fontName="Courier", fontSize=6.9, leading=8.4)

def H1(t):
    tb = Table([[Paragraph(t, h1)]], colWidths=[W], style=[("BACKGROUND", (0,0), (-1,-1), NAVY),
         ("LEFTPADDING", (0,0), (-1,-1), 12), ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8)])
    return [Spacer(1, 6), tb, Spacer(1, 8)]

def tabla(data, widths, bold_last=False):
    t = Table(data, colWidths=widths, repeatRows=1)
    st_ = [("BACKGROUND", (0,0), (-1,0), NAVY), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
           ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("FONTSIZE", (0,0), (-1,-1), 8.6),
           ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]), ("LINEBELOW", (0,0), (-1,0), 1.5, colors.HexColor("#e08e0b")),
           ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4), ("FONTNAME", (0,1), (-1,-1), "Helvetica")]
    if bold_last:
        st_ += [("BACKGROUND", (0,-1), (-1,-1), colors.HexColor("#cfdcf4")), ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold")]
    t.setStyle(TableStyle(st_)); return t

def img(path, w):
    from PIL import Image as PI
    iw, ih = PI.open(path).size
    return Image(path, width=w, height=w*ih/iw)

def ms(x): return f"{x*1000:.2f}"
cores = R["cpu"]
cor = R["corridas"]
seq_m, par_m = st.mean(c["seq"] for c in cor), st.mean(c["par"] for c in cor)
acel_m = st.mean(c["seq"]/c["par"] for c in cor)
ref_seq, ref_par = R["referencia"]["seq"], R["referencia"]["par"]   # corrida de referencia (salida.txt, semilla 2025)
mas_rapida = "secuencial" if seq_m < par_m else "paralela"

# ---------- encabezado / pie ----------
def deco(c, d):
    c.saveState()
    if d.page > 1:
        c.setFont("Helvetica", 8); c.setFillColor(colors.HexColor("#666666"))
        c.drawString(2*cm, letter[1]-1.3*cm, "Práctica 6 · Tareas paralelas y descomposición")
        c.drawRightString(letter[0]-2*cm, letter[1]-1.3*cm, "Programación paralela y concurrente")
        c.line(2*cm, letter[1]-1.5*cm, letter[0]-2*cm, letter[1]-1.5*cm)
        c.drawString(2*cm, 1.2*cm, "Gonzalez Martinez Alondra Goretti · 218534681")
        c.setFillColor(NAVY); c.roundRect(letter[0]-3*cm, 1.0*cm, 1*cm, 0.55*cm, 4, fill=1, stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 8); c.drawCentredString(letter[0]-2.5*cm, 1.2*cm, str(d.page))
    c.restoreState()

doc = BaseDocTemplate("Practica6_Paralelismo_Informe.pdf", pagesize=letter, leftMargin=2*cm, rightMargin=2*cm,
                      topMargin=2*cm, bottomMargin=1.9*cm, title="Práctica 6 · Tareas paralelas y descomposición",
                      author="Gonzalez Martinez Alondra Goretti")
doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(2*cm, 1.9*cm, W, letter[1]-3.9*cm, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=deco)])
S = []

# ---------- portada ----------
S += [Paragraph("<b>UNIVERSIDAD DE GUADALAJARA</b>", ParagraphStyle("u", fontName="Times-Bold", fontSize=24, alignment=TA_CENTER, leading=28)),
      Table([[""]], colWidths=[W], rowHeights=[4], style=[("BACKGROUND", (0,0), (-1,-1), colors.black)]), Spacer(1, 4),
      Paragraph("<b>CENTRO UNIVERSITARIO DE CIENCIAS EXACTAS E INGENIERÍAS</b>", ParagraphStyle("x", parent=body, alignment=TA_CENTER, fontSize=9.5, spaceAfter=0)),
      Paragraph("Departamento de Innovación Basada en la Información y el Conocimiento", ParagraphStyle("x2", parent=body, alignment=TA_CENTER, fontSize=10.5)),
      Spacer(1, 70), Paragraph("Ingeniería En Computación", ParagraphStyle("x3", parent=body, alignment=TA_CENTER, fontSize=12)), Spacer(1, 4)]
tit = Table([[Paragraph("<b>PRÁCTICA 6</b>", ParagraphStyle("t1", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white, alignment=TA_CENTER))],
             [Paragraph("Tareas Paralelas y Descomposición", ParagraphStyle("t2", fontName="Helvetica-Bold", fontSize=22, textColor=colors.white, alignment=TA_CENTER, leading=27))],
             [Paragraph("Comparación de rendimiento entre suma secuencial y multiprocessing.Pool(4)", ParagraphStyle("t3", fontName="Helvetica", fontSize=9.5, textColor=colors.HexColor("#c9d4ea"), alignment=TA_CENTER))]],
            colWidths=[W], style=[("BACKGROUND", (0,0), (-1,-1), NAVY), ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7)])
S.append(tit)
P = lambda a, b: Paragraph(f"<b>{a}</b>: {b}", ParagraphStyle("q", fontName="Times-Roman", fontSize=10, leading=13))
info = Table([[P("Nombre", "GONZALEZ MARTINEZ ALONDRA GORETTI"), P("Código", "218534681")],
              [P("Materia", "Programación paralela y concurrente"), P("Grupo", "____________")],
              [P("Nombre del profesor", "Mtro. Zeus Cobián"), P("Actividad", "Práctica 6 (100 puntos)")],
              [P("Fecha de entrega", "13 de noviembre del 2026"), P("Lenguaje", "Python 3.12 · multiprocessing")]],
             colWidths=[W*0.62, W*0.38], style=[("BACKGROUND", (0,0), (-1,-1), LIGHT), ("BOX", (0,0), (-1,-1), 1, colors.black), ("INNERGRID", (0,0), (-1,-1), 1, colors.black),
                                               ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6)])
S.append(info)
bib = Table([[Paragraph("<b>Bibliografía:</b><br/>Python Software Foundation. (s. f.). <i>multiprocessing — Process-based parallelism</i>. Python 3 Documentation.<br/>"
                        "Python Software Foundation. (s. f.). <i>concurrent.futures — Launching parallel tasks</i>. Python 3 Documentation.<br/>"
                        "Mattson, T., Sanders, B. y Massingill, B. (2004). <i>Patterns for Parallel Programming</i>. Addison-Wesley.<br/>"
                        "Recursos didácticos de la asignatura (Semana 9 – Tareas paralelas y descomposición de problemas).", small)]],
            colWidths=[W], style=[("BACKGROUND", (0,0), (-1,-1), SAND), ("BOX", (0,0), (-1,-1), 1, colors.black), ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5)])
S += [bib, PageBreak()]

# ---------- 1 objetivo, 2 fundamento ----------
S += H1("1. Objetivo de la práctica")
S.append(Paragraph("Implementar la descomposición de un problema en tareas paralelas: sumar una lista de 100,000 números aleatorios entre 1 y 100 dividiéndola en 4 segmentos iguales que se procesan con el módulo <font face='Courier'>multiprocessing</font>, y comparar su tiempo con el de una versión secuencial para analizar cuándo el paralelismo mejora el rendimiento.", body))
S += H1("2. Fundamento breve")
S.append(Paragraph("La <b>descomposición de problemas</b> consiste en dividir un problema complejo en subtareas lo más independientes posible, de modo que puedan ejecutarse simultáneamente. Puede hacerse por <b>datos</b> (<i>data parallelism</i>: el mismo cálculo sobre distintos fragmentos) o por <b>funciones</b> (<i>task parallelism</i>: cálculos distintos a la vez). La suma de una lista es un caso clásico de descomposición por datos: cada segmento se suma sin necesitar a los demás y al final se combinan los resultados parciales (esquema <i>dividir – procesar – combinar</i>).", body))
S.append(Paragraph("En Python, los hilos comparten el GIL (<i>Global Interpreter Lock</i>), así que el cálculo intensivo de CPU solo se acelera con <b>procesos</b>, cada uno con su propio intérprete. A cambio, crear procesos y enviarles los datos (serialización con <i>pickle</i>) tiene un costo. Por eso el beneficio depende de que el trabajo por tarea sea suficientemente grande frente a esa sobrecarga y de que existan núcleos físicos disponibles (Python Software Foundation, s. f.).", body))
S.append(img("fig_descomp.png", W*0.82)); S.append(Paragraph("<b>Figura 1.</b> Descomposición de datos del problema. <i>Fuente: elaboración propia.</i>", cap))
S.append(Paragraph("<b>Metodología de medición</b>", h2))
for t in ["Lista de 100,000 enteros con <font face='Courier'>random.Random(semilla).randint(1, 100)</font>; la misma lista se usa en ambas versiones y se verifica que las dos sumas coincidan.",
          "Se mide con <font face='Courier'>time.perf_counter()</font> solo el cálculo: en la versión paralela se incluye dividir la lista, crear el <font face='Courier'>Pool(4)</font>, enviar los segmentos y sumar los parciales.",
          f"Corrida de referencia con semilla 2025, 10 corridas con listas distintas y dos experimentos adicionales (tamaño de la lista y carga por elemento).",
          f"Entorno de prueba: Python {R['python']}, {R['so']}, <b>{cores} núcleo(s) lógico(s) disponible(s)</b>. Los tiempos absolutos dependen del equipo; la conclusión sobre núcleos disponibles es la clave para interpretarlos."]:
    S.append(Paragraph("• " + t, ParagraphStyle("bl", parent=body, leftIndent=12, firstLineIndent=-8, spaceAfter=3)))

# ---------- 3 código ----------
S.append(PageBreak()); S += H1("3. Código de la práctica")
S.append(Paragraph("3.1 Programa completo (sumas.py)", h2))
src = open("sumas.py").read().rstrip().split("\n")
numbered = "\n".join(f"{i+1:>3}  {l}" for i, l in enumerate(src))
code.backColor = colors.HexColor('#f4f6fb'); code.borderColor = colors.HexColor('#b8c4de'); code.borderWidth = .6; code.borderPadding = 6
ct = Preformatted(numbered, code)
S.append(ct)
S.append(Paragraph("Los scripts <font face='Courier'>experimento.py</font> y <font face='Courier'>generar_informe.py</font> (incluidos en la entrega) repiten las mediciones y generan las tablas y gráficas de la sección 4. Todo se ejecuta con <font face='Courier'>python sumas.py</font>, <font face='Courier'>python experimento.py</font> y <font face='Courier'>python generar_informe.py</font>.", ParagraphStyle("n", parent=body, spaceBefore=6)))

# ---------- 4 resultados ----------
S.append(PageBreak()); S += H1("4. Resultados")
S.append(Paragraph("4.1 Captura de la ejecución", h2))
S.append(Paragraph("Salida real del programa con la semilla 2025:", body))
S.append(img("captura.png", W*0.88)); S.append(Paragraph("<b>Figura 2.</b> Ejecución de la versión secuencial y de la paralela. <i>Fuente: elaboración propia.</i>", cap))
S.append(Paragraph("4.2 Comparación", h2))
S.append(Paragraph("<b>Tabla 1.</b> Tabla de comparación de la corrida de referencia (semilla 2025, 100,000 elementos).", body))
S.append(tabla([["Versión", "Tiempo de ejecución (s)", "Tiempo (ms)", "Aceleración"],
                ["Secuencial", f"{ref_seq:.6f}", ms(ref_seq), "1.00×"],
                ["Paralelo (4 procesos)", f"{ref_par:.6f}", ms(ref_par), f"{ref_seq/ref_par:.2f}×"]],
               [W*0.34, W*0.26, W*0.2, W*0.2]))
S.append(PageBreak())
S.append(Paragraph("<b>Tabla 2.</b> Diez corridas con listas aleatorias distintas (100,000 elementos).", body))
rows = [["Corrida", "Secuencial (ms)", "Paralelo 4 procesos (ms)", "Aceleración"]]
for c in cor: rows.append([str(c["n"]), ms(c["seq"]), ms(c["par"]), f"{c['seq']/c['par']:.2f}×"])
rows.append(["Promedio", ms(seq_m), ms(par_m), f"{acel_m:.2f}×"])
S.append(tabla(rows, [W*0.16, W*0.28, W*0.32, W*0.24], bold_last=True))
S.append(Spacer(1, 6)); S.append(img("fig_corridas.png", W*0.78))
S.append(Paragraph("<b>Figura 3.</b> Tiempo de cada versión en las 10 corridas. <i>Fuente: elaboración propia.</i>", cap))

S.append(Paragraph("4.3 Efecto del tamaño de la lista y del costo de crear los procesos", h2))
S.append(Paragraph("<b>Tabla 3.</b> Mediana de varias repeticiones según el número de elementos. «Pool ya creado» excluye el costo de arrancar los procesos.", body))
rows = [["Elementos", "Secuencial (ms)", "Paralelo creando pool (ms)", "Paralelo pool ya creado (ms)", "Acel. (con pool)"]]
for d in R["tamanos"]: rows.append([f"{d['n']:,}", ms(d["seq"]), ms(d["par_con_pool"]), ms(d["par_pool_listo"]), f"{d['seq']/d['par_con_pool']:.2f}×"])
S.append(tabla(rows, [W*0.16, W*0.19, W*0.25, W*0.24, W*0.16]))
S.append(Spacer(1, 6)); S.append(img("fig_tamanos.png", W*0.78))
S.append(Paragraph("<b>Figura 4.</b> Escalamiento con el tamaño (ejes logarítmicos). <i>Fuente: elaboración propia.</i>", cap))

pes = R["pesada"]
S.append(Paragraph("4.4 Carga con más cálculo por elemento", h2))
S.append(Paragraph("Para comprobar el efecto de la granularidad se repitió la comparación con 100,000 elementos, pero cada uno requiere 100 operaciones en lugar de una (<font face='Courier'>tarea_pesada</font> en <font face='Courier'>experimento.py</font>).", body))
S.append(Paragraph("<b>Tabla 4.</b> Mediana de 3 repeticiones con carga pesada por elemento.", body))
S.append(tabla([["Versión", "Tiempo (s)", "Aceleración"], ["Secuencial", f"{pes['seq']:.3f}", "1.00×"],
                ["Paralelo (4 procesos)", f"{pes['par']:.3f}", f"{pes['seq']/pes['par']:.2f}×"]], [W*0.4, W*0.3, W*0.3]))
S.append(Paragraph("<i>Nota:</i> los tiempos varían de una ejecución a otra y entre equipos. Este informe se midió en un equipo con " + f"{cores} núcleo(s) lógico(s); en una computadora con 4 o más núcleos la versión paralela con carga pesada debería acercarse a una aceleración mayor que 1× (ver la sección 5).", ParagraphStyle("nt", parent=body, spaceBefore=8)))

# ---------- 5 reflexión ----------
S += H1("5. Reflexión final")
if acel_m < 1:
    q1 = (f"En esta medición la versión <b>secuencial fue más rápida</b>: {ms(seq_m)} ms frente a {ms(par_m)} ms en promedio ({1/acel_m:.1f} veces más lenta la paralela). "
          "No es una falla de la descomposición, sino de su costo: sumar 100,000 enteros toma apenas 1–2 ms, mientras que crear 4 procesos, serializar los segmentos con <i>pickle</i>, enviarlos y recolectar los resultados cuesta decenas de milisegundos. "
          f"Además, el equipo de prueba solo ofrece {cores} núcleo(s), de modo que los 4 procesos se turnan en el mismo núcleo y no hay ejecución simultánea real. ")
else:
    q1 = (f"La versión paralela fue {acel_m:.2f} veces más rápida en promedio ({ms(par_m)} ms contra {ms(seq_m)} ms), porque los 4 procesos sumaron sus segmentos al mismo tiempo en núcleos distintos. ")
S.append(Paragraph("<b>¿Por qué el resultado se ve así y qué dice sobre la descomposición?</b> " + q1 +
    "La Tabla 3 muestra que al crecer la lista la brecha se reduce (el trabajo útil crece y el costo fijo de los procesos se vuelve relativo), y que sin el costo de crear el pool la versión paralela mejora notablemente. La Tabla 4 confirma el principio de <i>granularidad</i>: la paralelización solo conviene cuando cada tarea realiza suficiente cálculo.", body))
S.append(Paragraph("<b>¿Cuándo conviene esta técnica en programas reales?</b> Cuando el problema se puede partir en subtareas independientes con mucho cálculo por tarea y hay núcleos disponibles: procesamiento de imágenes o video por bloques, simulaciones (Monte Carlo), entrenamiento y evaluación de modelos con validación cruzada, análisis de grandes archivos de datos por fragmentos y cálculo científico con matrices. Para esperas de red o disco es más apropiada la asincronía (Práctica 5); para cálculo intensivo de CPU, los procesos; y para tareas muy pequeñas, la versión secuencial.", body))
S.append(Paragraph("<b>Limitaciones.</b> La ganancia máxima está acotada por la fracción secuencial del programa (ley de Amdahl): aquí dividir, enviar y combinar son partes no paralelizables. Con <i>p</i> núcleos reales la aceleración ideal es menor que <i>p</i>, nunca mayor.", body))

# ---------- 6 conclusión ----------
S += H1("6. Conclusión")
if acel_m < 1:
    c1 = (f"Se implementó la descomposición por datos de la suma de 100,000 enteros en 4 segmentos con <font face='Courier'>multiprocessing.Pool(4)</font>; ambas versiones obtuvieron el mismo resultado (5,054,170 con la semilla 2025). "
          f"En el equipo de prueba ({cores} núcleo) la versión <b>{mas_rapida}</b> fue la más rápida: {ref_seq*1000:.2f} ms frente a {ref_par*1000:.2f} ms en la corrida de referencia y {ms(seq_m)} ms frente a {ms(par_m)} ms en promedio de 10 corridas. ")
else:
    c1 = (f"Se implementó la descomposición por datos de la suma de 100,000 enteros en 4 segmentos con <font face='Courier'>multiprocessing.Pool(4)</font>; ambas versiones obtuvieron el mismo resultado. La versión <b>paralela</b> fue más rápida ({ms(par_m)} ms frente a {ms(seq_m)} ms en promedio). ")
S.append(Paragraph(c1 + "La práctica muestra que paralelizar no siempre es más rápido: el beneficio depende de que cada tarea tenga trabajo suficiente para compensar la creación de procesos y la transferencia de datos, y de contar con núcleos físicos disponibles. La descomposición correcta (segmentos independientes, mismo tamaño y combinación final de parciales) es necesaria, pero no suficiente.", body))

S += H1("Referencias")
refs = ["Python Software Foundation. (s. f.). <i>multiprocessing — Process-based parallelism</i>. Python 3 Documentation. https://docs.python.org/3/library/multiprocessing.html",
        "Python Software Foundation. (s. f.). <i>concurrent.futures — Launching parallel tasks</i>. Python 3 Documentation. https://docs.python.org/3/library/concurrent.futures.html",
        "Mattson, T. G., Sanders, B. A. y Massingill, B. L. (2004). <i>Patterns for Parallel Programming</i>. Addison-Wesley.",
        "Gutiérrez Cobián, Z. E. (2026). <i>Semana 9 – Tareas paralelas y descomposición de problemas</i> [Presentación]. CUCEI, Universidad de Guadalajara."]
for r in refs: S.append(Paragraph(r, ParagraphStyle("r", parent=body, leftIndent=14, firstLineIndent=-14, alignment=0)))

doc.build(S)
