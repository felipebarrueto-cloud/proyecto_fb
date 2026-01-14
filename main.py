import streamlit as st
import os
# Importamos tu base de datos de cartas
from cartas import obtener_mazo_oficial

st.set_page_config(page_title="Keyraken Adventure", layout="wide")
RUTA_BASE = "proyecto_keyforge/"

# --- 1. INICIALIZACIÓN DE LA SESIÓN ---
if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Rise of the Keyraken")
    if st.button("Iniciar Encuentro"):
        st.session_state.mazo = obtener_mazo_oficial()
        st.session_state.mesa = []
        st.session_state.descarte = []
        st.session_state.carta_previa = None  # Aquí guardamos la carta revelada
        st.session_state.juego_iniciado = True
        st.rerun()

# --- 2. LÓGICA DE BATALLA ---
else:
    # Sidebar con contadores
    st.sidebar.title("Estado")
    st.sidebar.write(f"🎴 Mazo: {len(st.session_state.mazo)}")
    st.sidebar.write(f"🗑️ Descarte: {len(st.session_state.descarte)}")
    
    # Botón principal para revelar
    if st.session_state.carta_previa is None:
        if st.button("🎴 REVELAR CARTA DEL MAZO"):
            if st.session_state.mazo:
                # Sacamos la carta y la ponemos en el estado de "previa"
                st.session_state.carta_previa = st.session_state.mazo.pop(0)
                st.rerun()
    
    st.divider()

    # --- 3. ZONA DE PREVISUALIZACIÓN (AQUÍ ESTÁ EL CAMBIO) ---
    if st.session_state.carta_previa is not None:
        carta = st.session_state.carta_previa
        
        # Usamos un contenedor con borde para que destaque
        with st.container(border=True):
            st.subheader("CARTA REVELADA")
            col_img, col_info = st.columns([1, 2])
            
            with col_img:
                # Forzamos la ruta de la imagen
                ruta_foto = RUTA_BASE + carta['img']
                if os.path.exists(ruta_foto):
                    st.image(ruta_foto, width=350)
                else:
                    st.error(f"No se encuentra la imagen: {carta['img']} en {RUTA_BASE}")
            
            with col_info:
                st.header(carta['nombre'])
                st.markdown(f"**TIPO:** {carta['tipo']}")
                st.info(f"**EFECTO:** {carta['efecto']}")
                
                # Botones de decisión
                if carta['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    if st.button(f"Enviar a la Mesa"):
                        carta['def_actual'] = carta.get('defensa', 0)
                        st.session_state.mesa.append(carta)
                        st.session_state.carta_previa = None # Limpiamos para poder revelar otra
                        st.rerun()
                else:
                    if st.button(f"⚡ Ejecutar y Descartar"):
                        st.session_state.descarte.append(carta)
                        st.session_state.carta_previa = None # Limpiamos
                        st.rerun()

    # --- 4. EL TABLERO (MESA) ---
    st.divider()
    st.subheader("Mesa de Combate")
    if st.session_state.mesa:
        cols = st.columns(6)
        for i, c in enumerate(st.session_state.mesa):
            with cols[i % 6]:
                with st.container(border=True):
                    img_mesa = RUTA_BASE + c['img']
                    if os.path.exists(img_mesa):
                        st.image(img_mesa, use_container_width=True)
                    st.caption(f"**{c['nombre']}**")
                    if c['tipo'] == "CRIATURA":
                        st.write(f"❤️ {c['def_actual']}")



