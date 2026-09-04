import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CORPORATIVOS
# ==============================================================================
st.set_page_config(
    page_title="ECOGEN S.A. - Tablero de Riesgos y Estrategia",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #F4F6F9;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Barra lateral institucional */   
    /* Barra lateral institucional */
    [data-testid="stSidebar"] {
        background-color: #0F2537;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #FFFFFF !important;
    }
    /* Texto oscuro y legible dentro de la lista desplegable */
    [data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #0F2537 !important;
    }
    /* Slider: valores y números (500 y 5000) siempre fijos y visibles en blanco */
    [data-testid="stSlider"] * {
        color: #FFFFFF !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    /* Títulos */
    h1, h2, h3, h4 {
        color: #0F2537 !important;
        font-weight: 700;
    }
    /* Tarjetas de métricas (KPIs) */
    div[data-testid="stMetricValue"] {
        color: #0F2537 !important;
        font-weight: 800 !important;
    }
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        padding: 1.1rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(15, 37, 55, 0.06);
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CONTROLES EN LA BARRA LATERAL
# ==============================================================================
st.sidebar.markdown("### ⚙️ Parámetros de Simulación")
n_iteraciones = st.sidebar.slider(
    "Número de iteraciones Monte Carlo:",
    min_value=500,
    max_value=5000,
    value=1000,
    step=100
)

programa_sel = st.sidebar.selectbox(
    "Filtrar por Programa Estratégico:",
    ["Portafolio Total", "Solar Equinox", "Eólica Andina", "HydroBalance"]
)

# ==============================================================================
# 3. BASE DE DATOS Y PERFILES DINÁMICOS POR PROGRAMA
# ==============================================================================
perfiles = {
    "Portafolio Total": {
        "desc": "Consolidado corporativo multitecnología (Solar, Eólico e Hídrico). Diversificación balanceada de riesgos.",
        "roi_mean": 12.0, "roi_std": 1.45,
        "lic_mean": 35.0, "lic_std": 8.0,
        "log_mean": 15.0, "log_std": 3.2,
        "cap_mean": 85.0, "cap_std": 5.5,
        "okr_target": 12.0,
        "riesgos": [
            {"Riesgo": "Retraso Licencias Ambientales", "Prob": 0.48, "Impacto": 0.72, "Severidad": 34.5, "Categoria": "Regulatorio"},
            {"Riesgo": "Sobrecosto Cadena Suministros", "Prob": 0.58, "Impacto": 0.55, "Severidad": 31.9, "Categoria": "Financiero"},
            {"Riesgo": "Falla Capacidad Puesta en Marcha", "Prob": 0.32, "Impacto": 0.80, "Severidad": 25.6, "Categoria": "Operacional"},
            {"Riesgo": "Volatilidad Tarifaria Mercado Mayorista", "Prob": 0.52, "Impacto": 0.65, "Severidad": 33.8, "Categoria": "Mercado"}
        ]
    },
    "Solar Equinox": {
        "desc": "Parque solar fotovoltaico de 150 MW. Sensible a importación de módulos solares y plazos UPME/ANLA.",
        "roi_mean": 13.8, "roi_std": 2.10,
        "lic_mean": 48.0, "lic_std": 11.0,
        "log_mean": 18.5, "log_std": 4.1,
        "cap_mean": 91.0, "cap_std": 4.0,
        "okr_target": 12.5,
        "riesgos": [
            {"Riesgo": "Trámites y Consultas Previas (UPME/ANLA)", "Prob": 0.70, "Impacto": 0.85, "Severidad": 59.5, "Categoria": "Regulatorio"},
            {"Riesgo": "Fluctuación Cambiaria y Aranceles Módulos", "Prob": 0.68, "Impacto": 0.62, "Severidad": 42.1, "Categoria": "Financiero"},
            {"Riesgo": "Congestión Subestación y Conexión al SIN", "Prob": 0.55, "Impacto": 0.75, "Severidad": 41.2, "Categoria": "Técnico"},
            {"Riesgo": "Afectación por Polvo y Clima Extremo", "Prob": 0.25, "Impacto": 0.35, "Severidad": 8.7, "Categoria": "Operacional"}
        ]
    },
    "Eólica Andina": {
        "desc": "Parque eólico en alta cordillera. Complejidad en transporte extrapesado y consulta con comunidades locales.",
        "roi_mean": 11.2, "roi_std": 1.75,
        "lic_mean": 38.0, "lic_std": 7.5,
        "log_mean": 21.0, "log_std": 4.8,
        "cap_mean": 82.0, "cap_std": 6.8,
        "okr_target": 11.5,
        "riesgos": [
            {"Riesgo": "Transporte Vial Especial (Torres y Aspas)", "Prob": 0.78, "Impacto": 0.82, "Severidad": 63.9, "Categoria": "Logístico"},
            {"Riesgo": "Licenciamiento Social y Acuerdos Territoriales", "Prob": 0.58, "Impacto": 0.86, "Severidad": 49.8, "Categoria": "Social"},
            {"Riesgo": "Variabilidad del Factor Planta (Recurso Eólico)", "Prob": 0.42, "Impacto": 0.52, "Severidad": 21.8, "Categoria": "Técnico"},
            {"Riesgo": "Demoras en Pólizas y Garantías Contractuales", "Prob": 0.35, "Impacto": 0.60, "Severidad": 21.0, "Categoria": "Financiero"}
        ]
    },
    "HydroBalance": {
        "desc": "Pequeña Central Hidroeléctrica (PCH). Alta predictibilidad operativa, regulada por variabilidad hidrológica.",
        "roi_mean": 10.4, "roi_std": 0.95,
        "lic_mean": 22.0, "lic_std": 4.2,
        "log_mean": 11.0, "log_std": 2.1,
        "cap_mean": 79.0, "cap_std": 4.8,
        "okr_target": 10.0,
        "riesgos": [
            {"Riesgo": "Caudales Mínimos por Fenómeno del Niño", "Prob": 0.62, "Impacto": 0.78, "Severidad": 48.3, "Categoria": "Climático"},
            {"Riesgo": "Inestabilidad Geotécnica y Sedimentación", "Prob": 0.46, "Impacto": 0.70, "Severidad": 32.2, "Categoria": "Operacional"},
            {"Riesgo": "Ajuste de Concesión de Aguas y Caudal Ecológico", "Prob": 0.32, "Impacto": 0.65, "Severidad": 20.8, "Categoria": "Regulatorio"},
            {"Riesgo": "Mantenimiento Mayor por Abrasión en Turbinas", "Prob": 0.48, "Impacto": 0.45, "Severidad": 21.6, "Categoria": "Técnico"}
        ]
    }
}

cfg = perfiles[programa_sel]

# ==============================================================================
# 4. MOTOR ESTOCÁSTICO MONTE CARLO (CONECTADO AL FILTRO)
# ==============================================================================
np.random.seed(42)

# Simulación de Factores de Riesgo (KRIs) e Indicadores de Rendimiento (KPIs)
kri_licencias = np.random.normal(cfg["lic_mean"], cfg["lic_std"], n_iteraciones)
kri_logistica = np.random.normal(cfg["log_mean"], cfg["log_std"], n_iteraciones)
kpi_capacidad = np.random.normal(cfg["cap_mean"], cfg["cap_std"], n_iteraciones)

# El ROI reacciona estocásticamente a los factores de riesgo
ruido_mercado = np.random.normal(0, cfg["roi_std"] * 0.6, n_iteraciones)
roi_simulado = (
    cfg["roi_mean"]
    - ((kri_licencias - cfg["lic_mean"]) * 0.05)
    - ((kri_logistica - cfg["log_mean"]) * 0.14)
    + ((kpi_capacidad - cfg["cap_mean"]) * 0.09)
    + ruido_mercado
)

# Estructura en DataFrame
df_sim = pd.DataFrame({
    "ROI": roi_simulado,
    "KRI Licenciamiento (Días)": kri_licencias,
    "KRI Sobrecosto Logístico (%)": kri_logistica,
    "KPI Capacidad Operativa (%)": kpi_capacidad
})

# Métricas probabilísticas
p10 = np.percentile(roi_simulado, 10)
p50 = np.percentile(roi_simulado, 50)
p90 = np.percentile(roi_simulado, 90)
prob_okr = (roi_simulado >= cfg["okr_target"]).mean() * 100

# ==============================================================================
# 5. ENCABEZADO Y TARJETAS MÉTRICAS
# ==============================================================================
st.markdown("## ⚡ ECOGEN S.A. - Gestión Estratégica de Riesgos e Incertidumbre")
st.markdown(f"**Oficina Estratégica de Riesgos (OER)** | Simulación Monte Carlo ({n_iteraciones:,} iteraciones) | **Programa en análisis:** `{programa_sel}`")
st.caption(cfg["desc"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("ROI Esperado (P50)", f"{p50:.2f}%", f"{p50 - cfg['okr_target']:+.2f}% vs Meta")
col2.metric("Probabilidad Cumplir OKR", f"{prob_okr:.1f}%", f"Meta: ≥{cfg['okr_target']}%")
col3.metric("Escenario Pesimista (P10)", f"{p10:.2f}%", "Riesgo en cola (VaR)", delta_color="inverse")
col4.metric("Escenario Optimista (P90)", f"{p90:.2f}%", "Potencial superior")

st.markdown("---")

# ==============================================================================
# 6. FILA 1: HISTOGRAMA MONTE CARLO Y MATRIZ DE CORRELACIÓN
# ==============================================================================
f1_col1, f1_col2 = st.columns(2)

with f1_col1:
    st.markdown("### 1. Distribución Monte Carlo: Retorno sobre Inversión (ROI)")
    fig_hist = go.Figure()
    
    fig_hist.add_trace(go.Histogram(
        x=df_sim["ROI"],
        nbinsx=40,
        name="Iteraciones",
        marker_color="#1E4D6B",
        opacity=0.85
    ))
    
    # Líneas con posiciones escalonadas, mayor tamaño de letra y fondo blanco para legibilidad total
    fig_hist.add_vline(
        x=p10, line_dash="dash", line_color="#D9534F", line_width=2,
        annotation_text=f"<b>P10: {p10:.1f}%</b>", annotation_position="top left",
        annotation_font_size=13, annotation_font_color="#D9534F",
        annotation_bgcolor="rgba(255,255,255,0.9)"
    )
    fig_hist.add_vline(
        x=cfg["okr_target"], line_dash="dot", line_color="#0F2537", line_width=2.5,
        annotation_text=f"<b>Meta: {cfg['okr_target']:.1f}%</b>", annotation_position="bottom right",
        annotation_font_size=13, annotation_font_color="#0F2537",
        annotation_bgcolor="rgba(255,255,255,0.9)"
    )
    fig_hist.add_vline(
        x=p50, line_dash="solid", line_color="#E67E22", line_width=2,
        annotation_text=f"<b>P50: {p50:.1f}%</b>", annotation_position="top right",
        annotation_font_size=13, annotation_font_color="#D35400",
        annotation_bgcolor="rgba(255,255,255,0.9)"
    )
    fig_hist.add_vline(
        x=p90, line_dash="dash", line_color="#27AE60", line_width=2,
        annotation_text=f"<b>P90: {p90:.1f}%</b>", annotation_position="top right",
        annotation_font_size=13, annotation_font_color="#1E8449",
        annotation_bgcolor="rgba(255,255,255,0.9)"
    )

    fig_hist.update_layout(
        template="plotly_white",
        margin=dict(l=25, r=25, t=35, b=25),
        xaxis=dict(
            title=dict(text="ROI Estimado (%)", font=dict(size=14, color="#0F2537")),
            tickfont=dict(size=12, color="#0F2537")
        ),
        yaxis=dict(
            title=dict(text="Frecuencia", font=dict(size=14, color="#0F2537")),
            tickfont=dict(size=12, color="#0F2537")
        ),
        showlegend=False,
        height=380
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with f1_col2:
    st.markdown("### 2. Matriz de Sensibilidad: Correlación KRI vs KPI")
    matriz_corr = df_sim.corr().round(2)
    
    fig_corr = px.imshow(
        matriz_corr,
        text_auto=".2f",
        color_continuous_scale="Blues",
        aspect="auto"
    )
    
    # Texto más grande, negrita y etiquetas de ejes claras
    fig_corr.update_traces(
        textfont=dict(size=16, family="Arial")
    )
    fig_corr.update_layout(
        template="plotly_white",
        margin=dict(l=25, r=25, t=35, b=25),
        xaxis=dict(tickfont=dict(size=12, color="#0F2537")),
        yaxis=dict(tickfont=dict(size=12, color="#0F2537")),
        height=380
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# ==============================================================================
# 7. FILA 2: DIAGRAMA TORNADO Y MAPA DE RIESGOS ESTRATÉGICOS (BURBUJAS)
# ==============================================================================
f2_col1, f2_col2 = st.columns(2)

with f2_col1:
    st.markdown("### 3. Diagrama Tornado: Sensibilidad del ROI")
    
    # Cálculo de impacto diferencial (P90 - P10) por factor sobre el ROI
    impacto_lic = (df_sim[df_sim["KRI Licenciamiento (Días)"] > np.percentile(kri_licencias, 80)]["ROI"].mean()
                   - df_sim[df_sim["KRI Licenciamiento (Días)"] < np.percentile(kri_licencias, 20)]["ROI"].mean())
    impacto_log = (df_sim[df_sim["KRI Sobrecosto Logístico (%)"] > np.percentile(kri_logistica, 80)]["ROI"].mean()
                   - df_sim[df_sim["KRI Sobrecosto Logístico (%)"] < np.percentile(kri_logistica, 20)]["ROI"].mean())
    impacto_cap = (df_sim[df_sim["KPI Capacidad Operativa (%)"] > np.percentile(kpi_capacidad, 80)]["ROI"].mean()
                   - df_sim[df_sim["KPI Capacidad Operativa (%)"] < np.percentile(kpi_capacidad, 20)]["ROI"].mean())
    
    df_tornado = pd.DataFrame({
        "Variable": ["Retraso Licenciamiento", "Sobrecosto Logístico", "Capacidad Operativa"],
        "Impacto_ROI": [impacto_lic, impacto_log, impacto_cap]
    }).sort_values(by="Impacto_ROI", key=abs, ascending=True)

    colores_tornado = ["#D9534F" if val < 0 else "#2E7D32" for val in df_tornado["Impacto_ROI"]]

    fig_tornado = go.Figure(go.Bar(
        x=df_tornado["Impacto_ROI"],
        y=df_tornado["Variable"],
        orientation='h',
        marker_color=colores_tornado,
        text=[f"{val:+.2f}%" for val in df_tornado["Impacto_ROI"]],
        textposition="outside"
    ))
    fig_tornado.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Desviación Promedio en el ROI (%)",
        height=360
    )
    st.plotly_chart(fig_tornado, use_container_width=True)

with f2_col2:
    st.markdown("### 4. Matriz de Exposición de Riesgos Críticos")
    df_riesgos = pd.DataFrame(cfg["riesgos"])
    
    fig_bubble = px.scatter(
        df_riesgos,
        x="Prob",
        y="Impacto",
        size="Severidad",
        color="Categoria",
        hover_name="Riesgo",
        text="Riesgo",
        size_max=38,
        color_discrete_sequence=["#D9534F", "#0F2537", "#2E7D32", "#F0AD4E"]
    )
    fig_bubble.update_traces(textposition='top center')
    fig_bubble.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(title="Probabilidad de Ocurrencia", range=[0.1, 1.0]),
        yaxis=dict(title="Impacto Estratégico (0-1)", range=[0.2, 1.05]),
        height=360
    )
    st.plotly_chart(fig_bubble, use_container_width=True)