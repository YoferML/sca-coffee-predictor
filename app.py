# -*- coding: utf-8 -*-
"""
☕ Estimador SCA — Streamlit
Calculadora oficial SCA (reglas, con las 5 tazas) + estimador ML entrenado con datos CQI.
Ejecutar:  streamlit run app.py
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

RUTA_MODELO = Path(__file__).parent / "modelo_sca_v3.pkl"
N_TAZAS = 5

# ----------------------------------------------------------- CONSTANTES SCA
# Atributos puntuados UNA vez por muestra (6.00-10.00, pasos de 0.25)
ATRIB_ESCALA = {
    "Aroma": "Fragancia/Aroma", "Flavor": "Sabor", "Aftertaste": "Postgusto",
    "Acidity": "Acidez", "Body": "Cuerpo", "Balance": "Balance",
    "Cupper.Points": "General (catador)",
}
# Atributos evaluados TAZA POR TAZA: 2 puntos por cada taza uniforme / limpia / dulce
ATRIB_TAZAS = {
    "Uniformity": "Tazas uniformes", "Clean.Cup": "Tazas limpias", "Sweetness": "Tazas dulces",
}
NOTAS_POSITIVAS = ["Chocolate", "Caramelo", "Panela", "Miel", "Nueces", "Naranja",
                   "Limon", "Frutos_Rojos", "Durazno", "Jazmin", "Floral", "Especias"]


PAISES_ES = {
    "Mexico": "México", "Colombia": "Colombia", "Guatemala": "Guatemala", "Brazil": "Brasil",
    "Taiwan": "Taiwán", "United States (Hawaii)": "EE. UU. (Hawái)", "Honduras": "Honduras",
    "Costa Rica": "Costa Rica", "Ethiopia": "Etiopía", "Tanzania, United Republic Of": "Tanzania",
    "Thailand": "Tailandia", "Uganda": "Uganda", "Peru": "Perú", "Otro": "Otro país",
}


def opciones_pais(paises_modelo):
    """Lista en español con Perú siempre primero; devuelve (etiquetas, {etiqueta: valor del modelo})."""
    mapa = {PAISES_ES.get(p, p): p for p in paises_modelo}
    # El CSV tiene solo 10 lotes de Perú: si el modelo no lo trae como categoría, usa "Otro"
    mapa["Perú"] = "Peru" if "Peru" in paises_modelo else "Otro"
    etiquetas = ["Perú"] + sorted(e for e in mapa if e != "Perú")
    return etiquetas, mapa


def indice(opciones, preferido):
    """Posición de `preferido` en la lista (0 si no está)."""
    return opciones.index(preferido) if preferido in opciones else 0


# ------------------------------------------------------------- LÓGICA (sin UI)
def calcular_puntaje_sca(ficha, tazas_defecto, peso_defecto):
    """Suma de los 10 atributos − Σ(tazas afectadas × peso del defecto).
    ficha ya trae los 10 atributos en puntos (los 3 de tazas = 2 × nº de tazas)."""
    suma = sum(float(ficha[a]) for a in list(ATRIB_ESCALA) + list(ATRIB_TAZAS))
    descuento = sum(peso_defecto[d] * t for d, t in (tazas_defecto or {}).items())
    return suma - descuento


def clasificar_sca(puntaje, tazas_defecto=None):
    if tazas_defecto and any(t > 0 for t in tazas_defecto.values()):
        return "🔴 No califica como especialidad: hay taints/faults en taza", "error"
    if puntaje < 80:
        return "🔴 Por debajo de especialidad (< 80.00)", "error"
    if puntaje < 85:
        return "🟡 Muy Bueno (80.00 - 84.99)", "warning"
    if puntaje < 90:
        return "🟢 Excelente (85.00 - 89.99)", "success"
    return "🏆 Sobresaliente (90.00+)", "success"


def fila_modelo(art, altitud, humedad, proceso, variedad, pais, def1, def2):
    fila = {"altitud": altitud, "humedad": humedad, "def_cat1": def1, "def_cat2": def2,
            "quakers": 0, "anio": np.nan,
            "proceso": proceso, "variedad": variedad, "pais": pais}
    return pd.DataFrame([fila])[art["features_num"] + art["features_cat"]]


# ----------------------------------------------------------------- CARGA
@st.cache_resource
def cargar_artefacto():
    art = joblib.load(RUTA_MODELO)
    cats = art["modelo"].named_steps["pre"].named_transformers_["cat"].categories_
    art["categorias"] = {n: list(c) for n, c in zip(art["features_cat"], cats)}
    return art


# ------------------------------------------------------------ PESTAÑA: CATA
def pestana_evaluar(art):
    modelo, umbral = art["modelo"], art["umbral_revision"]
    peso_defecto = art["peso_defecto"]
    hum_min, hum_max = art["humedad_rango"]
    cats = art["categorias"]

    with st.form("ficha"):
        st.subheader("1. Origen y grano verde")
        c1, c2, c3 = st.columns(3)
        altitud = c1.slider("Altitud (msnm)", 300, 3000, 1600, 50)
        humedad = c2.slider("Humedad (%)", 5.0, 20.0, 11.0, 0.1)
        proceso = c3.selectbox("Proceso", cats["proceso"], index=indice(cats["proceso"], "Lavado"))
        c4, c5, c6, c7 = st.columns(4)
        variedad = c4.selectbox("Variedad", cats["variedad"], index=indice(cats["variedad"], "Caturra"))
        etiquetas_pais, mapa_pais = opciones_pais(cats["pais"])
        pais_sel = c5.selectbox("País", etiquetas_pais)
        pais = mapa_pais[pais_sel]
        def1 = c6.number_input("Defectos categoría 1", 0, 30, 0)
        def2 = c7.number_input("Defectos categoría 2", 0, 60, 0)

        st.subheader(f"2. Atributos de la muestra (una puntuación por muestra)")
        st.caption("Escala 6.00–10.00 en pasos de 0.25.")
        ficha = {}
        cols = st.columns(2)
        for i, (k, etq) in enumerate(ATRIB_ESCALA.items()):
            ficha[k] = cols[i % 2].slider(etq, 6.0, 10.0, 7.75, 0.25)

        st.subheader(f"3. Evaluación taza por taza ({N_TAZAS} tazas)")
        st.caption("Cuenta cuántas de las 5 tazas fueron uniformes, limpias y dulces. Cada taza vale 2 puntos.")
        cc = st.columns(3)
        tazas_ok = {k: cc[i].slider(etq + f" (de {N_TAZAS})", 0, N_TAZAS, N_TAZAS)
                    for i, (k, etq) in enumerate(ATRIB_TAZAS.items())}

        st.subheader("4. Defectos de taza y notas")
        st.caption("Nº de tazas (de 5) con cada defecto; 0 = ausente. Taint = 2 pts por taza, fault = 4.")
        dcols = st.columns(len(peso_defecto))
        tazas_def = {d: dcols[i].number_input(d.replace("_", " "), 0, N_TAZAS, 0)
                     for i, d in enumerate(peso_defecto)}
        notas = st.multiselect("Notas positivas (descriptivas, no suman puntos)", NOTAS_POSITIVAS)

        enviar = st.form_submit_button("Calcular puntaje SCA", type="primary")

    if not enviar:
        return

    defectos = {d: t for d, t in tazas_def.items() if t > 0}
    # Una taza con defecto no puede contarse como limpia
    max_def = max(defectos.values(), default=0)
    limpias = min(tazas_ok["Clean.Cup"], N_TAZAS - max_def)
    ajuste_limpia = limpias < tazas_ok["Clean.Cup"]
    tazas_ok["Clean.Cup"] = limpias
    for k, n in tazas_ok.items():
        ficha[k] = 2 * n

    puntaje = calcular_puntaje_sca(ficha, defectos, peso_defecto)
    categoria, nivel = clasificar_sca(puntaje, defectos)
    esperado = float(modelo.predict(
        fila_modelo(art, altitud, humedad, proceso, variedad, pais, def1, def2))[0])
    diferencia = puntaje - esperado
    descuento = sum(peso_defecto[d] * t for d, t in defectos.items())

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Puntaje SCA final (5 tazas)", f"{puntaje:.2f}")
    m2.metric("Esperado por ML (origen + defectos verdes)", f"{esperado:.2f}")
    m3.metric("Diferencia", f"{diferencia:+.2f}")
    getattr(st, nivel)(categoria)

    st.markdown("**Desglose del puntaje**")
    filas = [{"Concepto": etq, "Detalle": "una puntuación por muestra", "Puntos": ficha[k]}
             for k, etq in ATRIB_ESCALA.items()]
    filas += [{"Concepto": etq, "Detalle": f"{tazas_ok[k]} de {N_TAZAS} tazas × 2", "Puntos": ficha[k]}
              for k, etq in ATRIB_TAZAS.items()]
    filas.append({"Concepto": "Defectos de taza", "Detalle": "tazas × peso del defecto",
                  "Puntos": -float(descuento)})
    filas.append({"Concepto": "TOTAL", "Detalle": "", "Puntos": puntaje})
    st.dataframe(pd.DataFrame(filas), hide_index=True, use_container_width=True,
                 height=(len(filas) + 1) * 35 + 3)

    if pais_sel == "Perú" and pais != "Peru":
        st.info("🇵🇪 El dataset CQI tiene solo 10 lotes de Perú, así que el estimado ML usa un perfil "
                "general (\"otro país\"). La fórmula SCA del puntaje final es exacta para cualquier origen.")
    if ajuste_limpia:
        st.info("ℹ️ Las tazas limpias se ajustaron: una taza con defecto no puede contarse como limpia.")
    if abs(diferencia) > umbral:
        st.warning(f"🔎 La ficha se aleja más de ±{umbral:.1f} puntos de lo esperado: "
                   "conviene recatar o revisar la ficha.")
    if defectos:
        st.error("🚨 Defectos de taza: " + ", ".join(f"{d} ({t} tazas)" for d, t in defectos.items())
                 + f" → −{descuento} pts")
    if notas:
        st.write("📝 Notas: " + ", ".join(notas))
    if not (hum_min <= humedad <= hum_max):
        st.warning(f"⚠️ Humedad fuera de {hum_min}–{hum_max}% (riesgo en grano verde).")


# ------------------------------------------------------- PESTAÑA: PROTOCOLO
def pestana_protocolo():
    st.subheader("📖 Protocolo de cata (receta de preparación)")
    st.caption("Valores habituales del protocolo de cata SCA. Verifícalos con el manual vigente "
               "de la SCA antes de usarlos en una evaluación oficial.")
    st.markdown(
        f"""
| Paso | Indicación |
|---|---|
| **Muestras** | **{N_TAZAS} tazas** del mismo lote, tostadas y molidas por separado |
| **Tueste** | Medio-claro, reposado entre 8 y 24 h antes de catar |
| **Dosis** | 8.25 g de café por cada 150 ml de agua (≈ 55 g/L) |
| **Molienda** | Media (≈ 70–75 % pasa por malla 20), justo antes de catar |
| **Agua** | Limpia, sin sabor, a ≈ 93 °C (92–94 °C) |
| **Infusión** | Verter sobre el café molido, cubrir y dejar reposar 3–5 min |
| **Romper la costra** | A los 4 min, con 3 movimientos de cuchara; retirar la espuma |
| **Evaluación** | Fragancia (seco) → aroma (costra) → cata del líquido desde ≈ 70 °C hasta que enfríe |
"""
    )
    st.markdown("**Calculadora de dosis**")
    a, b = st.columns(2)
    n = a.number_input("Número de tazas", 1, 10, N_TAZAS)
    ml = b.number_input("Agua por taza (ml)", 100, 300, 150, 10)
    g_taza = 8.25 * ml / 150
    c1, c2, c3 = st.columns(3)
    c1.metric("Café por taza", f"{g_taza:.2f} g")
    c2.metric("Café total", f"{g_taza * n:.2f} g")
    c3.metric("Agua total", f"{ml * n} ml")
    st.caption("Prepara un poco más de agua que el total para compensar la que absorbe el café.")


def pestana_ayuda():
    st.subheader("¿Cómo se calcula?")
    st.markdown(
        "- **Puntaje final** = fragancia + sabor + postgusto + acidez + cuerpo + balance + general "
        "+ 2×(tazas uniformes + limpias + dulces) − defectos.\n"
        "- **Defectos:** tazas afectadas × 2 (taint) o × 4 (fault). Con cualquier defecto, la muestra "
        "no califica como especialidad aunque el número sea ≥ 80.\n"
        "- **Esperado ML:** estimación a partir de origen y defectos de grano verde (datos reales CQI). "
        "Explica solo una parte del puntaje: sirve como referencia para detectar fichas raras, "
        "no como veredicto.")


# -------------------------------------------------------------------- MAIN
def main():
    st.set_page_config(page_title="Estimador SCA", page_icon="☕", layout="wide")
    st.title("☕ Estimador de puntaje SCA")
    st.caption("Puntaje oficial por fórmula SCA (5 tazas) + estimación ML con datos reales CQI.")

    if not RUTA_MODELO.exists():
        st.error(f"No encuentro `{RUTA_MODELO.name}`. Colócalo junto a app.py.")
        st.stop()
    art = cargar_artefacto()

    t1, t2, t3 = st.tabs(["☕ Evaluar muestra", "📖 Protocolo de cata", "ℹ️ Cómo se calcula"])
    with t1:
        pestana_evaluar(art)
    with t2:
        pestana_protocolo()
    with t3:
        pestana_ayuda()


main()
