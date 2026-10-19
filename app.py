import streamlit as st
import numpy as np
import plotly.graph_objects as go
import base64

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Simulador de Trayectoria",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNCIÓN PARA PONER IMAGEN DE FONDO EN STREAMLIT ---
# Usamos una imagen de Unsplash (puedes cambiarla por una local)
def set_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop");
             background-size: cover;
             background-position: center;
             background-attachment: fixed;
         }}
         
         /* Oscurecer un poco el fondo para que resalte el texto */
         .stApp::before {{
             content: "";
             position: absolute;
             top: 0; left: 0; width: 100%; height: 100%;
             background: rgba(15, 23, 42, 0.85); /* Azul muy oscuro semitransparente */
             z-index: -1;
         }}

         /* Tipografía más elegante */
         @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
         html, body, [class*="css"] {{
             font-family: 'Poppins', sans-serif;
         }}

         /* Estilo para las métricas (tarjetas) */
         div[data-testid="metric-container"] {{
             background: rgba(30, 41, 59, 0.7);
             border: 1px solid rgba(0, 229, 255, 0.3);
             padding: 15px;
             border-radius: 12px;
             backdrop-filter: blur(10px);
             box-shadow: 0 4px 6px rgba(0,0,0,0.3);
         }}
         
         /* Título principal */
         .main-title {{
             font-size: 42px !important;
             font-weight: 600;
             color: #FFFFFF;
             text-align: center;
             text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
             margin-bottom: 20px;
         }}
         
         .highlight {{
             color: #00E5FF;
         }}
         </style>
         """,
         unsafe_allow_html=True
    )

set_bg_from_url()

# --- INTERFAZ PRINCIPAL ---
st.markdown('<p class="main-title">Simulador de <span class="highlight">Trayectoria Parabólica</span></p>', unsafe_allow_html=True)

# Información del equipo en un expander
with st.expander("🎓 Datos del equipo | Grupo 505 · Equipo 6"):
    st.markdown("""
        <div style="
            background-color: rgba(30, 41, 59, 0.8);
            border-left: 5px solid #00E5FF;
            padding: 18px 24px;
            border-radius: 10px;
            color: #E2E8F0;
        ">
            <p><b>CARRERA:</b> Programación</p>
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

# Controles en la barra lateral con estilo
with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    st.markdown("---")
    v0 = st.slider("Velocidad Inicial (m/s)", 1.0, 100.0, 45.0, step=1.0)
    angulo = st.slider("Ángulo de Lanzamiento (°)", 0.0, 90.0, 45.0, step=1.0)
    h0 = st.slider("Altura Inicial (m)", 0.0, 50.0, 0.0, step=1.0)
    st.markdown("---")
    st.info("💡 **Tip:** Mueve los deslizadores y presiona 'Reproducir' en el gráfico.")

# --- CÁLCULOS FÍSICOS ---
g = 9.81
theta = np.radians(angulo)
v0x = v0 * np.cos(theta)
v0y = v0 * np.sin(theta)

t_vuelo = (v0y + np.sqrt(v0y**2 + 2 * g * h0)) / g
if t_vuelo <= 0:
    t_vuelo = 0.1

t = np.linspace(0, t_vuelo, 120)
x = v0x * t
y = h0 + v0y * t - 0.5 * g * t**2

# --- CREACIÓN DE LA GRÁFICA EN PLOTLY ---

# Fotogramas de la animación
frames = []
for i in range(len(t)):
    frames.append(
        go.Frame(
            data=[
                go.Scatter(x=[x[i]], y=[y[i]], mode="markers", 
                           marker=dict(color="#FF3366", size=16, line=dict(color="white", width=2))),
                go.Scatter(x=x[:i + 1], y=y[:i + 1], mode="lines", 
                           line=dict(color="#00E5FF", width=4, shape="spline"))
            ],
            name=f"frame{i}"
        )
    )

# Fondo personalizado para Plotly (opcional, aquí usamos una imagen de un cielo)
# Si quieres usar una imagen local, cambia el 'source' por 'data:image/jpeg;base64,...'
bg_image = "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?q=80&w=1000&auto=format&fit=crop"

fig = go.Figure(
    data=[
        go.Scatter(x=[x[0]], y=[y[0]], mode="markers", 
                   marker=dict(color="#FF3366", size=16, line=dict(color="white", width=2)), name="Proyectil"),
        go.Scatter(x=[], y=[], mode="lines", line=dict(color="#00E5FF", width=4), name="Estela"),
        go.Scatter(x=x, y=y, mode="lines", line=dict(color="rgba(255, 255, 255, 0.4)", width=2, dash="dot"), name="Trayectoria Teórica"),
        go.Scatter(x=[0, max(x) * 1.1 if max(x) > 0 else 10], y=[0, 0], mode="lines", line=dict(color="gray", width=2, dash="dash"), name="Suelo")
    ],
    layout=go.Layout(
        # Hacemos el fondo transparente para que se vea la imagen o el color de Streamlit
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        
        # Añadimos una imagen de fondo al gráfico (opcional, quítalo si no lo quieres)
        images=[dict(
            source=bg_image,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            sizex=1, sizey=1,
            sizing="stretch",
            opacity=0.3, # Opacidad baja para no distraer
            layer="below"
        )],
        
        xaxis=dict(
            title="Distancia horizontal (m)",
            showgrid=True, gridcolor='rgba(255,255,255,0.1)',
            zeroline=False, color="#E2E8F0"
        ),
        yaxis=dict(
            title="Altura (m)",
            showgrid=True, gridcolor='rgba(255,255,255,0.1)',
            zeroline=False, color="#E2E8F0"
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        
        # Botones estilizados
        updatemenus=[dict(
            type="buttons", direction="right", x=0.5, y=1.15, xanchor="center", showactive=False,
            bgcolor="rgba(30, 41, 59, 0.8)", bordercolor="#00E5FF", borderwidth=1, font=dict(color="#FFFFFF"),
            buttons=[
                dict(label="▶ Reproducir", method="animate", args=[None, dict(frame=dict(duration=25, redraw=True), fromcurrent=True, transition=dict(duration=0))]),
                dict(label="⏸ Pausar", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])
            ]
        )]
    ),
    frames=frames
)

# Límites de los ejes (ligeramente ajustados)
fig.update_yaxes(range=[0, max(y) * 1.2 if max(y) > 0 else 10])
fig.update_xaxes(range=[0, max(x) * 1.05 if max(x) > 0 else 10])

# Mostrar el gráfico
st.plotly_chart(fig, use_container_width=True)

# --- RESULTADOS ESTILIZADOS ---
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

col1.metric("⏱️ Tiempo de Vuelo", f"{t_vuelo:.2f} s")
col2.metric("📈 Altura Máxima", f"{max(y):.2f} m")
col3.metric("📏 Alcance Máximo", f"{max(x):.2f} m")
