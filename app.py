import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="F1 Performance Dashboard",
    page_icon="🏎️",
    layout="wide"
)

# --- INTEGRACIÓN CON BACKEND / FALLBACK MOCK ---
try:
    from src.processor import get_telemetry_data
except ImportError:
    st.warning("⚠️ Backend no detectado. Cargando modo de simulación (Mock Data).")

    def get_telemetry_data(year, gp, session, main_driver, ref_drivers):
        """
        Genera datos simulados que cumplen con el contrato:
        Driver (str), Distance (float), Speed (float), Throttle (float), Brake (bool), Gear (int)
        """
        drivers = [main_driver] + ref_drivers
        all_data = []
        
        for driver in drivers:
            # Crear una vuelta de ~5000 metros
            distance = np.linspace(0, 5000, 500)
            # Simular velocidad (onda senoidal con ruido para realismo)
            base_speed = 200 + 80 * np.sin(distance / 400)
            speed = base_speed + np.random.normal(0, 5, len(distance))
            # Simular acelerador (0 a 100)
            throttle = np.clip(100 * np.sin(distance / 600) + 20, 0, 100)
            # Simular Freno y Marcha
            brake = throttle < 10
            gear = np.random.randint(3, 8, len(distance))
            
            df = pd.DataFrame({
                'Driver': driver,
                'Distance': distance,
                'Speed': speed,
                'Throttle': throttle,
                'Brake': brake,
                'Gear': gear
            })
            all_data.append(df)
            
        return pd.concat(all_data, ignore_index=True)

# --- SIDEBAR: FILTROS JERÁRQUICOS ---
st.sidebar.header("⚙️ Configuración de Sesión")

# Simulación de metadatos (En v1 se obtendrían de FastF1)
years = [2024, 2023, 2022]
selected_year = st.sidebar.selectbox("Año", years)

gps = ["Bahrain Grand Prix", "Monaco Grand Prix", "Spanish Grand Prix", "Silverstone"]
selected_gp = st.sidebar.selectbox("Gran Premio", gps)

sessions = ["Práctica 1", "Práctica 2", "Práctica 3", "Clasificación", "Carrera"]
selected_session = st.sidebar.selectbox("Sesión", sessions)

session_mapping = {
    "Práctica 1": "FP1",
    "Práctica 2": "FP2",
    "Práctica 3": "FP3",
    "Clasificación": "Q",
    "Carrera": "R"
}

st.sidebar.markdown("---")
st.sidebar.subheader("🏎️ Selección de Pilotos")

# Lista de pilotos (Simulada)
available_drivers = ["VER", "HAM", "LEC", "NOR", "ALO", "SAI", "PER", "RUS"]

main_driver = st.sidebar.selectbox("Piloto Principal", available_drivers, index=0)
ref_drivers = st.sidebar.multiselect(
    "Pilotos de Referencia (Comparativa)", 
    [d for d in available_drivers if d != main_driver],
    default=[available_drivers[1]] if len(available_drivers) > 1 else None
)

# Botón para disparar la carga de datos
load_btn = st.sidebar.button("🚀 Cargar Telemetría", use_container_width=True)

# --- LÓGICA DE ESTADO (SESSION STATE) ---
if "data" not in st.session_state:
    st.session_state.data = None

if load_btn:
    with st.spinner("Extrayendo datos de FastF1..."):
        # Llamada a la función del contrato
        fastf1_session = session_mapping[selected_session]
        st.session_state.data = get_telemetry_data(
            selected_year, selected_gp, fastf1_session, main_driver, ref_drivers
        )
        st.success(f"Datos cargados para {selected_gp} ({selected_year})")

# --- PANEL CENTRAL (UI PRINCIPAL) ---
st.title(f"🏎️ {selected_gp} - {selected_year}")
st.subheader(f"Análisis de Rendimiento: {selected_session}")

if st.session_state.data is not None:
    tab1, tab2, tab3 = st.tabs(["📊 Resumen de Sesión", "📈 Telemetría Comparativa", "⚙️ Setup"])

    # --- TAB 1: RESUMEN ---
    with tab1:
        st.markdown("### Métricas Clave (Mejor Vuelta)")
        cols = st.columns(len(ref_drivers) + 1)
        
        # Simulación de métricas basadas en los datos cargados
        all_selected_drivers = [main_driver] + ref_drivers
        for i, driver in enumerate(all_selected_drivers):
            driver_data = st.session_state.data[st.session_state.data['Driver'] == driver]
            max_speed = round(driver_data['Speed'].max(), 1)
            avg_throttle = round(driver_data['Throttle'].mean(), 1)
            
            with cols[i]:
                st.metric(label=f"Piloto: {driver}", value=f"{max_speed} km/h", delta="Top Speed")
                st.caption(f"Avg Throttle: {avg_throttle}%")

    # --- TAB 2: TELEMETRÍA (PLOTLY) ---
    with tab2:
        st.markdown("### Comparativa de Telemetría (Velocidad vs Distancia)")
        
        df_plot = st.session_state.data
        
        # Crear Subplots: 1 para Speed, 1 para Throttle
        fig = make_subplots(
            rows=2, cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.05,
            subplot_titles=("Velocidad (km/h)", "Acelerador (%)")
        )

        # Colores para pilotos
        colors = ['#06D6A0', '#EF476F', '#118AB2', '#FFD166']

        for i, driver in enumerate(all_selected_drivers):
            driver_df = df_plot[df_plot['Driver'] == driver]
            
            # Gráfico de Velocidad
            fig.add_trace(
                go.Scatter(
                    x=driver_df['Distance'], 
                    y=driver_df['Speed'],
                    name=f"{driver} - Speed",
                    line=dict(color=colors[i % len(colors)], width=2),
                    hovertemplate="%{y:.1f} km/h"
                ),
                row=1, col=1
            )
            
            # Gráfico de Acelerador
            fig.add_trace(
                go.Scatter(
                    x=driver_df['Distance'], 
                    y=driver_df['Throttle'],
                    name=f"{driver} - Throttle",
                    line=dict(color=colors[i % len(colors)], width=1.5, dash='dot'),
                    hovertemplate="%{y:.1f}%"
                ),
                row=2, col=1
            )

        fig.update_layout(
            height=600,
            template="plotly_dark",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        fig.update_xaxes(title_text="Distancia (m)", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.info("Configuración de neumáticos y sectores disponible en v1.1.0")
        st.dataframe(st.session_state.data.head(20))

else:
    st.info("👈 Selecciona los pilotos y haz clic en 'Cargar Telemetría' en la barra lateral para comenzar el análisis.")

# --- FOOTER ---
st.markdown("---")
st.caption("F1 Telemetry Dashboard v1.0.0 | Desarrollado por Ingeniería de Rendimiento")