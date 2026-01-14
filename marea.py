import streamlit as st

def gestionar_avance_keyraken():
    # Inicialización de estados
    if 'marea' not in st.session_state: st.session_state.marea = "Baja"
    if 'avances_jefe' not in st.session_state: st.session_state.avances_jefe = 0
    
    # Coste: 3 por jugador (Baja) o 6 por jugador (Alta)
    coste_unidad = 3 if st.session_state.marea == "Baja" else 6
    coste_total = coste_unidad * st.session_state.n_jugadores

    # Lógica de Avance
    if st.session_state.recursos_jefe >= coste_total:
        st.session_state.recursos_jefe -= coste_total
        st.session_state.avances_jefe += 1
        st.toast(f"🚀 Avance del Jefe: {st.session_state.avances_jefe}/4")

        # Regla: Si avanza en marea Alta, cambia a Baja
        if st.session_state.marea == "Alta":
            st.session_state.marea = "Baja"
            st.toast("🌊 La marea ha bajado")

    # Condición de derrota
    if st.session_state.avances_jefe >= 4:
        st.error("💀 ¡PARTIDA PERDIDA! El Keyraken avanzó 4 veces.")
