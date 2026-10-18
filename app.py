
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Trayectoria Parabólica Animada",
    page_icon="🚀",
    layout="wide"
)

# Estilos CSS
st.markdown("""
    <style>
    .big-font {
        font-size: 30px !important;
        font-weight: bold;
        color: #00E5FF;
    }

    .stSlider {
        padding-bottom: 20px;
    }

    /* Estilo de la lista desplegable */
    [data-testid="stExpander"] {
        border: 1px solid #00E5FF;
        border-radius: 10px;
        background-color: #111827;
    }

    [data-testid="stExpander"] summary {
        color: #00E5FF;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown(
    '<p class="big-font">🚀 Simulador Animado de Trayectorias Parabólicas</p>',
    unsafe_allow_html=True
)

# Información del equipo: lista desplegable
with st.expander("🎓 Datos del equipo | Grupo 505 · Equipo 6"):
    st.markdown("""
        <div style="
            background-color: #1E293B;
            border-left: 5px solid #00E5FF;
            padding: 18px 24px;
            border-radius: 10px;
            color: #FFFFFF;
        ">
            <p><b>GRUPO:</b> 505</p>
            <p><b>CARRERA:</b> Programación</p>
            <p><b>EQUIPO:</b> 6</p>
            <hr style="border-color: #475569;">
            <p><b>INTEGRANTES:</b></p>
            <ol>
                <li>Castillo Aguilar Dylan Jonathan</li>
                <li>Cerecero García Aline Arizbeth</li>
                <li>González Rojas Jael Abigail</li>
                <li>Maya Zavala Angel De Jesus</li>
                <li>Salazar Bello Maria Fernanda</li>
                <li>Salvador Martinez Cristian Eduardo</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

# Instrucciones
st.write(
    "Ajusta los parámetros y presiona el botón "
    "**▶ Reproducir** en el gráfico para ver el movimiento."
)

# Controles de la barra lateral
with st.sidebar:
    st.header("⚙️ Parámetros de Lanzamiento")

    v0 = st.slider(
        "Velocidad inicial (m/s)",
        1.0, 100.0, 35.0, step=1.0
    )

    angulo = st.slider(
        "Ángulo de lanzamiento (°)",
        0.0, 90.0, 45.0, step=1.0
    )

    h0 = st.slider(
        "Altura inicial (m)",
        0.0, 50.0, 0.0, step=1.0
    )

# Cálculos físicos
g = 9.81
theta = np.radians(angulo)

v0x = v0 * np.cos(theta)
v0y = v0 * np.sin(theta)

# Tiempo de vuelo
t_vuelo = (
    v0y + np.sqrt(v0y**2 + 2 * g * h0)
) / g

if t_vuelo <= 0:
    t_vuelo = 0.1

# Datos de la trayectoria
t = np.linspace(0, t_vuelo, 120)

x = v0x * t
y = h0 + v0y * t - 0.5 * g * t**2

# Creación de los fotogramas de la animación
frames = []

for i in range(len(t)):
    frames.append(
        go.Frame(
            data=[
                # Proyectil
                go.Scatter(
                    x=[x[i]],
                    y=[y[i]],
                    mode="markers",
                    marker=dict(
                        color="#FF3366",
                        size=15,
                        line=dict(color="white", width=2)
                    )
                ),

                # Estela del proyectil
                go.Scatter(
                    x=x[:i + 1],
                    y=y[:i + 1],
                    mode="lines",
                    line=dict(
                        color="#00E5FF",
                        width=4,
                        shape="spline"
                    )
                )
            ],
            name=f"frame{i}"
        )
    )

# Configuración del gráfico
fig = go.Figure(
    data=[
        # Proyectil en la posición inicial
        go.Scatter(
            x=[x[0]],
            y=[y[0]],
            mode="markers",
            marker=dict(
                color="#FF3366",
                size=15,
                line=dict(color="white", width=2)
            ),
            name="Proyectil"
        ),

        # Estela
        go.Scatter(
            x=[],
            y=[],
            mode="lines",
            line=dict(color="#00E5FF", width=4),
            name="Estela"
        ),

        # Trayectoria completa
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            line=dict(
                color="rgba(255, 255, 255, 0.2)",
                width=2,
                dash="dot"
            ),
            name="Trayectoria total"
        ),

        # Suelo
        go.Scatter(
            x=[0, max(x) * 1.1 if max(x) > 0 else 10],
            y=[0, 0],
            mode="lines",
            line=dict(
                color="gray",
                width=2,
                dash="dash"
            ),
            name="Suelo"
        )
    ],

    layout=go.Layout(
        template="plotly_dark",
        xaxis_title="Distancia horizontal (m)",
        yaxis_title="Altura (m)",
        margin=dict(l=0, r=0, t=40, b=0),

        # Botones de reproducción y pausa
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=0.1,
                y=1.15,
                showactive=False,
                buttons=[
                    dict(
                        label="▶ Reproducir",
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(
                                    duration=25,
                                    redraw=True
                                ),
                                fromcurrent=True,
                                transition=dict(duration=0)
                            )
                        ]
                    ),
                    dict(
                        label="⏸ Pausar",
                        method="animate",
                        args=[
                            [None],
                            dict(
                                frame=dict(
                                    duration=0,
                                    redraw=False
                                ),
                                mode="immediate"
                            )
                        ]
                    )
                ]
            )
        ]
    ),

    frames=frames
)

# Límites de los ejes
fig.update_yaxes(
    range=[
        0,
        max(y) * 1.2 if max(y) > 0 else 10
    ]
)

fig.update_xaxes(
    range=[
        0,
        max(x) * 1.05 if max(x) > 0 else 10
    ]
)

# Mostrar el gráfico
st.plotly_chart(fig, use_container_width=True)

# Resultados de la simulación
st.markdown("### 📊 Resultados de la Simulación")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Tiempo de vuelo",
    f"{t_vuelo:.2f} s"
)

col2.metric(
    "Altura máxima",
    f"{max(y):.2f} m"
)

col3.metric(
    "Alcance máximo",
    f"{max(x):.2f} m"
)
