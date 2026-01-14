# estado.py
import streamlit as st

def mostrar_tablero_jefe():
    st.subheader("🐙 Estatus del Keyraken")
    
    # Diseño en 4 métricas clave
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Vida Total", f"{st.session_state.vida_jefe} HP")
    
    with col2:
        # La armadura base es 2 por cada llave no forjada del jugador
        armadura_base = 2 * st.session_state.llaves_unforged_jugador
        st.metric("Armadura", f"{st.session_state.armadura_actual} / {armadura_base}")
    
    with col3:
        st.metric("Recursos (Ámbar)", f"{st.session_state.recursos_jefe} / 6")
        
    with col4:
        st.metric("Llaves Forjadas", f"{st.session_state.llaves_jefe} / 3")

    # Alerta visual si el jefe está a punto de ganar
    if st.session_state.llaves_jefe >= 2:
        st.error("⚠️ ¡El Keyraken está a punto de forjar su tercera llave!")
