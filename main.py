import streamlit as st
from cartas import obtener_mazo_oficial
import estado, tablero, descarte

st.set_page_config(page_title="Keyraken Adventure", layout="wide")

if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Rise of the Keyraken")
    n_jug = st.number_input("Número de Jugadores", min_value=1, max_value=4, value=1)
    
    if st.button("INICIAR ENCUENTRO", use_container_width=True):
        st.session_state.mazo = obtener_mazo_oficial()
        st.session_state.mesa = []
        st.session_state.descarte = []
        st.session_state.carta_activa = None
        st.session_state.n_jugadores = n_jug
        st.session_state.vida_jefe = 30 * n_jug
        st.session_state.recursos_jefe = 0
        st.session_state.marea = "Baja"
        st.session_state.avances_jefe = 0
        # ESTA VARIABLE FALTABA:
        st.session_state.armadura_actual = 6 
        
        st.session_state.juego_iniciado = True
        st.rerun()
else:
    # Usamos selectbox para evitar que el menú sidebar desaparezca en móvil
    pagina = st.selectbox("Sección:", ["Tablero", "Estado", "Descarte"])
    
    if pagina == "Tablero":
        tablero.mostrar_tablero()
    elif pagina == "Estado":
        estado.mostrar_estado()
    elif pagina == "Descarte":
        descarte.mostrar_descarte()

    if "archivo_jefe" not in st.session_state:
        st.session_state.archivo_jefe = []
    if "penalizacion_robo" not in st.session_state:
        st.session_state.penalizacion_robo = 0  # Cantidad de turnos que roba menos

