import streamlit as st
from cartas import obtener_mazo_oficial
import estado, tablero, descarte

# 1. Configuración de página - DEBE SER LA PRIMERA LÍNEA DE STREAMLIT
st.set_page_config(page_title="Keyraken Adventure", layout="wide", initial_sidebar_state="collapsed")

# 2. Inicialización de la sesión
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
        st.session_state.juego_iniciado = True
        st.rerun()
else:
    # Navegación sencilla para móvil
    pagina = st.selectbox("Sección:", ["Tablero", "Estado", "Descarte"])
    
    if pagina == "Tablero":
        tablero.mostrar_tablero()
    elif pagina == "Estado":
        estado.mostrar_estado()
    elif pagina == "Descarte":
        descarte.mostrar_descarte()
        
