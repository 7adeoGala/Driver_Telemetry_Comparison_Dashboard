# 🏎️ F1 Telemetry & Performance Dashboard

Un sistema interactivo y escalable para el análisis de rendimiento en la Fórmula 1, diseñado para equipos permitiendo la extracción, procesamiento y visualización de datos de telemetría y tiempos de vuelta de sus pilotos, y compararlos con otros,utilizando la API de FastF1 para simular la obtención de datos de las distintas sesiones.

## 🎯 Objetivo del Proyecto

Proveer una herramienta de análisis comparativo que permita a ingenieros y analistas evaluar el rendimiento de los pilotos en diferentes sesiones (Prácticas, Clasificación, Sprint, Carrera). El sistema está diseñado con una arquitectura modular para facilitar la futura integración de pronósticos basados en machine learning y análisis en tiempo real.

## ⚙️ Stack Tecnológico

**Lenguaje:** Python 
**Ingesta de Datos:** `FastF1`
**Procesamiento:** `Pandas`, `NumPy`
**Frontend/UI:** `Streamlit`
**Visualización:** `Plotly`, `Matplotlib`

## 🚀 Características (MVP)

**Búsqueda Jerárquica:** Filtrado estructurado por Año > Gran Premio > Sesión.
**Análisis de Piloto Principal:** Resumen de tiempos de vuelta, sectores (S1, S2, S3) y neumáticos utilizados.
**Comparativa H2H (Head-to-Head):** Superposición de telemetría entre un piloto principal y pilotos de referencia.
**Telemetría Sincronizada:** Gráficos de Velocidad, Freno, Acelerador y Marchas en una determinada vuelta o sector
**Sistema de Caché:** Almacenamiento local de consultas para optimizar tiempos de carga y evitar la saturación de la API.

## 🗺️ Roadmap (Futuras Implementaciones)

-   [ ] Integración de datos en tiempo real (Live Timing).
-   [ ] Modelos de pronóstico de degradación de neumáticos.
-   [ ] Soporte de extracción de datos para otras categorías del automovilismo.

## 📂 Estructura del Proyecto

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