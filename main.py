import streamlit as st
import os
from cartas import obtener_mazo_oficial

st.set_page_config(page_title="Keyraken Adventure - Pre-view Mode", layout="wide")
RUTA_BASE = "proyecto_keyforge/"

# --- ESTADOS DEL JUEGO ---
if 'mazo' not in st.session_state:
    st.session_state.mazo = obtener_mazo_oficial()
    st.session_state.mesa = []
    st.session_state.descarte = []
    st.session_state.carta_previa = None # Carta que se está previsualizando
    st.session_state.log = []

# --- INTERFAZ ---
st.title("🏟️ Campo de Batalla Keyraken")

col_control, col_tablero = st.columns([1, 2.5])

with col_control:
    st.subheader("Turno del Jefe")
    # BOTÓN PARA REVELAR (Solo si no hay una carta pendiente de previsualizar)
    if st.session_state.carta_previa is None:
        if st.button("🎴 REVELAR NUEVA CARTA"):
            if st.session_state.mazo:
                st.session_state.carta_previa = st.session_state.mazo.pop(0)
                st.rerun()
    else:
        st.warning("Resuelve la carta actual antes de revelar otra.")

    st.divider()
    st.write(f"Mazo: {len(st.session_state.mazo)} | Descarte: {len(st.session_state.descarte)}")

# --- ZONA DE PREVISUALIZACIÓN (CARTA REVELADA) ---
if st.session_state.carta_previa:
    cp = st.session_state.carta_previa
    st.divider()
    st.subheader("👁️ Previsualización de Amenaza")
    
    with st.container(border=True):
        c1, c2 = st.columns([1, 2])
        with c1:
            img_p = RUTA_BASE + cp['img']
            if os.path.exists(img_p):
                st.image(img_p, width=300)
            else:
                st.error(f"Imagen no encontrada: {cp['img']}")
        
        with c2:
            st.title(cp['nombre'])
            st.write(f"**TIPO:** {cp['tipo']}")
            st.info(f"**EFECTO:** {cp['efecto']}")
            
            # BOTÓN SEGÚN EL TIPO DE CARTA
            if cp['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                if st.button(f"📥 Enviar {cp['nombre']} al TABLERO"):
                    cp['def_actual'] = cp.get('defensa', 0)
                    st.session_state.mesa.append(cp)
                    st.session_state.log.append(f"Nueva criatura en mesa: {cp['nombre']}")
                    st.session_state.carta_previa = None # Limpia la previsualización
                    st.rerun()
            else:
                # Es una ACCION
                if st.button(f"⚡ Ejecutar y enviar al DESCARTE"):
                    st.session_state.descarte.append(cp)
                    st.session_state.log.append(f"Acción ejecutada: {cp['nombre']}")
                    st.session_state.carta_previa = None # Limpia la previsualización
                    st.rerun()

# --- TABLERO (CARRIL DE CARTAS) ---
st.divider()
st.subheader("🏟️ Mesa Actual")
if st.session_state.mesa:
    cols = st.columns(6)
    for i, carta in enumerate(st.session_state.mesa):
        with cols[i % 6]:
            with st.container(border=True):
                p_m = RUTA_BASE + carta['img']
                if os.path.exists(p_m):
                    st.image(p_m, use_container_width=True)
                st.caption(f"**{carta['nombre']}**")
                if carta['tipo'] == "CRIATURA":
                    st.write(f"❤️ {carta['def_actual']}")
                
                # Botón para destruir manualmente si es necesario
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.descarte.append(st.session_state.mesa.pop(i))
                    st.rerun()
else:
    st.info("No hay cartas en la mesa.")

