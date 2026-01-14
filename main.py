import streamlit as st
from cartas import obtener_mazo_oficial
import tablero #, descarte estado, 

st.set_page_config(page_title="Keyraken Adventure", layout="wide")

if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Bienvenid@ a Rise of the Keyraken")
    n_jug = st.number_input("Número de Jugadores", min_value=1, max_value=4, value=1)
    if st.button("Iniciar Encuentro"):
        st.session_state.mazo = obtener_mazo_oficial()
        st.session_state.mesa = []
        st.session_state.descarte = []
        st.session_state.carta_activa = None
        st.session_state.vida_jefe = 30 * n_jug
        st.session_state.recursos_jefe = 0
        st.session_state.llaves_jefe = 0
        st.session_state.llaves_unforged_jugador = 3
        st.session_state.armadura_actual = 6
        st.session_state.juego_iniciado = True
        st.rerun()
else:
    with st.sidebar:
        st.header("Navegación")
        pagina = st.radio("Ir a:", ["Tablero", "Estado", "Descarte"])
    
    if pagina == "Tablero":
        tablero.mostrar_tablero()
    elif pagina == "Estado":
        estado.mostrar_estado()
    elif pagina == "Descarte":
        descarte.mostrar_descarte()


