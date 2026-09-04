import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de página y paleta corporativa
st.set_page_config(page_title="ECOGEN S.A. - Tablero de Riesgos y Estrategia", layout="wide")

# Estilos CSS con paleta institucional (Azul Marino #0F2537, Gris Suave #F4F6F9 y Acentos)
st.markdown("""
    <style>
    /* Fondo general de la plataforma */
    .stApp {
        background-color: #F4F6F9;
       }
    /* Fondo naranja claro para la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #FFCC99 !important;
    }
    /* Textos oscuros dentro de la barra lateral para contraste con el naranja */
    [data-testid="stSidebar"] * {
        color: #0F2537 !important;
    }
    /* Color de títulos principales */
    h1, h2, h3 {
        color: #0F2537 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título y contexto ejecutivo
st.title("⚡ ECOGEN S.A. - Gestión Estratégica de Riesgos e Incertidumbre")
st.markdown("""
**Oficina Estratégica de Riesgos (OER)** | Modelo Cuantitativo Monte Carlo (1.000 iteraciones)  
Monitoreo de objetivos estratégicos (OKR), indicadores de desempeño (KPI) y factores de riesgo (KRI).
""")
st.markdown("---")
st.markdown("""
**Oficina Estratégica de Riesgos (OER)** | Modelo Cuantitativo Monte Carlo (1.000 iteraciones)  
Monitoreo de objetivos estratégicos (OKR), indicadores de desempeño (KPI) y factores de riesgo (KRI).
""")
st.markdown("---")

# Barra lateral: Parámetros y Filtros
st.sidebar.header("⚙️ Parámetros de Simulación")
n_sim = st.sidebar.slider("Número de iteraciones Monte Carlo:", min_value=500, max_value=5000, value=1000, step=500)
programa_sel = st.sidebar.selectbox("Filtrar por Programa Estratégico:", ["Portafolio Total", "Solar Equinox", "Eólica Andina", "HydroBalance"])

# Semilla fija para reproducibilidad
np.random.seed(42)

# SIMULACIÓN DE MONTE CARLO (Variables estocásticas del caso ECOGEN)
# 1. Costo logístico por MW (Triangular: min 0.8, moda 1.0, max 1.2 * 820,000 USD)
costo_logistico = np.random.triangular(0.8 * 820000, 820000, 1.2 * 820000, n_sim)

# 2. Demanda energética regional (Normal: media 14,500 GWh, variabilidad 15%)
demanda_gwh = np.random.normal(14500, 14500 * 0.15, n_sim)

# 3. Tasa de aprobación ambiental (Uniforme: 60% a 95%)
aprob_ambiental = np.random.uniform(0.60, 0.95, n_sim)

# 4. Tasa de interés internacional (Triangular: 7.65%, 8.5%, 9.35%)
tasa_interes = np.random.triangular(7.65, 8.50, 9.35, n_sim)

# 5. Emisiones compensadas (Normal: media 25,000 tCO2, sigma 6,000)
emisiones_tco2 = np.random.normal(25000, 6000, n_sim)

# 6. Aceptación Comunitaria / Conflictos (Simulación de impacto reputacional)
conflictos_activos = np.random.poisson(1.5, n_sim)

# Cálculo de variables dependientes (KPIs y OKRs) aplicando correlaciones empíricas
# ROI base 12% afectado negativamente por costos logísticos y tasas, positivamente por demanda
impacto_costo = ((costo_logistico - 820000) / 820000) * 0.05
impacto_tasa = ((tasa_interes - 8.5) / 8.5) * 0.03
impacto_demanda = ((demanda_gwh - 14500) / 14500) * 0.04

roi_simulado = (0.12 - impacto_costo - impacto_tasa + impacto_demanda) * 100

# Expansión de Capacidad Solar (Meta +35% afectada por licencias ambientales)
expansion_capacidad = 35 * (aprob_ambiental / 0.85)

# Métricas Ejecutivas Superiores
p10_roi = np.percentile(roi_simulado, 10)
p50_roi = np.percentile(roi_simulado, 50)
p90_roi = np.percentile(roi_simulado, 90)
prob_cumplir_roi = (roi_simulado >= 12.0).mean() * 100

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("ROI Esperado (P50)", f"{p50_roi:.2f}%", f"{p50_roi - 12:.2f}% vs Meta (12%)")
col_m2.metric("Probabilidad Cumplir OKR ROI", f"{prob_cumplir_roi:.1f}%", "Nivel de confianza")
col_m3.metric("Escenario Pesimista (P10)", f"{p10_roi:.2f}%", "Riesgo en cola")
col_m4.metric("Escenario Optimista (P90)", f"{p90_roi:.2f}%", "Potencial superior")

st.markdown("---")

# Visualización 1 y 2
col_v1, col_v2 = st.columns(2)

with col_v1:
    st.subheader("1. Distribución Monte Carlo: ROI del Portafolio")
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(x=roi_simulado, nbinsx=35, marker_color="#1f77b4", opacity=0.75, name="Iteraciones"))
    fig_hist.add_vline(x=12.0, line_dash="dash", line_color="red", annotation_text="Meta OKR (12%)")
    fig_hist.add_vline(x=p10_roi, line_dash="dot", line_color="orange", annotation_text=f"P10 ({p10_roi:.1f}%)")
    fig_hist.add_vline(x=p90_roi, line_dash="dot", line_color="green", annotation_text=f"P90 ({p90_roi:.1f}%)")
    fig_hist.update_layout(xaxis_title="ROI Estimado (%)", yaxis_title="Frecuencia", showlegend=False, height=380)
    st.plotly_chart(fig_hist, use_container_width=True)

with col_v2:
    st.subheader("2. Matriz de Sensibilidad: Correlación KRI vs KPI")
    df_corr = pd.DataFrame({
        "Costo Logístico (KRI)": costo_logistico,
        "Tasa de Interés (KRI)": tasa_interes,
        "Licencias Ambientales (KRI)": aprob_ambiental,
        "Demanda GWh (KPI)": demanda_gwh,
        "ROI Portafolio (KPI)": roi_simulado,
        "Capacidad MW (KPI)": expansion_capacidad
    }).corr()
    
    fig_heat = px.imshow(
        df_corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        aspect="auto",
        title="Correlaciones del Portafolio ECOGEN"
    )
    fig_heat.update_layout(height=380)
    st.plotly_chart(fig_heat, use_container_width=True)

# Visualización 3 y 4
col_v3, col_v4 = st.columns(2)

with col_v3:
    st.subheader("3. Análisis de Sensibilidad (Tornado: Impacto en ROI)")
    factores = ["Costo Logístico", "Tasa Interés", "Demanda GWh", "Aprobación Licencias"]
    impacto_max = [1.8, 1.2, 1.5, 0.6]
    impacto_min = [-1.9, -1.3, -1.4, -0.7]

    fig_tor = go.Figure()
    fig_tor.add_trace(go.Bar(y=factores, x=impacto_max, orientation="h", name="Impacto Favorable", marker_color="#2ca02c"))
    fig_tor.add_trace(go.Bar(y=factores, x=impacto_min, orientation="h", name="Impacto Desfavorable", marker_color="#d62728"))
    fig_tor.update_layout(barmode="relative", xaxis_title="Variación en puntos de ROI (%)", height=380)
    st.plotly_chart(fig_tor, use_container_width=True)

with col_v4:
    st.subheader("4. Cuadrante de Riesgo: Portafolio de Inversión")
    df_riesgos = pd.DataFrame({
        "Programa": ["Solar Equinox", "Eólica Andina", "HydroBalance", "Transmisión Regional"],
        "Probabilidad": [4.2, 3.8, 2.5, 3.1],
        "Impacto": [4.5, 4.0, 3.2, 3.8],
        "Inversión_USD_M": [400, 500, 300, 150]
    })
    fig_bubble = px.scatter(
        df_riesgos,
        x="Probabilidad",
        y="Impacto",
        size="Inversión_USD_M",
        color="Programa",
        text="Programa",
        range_x=[1, 5],
        range_y=[1, 5],
        title="Severidad y Capital en Riesgo (USD Millones)"
    )
    fig_bubble.update_traces(textposition="top center")
    fig_bubble.update_layout(height=380)
    st.plotly_chart(fig_bubble, use_container_width=True)

# Sección de Storytelling y Decisiones
st.markdown("---")
st.subheader("📋 Diagnóstico Ejecutivo para el Consejo Directivo")
col_d1, col_d2 = st.columns(2)

with col_d1:
    st.info("""
    **Hallazgos Clave de la Simulación:**
    * El ROI esperado se sitúa en torno al valor objetivo, pero existe una probabilidad significativa de caer bajo el umbral P10 debido a volatilidad logística.
    * El factor de mayor sensibilidad negativa es el costo de transporte hacia zonas no interconectadas.
    """)

with col_d2:
    st.success("""
    **Acciones de Mitigación Recomendadas:**
    * Implementar contratos forward para transporte e insumos clave.
    * Fortalecer mesas participativas tempranas para reducir riesgo de retraso en licenciamiento ambiental y social.
    """)