import pandas as pd
from src.data_client import get_session_data

def get_telemetry_data(year: int, gp: str, session: str, main_driver: str, ref_drivers_list: list) -> pd.DataFrame:
    """
    Obtiene y procesa los datos de telemetría para la vuelta más rápida de los pilotos indicados.
    
    Args:
        year (int): El año del campeonato.
        gp (str): El nombre o ubicación del Gran Premio.
        session (str): El identificador de la sesión (ej. 'FP1', 'Q', 'R').
        main_driver (str): El código de 3 letras del piloto principal (ej. 'VER').
        ref_drivers_list (list): Lista de códigos de pilotos de referencia (ej. ['LEC', 'SAI']).
        
    Returns:
        pd.DataFrame: Un único DataFrame con la telemetría concatenada de todos los pilotos.
                      Contrato de Datos Estricto: Driver, Distance, Speed, Throttle, Brake, Gear.
    """
    # 1. Ingesta: cargar datos de la sesión
    f1_session = get_session_data(year, gp, session)
    
    # Combinar piloto principal y referencias sin duplicados
    drivers_to_process = [main_driver] + ref_drivers_list
    drivers_to_process = list(dict.fromkeys(drivers_to_process))
    
    all_telemetry = []
    
    for driver in drivers_to_process:
        try:
            # Manejo de Errores: Validar que el piloto participó en la sesión
            if driver not in f1_session.results['Abbreviation'].values:
                print(f"Advertencia: El piloto {driver} no participó en esta sesión. Omitiendo.")
                continue
                
            # Aislar las vueltas del piloto
            driver_laps = f1_session.laps.pick_driver(driver)
            if driver_laps.empty:
                print(f"Advertencia: No se encontraron vueltas válidas para el piloto {driver}. Omitiendo.")
                continue
                
            # Extraer la vuelta más rápida
            fastest_lap = driver_laps.pick_fastest()
            if pd.isna(fastest_lap['LapTime']):
                print(f"Advertencia: La vuelta más rápida de {driver} es inválida (NaN). Omitiendo.")
                continue
            
            # Extraer telemetría
            telemetry = fastest_lap.get_telemetry()
            
            # CRÍTICO: Asegurarse de añadir/calcular la distancia mediante el método de fastf1
            # get_telemetry() la trae por defecto en las versiones recientes, pero lo validamos
            if 'Distance' not in telemetry.columns or telemetry['Distance'].isna().all():
                telemetry = telemetry.add_distance()
            
            # Seleccionar las columnas estándar de FastF1 requeridas para la transformación
            cols_to_keep = ['Distance', 'Speed', 'Throttle', 'Brake', 'nGear']
            
            # Validar que no falten datos inesperados en la API
            missing_cols = [col for col in cols_to_keep if col not in telemetry.columns]
            if missing_cols:
                print(f"Advertencia: Faltan las columnas {missing_cols} en la telemetría de {driver}. Omitiendo.")
                continue
                
            telemetry = telemetry[cols_to_keep].copy()
            
            # Renombrar 'nGear' a 'Gear' para cumplir el contrato
            telemetry.rename(columns={'nGear': 'Gear'}, inplace=True)
            
            # Añadir la columna del piloto
            telemetry['Driver'] = driver
            
            # Asegurar que Brake sea 1/0 en lugar de booleano
            telemetry['Brake'] = telemetry['Brake'].astype(int)
            
            # Reordenar las columnas exactamente como lo exige el contrato con el Frontend
            telemetry = telemetry[['Driver', 'Distance', 'Speed', 'Throttle', 'Brake', 'Gear']]
            
            all_telemetry.append(telemetry)
            
        except Exception as e:
            print(f"Error procesando los datos del piloto {driver}: {e}")
            continue
            
    # Concatenar la telemetría en un único DataFrame consolidado
    if all_telemetry:
        final_df = pd.concat(all_telemetry, ignore_index=True)
    else:
        # Retornar un dataframe vacío respetando el contrato en caso de no haber datos en absoluto
        final_df = pd.DataFrame(columns=['Driver', 'Distance', 'Speed', 'Throttle', 'Brake', 'Gear'])
    
    return final_df

def get_session_summary(year: int, gp: str, session: str, driver: str) -> dict:
    """
    Extrae métricas resumidas de la sesión para un piloto específico,
    dependiendo del tipo de sesión.
    """
    try:
        f1_session = get_session_data(year, gp, session)
        
        if driver not in f1_session.results['Abbreviation'].values:
            return {"error": f"El piloto {driver} no participó en esta sesión."}
            
        driver_results = f1_session.results[f1_session.results['Abbreviation'] == driver].iloc[0]
        driver_laps = f1_session.laps.pick_driver(driver)
        
        summary = {
            "SessionType": session,
            "Driver": driver
        }
        
        # Prácticas (FP1, FP2, FP3)
        if session in ['FP1', 'FP2', 'FP3']:
            summary['TotalLaps'] = len(driver_laps)
            
            fastest_lap = driver_laps.pick_fastest()
            summary['BestTime'] = "N/A" if pd.isna(fastest_lap.get('LapTime')) else str(fastest_lap['LapTime']).split(' ')[-1][:-3]
            
            summary['FinalPosition'] = driver_results.get('Position', 'N/A')
            
            # Stints / Neumáticos
            stints = []
            if not driver_laps.empty:
                for stint, group in driver_laps.groupby('Stint'):
                    compound = group['Compound'].iloc[0]
                    laps_count = len(group)
                    stint_fastest = group.pick_fastest()
                    stint_time = "N/A" if pd.isna(stint_fastest.get('LapTime')) else str(stint_fastest['LapTime']).split(' ')[-1][:-3]
                    stints.append({"Stint": int(stint), "Compound": compound, "Laps": laps_count, "BestTime": stint_time})
            summary['Stints'] = stints

        # Clasificación (Q)
        elif session == 'Q':
            summary['FinalPosition'] = driver_results.get('Position', 'N/A')
            
            for q_session in ['Q1', 'Q2', 'Q3']:
                time = driver_results.get(q_session, pd.NaT)
                summary[f'{q_session}_Time'] = "N/A" if pd.isna(time) else str(time).split(' ')[-1][:-3]

        # Carrera (R, SQ, SR)
        else:
            summary['FinalPosition'] = driver_results.get('Position', 'N/A')
            
            grid_pos = driver_results.get('GridPosition', 'N/A')
            if pd.notna(grid_pos) and pd.notna(summary['FinalPosition']):
                summary['PositionsGained'] = int(grid_pos - summary['FinalPosition'])
            else:
                summary['PositionsGained'] = "N/A"
            
            fastest_lap = driver_laps.pick_fastest()
            summary['FastestLap'] = "N/A" if pd.isna(fastest_lap.get('LapTime')) else str(fastest_lap['LapTime']).split(' ')[-1][:-3]
            
            # Estrategia de paradas
            strategy = []
            if not driver_laps.empty:
                for stint, group in driver_laps.groupby('Stint'):
                    comp = group['Compound'].iloc[0]
                    if pd.notna(comp):
                        strategy.append(str(comp))
            summary['Strategy'] = " ➡️ ".join(strategy) if strategy else "N/A"
            summary['PitStops'] = max(0, len(strategy) - 1)
            
        return summary
    except Exception as e:
        print(f"Error extrayendo resumen de sesión: {e}")
        return {"error": str(e)}
