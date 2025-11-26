import streamlit as st

st.set_page_config(
    page_title="Plan de Alto Nivel – KaryoLink",
    layout="centered"
)

st.title("Plan de Alto Nivel para KaryoLink 🧬")

st.markdown(
    """
El objetivo de esta página es presentar de forma **clara y visual**
mi propuesta sobre el ritmo de trabajo durante las primeras semanas
del proyecto y el estilo de colaboración que sugiero para el equipo.

---

## 🎯 Objetivo general

Construir un **MVP funcional** capaz de:

- Recibir y subir imágenes de cariotipos  
- Pasar por un pipeline completo: **preprocesamiento (equipo externo) → IA → postprocesamiento**  
- Generar un informe estructurado (JSON / PDF) y visualizarlo en la interfaz  
- Mantener una base sólida para futuras ampliaciones (roles, multiusuario, entorno clínico)

"""
)

st.markdown("---")

st.subheader("📆 Plan de trabajo (visión general)")

st.markdown(
    """
El ritmo real puede variar según las prioridades del equipo y la disponibilidad
del módulo de preprocesamiento.  
Este plan está pensado como una propuesta lógica para organizar las primeras semanas.
"""
)

dot = r"""
digraph PlanKaryoLink {
    rankdir=TB;
    fontsize=11;
    node [shape=rect, style="rounded,filled", fontname="Helvetica", fontsize=11, color="#333333"];

    inicio  [label="Inicio\n(si decidimos comenzar ahora)", fillcolor="#FFF7D6"];
    semana1 [label="Semana 1\nBase del MVP\nStreamlit + FastAPI", fillcolor="#E2F0FF"];
    semana2 [label="Semana 2\nPreprocesamiento\n+ Pipeline de IA", fillcolor="#E2FFE2"];
    semana3 [label="Semana 3\nInforme + UI\n(visualización básica)", fillcolor="#FBE2FF"];
    navidad [label="Alrededor de Navidad 🎄\nMVP visible\n(flujo completo testeable)", fillcolor="#FFD8D8"];

    inicio -> semana1 -> semana2 -> semana3 -> navidad;
}
"""

st.graphviz_chart(dot, use_container_width=True)

st.markdown("---")

st.subheader("💬 Estilo de comunicación sugerido")

st.markdown(
    """
Para asegurar un proceso claro y eficaz, propongo el siguiente estilo de colaboración:

### 1️⃣ Canal principal: correo electrónico

Prefiero usar **email** para decisiones y puntos importantes porque:

- Facilita revisar el historial  
- Permite compartir información fácilmente con todo el equipo  
- Es ideal para proyectos relacionados con datos médicos (auditoría, trazabilidad)

### 2️⃣ Checkpoints regulares

Cada semana puedo preparar un breve resumen con:

- Lo completado  
- Lo que está en proceso  
- Próximos pasos  
- Riesgos o decisiones necesarias (si las hubiera)

### 3️⃣ Canales rápidos (si el equipo lo necesita)

Para dudas pequeñas o temas urgentes, puedo usar:

- Mensajes breves  
- Reuniones cortas / videollamadas ligeras  

Pero cualquier **decisión importante** siempre se registrará por email
para mantener un historial claro.

---

Si lo consideráis útil, este plan se puede ajustar fácilmente según vuestras
prioridades, restricciones técnicas o necesidades médicas. 🙂
"""
)
