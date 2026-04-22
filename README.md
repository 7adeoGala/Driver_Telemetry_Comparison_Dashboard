# Driver Telemetry Comparison Dashboard

Un sistema interactivo y escalable para el análisis de rendimiento en la Fórmula 1, diseñado para equipos permitiendo la extracción, procesamiento y visualización de datos de telemetría y tiempos de vuelta de sus pilotos, y compararlos con otros,utilizando la API de FastF1 para simular la obtención de datos de las distintas sesiones.

## Objetivo del Proyecto

Proveer una herramienta de análisis comparativo que permita a ingenieros y analistas evaluar el rendimiento de los pilotos en diferentes sesiones (Prácticas, Clasificación, Sprint, Carrera). El sistema está diseñado con una arquitectura modular para facilitar la futura integración de pronósticos basados en machine learning y análisis en tiempo real.

## Tecnologías

**Lenguaje:** Python 
**Ingesta de Datos:** `FastF1` --> Documentación: https://docs.fastf1.dev/index.html
**Procesamiento:** `Pandas`, `NumPy`
**Frontend/UI:** `Streamlit`
**Visualización:** `Plotly`, `Matplotlib`

## Características (MVP)

**Búsqueda Jerárquica:** Permitir una vez seleccionado el piloto a analizar, realizar un filtrado por distintas variables: Año > Gran Premio > Sesión.
**Análisis de Piloto Principal:** Resumen de tiempos de vuelta, sectores (S1, S2, S3) y neumáticos utilizados.
**Comparativa H2H (Head-to-Head):** Superposición de telemetría entre un piloto principal y pilotos de referencia.
**Telemetría Sincronizada:** Gráficos de Velocidad, Freno, Acelerador y Marchas en una determinada vuelta o sector
**Sistema de Caché:** Almacenamiento local de consultas para optimizar tiempos de carga y evitar la saturación de la API.
**Conclusiones y Reportes:** Generación de métricas de rendimiento, sugerencias de puesta a punto del vehículo, y facilitación en la toma de decisiones de los encargados o ingenieros de pista.

## Versiones

El desarrollo del proyecto está planteado en las siguientes fases evolutivas:

- **v1.0.0 - Estructura Funcional (Actual):** Utilización de la API de `FastF1` para simular la obtención de datos de sesiones de Fórmula 1. El objetivo es armar y validar toda la estructura base del sistema (extracción, procesamiento y visualización de telemetría).
- **v2.0.0 - Pronóstico y Entrenamiento:** Desarrollo, entrenamiento e integración de modelos de pronóstico (Machine Learning) sobre el flujo de datos consolidado en la versión inicial.
Contemplar la posibilidad de obtener datos mediante otras fuentes de datos, como por ejemplo grabaciones de video mediante webcams de los pilotos, y realizar comparativas con los datos obtenidos mediante FastF1.
- **v3.0.0 - Expansión Multicategoría:** Implementación y adaptación del sistema para consumir datos reales provenientes de distintas categorías de automovilismo, ampliando su alcance más allá de la Fórmula 1.

##  Estructura

La arquitectura sigue una separación de responsabilidades (Ingesta, Procesamiento, Presentación):

```text
f1-dashboard/
│
├── data/                   # Carpeta ignorada en git para la caché de FastF1
├── src/
│   ├── data_client.py      # Lógica de conexión y extracción (FastF1)
│   ├── processor.py        # Limpieza y transformación de datos (Pandas)
│   └── visualization.py    # Funciones generadoras de gráficos (Plotly)
│
├── app.py                  # Aplicación principal y UI (Streamlit)
├── requirements.txt        # Dependencias del proyecto
├── .gitignore              # Archivos a ignorar (entornos virtuales, caché)
└── README.md               # Documentación del proyecto
```

## Instalación

1. Crear el entorno virtual:

```bash
uv venv
```

2. Activar el entorno virtual:

```bash
uv .venv\Scripts\Activate
```

3. Instalar las dependencias:

```bash
uv pip install streamlit fastf1 plotly pandas numpy
```

4. Guardar las dependencias en el archivo requirements.txt:

```bash
uv pip freeze > requirements.txt
```

5. Ejecutar la aplicación:

```bash
streamlit run app.py
```
