import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Simulador de Trayectoria",
    page_icon="📡",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    h1, h2, h3, p, div {
        color: #E2E8F0 !important;
        font-family: 'Roboto Mono', monospace !important;
    }

    .main-title {
        font-size: 28px !important;
        font-weight: 700;
        letter-spacing: 2px;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 10px;
        margin-bottom: 30px;
        text-transform: uppercase;
    }

    [data-testid="stExpander"] {
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 0px !important;
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(5px);
    }

    [data-testid="stExpander"] summary {
        color: #94A3B8 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-family: 'Roboto Mono', monospace !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Simulador de Trayectorias Parabólicas</p>', unsafe_allow_html=True)

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

st.write("Ajusta los parámetros y presiona **▶ PLAY** en el gráfico.")

with st.sidebar:
    st.header("Parámetros")
    
    v0 = st.slider("Velocidad inicial (m/s)", 1.0, 100.0, 35.0, step=1.0)
    angulo = st.slider("Ángulo de lanzamiento (°)", 0.0, 90.0, 45.0, step=1.0)
    h0 = st.slider("Altura inicial (m)", 0.0, 50.0, 0.0, step=1.0)

g = 9.81
theta = np.radians(angulo)

# Redondeo para evitar errores de punto flotante (ej. cos(90°) ≈ 6e-17)
v0x = round(v0 * np.cos(theta), 10)
v0y = round(v0 * np.sin(theta), 10)

t_vuelo = (v0y + np.sqrt(v0y**2 + 2 * g * h0)) / g

if t_vuelo <= 1e-9:
    # Ángulo 0° y altura 0 m: el proyectil no despega
    st.warning("Con ángulo 0° y altura inicial 0 m el proyectil no despega. Aumenta el ángulo o la altura.")
    t_vuelo = 0.0
    t = np.linspace(0, 0.1, 120)
    x = np.zeros_like(t)
    y = np.zeros_like(t)
else:
    t = np.linspace(0, t_vuelo, 120)
    x = v0x * t
    y = h0 + v0y * t - 0.5 * g * t**2
    y = np.maximum(y, 0.0)  # evita valores negativos por redondeo

x_max = max(x.max() * 1.05, 10)
y_max = max(y.max() * 1.2, 10)

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
                    line=dict(color="#38BDF8", width=2, shape="spline")
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
            x=[0, x_max], y=[0, 0],
            mode="lines",
            line=dict(color="rgba(255, 255, 255, 0.4)", width=1, dash="dash"),
            name="Suelo"
        )
    ],
    layout=go.Layout(
        template="plotly_dark",
        paper_bgcolor='rgba(10, 15, 25, 0.65)',
        plot_bgcolor='rgba(10, 15, 25, 0.65)',
        font=dict(family="Roboto Mono, monospace", color="#E2E8F0"),
        xaxis=dict(
            title="Distancia horizontal (m)",
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.05)',
            zeroline=False
        ),
        yaxis=dict(
            title="Altura (m)",
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.05)',
            zeroline=False,
            scaleanchor="x",   # misma escala en X e Y para que los ángulos se vean reales
            scaleratio=1
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

fig.update_yaxes(range=[0, y_max])
fig.update_xaxes(range=[0, x_max])

st.plotly_chart(fig, use_container_width=True)

st.markdown("### Métricas de Vuelo")

col1, col2, col3 = st.columns(3)

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
col2.metric("Altura máxima", f"{y.max():.2f} m")
col3.metric("Alcance máximo", f"{x.max():.2f} m")
