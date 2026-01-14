import streamlit as st

def mostrar_estado():
    st.header("🐙 Estado Actual del Keyraken")
    col1, col2 = st.columns(2)
    col1.metric("Vida", f"{st.session_state.vida_jefe} HP")
    col2.metric("Llaves del Jefe", f"{st.session_state.llaves_jefe}/3")
    st.progress(st.session_state.recursos_jefe / 6, text=f"Ámbar: {st.session_state.recursos_jefe}/6")
        st.error("⚠️ ¡El Keyraken está a punto de forjar su tercera llave!")
