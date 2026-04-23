import fastf1
import streamlit as st

@st.cache_resource(ttl=3600)
def get_session_data(year: int, gp: str, session: str) -> fastf1.core.Session:
    """
    Descarga y carga la información de telemetría de una sesión de F1.
    
    Args:
        year (int): El año del campeonato (ej. 2023).
        gp (str): El nombre o ubicación del Gran Premio (ej. 'Monza').
        session (str): El identificador de la sesión (ej. 'FP1', 'Q', 'R').
        
    Returns:
        fastf1.core.Session: El objeto de sesión cargado.
    """
    try:
        f1_session = fastf1.get_session(year, gp, session)
        # Descargamos solo lo estrictamente necesario en RAM (sin guardar a disco)
        f1_session.load(telemetry=True, weather=True, messages=False)
        return f1_session
    except Exception as e:
        print(f"Error cargando los datos de la sesión: {e}")
        raise e
