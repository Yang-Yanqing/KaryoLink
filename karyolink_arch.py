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

    // Nodos principales
    tecnico      [label="Técnico\n(Usuario)", fillcolor="#BBDEFB"];
    frontend     [label="Frontend\n(React / Streamlit)", fillcolor="#E3F2FD"];
    upload       [label="Upload API\n(FastAPI)", fillcolor="#E3F2FD"];
    preprocess   [label="Preprocesamiento\n(Normalización / limpieza)", fillcolor="#FFF9C4"];

    // Almacenamiento de imagen / metadatos
    storage      [label="Object Storage\n(Imagen normalizada) (?)", fillcolor="#FFCCBC"];
    mongo        [label="MongoDB\n(Metadatos / rutas / autor)", fillcolor="#FFCCBC"];

    // IA y salida
    ia           [label="Servicio de IA\n(Inferencia desde MongoDB)", fillcolor="#FFE082"];
    postprocess  [label="Postprocesamiento\n(Limpieza / validación / etiquetas)", fillcolor="#FFE0B2"];
    report       [label="Generación de informe\n(Estructura JSON / PDF)", fillcolor="#E1BEE7"];
    postgres     [label="PostgreSQL\n(Resultados estructurados)", fillcolor="#C8E6C9"];
    frontend_rep [label="Frontend\n(Vista de informe / descarga PDF)", fillcolor="#D1C4E9"];

    // --------- Flujo de entrada ---------
    subgraph cluster_input {
        label="Flujo de entrada: imagen del cariotipo";
        style="dashed";
        color="#90CAF9";

        tecnico    -> frontend   [label=" subir imagen "];
        frontend   -> upload;
        upload     -> preprocess;

        // Desde preprocesamiento: guardar imagen normalizada (opcional) y metadatos
        preprocess -> storage    [label=" guardar imagen\nnormalizada (?) "];
        preprocess -> mongo      [label=" ruta / metadatos "];

        // IA consume los datos desde MongoDB / ruta
        mongo      -> ia         [label=" leer datos\npara inferencia "];
    }

    // --------- Flujo de salida ---------
    subgraph cluster_output {
        label="Flujo de salida: informe generado";
        style="dashed";
        color="#CE93D8";

        ia          -> postprocess [label=" resultados brutos "];
        postprocess -> report      [label=" resultados limpios "];
        report      -> postgres    [label=" guardar resultados "];
    }

    // --------- Resultados -> vista en frontend ---------
    postgres -> frontend_rep [label=" consultar resultados\npara mostrar informe "];
}
"""



st.subheader("Diagrama de alto nivel (dos flujos: entrada y salida)")
st.graphviz_chart(dot)

st.caption(
    "Esquema conceptual para discutir la arquitectura: flujo de entrada (imagen) "
    "y flujo de salida (informe de IA). Los detalles se pueden ajustar según el modelo y los requisitos médicos."
)
