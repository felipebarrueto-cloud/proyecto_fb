import streamlit as st
import os
from cartas import obtener_mazo_oficial
from estado import mostrar_tablero_jefe # Importamos el nuevo módulo

st.set_page_config(page_title="Keyraken Adventure", layout="wide")
RUTA_BASE = "proyecto_keyforge/"

# --- INICIALIZACIÓN DE LA PARTIDA ---
if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Configuración de la Aventura")
    n_jug = st.number_input("Número de Jugadores", min_value=1, value=1)
    if st.button("Iniciar Batalla"):
        st.session_state.vida_jefe = 30 * n_jug
        st.session_state.llaves_unforged_jugador = 3
        st.session_state.armadura_actual = 6
        st.session_state.recursos_jefe = 0
        st.session_state.llaves_jefe = 0
        st.session_state.mazo = obtener_mazo_oficial()
        st.session_state.mesa = []
        st.session_state.carta_activa = None
        st.session_state.juego_iniciado = True
        st.rerun()

else:
    # 1. MOSTRAR EL ESTADO (Desde el script secundario)
    mostrar_tablero_jefe()
    
    st.divider()

    # 2. LÓGICA DE CASCADA (Revelar cartas)
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        if st.session_state.mazo:
            if st.session_state.carta_activa:
                c_v = st.session_state.carta_activa
                if c_v['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_v['def_actual'] = c_v.get('defensa', 0)
                    st.session_state.mesa.append(c_v)
                else:
                    # Si es ACCIÓN, sumamos recursos al jefe
                    st.session_state.recursos_jefe += 2
            
            st.session_state.carta_activa = st.session_state.mazo.pop(0)
            
            # Chequeo automático de llaves del jefe
            if st.session_state.recursos_jefe >= 6:
                st.session_state.recursos_jefe -= 6
                st.session_state.llaves_jefe += 1
            st.rerun()

    # 3. VISUALIZACIÓN DE CARTA ACTIVA Y MESA (Igual que antes...)
    # [Aquí iría el código de las imágenes que ya tienes]


