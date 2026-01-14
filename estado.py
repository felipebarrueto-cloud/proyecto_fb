import streamlit as st

def mostrar_estado():
    st.header("Estado del Keyraken")
    
    # Contenedor para métricas
    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Vida del Jefe", f"{st.session_state.vida_jefe} HP")
            st.metric("Armadura Actual", f"{st.session_state.armadura_actual}")
            
        with col2:
            # Barra de progreso para el Ámbar (Recursos)
            progreso_ambar = min(st.session_state.recursos_jefe / 6, 1.0)
            st.write(f"💎 Ámbar: {st.session_state.recursos_jefe} / 6")
            st.progress(progreso_ambar)
            
            st.metric("Llaves Forjadas", f"{st.session_state.llaves_jefe} / 3")

    # Mensajes de advertencia según el estado
    if st.session_state.llaves_jefe >= 2:
        st.warning("⚠️ ¡El Keyraken está a punto de ganar!")
    
    if st.session_state.vida_jefe <= 10:
        st.error("🐉 ¡El Jefe está herido de muerte!")
