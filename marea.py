import streamlit as st

def gestionar_avance_keyraken():
    # Inicialización de variables de marea si no existen
    if 'marea' not in st.session_state:
        st.session_state.marea = "Baja"  # "Baja" o "Alta"
    if 'avances_jefe' not in st.session_state:
        st.session_state.avances_jefe = 0
    if 'n_jugadores' not in st.session_state:
        st.session_state.n_jugadores = 1

    # Cálculo de costes
    coste_por_jugador = 3 if st.session_state.marea == "Baja" else 6
    coste_total = coste_por_jugador * st.session_state.n_jugadores

    # LOGICA DE AVANCE (Se llama antes de revelar carta)
    if st.session_state.recursos_jefe >= coste_total:
        # El Jefe paga y avanza
        st.session_state.recursos_jefe -= coste_total
        st.session_state.avances_jefe += 1
        st.toast(f"🚨 ¡El Keyraken ha avanzado! ({st.session_state.avances_jefe}/4)")

        # Si avanzó con marea alta, la marea baja
        if st.session_state.marea == "Alta":
            st.session_state.marea = "Baja"
            st.toast("🌊 La marea ha bajado.")

    # Verificación de derrota
    if st.session_state.avances_jefe >= 4:
        st.error("💀 ¡EL KEYRAKEN HA AVANZADO 4 VECES! PARTIDA PERDIDA.")
        st.balloons() # Opcional: para marcar el final

def mostrar_interfaz_marea():
    # Esta función se puede llamar en la pestaña de "Estado"
    st.markdown("### 🌊 Control de Marea")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Estado Marea", st.session_state.marea)
    with col2:
        st.metric("Avances Jefe", f"{st.session_state.avances_jefe} / 4")
    
    # Botón manual para cambiar la marea (por efectos de cartas de jugador)
    if st.button("🔄 Cambiar Marea"):
        st.session_state.marea = "Alta" if st.session_state.marea == "Baja" else "Baja"
        st.rerun()
