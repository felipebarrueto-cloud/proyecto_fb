import streamlit as st
from cartas import obtener_mazo_oficial
import estado, tablero, descarte # Importamos tus scripts secundarios

st.set_page_config(page_title="Keyraken Adventure", layout="wide")

# --- INICIALIZACIÓN DE LA PARTIDA ---
if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Keyraken Adventure Setup")
    if st.button("Iniciar Nueva Batalla"):
        st.session_state.mazo = obtener_mazo_oficial()
        st.session_state.mesa = []
        st.session_state.descarte = []
        st.session_state.vida_jefe = 90 # Ejemplo para 3 jugadores
        st.session_state.llaves_jefe = 0
        st.session_state.recursos_jefe = 0
        st.session_state.carta_activa = None
        st.session_state.juego_iniciado = True
        st.rerun()

else:
    # --- MENÚ DE NAVEGACIÓN LATERAL ---
    with st.sidebar:
        st.title("🎮 Menú de Juego")
        pagina = st.radio("Ir a:", ["Estado del Kraken", "Tablero de Batalla", "Zona de Descarte"])
    
    # --- LÓGICA DE PÁGINAS ---
    if pagina == "Estado del Kraken":
        estado.mostrar_estado()
        
    elif pagina == "Tablero de Batalla":
        tablero.mostrar_tablero()
        
    elif pagina == "Zona de Descarte":
        descarte.mostrar_descarte()
