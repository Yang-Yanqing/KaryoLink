import streamlit as st

st.set_page_config(page_title="KaryoLink – Arquitectura (versión mejorada)", layout="centered")

st.title("Arquitectura mejorada – Plataforma KaryoLink")

st.markdown(
    """
La arquitectura se amplía con **siete mejoras clave** para preparar la plataforma hacia un entorno profesional y seguro:

1. **Almacenamiento centralizado en Object Storage (S3 / GCS / MinIO)**  
   Las imágenes normalizadas se guardan fuera de la base de datos, y solo se almacenan rutas y metadatos.

2. **Servicio de tareas asíncronas (Celery / RQ / RabbitMQ)**  
   Permite procesar análisis de IA en segundo plano y notificar progreso al usuario.

3. **Capa de seguridad y cumplimiento (Data Gateway)**  
   Valida el archivo, verifica autenticación y elimina información sensible antes de guardarlo.

4. **Sistema de auditoría y trazabilidad**  
   Cada paso (subida, inferencia, informe) se registra con usuario, tiempo y estado.

5. **Capa de caché (Redis)**  
   Guarda estados intermedios y acelera la recuperación de resultados o progreso de tareas.

6. **Consistencia de datos mediante un ID único (`job_id`)**  
   Todas las entidades (imagen, inferencia, informe) se vinculan por el mismo identificador.

7. **Generación de informes en dos fases**  
   Primero JSON estructurado (para análisis/estadísticas) y luego PDF bajo demanda.
"""
)

dot = r"""
digraph KaryoLink {
    rankdir=TB;
    fontsize=10;
    node [shape=rect, style="rounded,filled", fontname="Helvetica"];

    // --------- Nodos principales ---------
    tecnico      [label="Técnico\n(Usuario)", fillcolor="#BBDEFB"];
    auth         [label="Autenticación / Control de acceso\n(SSO / Token)", fillcolor="#C5CAE9"];
    frontend     [label="Frontend\n(React / Streamlit)", fillcolor="#E3F2FD"];
    datagw       [label="Data Gateway\n(Validación / Cumplimiento / Desidentificación)", fillcolor="#B3E5FC"];
    upload       [label="Upload API\n(FastAPI)", fillcolor="#E3F2FD"];
    queue        [label="Cola de tareas asíncronas\n(Celery / RQ / RabbitMQ)", fillcolor="#FFECB3"];
    preprocess   [label="Preprocesamiento\n(Normalización / limpieza)", fillcolor="#FFF9C4"];
    storage      [label="Object Storage\n(Imagen normalizada)", fillcolor="#FFCCBC"];
    mongo        [label="MongoDB\n(Metadatos / rutas / autor / job_id)", fillcolor="#FFCCBC"];
    redis        [label="Redis\n(Cache / Estado de tareas)", fillcolor="#C8E6C9"];
    ia           [label="Servicio de IA\n(Inferencia con imágenes normalizadas)", fillcolor="#FFE082"];
    postprocess  [label="Postprocesamiento\n(Limpieza / validación / etiquetas)", fillcolor="#FFE0B2"];
    report_json  [label="Generación de informe JSON\n(Estructura estructurada)", fillcolor="#E1BEE7"];
    report_pdf   [label="Conversión a PDF\n(Plantilla institucional)", fillcolor="#CE93D8"];
    postgres     [label="PostgreSQL\n(Resultados estructurados / auditoría)", fillcolor="#C8E6C9"];
    audit        [label="Registro de auditoría\n(Eventos / tiempos / usuario)", fillcolor="#FFCDD2"];
    frontend_rep [label="Frontend\n(Vista de informe / descarga PDF)", fillcolor="#D1C4E9"];

    // --------- Flujo de entrada ---------
    subgraph cluster_input {
        label="Flujo de entrada: imagen del cariotipo";
        style="dashed";
        color="#90CAF9";

        tecnico -> auth -> frontend -> datagw -> upload -> queue -> preprocess;
        preprocess -> storage    [label=" guardar imagen normalizada "];
        preprocess -> mongo      [label=" guardar metadatos / ruta / job_id "];
        preprocess -> redis      [label=" estado temporal "];
        queue -> ia              [label=" leer desde Object Storage y MongoDB "];
    }

    // --------- Flujo de salida ---------
    subgraph cluster_output {
        label="Flujo de salida: informe generado";
        style="dashed";
        color="#CE93D8";

        ia -> postprocess [label=" resultados brutos "];
        postprocess -> report_json [label=" resultados limpios "];
        report_json -> report_pdf  [label=" conversión a PDF bajo demanda "];
        report_json -> postgres    [label=" guardar resultados estructurados "];
        report_pdf -> postgres     [label=" guardar metadatos de archivo "];
    }

    // --------- Auditoría y visualización ---------
    postgres -> frontend_rep [label=" consultar resultados / descarga PDF "];
    datagw -> audit          [label=" registrar acceso / subida "];
    ia -> audit              [label=" registrar inferencia "];
    report_pdf -> audit      [label=" registrar generación de informe "];
}
"""

st.subheader("Diagrama de alto nivel con mejoras (seguridad, asíncrono, auditoría)")
st.graphviz_chart(dot)

st.caption(
    "Versión ampliada del esquema conceptual incorporando las 7 mejoras: seguridad, tareas asíncronas, almacenamiento externo, "
    "auditoría, caché, consistencia de datos y generación estructurada de informes."
)
