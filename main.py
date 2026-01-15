import streamlit as st
try:
    from cartas import obtener_mazo_oficial
except ImportError:
    st.error("No se pudo encontrar el archivo 'cartas.py'. Asegúrate de que esté en la misma carpeta.")

import estado, tablero, descarte

# 1. Configuración de página
st.set_page_config(page_title="Keyraken Adventure", layout="wide")

# 2. Inicialización de la sesión
if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Preparación de la Batalla")
    n_jug = st.number_input("Número de Jugadores", min_value=1, max_value=4, value=1)
    
    if st.button("Iniciar Encuentro"):
        # Variables de Cartas e Imágenes
        st.session_state.mazo = obtener_mazo_oficial()
        st.session_state.mesa = []
        st.session_state.descarte = []
        st.session_state.carta_activa = None
        
        # Variables de Lógica de Juego y Marea
        st.session_state.n_jugadores = n_jug
        st.session_state.vida_jefe = 30 * n_jug
        st.session_state.recursos_jefe = 0
        st.session_state.marea = "Baja"  # Inicialización de marea
        st.session_state.avances_jefe = 0 # Inicialización de avances
        st.session_state.armadura_actual = 6
        
        st.session_state.juego_iniciado = True
        st.rerun()

else:
    # Barra lateral de navegación
    with st.sidebar:
        st.header("🎮 Menú")
        pagina = st.radio("Ir a:", ["Tablero", "Estado", "Descarte"])
        st.divider()
        if st.button("Reiniciar Partida"):
            st.session_state.juego_iniciado = False
            st.rerun()

    # Carga de Pestañas
    if pagina == "Tablero":
        tablero.mostrar_tablero()
    elif pagina == "Estado":
        estado.mostrar_estado()
    elif pagina == "Descarte":
        descarte.mostrar_descarte()
        
