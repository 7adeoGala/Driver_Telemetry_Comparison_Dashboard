import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIGURACIÓN E INYECCIÓN DE ESTILO ---
st.set_page_config(page_title="F1 STRATOS | Telemetry", page_icon="🏎️", layout="wide")

def load_custom_css():
        st.markdown("""
        <style>
        /* Importación de fuentes técnicas */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&family=JetBrains+Mono:wght@400;700&display=swap');

        /* Ocultar UI Genérica de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}

        :root {
            --f1-red: #ff1801;
            --f1-dark: #0f0f0f;
            --f1-green: #00ff41;
            --f1-purple: #9d4edd;
            --f1-yellow: #fffb00;
        }

        /* Contenedor Base */
        .stApp {
            background-color: var(--f1-dark);
            background-image: radial-gradient(circle at top right, rgba(255, 24, 1, 0.05), transparent 40%);
            color: #e0e0e0;
            font-family: 'Rajdhani', sans-serif;
        }

        /* Sidebar Estilo Panel de Control */
        section[data-testid="stSidebar"] {
            background-color: rgba(10, 10, 10, 0.98) !important;
            border-right: 1px solid #222;
            box-shadow: 5px 0 20px rgba(0,0,0,0.8);
        }

        /* Glassmorphism Cards */
        .big-kpi-box {
            background: rgba(30, 30, 30, 0.4);
            border-left: 3px solid var(--f1-red);
            padding: 15px;
            border-radius: 4px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.6);
            backdrop-filter: blur(8px);
            margin-bottom: 15px;
            border-top: 1px solid rgba(255,255,255,0.02);
            border-right: 1px solid rgba(255,255,255,0.02);
            border-bottom: 1px solid rgba(255,255,255,0.02);
            transition: all 0.3s ease;
        }
        .big-kpi-box:hover {
            background: rgba(40, 40, 40, 0.6);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 24, 1, 0.15);
        }
        .big-kpi-label {
            color: #777;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 700;
        }
        .big-kpi-value {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            color: #fff;
            margin-top: 5px;
            font-weight: 700;
        }

        /* Sector Ribbon */
        .mission-panel {
            background: rgba(20, 20, 20, 0.6);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .sector-ribbon {
            display: flex;
            width: 100%;
            height: 45px;
            border-radius: 4px;
            overflow: hidden;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.8);
        }
        .sector-segment {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 15px;
            border-right: 1px solid rgba(0,0,0,0.8);
        }
        .sector-segment:last-child { border-right: none; }
        .sec-green { background: linear-gradient(90deg, rgba(0, 255, 65, 0.1), rgba(0, 255, 65, 0.2)); border-bottom: 3px solid var(--f1-green); }
        .sec-purple { background: linear-gradient(90deg, rgba(157, 78, 221, 0.1), rgba(157, 78, 221, 0.2)); border-bottom: 3px solid var(--f1-purple); }
        .sec-yellow { background: linear-gradient(90deg, rgba(255, 251, 0, 0.1), rgba(255, 251, 0, 0.2)); border-bottom: 3px solid var(--f1-yellow); }
        .sec-label { font-weight: bold; font-size: 0.8rem; color: rgba(255,255,255,0.6); font-family: 'Orbitron', sans-serif;}
        .sec-time { font-family: 'JetBrains Mono', monospace; font-size: 1rem; color: #fff; font-weight: 700; }

        /* Strategy Timeline */
        .strat-line {
            display: flex;
            align-items: center;
            background: rgba(0,0,0,0.5);
            padding: 12px 20px;
            border-radius: 50px;
            overflow-x: auto;
            border: 1px solid rgba(255,255,255,0.05);
        }
        .tyre-dot {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            box-shadow: 0 0 8px rgba(255,255,255,0.3);
            border: 2px solid #222;
        }
        .S { background-color: #ff1801; }
        .M { background-color: #fffb00; }
        .H { background-color: #ffffff; }
        .I { background-color: #00ff41; }
        .W { background-color: #00aaff; }
        
        /* Estilo para los Tabs */
        .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: transparent; }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(20,20,20,0.8);
            border: 1px solid #333;
            color: #666;
            padding: 10px 25px;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.75rem;
            border-radius: 4px 4px 0 0;
            transition: all 0.2s;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #fff;
            background-color: rgba(40,40,40,0.8);
        }
        .stTabs [aria-selected="true"] {
            background-color: var(--f1-red) !important;
            color: white !important;
            border-color: var(--f1-red) !important;
            box-shadow: 0 -2px 10px rgba(255,24,1,0.2);
        }

        /* Botones de Acción */
        .stButton>button {
            background: transparent;
            color: var(--f1-red);
            border: 1px solid var(--f1-red);
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            padding: 15px;
            border-radius: 4px;
            transition: all 0.3s;
            font-weight: 700;
        }
        .stButton>button:hover {
            background: var(--f1-red);
            color: white;
            box-shadow: 0 0 20px rgba(255, 24, 1, 0.4);
            transform: scale(1.02);
        }

        /* Títulos */
        h1, h2, h3, h4 { font-family: 'Orbitron', sans-serif !important; font-weight: 900 !important; }
        </style>
        """, unsafe_allow_html=True)

# --- 2. HELPERS DE FORMATO ---
def format_time(time_str):
    if not time_str or time_str == "N/A" or pd.isna(time_str):
        return "--:--.---"
    try:
        parts = str(time_str).split(':')
        if len(parts) == 3:
            mins = int(parts[1])
            secs = parts[2]
            if mins == 0:
                return f"{secs}"
            return f"{mins}:{secs}"
        return str(time_str)
    except:
        return str(time_str)

def format_pos(pos_val):
    if not pos_val or pos_val == "N/A" or pd.isna(pos_val):
        return "N/A"
    try:
        return f"{int(float(pos_val))}°"
    except:
        return str(pos_val)

# --- 3. INTEGRACIÓN CON BACKEND ---
try:
    from src.processor import get_telemetry_data, get_session_summary
except ImportError:
    st.warning("Running in MOCK mode - Backend not found")
    def get_telemetry_data(year, gp, session, main_driver, ref_drivers):
        drivers = [main_driver] + ref_drivers
        all_data = []
        for driver in drivers:
            dist = np.linspace(0, 5000, 400)
            speed = 220 + 75 * np.sin(dist / 400) + np.random.normal(0, 2, 400)
            df = pd.DataFrame({
                'Driver': driver, 'Distance': dist, 'Speed': speed,
                'Throttle': np.clip(100 * np.sin(dist / 500) + 25, 0, 100),
                'Brake': np.random.choice([0, 1], 400), 'Gear': np.random.randint(4, 8, 400),
                'X': dist, 'Y': np.sin(dist / 100) * 500
            })
            all_data.append(df)
        return pd.concat(all_data)

    def get_session_summary(year, gp, session, driver):
        return {
            "SessionType": session, "Driver": driver, "FinalPosition": "1.0", "BestTime": "00:01:21.456", 
            "TotalLaps": 57, "Strategy": "S ➡️ M ➡️ H", "PitStops": 2, "PositionsGained": 2,
            "Sector1": "00:00:28.123", "Sector2": "00:00:29.456", "Sector3": "00:00:23.877",
            "TrackTemp": 35.5, "AirTemp": 22.1,
            "Stints": [{"Compound": "SOFT", "Laps": 18, "BestTime": "1:21.456"}]
        }

# --- 4. APLICACIÓN PRINCIPAL ---
load_custom_css()

@st.cache_data(ttl=86400)
def get_races(year):
    import fastf1
    try:
        schedule = fastf1.get_event_schedule(year)
        # Limpiamos nombres con acentos extraños y filtramos testing
        races = schedule[schedule['EventFormat'] != 'testing']['EventName'].tolist()
        return races
    except:
        # Fallback en caso de fallo de API
        return ["Bahrain Grand Prix", "Saudi Arabian Grand Prix", "Australian Grand Prix", "Monaco Grand Prix", "Silverstone"]

# Sidebar Setup
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#ff1801; font-size:2rem; letter-spacing:4px;'>DRIVER TELEMETRY COMPARISON</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    selected_year = st.selectbox("SEASON", [2024, 2023, 2022])
    
    # 1. Obtenemos los pilotos de esa temporada
    drivers_by_year = {
        2024: ["VER", "PER", "HAM", "RUS", "LEC", "SAI", "NOR", "PIA", "ALO", "STR", "GAS", "OCO", "ALB", "SAR", "COL", "TSU", "RIC", "LAW", "BOT", "ZHO", "MAG", "HUL", "BEA"],
        2023: ["VER", "PER", "HAM", "RUS", "LEC", "SAI", "NOR", "PIA", "ALO", "STR", "GAS", "OCO", "ALB", "SAR", "TSU", "DEV", "RIC", "LAW", "BOT", "ZHO", "MAG", "HUL"],
        2022: ["VER", "PER", "HAM", "RUS", "LEC", "SAI", "NOR", "RIC", "ALO", "OCO", "GAS", "TSU", "ALB", "LAT", "DEV", "STR", "HUL", "VET", "BOT", "ZHO", "MAG", "MSC"]
    }
    available_drivers = drivers_by_year.get(selected_year, ["VER", "HAM", "LEC", "NOR", "ALO"])
    
    # 2. El usuario elige el piloto
    main_driver = st.selectbox("DRIVER", available_drivers, index=0)
    
    # Mapeo estático de excepciones para filtrar los Grandes Premios
    driver_exceptions = {
        2024: {
            "BEA": ["Saudi Arabian Grand Prix", "Azerbaijan Grand Prix", "São Paulo Grand Prix"],
            "COL": ["Italian Grand Prix", "Azerbaijan Grand Prix", "Singapore Grand Prix", "United States Grand Prix", "Mexico City Grand Prix", "São Paulo Grand Prix", "Las Vegas Grand Prix", "Qatar Grand Prix", "Abu Dhabi Grand Prix"],
            "SAR": ["Bahrain Grand Prix", "Saudi Arabian Grand Prix", "Japanese Grand Prix", "Chinese Grand Prix", "Miami Grand Prix", "Emilia Romagna Grand Prix", "Monaco Grand Prix", "Canadian Grand Prix", "Spanish Grand Prix", "Austrian Grand Prix", "British Grand Prix", "Hungarian Grand Prix", "Belgian Grand Prix", "Dutch Grand Prix"],
            "LAW": ["United States Grand Prix", "Mexico City Grand Prix", "São Paulo Grand Prix", "Las Vegas Grand Prix", "Qatar Grand Prix", "Abu Dhabi Grand Prix"],
            "RIC": ["Bahrain Grand Prix", "Saudi Arabian Grand Prix", "Australian Grand Prix", "Japanese Grand Prix", "Chinese Grand Prix", "Miami Grand Prix", "Emilia Romagna Grand Prix", "Monaco Grand Prix", "Canadian Grand Prix", "Spanish Grand Prix", "Austrian Grand Prix", "British Grand Prix", "Hungarian Grand Prix", "Belgian Grand Prix", "Dutch Grand Prix", "Italian Grand Prix", "Azerbaijan Grand Prix", "Singapore Grand Prix"],
            "SAI": {"missed": ["Saudi Arabian Grand Prix"]},
            "MAG": {"missed": ["Azerbaijan Grand Prix", "São Paulo Grand Prix"]}
        },
        2023: {
            "DEV": ["Bahrain Grand Prix", "Saudi Arabian Grand Prix", "Australian Grand Prix", "Azerbaijan Grand Prix", "Miami Grand Prix", "Monaco Grand Prix", "Spanish Grand Prix", "Canadian Grand Prix", "Austrian Grand Prix", "British Grand Prix"],
            "RIC": ["Hungarian Grand Prix", "Belgian Grand Prix", "United States Grand Prix", "Mexico City Grand Prix", "São Paulo Grand Prix", "Las Vegas Grand Prix", "Abu Dhabi Grand Prix"],
            "LAW": ["Dutch Grand Prix", "Italian Grand Prix", "Singapore Grand Prix", "Japanese Grand Prix", "Qatar Grand Prix"],
            "STR": {"missed": ["Singapore Grand Prix"]}
        },
        2022: {
            "HUL": ["Bahrain Grand Prix", "Saudi Arabian Grand Prix"],
            "VET": {"missed": ["Bahrain Grand Prix", "Saudi Arabian Grand Prix"]},
            "DEV": ["Italian Grand Prix"],
            "ALB": {"missed": ["Italian Grand Prix"]}
        }
    }
    
    # 3. Obtenemos y filtramos los Grandes Premios según el piloto
    all_races_for_year = get_races(selected_year)
    exc = driver_exceptions.get(selected_year, {}).get(main_driver)
    
    if exc:
        if isinstance(exc, dict) and "missed" in exc:
            races_for_driver = [r for r in all_races_for_year if r not in exc["missed"]]
        else:
            races_for_driver = [r for r in all_races_for_year if r in exc]
    else:
        races_for_driver = all_races_for_year
        
    selected_gp = st.selectbox("GRAND PRIX", races_for_driver)
    
    # 4. El usuario elige la sesión
    selected_session = st.selectbox("SESSION", ["Practice 1", "Practice 2", "Qualy", "Race"])
    
    session_mapping = {
        "Practice 1": "FP1", "Practice 2": "FP2", 
        "Qualy": "Q", "Race": "R"
    }
    fastf1_session = session_mapping[selected_session]
    
    st.markdown("---")
    
    st.markdown("<br style='font-size:10px;'>", unsafe_allow_html=True)
    #st.markdown("<h2 style='text-align:center; color:#ff1801; font-size:2rem; letter-spacing:4px;'>DRIVER TELEMETRY COMPARISON</h2>", unsafe_allow_html=True)
    load_btn = st.button("OBTAIN DATA", use_container_width=True)

# --- Lógica de Estado y Sincronización ---
main_container = st.empty()

if load_btn:
    st.session_state.is_syncing = True
    st.session_state.active_year = selected_year
    st.session_state.active_gp = selected_gp
    st.session_state.active_session = fastf1_session
    st.session_state.active_session_name = selected_session
    st.session_state.active_driver = main_driver
    st.session_state.telemetry_data = None
    st.rerun()

if st.session_state.get('is_syncing', False):
    st.markdown("""
        <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: rgba(15, 15, 15, 0.98); z-index: 999999; display: flex; flex-direction: column; align-items: center; justify-content: center; backdrop-filter: blur(5px);">
            <div style="width: 80px; height: 80px; border: 4px solid var(--f1-red); border-top: 4px solid transparent; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 30px;"></div>
            <h1 style="font-family: 'Orbitron'; color: var(--f1-red); font-size: 2.5rem; letter-spacing: 5px; margin-bottom: 10px; text-align: center;">GATHERING SESSION INFORMATION...</h1>
            <p style="color: #aaa; font-family: 'JetBrains Mono'; font-size: 1.2rem; text-align: center;">DOWNLOADING ENCRYPTED TELEMETRY PACKETS</p>
        </div>
        <style>@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>
    """, unsafe_allow_html=True)
    
    st.session_state.summary_data = get_session_summary(
        st.session_state.active_year, 
        st.session_state.active_gp, 
        st.session_state.active_session, 
        st.session_state.active_driver
    )
    
    st.session_state.is_syncing = False
    st.rerun()

elif "summary_data" in st.session_state and st.session_state.summary_data is not None:
    main_container.empty()
    with main_container.container():
        # Usamos las variables activas para que el dashboard no mute si el usuario toca el sidebar sin sincronizar
        disp_gp = st.session_state.get('active_gp', selected_gp)
        disp_session = st.session_state.get('active_session_name', selected_session)
    
        st.markdown(f"""
            <div style="padding: 10px 0; border-bottom: 1px solid #333; margin-bottom: 25px;">
                <h1 style="margin:0; font-size: 3rem; letter-spacing: 2px; text-transform: uppercase;">{disp_gp}</h1>
                <p style="color: #ff1801; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; letter-spacing: 2px; margin-top: 5px;">
                    > SYSTEM STATUS: ONLINE // {disp_session.upper()}
                </p>
            </div>
        """, unsafe_allow_html=True)

        summary = st.session_state.summary_data
    
        if "error" in summary:
            st.error(f"DATA_ERROR: {summary['error']}")
        else:
            tab1, tab2, tab3 = st.tabs(["PERFORMANCE", "TELEMETRY", "TRACK MAP"])

            with tab1:
                # 1. LOGICA DE EXTRACCIÓN DE TIEMPO RESILIENTE
                best_lap_val = summary.get('BestTime')
                if not best_lap_val or best_lap_val == "N/A":
                    q3 = summary.get('Q3_Time')
                    q2 = summary.get('Q2_Time')
                    q1 = summary.get('Q1_Time')
                    best_lap_val = q3 if q3 and q3 != "N/A" else (q2 if q2 and q2 != "N/A" else q1)
                if not best_lap_val or best_lap_val == "N/A":
                    best_lap_val = summary.get('FastestLap', "N/A")

                # 2. RENDERIZADO DE KPIs
                st.markdown(f"<h3 style='margin-bottom:20px;'><span style='color:var(--f1-red);'>//</span> DRIVER ANALYSIS: {summary.get('Driver', 'UNK')}</h3>", unsafe_allow_html=True)
            
                session_type = summary.get('SessionType', 'R')
                is_race = session_type == 'R'
                is_practice = session_type in ['FP1', 'FP2', 'FP3']
                is_qualy = session_type == 'Q'
            
                if is_race:
                    c_pos, c_time, c_delta, c_pits = st.columns(4)
                elif is_qualy:
                    c_pos, c_time = st.columns(2)
                else: # Practice
                    c_time = st.columns(1)[0]
            
                if not is_practice:
                    with c_pos:
                        pos_formatted = format_pos(summary.get('FinalPosition', 'N/A'))
                        pos_label = "Final Position" if is_race else "Qualy Position"
                        st.markdown(f"""<div class="big-kpi-box"><div class="big-kpi-label">{pos_label}</div><div class="big-kpi-value">{pos_formatted}</div></div>""", unsafe_allow_html=True)
            
                with c_time:
                    st.markdown(f"""<div class="big-kpi-box"><div class="big-kpi-label">Best Lap</div><div class="big-kpi-value">{format_time(best_lap_val)}</div></div>""", unsafe_allow_html=True)
            
                if is_race:
                    with c_delta:
                        gain = summary.get('PositionsGained', 'N/A')
                        if gain != 'N/A':
                            color = "var(--f1-green)" if int(gain) >= 0 else "var(--f1-red)"
                            val = f"+{gain}" if int(gain) >= 0 else str(gain)
                        else:
                            color = "#777"
                            val = "---"
                        st.markdown(f"""<div class="big-kpi-box"><div class="big-kpi-label">Pos. Delta</div><div class="big-kpi-value" style="color:{color}">{val}</div></div>""", unsafe_allow_html=True)
                
                    with c_pits:
                        pits_val = summary.get('PitStops')
                        pits_str = str(pits_val) if pits_val is not None else "0"
                        st.markdown(f"""<div class="big-kpi-box"><div class="big-kpi-label">Pit Stops</div><div class="big-kpi-value">{pits_str}</div></div>""", unsafe_allow_html=True)

                # 3. SECTOR RIBBON
                # Lógica para determinar color de sector basada en disponibilidad (simulación visual)
                sec1 = format_time(summary.get('Sector1'))
                sec2 = format_time(summary.get('Sector2'))
                sec3 = format_time(summary.get('Sector3'))
            
                # Asignamos clases de color basadas en datos (o estático para look F1 si no hay lógica de récord)
                st.markdown(f"""
                    <div class="mission-panel">
                        <div class="big-kpi-label" style="margin-bottom:12px;">Sector Breakdown (Best Lap)</div>
                        <div class="sector-ribbon">
                            <div class="sector-segment sec-green">
                                <span class="sec-label">S1</span><span class="sec-time">{sec1}</span>
                            </div>
                            <div class="sector-segment sec-purple">
                                <span class="sec-label">S2</span><span class="sec-time">{sec2}</span>
                            </div>
                            <div class="sector-segment sec-yellow">
                                <span class="sec-label">S3</span><span class="sec-time">{sec3}</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # 4. STRATEGY TIMELINE
                if is_race:
                    strat_str = summary.get('Strategy', '')
                    if strat_str and strat_str != "N/A":
                        steps = strat_str.split('➡️')
                        html_steps = []
                        for i, step in enumerate(steps):
                            s = step.strip()
                            t_class = s[0] if s else "S"
                            step_html = f'<div style="display:inline-flex; align-items:center;"><div class="tyre-dot {t_class}"></div><span style="font-family:\'JetBrains Mono\'; font-size:1rem; font-weight:bold;">{s}</span></div>'
                            html_steps.append(step_html)
                    
                        strat_inner_html = '<span style="color:#666; margin: 0 15px;">❯</span>'.join(html_steps)
                        st.markdown(f'<div class="mission-panel"><div class="big-kpi-label" style="margin-bottom:15px;">Tyre Life & Strategy</div><div class="strat-line">{strat_inner_html}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="mission-panel"><div class="big-kpi-label" style="margin-bottom:15px;">Tyre Life & Strategy</div><div class="strat-line"><span style="color:#666; font-family:\'JetBrains Mono\';">NO STRATEGY DATA</span></div></div>', unsafe_allow_html=True)

                # 5. AMBIENT DATA
                c_track, c_air, _ = st.columns([1, 1, 2])
                with c_track:
                    st.markdown(f"""<div class="mission-panel" style="padding:15px;"><div class="big-kpi-label">Track Temp</div><div style="font-family:Orbitron; font-size:1.8rem; font-weight:700; margin-top:5px;">{summary.get('TrackTemp', '--')}°C</div></div>""", unsafe_allow_html=True)
                with c_air:
                    st.markdown(f"""<div class="mission-panel" style="padding:15px;"><div class="big-kpi-label">Air Temp</div><div style="font-family:Orbitron; font-size:1.8rem; font-weight:700; margin-top:5px;">{summary.get('AirTemp', '--')}°C</div></div>""", unsafe_allow_html=True)

            with tab2:
                st.markdown("### <span style='color:var(--f1-red);'>//</span> LIVE TELEMETRY COMPARISON", unsafe_allow_html=True)
            
                c1, c2 = st.columns([3, 1])
                with c1:
                    refs = st.multiselect("REFERENCE DRIVERS", [d for d in available_drivers if d != st.session_state.get('active_driver', main_driver)], default=["HAM"])
                with c2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    compare_btn = st.button("RUN ANALYSIS", use_container_width=True)

                if compare_btn or st.session_state.telemetry_data is not None:
                    if compare_btn:
                        with st.spinner("Conectando con Pit Wall y procesando telemetría... (1-2 min)"):
                            st.session_state.telemetry_data = get_telemetry_data(
                                st.session_state.get('active_year', selected_year), 
                                st.session_state.get('active_gp', selected_gp), 
                                st.session_state.get('active_session', fastf1_session), 
                                st.session_state.get('active_driver', main_driver), 
                                refs
                            )
                
                    df_plot = st.session_state.telemetry_data
                    all_drivers = [st.session_state.get('active_driver', main_driver)] + refs
                
                    fig = make_subplots(
                        rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.04, 
                        row_heights=[0.5, 0.25, 0.25], subplot_titles=("SPEED (KM/H)", "THROTTLE %", "GEAR")
                    )

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
                            line=dict(color=color, width=1.5, dash='dot'),
                            showlegend=False
                        ), row=2, col=1)
                    
                        fig.add_trace(go.Scatter(
                            x=d_df['Distance'], y=d_df['Gear'], name=driver,
                            line=dict(color=color, width=1.5, shape='hv'),
                            showlegend=False
                        ), row=3, col=1)

                    fig.update_layout(
                        height=700, template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=0, r=0, t=30, b=0),
                        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
                        hovermode="x unified",
                        font=dict(family="Rajdhani", size=12)
                    )
                    fig.update_xaxes(showgrid=True, gridcolor='#222')
                    fig.update_yaxes(showgrid=True, gridcolor='#222')
                
                    st.plotly_chart(fig, use_container_width=True)

            with tab3:
                st.markdown("### <span style='color:var(--f1-red);'>//</span> TRACK MAP (X/Y SPATIAL)", unsafe_allow_html=True)
                if st.session_state.telemetry_data is not None:
                    df_plot = st.session_state.telemetry_data
                    map_fig = go.Figure()
                
                    neon_colors = ['#00F2FF', '#FF1801', '#9D4EDD', '#00FF41', '#FFFB00']
                    unique_drivers = df_plot['Driver'].unique()
                
                    for i, driver in enumerate(unique_drivers):
                        d_df = df_plot[df_plot['Driver'] == driver]
                        color = neon_colors[i % len(neon_colors)]
                    
                        if 'X' in d_df.columns and 'Y' in d_df.columns and not d_df['X'].isna().all():
                            map_fig.add_trace(go.Scatter(
                                x=d_df['X'], y=d_df['Y'], name=driver,
                                mode='lines',
                                line=dict(color=color, width=3),
                                hovertemplate="Driver: " + driver + "<br>Speed: %{customdata[0]:.1f} km/h<br>Gear: %{customdata[1]}",
                                customdata=d_df[['Speed', 'Gear']]
                            ))
                
                    map_fig.update_layout(
                        height=700, template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=0, r=0, t=30, b=0),
                        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
                        font=dict(family="Rajdhani", size=14)
                    )
                    map_fig.update_yaxes(scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False, visible=False)
                    map_fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
                
                    st.plotly_chart(map_fig, use_container_width=True)
                else:
                    st.info(">> PLEASE INITIALIZE TELEMETRY SYNC IN THE 'TELEMETRY OVERLAY' TAB.")

else:
    with main_container.container():
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 60vh; border: 1px dashed #333; border-radius: 10px; background: rgba(0,0,0,0.3);">
            <div style="width: 50px; height: 50px; border: 3px solid var(--f1-red); border-top: 3px solid transparent; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 20px;"></div>
            <p style="font-family: 'Orbitron'; color: var(--f1-red); font-size: 1.5rem; letter-spacing: 3px;">AWAITING PIT WALL SYNC...</p>
            <p style="color: #666; font-family: 'JetBrains Mono';">SELECT PARAMETERS ON TERMINAL AND INITIALIZE.</p>
        </div>
            <style>@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>
        """, unsafe_allow_html=True)