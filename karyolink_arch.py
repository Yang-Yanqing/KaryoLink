import streamlit as st

st.set_page_config(page_title="KaryoLink – Arquitectura", layout="centered")

st.title("Arquitectura propuesta para la plataforma KaryoLink")

st.markdown(
    """
La idea es ver la plataforma como **dos flujos principales**:

- **Flujo de entrada:** la imagen del cariotipo entra en el sistema, se prepara y se analiza con IA.  
- **Flujo de salida:** los resultados de la IA se limpian, se validan y se convierten en un informe estructurado (JSON / PDF).

El diagrama de abajo es solo un esquema conceptual para discutir juntos la arquitectura.
"""
)

dot = r"""
digraph KaryoLink {
    rankdir=TB;
    fontsize=10;
    node [shape=rect, style="rounded,filled", fontname="Helvetica"];

    tecnico      [label="Técnico\n(Usuario)", fillcolor="#BBDEFB"];
    frontend     [label="Frontend\n(React / Streamlit)", fillcolor="#E3F2FD"];
    upload       [label="Upload API\n(FastAPI)", fillcolor="#E3F2FD"];

    preprocess   [label="Preprocesamiento\n(Normalización / limpieza)", fillcolor="#FFF9C4"];

    storage      [label="Object Storage (S3)\n(Imagen normalizada)", fillcolor="#FFCCBC"];
    mongo        [label="MongoDB\n(Metadatos del proceso\n(task_id / S3_path / estado))", fillcolor="#FFCCBC"];

    ia           [label="Servicio de IA (GPU)\n(Lee imagen desde S3)", fillcolor="#FFE082"];

    postprocess  [label="Postprocesamiento\n(Limpieza / validación)", fillcolor="#FFE0B2"];
    report       [label="Generación de informe\n(JSON / PDF)", fillcolor="#E1BEE7"];

    postgres     [label="PostgreSQL\n(Resultados estructurados)", fillcolor="#C8E6C9"];
    frontend_rep [label="Frontend\n(Vista de informe / descarga PDF)", fillcolor="#D1C4E9"];


    // Entrada
    tecnico    -> frontend   [label=" subir imagen "];
    frontend   -> upload;
    upload     -> preprocess;

    preprocess -> storage   [label=" guardar en S3 "];
    preprocess -> mongo     [label=" crear task\n(S3_path)"];

    mongo -> ia [label=" leer S3_path\npara inferencia "];

    // Salida
    ia          -> postprocess [label=" resultados brutos "];
    postprocess -> report      [label=" resultados limpios "];
    report      -> postgres    [label=" guardar informe "];
    postgres    -> frontend_rep[label=" mostrar informe\n/ descargar PDF "];

    report      -> mongo       [style=dashed, label=" actualizar task: done "];
}
"""




st.subheader("Diagrama de alto nivel (dos flujos: entrada y salida)")
st.graphviz_chart(dot)

st.caption(
    "Esquema conceptual para discutir la arquitectura: flujo de entrada (imagen) "
    "y flujo de salida (informe de IA). Los detalles se pueden ajustar según el modelo y los requisitos médicos."
)
