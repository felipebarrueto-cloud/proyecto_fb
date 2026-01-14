import streamlit as st
from cartas import obtener_mazo_oficial
import estado, tablero, descarte

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción de Streamlit)
st.set_page_config(page_title="Keyraken Adventure", layout="wide")

# 2. INICIALIZACIÓN DE LA SESIÓN (Solo ocurre una vez)
if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

# 3. PANTALLA DE BIENVENIDA / CONFIGURACIÓN
if not st.session_state.juego_iniciado:
    st.title("🐙 Bienvenid@ a Rise of the Keyraken")
    st.write("Configura tu partida antes de sumergirte en el abismo.")
    
    n_jug = st.number_input("Número de Jugadores", min_value=1, max_value=4, value=1)
    
    if st.button("Iniciar Encuentro"):
        # Variables Globales del Juego
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

# 4. INTERFAZ DE JUEGO (Navegación)
else:
    # Sidebar para moverte entre las secciones que creamos
    with st.sidebar:
        st.header("Navegación")
        pagina = st.radio("Selecciona una vista:", 
                         ["🏟️ Tablero de Batalla", 
                          "📊 Estado del Kraken", 
                          "🗑️ Zona de Descarte"])
        
        st.divider()
        if st.button("Reiniciar Partida"):
            st.session_state.juego_iniciado = False
            st.rerun()

    # Renderizado de la página seleccionada llamando a tus otros scripts
    if pagina == "🏟️ Tablero de Batalla":
        tablero.mostrar_tablero()
        
    elif pagina == "📊 Estado del Kraken":
        estado.mostrar_estado()
        
    elif pagina == "🗑️ Zona de Descarte":
        descarte.mostrar_descarte()
