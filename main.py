import streamlit as st
import os
from cartas import obtener_mazo_oficial

st.set_page_config(page_title="Keyraken Adventure - Cascada", layout="wide")
RUTA_BASE = "proyecto_keyforge/"

# --- INICIALIZACIÓN ---
if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Modo Cascada: Keyraken")
    if st.button("Iniciar Batalla"):
        st.session_state.mazo = obtener_mazo_oficial()
        st.session_state.mesa = []
        st.session_state.descarte = []
        st.session_state.carta_activa = None  # La carta que está arriba
        st.session_state.juego_iniciado = True
        st.rerun()

else:
    # --- BARRA LATERAL ---
    st.sidebar.metric("Mazo", len(st.session_state.mazo))
    st.sidebar.metric("Descarte", len(st.session_state.descarte))

    # --- BOTÓN DE REVELAR (Lógica de Cascada) ---
    if st.button("REVELAR SIGUIENTE CARTA"):
        if st.session_state.mazo:
            # 1. Si ya hay una carta arriba, moverla a su destino
            if st.session_state.carta_activa is not None:
                carta_vieja = st.session_state.carta_activa
                if carta_vieja['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    carta_vieja['def_actual'] = carta_vieja.get('defensa', 0)
                    st.session_state.mesa.append(carta_vieja)
                else:
                    st.session_state.descarte.append(carta_vieja)
            
            # 2. Poner la nueva carta arriba
            st.session_state.carta_activa = st.session_state.mazo.pop(0)
            st.rerun()
        else:
            st.error("¡El mazo está vacío!")

    st.divider()

    # --- ZONA SUPERIOR: CARTA ACTIVA (MÁS GRANDE) ---
    if st.session_state.carta_activa:
        st.subheader("⚡ Amenaza Actual (Activa)")
        ca = st.session_state.carta_activa
        
        with st.container(border=True):
            col_img, col_info = st.columns([1, 3])
            with col_img:
                ruta = RUTA_BASE + ca['img']
                if os.path.exists(ruta):
                    st.image(ruta, width=250)
            with col_info:
                st.title(ca['nombre'])
                st.write(f"**TIPO:** {ca['tipo']}")
                st.info(f"**EFECTO:** {ca['efecto']}")
                st.caption("Esta carta bajará al tablero cuando reveles la siguiente.")

    # --- ZONA INFERIOR: EL TABLERO (MESA) ---
    st.divider()
    st.subheader("Mesa de Combate")
    if st.session_state.mesa:
        # Mostramos las cartas en una fila horizontal
        cols = st.columns(6)
        for i, c in enumerate(st.session_state.mesa):
            with cols[i % 6]:
                with st.container(border=True):
                    img_m = RUTA_BASE + c['img']
                    if os.path.exists(img_m):
                        st.image(img_m, use_container_width=True)
                    st.caption(f"**{c['nombre']}**")
                    if c['tipo'] == "CRIATURA":
                        st.write(f"❤️ {c['def_actual']}")
    else:
        st.info("Aún no hay cartas permanentes en la mesa.")
