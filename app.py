import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIGURACIÓN E INYECCIÓN DE ESTILO ---
st.set_page_config(page_title="F1 STRATOS | Telemetry", page_icon="🏎️", layout="wide")

def load_f1_theme():
    st.markdown("""
        <style>
        /* Importación de fuentes técnicas */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');

        /* Ocultar UI Genérica de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}

        /* Contenedor Base */
        .stApp {
            background: radial-gradient(circle at top right, #1a1a1a, #050505);
            color: #e0e0e0;
            font-family: 'Rajdhani', sans-serif;
        }

        /* Sidebar Estilo Panel de Control */
        section[data-testid="stSidebar"] {
            background-color: rgba(10, 10, 10, 0.95) !important;
            border-right: 1px solid #333;
            box-shadow: 5px 0 15px rgba(0,0,0,0.5);
        }

        /* Estilo de Tarjetas KPI (Glassmorphism) */
        .kpi-card {
            background: rgba(255, 255, 255, 0.03);
            border-left: 4px solid #ff1801;
            padding: 20px;
            border-radius: 8px;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255,255,255,0.05);
            border-top: 1px solid rgba(255,255,255,0.05);
            border-bottom: 1px solid rgba(255,255,255,0.05);
            transition: transform 0.3s ease;
        }
        .kpi-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.06);
        }
        .kpi-label { color: #888; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; }
        .kpi-value { font-family: 'Orbitron', sans-serif; font-size: 1.8rem; color: #fff; margin-top: 5px; }

        /* Estilo para los Tabs */
        .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: transparent; }
        .stTabs [data-baseweb="tab"] {
            background-color: #111;
            border: 1px solid #333;
            color: #888;
            padding: 10px 25px;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.7rem;
            border-radius: 4px 4px 0 0;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ff1801 !important;
            color: white !important;
            border-color: #ff1801 !important;
        }

        /* Botones de Acción */
        .stButton>button {
            background: linear-gradient(135deg, #ff1801 0%, #a00d00 100%);
            color: white;
            border: none;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 12px;
            border-radius: 4px;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            box-shadow: 0 0 20px rgba(255, 24, 1, 0.4);
            transform: scale(1.02);
        }

        /* Títulos */
        h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; font-weight: 700 !important; }
        </style>
    """, unsafe_allow_html=True)

# --- 2. HELPERS DE INTERFAZ ---
def render_kpi(label, value):
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

# --- 3. MOCK / BACKEND INTEGRATION ---
try:
    from src.processor import get_telemetry_data, get_session_summary
except ImportError:
    def get_telemetry_data(year, gp, session, main_driver, ref_drivers):
        drivers = [main_driver] + ref_drivers
        all_data = []
        for driver in drivers:
            dist = np.linspace(0, 5000, 400)
            speed = 220 + 75 * np.sin(dist / 400) + np.random.normal(0, 2, 400)
            df = pd.DataFrame({
                'Driver': driver, 'Distance': dist, 'Speed': speed,
                'Throttle': np.clip(100 * np.sin(dist / 500) + 25, 0, 100),
                'Brake': np.random.choice([0, 1], 400), 'Gear': np.random.randint(4, 8, 400)
            })
            all_data.append(df)
        return pd.concat(all_data)

    def get_session_summary(year, gp, session, driver):
        return {
            "Driver": driver, "FinalPosition": "P1", "BestTime": "1:21.456", 
            "TotalLaps": 57, "Strategy": "M ⮕ H", "Q3_Time": "1:10.222", 
            "Stints": [{"Compound": "SOFT", "Laps": 18}, {"Compound": "MEDIUM", "Laps": 39}]
        }

# --- 4. APLICACIÓN PRINCIPAL ---
load_f1_theme()

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#ff1801;'>SYSTEMS</h2>", unsafe_allow_html=True)
    
    selected_year = st.selectbox("SEASON", [2024, 2023, 2022])
    selected_gp = st.selectbox("GRAND PRIX", ["Bahrain Grand Prix", "Monaco Grand Prix", "Silverstone"])
    selected_session = st.selectbox("SESSION", ["Práctica 1", "Práctica 2", "Clasificación", "Carrera"])
    
    session_mapping = {
        "Práctica 1": "FP1", "Práctica 2": "FP2", 
        "Clasificación": "Q", "Carrera": "R"
    }
    fastf1_session = session_mapping[selected_session]
    
    st.markdown("---")
    available_drivers = ["VER", "HAM", "LEC", "NOR", "ALO", "SAI", "PER", "RUS"]
    main_driver = st.selectbox("PRIMARY PILOT", available_drivers, index=0)
    
    load_btn = st.button("INITIALIZE SYNC", use_container_width=True)

# Main Dashboard Header
st.markdown(f"""
    <div style="padding: 10px; border-bottom: 2px solid #333; margin-bottom: 30px;">
        <h1 style="margin:0; font-size: 2.5rem; letter-spacing: -1px;">{selected_gp.upper()}</h1>
        <p style="color: #ff1801; font-family: 'Orbitron'; letter-spacing: 4px;">SYSTEM STATUS: ONLINE // {selected_session.upper()}</p>
    </div>
""", unsafe_allow_html=True)

# Lógica de Datos
if load_btn or "summary_data" in st.session_state:
    if load_btn:
        st.session_state.summary_data = get_session_summary(selected_year, selected_gp, fastf1_session, main_driver)
        st.session_state.current_driver = main_driver
        st.session_state.telemetry_data = None

    summary = st.session_state.summary_data
    
    if "error" in summary:
        st.error(f"Error de origen de datos: {summary['error']}")
    else:
        tab1, tab2 = st.tabs(["📊 PERFORMANCE FEED", "📈 TELEMETRY OVERLAY"])

        with tab1:
            st.markdown(f"### <span style='color:#ff1801;'>//</span> DRIVER: {summary['Driver']}", unsafe_allow_html=True)
            
            # Grid de KPIs Dinámico
            c1, c2, c3, c4 = st.columns(4)
            with c1: render_kpi("FINISH POS", summary.get('FinalPosition', 'N/A'))
            
            # Adaptar métricas según lo que devuelva el backend
            if 'BestTime' in summary:
                with c2: render_kpi("BEST LAP", summary['BestTime'])
            elif 'FastestLap' in summary:
                with c2: render_kpi("FASTEST LAP", summary['FastestLap'])
            elif 'Q3_Time' in summary:
                with c2: render_kpi("Q3 TIME", summary.get('Q3_Time', 'N/A'))
            else:
                with c2: render_kpi("TIME", "N/A")
                
            if 'TotalLaps' in summary:
                with c3: render_kpi("TOTAL LAPS", summary['TotalLaps'])
            elif 'PositionsGained' in summary:
                with c3: render_kpi("POS GAINED", summary['PositionsGained'])
            elif 'Q1_Time' in summary:
                with c3: render_kpi("Q1 TIME", summary.get('Q1_Time', 'N/A'))
            else:
                with c3: render_kpi("LAPS", "N/A")
                
            if 'Strategy' in summary:
                with c4: render_kpi("STRATEGY", summary['Strategy'])
            elif 'PitStops' in summary:
                with c4: render_kpi("PIT STOPS", summary['PitStops'])
            elif 'Q2_Time' in summary:
                with c4: render_kpi("Q2 TIME", summary.get('Q2_Time', 'N/A'))
            else:
                with c4: render_kpi("INFO", "N/A")

            # Sección de Stints con diseño mejorado (solo si hay datos de stints)
            if 'Stints' in summary and summary['Stints']:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### TYRE LIFE & STINTS")
                st.dataframe(
                    pd.DataFrame(summary['Stints']).style.background_gradient(cmap='Reds', subset=['Laps']),
                    use_container_width=True
                )

        with tab2:
            st.markdown("### LIVE COMPARISON")
            
            c1, c2 = st.columns([3, 1])
            with c1:
                refs = st.multiselect("REFERENCE DRIVERS", [d for d in available_drivers if d != main_driver], default=["HAM"])
            with c2:
                st.markdown("<br>", unsafe_allow_html=True)
                compare_btn = st.button("RUN ANALYSIS", use_container_width=True)

            if compare_btn or st.session_state.telemetry_data is not None:
                if compare_btn:
                    st.session_state.telemetry_data = get_telemetry_data(selected_year, selected_gp, fastf1_session, main_driver, refs)
                
                df_plot = st.session_state.telemetry_data
                all_drivers = [main_driver] + refs
                
                fig = make_subplots(
                    rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.04, 
                    row_heights=[0.7, 0.3], subplot_titles=("SPEED (KM/H)", "THROTTLE %")
                )

                # Colores Neón F1
                neon_colors = ['#00F2FF', '#FF1801', '#9D4EDD', '#00FF41', '#FFFB00']
                
                for i, driver in enumerate(all_drivers):
                    d_df = df_plot[df_plot['Driver'] == driver]
                    color = neon_colors[i % len(neon_colors)]
                    
                    fig.add_trace(go.Scatter(
                        x=d_df['Distance'], y=d_df['Speed'], name=driver,
                        line=dict(color=color, width=2.5),
                        hovertemplate="%{y:.1f} km/h"
                    ), row=1, col=1)
                    
                    fig.add_trace(go.Scatter(
                        x=d_df['Distance'], y=d_df['Throttle'], name=driver,
                        line=dict(color=color, width=1.2, dash='dot'),
                        showlegend=False
                    ), row=2, col=1)

                fig.update_layout(
                    height=650, template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=30, b=0),
                    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
                    hovermode="x unified"
                )
                fig.update_xaxes(showgrid=True, gridcolor='#222')
                fig.update_yaxes(showgrid=True, gridcolor='#222')
                
                st.plotly_chart(fig, use_container_width=True)

else:
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 300px; border: 1px dashed #333; border-radius: 10px;">
            <p style="font-family: 'Orbitron'; color: #444; font-size: 1.2rem;">AWAITING DATA UPLOAD FROM PIT WALL...</p>
            <p style="color: #666;">Selecciona piloto en la barra lateral para iniciar.</p>
        </div>
    """, unsafe_allow_html=True)

# Footer Técnico
st.markdown(f"""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background: #000; padding: 5px; text-align: center; font-size: 0.7rem; color: #444; border-top: 1px solid #222;">
        v1.2.0 | ENGINE_LOAD: STABLE | DATA_SOURCE: FASTF1_FIA_API | ENCRYPTION: AES_256
    </div>
""", unsafe_allow_html=True)