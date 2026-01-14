import streamlit as st
import os
from cartas import obtener_mazo_oficial

st.set_page_config(page_title="Keyraken Adventure", layout="wide")
RUTA_BASE = "proyecto_keyforge/"

# --- INICIALIZACIÓN ---
if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Rise of the Keyraken")
    if st.button("Iniciar Batalla"):
        st.session_state.mazo = obtener_mazo_oficial()
        st.session_state.mesa = []
        st.session_state.descarte = []
        st.session_state.carta_activa = None
        st.session_state.reserva_daño = 0
        st.session_state.juego_iniciado = True
        st.rerun()

else:
    # --- INTERFAZ SUPERIOR (REVELADO) ---
    col_jefe, col_revelar = st.columns([1, 2])
    
    with col_jefe:
        # Imagen del Jefe siempre presente
        img_jefe = RUTA_BASE + "kf_adv_keyraken_keyraken.pdf.png"
        if os.path.exists(img_jefe):
            st.image(img_jefe, width=200)
        st.write(f"🎴 Mazo: {len(st.session_state.mazo)}")

    with col_revelar:
        if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
            if st.session_state.mazo:
                # Mover la anterior al tablero o descarte antes de sacar la nueva
                if st.session_state.carta_activa:
                    c_vieja = st.session_state.carta_activa
                    if c_vieja['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                        c_vieja['def_actual'] = c_vieja.get('defensa', 0)
                        st.session_state.mesa.append(c_vieja)
                    else:
                        st.session_state.descarte.append(c_vieja)
                
                # Nueva carta activa
                st.session_state.carta_activa = st.session_state.mazo.pop(0)
                st.rerun()

    # --- ZONA DE CARTA ACTIVA (LA REVELADA) ---
    st.divider()
    if st.session_state.carta_activa:
        c_activa = st.session_state.carta_activa
        col_espacio1, col_img_activa, col_espacio2 = st.columns([1, 1, 1])
        with col_img_activa:
            ruta_activa = RUTA_BASE + c_activa['img']
            if os.path.exists(ruta_activa):
                st.image(ruta_activa, caption="NUEVA AMENAZA", use_container_width=True)
            else:
                st.error(f"Imagen {c_activa['img']} no encontrada")

    # --- TABLERO (CARRIL DE CRIATURAS EN MESA) ---
    st.divider()
    st.subheader("Criaturas y Artefactos en Juego")
    
    if st.session_state.mesa:
        # Mostramos las cartas en el carril inferior
        filas = st.columns(6)
        for i, c in enumerate(st.session_state.mesa):
            with filas[i % 6]:
                ruta_mesa = RUTA_BASE + c['img']
                if os.path.exists(ruta_mesa):
                    st.image(ruta_mesa, use_container_width=True)
                
                # Gestión de Criaturas (Daño)
                if c['tipo'] == "CRIATURA":
                    st.write(f"❤️ **{c['def_actual']} / {c['defensa']}**")
                    # Botón pequeño para reducir vida manualmente por ahora
                    if st.button("💥 -1 HP", key=f"dmg_{i}"):
                        c['def_actual'] -= 1
                        if c['def_actual'] <= 0:
                            st.session_state.descarte.append(st.session_state.mesa.pop(i))
                        st.rerun()
                else:
                    st.caption("💠 ARTEFACTO")
    else:
        st.info("No hay cartas en el tablero todavía.")
