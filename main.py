# Dentro de main.py, al presionar "Iniciar Encuentro"
if st.button("Iniciar Encuentro"):
    st.session_state.mazo = obtener_mazo_oficial()
    st.session_state.mesa = []
    st.session_state.descarte = []
    st.session_state.carta_activa = None
    st.session_state.vida_jefe = 30 * n_jug
    st.session_state.recursos_jefe = 0
    st.session_state.n_jugadores = n_jug
    
    # ESTAS LÍNEAS SON CRÍTICAS PARA EVITAR EL ERROR
    st.session_state.marea = "Baja"
    st.session_state.avances_jefe = 0
    st.session_state.llaves_jefe = 0 # Aunque no forje, se usa en la tabla
    
    st.session_state.juego_iniciado = True
    st.rerun()
