import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Simulador de Trayectoria",
    page_icon="📡",
    layout="wide"
)

# --- CSS PERSONALIZADO (ESTILO MINIMALISTA Y AFILADO) ---
st.markdown("""
    <style>
    /* Fondo de estrellas (Puedes cambiar la URL por tu propio archivo local) */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Tipografía y colores generales */
    h1, h2, h3, p, div {
        color: #E2E8F0 !important;
        font-family: 'Roboto Mono', monospace !important;
    }

    /* Título principal sin emojis excesivos */
    .main-title {
        font-size: 28px !important;
        font-weight: 700;
        letter-spacing: 2px;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 10px;
        margin-bottom: 30px;
        text-transform: uppercase;
    }

    /* Bordes afilados para los paneles */
    [data-testid="stExpander"] {
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 0px !important; /* Bordes afilados */
        background-color: rgba(15, 23, 42, 0.8) !important; /* Fondo oscuro semitransparente */
        backdrop-filter: blur(5px);
    }

    [data-testid="stExpander"] summary {
        color: #94A3B8 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Estilo para las métricas */
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-family: 'Roboto Mono', monospace !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }

    /* Ocultar el menú de Streamlit y el footer para un look más limpio */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<p class="main-title">Simulador de Trayectorias Parabólicas</p>', unsafe_allow_html=True)

# Información del equipo (Estilo Terminal)
with st.expander("Datos del equipo | Grupo 505 · Equipo 6"):
    st.markdown("""
        <div style="
            border-left: 2px solid #E2E8F0;
            padding: 10px 20px;
            color: #CBD5E1;
            font-size: 14px;
        ">
            <p><b>GRUPO:</b> 505 &nbsp;|&nbsp; <b>CARRERA:</b> Programación &nbsp;|&nbsp; <b>EQUIPO:</b> 6</p>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 15px 0;">
            <p><b>INTEGRANTES:</b></p>
            <ul style="list-style-type: square; margin-top: 5px;">
                <li>Castillo Aguilar Dylan Jonathan</li>
                <li>Cerecero García Aline Arizbeth</li>
                <li>González Rojas Jael Abigail</li>
                <li>Maya Zavala Angel De Jesus</li>
                <li>Salazar Bello Maria Fernanda</li>
                <li>Salvador Martinez Cristian Eduardo</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.write("Ajusta los parámetros y presiona **▶ Reproducir** en el gráfico.")

# Controles de la barra lateral
with st.sidebar:
    st.header("Parámetros")
    
    v0 = st.slider("Velocidad inicial (m/s)", 1.0, 100.0, 35.0, step=1.0)
    angulo = st.slider("Ángulo de lanzamiento (°)", 0.0, 90.0, 45.0, step=1.0)
    h0 = st.slider("Altura inicial (m)", 0.0, 50.0, 0.0, step=1.0)

# Cálculos físicos
g = 9.81
theta = np.radians(angulo)

v0x = v0 * np.cos(theta)
v0y = v0 * np.sin(theta)

# Tiempo de vuelo
t_vuelo = (v0y + np.sqrt(v0y**2 + 2 * g * h0)) / g
if t_vuelo <= 0:
    t_vuelo = 0.1

# Datos de la trayectoria
t = np.linspace(0, t_vuelo, 120)
x = v0x * t
y = h0 + v0y * t - 0.5 * g * t**2

# --- CONFIGURACIÓN DEL GRÁFICO (ESTILO MINIMALISTA) ---

frames = []
for i in range(len(t)):
    frames.append(
        go.Frame(
            data=[
                go.Scatter(
                    x=[x[i]], y=[y[i]],
                    mode="markers",
                    marker=dict(color="#FFFFFF", size=10, line=dict(color="#94A3B8", width=1))
                ),
                go.Scatter(
                    x=x[:i + 1], y=y[:i + 1],
                    mode="lines",
                    line=dict(color="#38BDF8", width=2, shape="spline") # Azul sobrio, no neón
                )
            ],
            name=f"frame{i}"
        )
    )

fig = go.Figure(
    data=[
        go.Scatter(
            x=[x[0]], y=[y[0]],
            mode="markers",
            marker=dict(color="#FFFFFF", size=10, line=dict(color="#94A3B8", width=1)),
            name="Proyectil"
        ),
        go.Scatter(x=[], y=[], mode="lines", line=dict(color="#38BDF8", width=2), name="Estela"),
        go.Scatter(
            x=x, y=y, mode="lines",
            line=dict(color="rgba(255, 255, 255, 0.2)", width=1, dash="dot"),
            name="Trayectoria total"
        ),
        go.Scatter(
            x=[0, max(x) * 1.1 if max(x) > 0 else 10], y=[0, 0],
            mode="lines",
            line=dict(color="rgba(255, 255, 255, 0.4)", width=1, dash="dash"),
            name="Suelo"
        )
    ],
    layout=go.Layout(
        template="plotly_dark",
        # HACER EL FONDO TRANSPARENTE PARA VER LAS ESTRELLAS
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        
        font=dict(family="Roboto Mono, monospace", color="#E2E8F0"),
        xaxis=dict(
            title="Distancia horizontal (m)",
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.05)', # Cuadrícula muy tenue
            zeroline=False
        ),
        yaxis=dict(
            title="Altura (m)",
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.05)',
            zeroline=False
        ),
        margin=dict(l=40, r=20, t=40, b=40),
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=0.0,
                y=1.15,
                showactive=False,
                bgcolor="rgba(15, 23, 42, 0.8)",
                bordercolor="rgba(255, 255, 255, 0.3)",
                font=dict(color="#E2E8F0"),
                buttons=[
                    dict(
                        label="▶ PLAY",
                        method="animate",
                        args=[None, dict(frame=dict(duration=25, redraw=True), fromcurrent=True, transition=dict(duration=0))]
                    ),
                    dict(
                        label="⏸ PAUSE",
                        method="animate",
                        args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")]
                    )
                ]
            )
        ]
    ),
    frames=frames
)

fig.update_yaxes(range=[0, max(y) * 1.2 if max(y) > 0 else 10])
fig.update_xaxes(range=[0, max(x) * 1.05 if max(x) > 0 else 10])

# Mostrar el gráfico
st.plotly_chart(fig, use_container_width=True)

# Resultados de la simulación
st.markdown("### Métricas de Vuelo")

col1, col2, col3 = st.columns(3)

# Inyectamos un pequeño estilo CSS para las métricas
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 10px 15px;
        border-radius: 0px;
    }
    </style>
""", unsafe_allow_html=True)

col1.metric("Tiempo de vuelo", f"{t_vuelo:.2f} s")
col2.metric("Altura máxima", f"{max(y):.2f} m")
col3.metric("Alcance máximo", f"{max(x):.2f} m")
