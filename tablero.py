import streamlit as st
import os

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- 1. LÓGICA DE REVELADO (CASCADA) ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        if st.session_state.mazo:
            if st.session_state.carta_activa:
                c_vieja = st.session_state.carta_activa
                if c_vieja['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_vieja['def_actual'] = c_vieja.get('defensa', 0)
                    st.session_state.mesa.append(c_vieja)
                else:
                    st.session_state.descarte.append(c_vieja)
            
            st.session_state.carta_activa = st.session_state.mazo.pop(0)
            
            # Suma de Ámbar automático
            regalo = st.session_state.carta_activa.get('ambar_regalo', 0)
            if regalo > 0:
                st.session_state.recursos_jefe += regalo
            
            st.rerun()

    # --- 2. RESUMEN DE COMBATE ACTUALIZADO ---
    # Daño de las criaturas en la mesa
    daño_mesa = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo'] == "CRIATURA")
    # Daño de la carta activa
    daño_activa = 0
    if st.session_state.carta_activa and st.session_state.carta_activa['tipo'] == "CRIATURA":
        daño_activa = st.session_state.carta_activa.get('defensa', 0)
    
    total_jugador = daño_mesa + daño_activa
    ataque_fijo_jefe = 3  # El daño constante que mencionaste

    # Panel informativo de doble vía
    with st.container(border=True):
        st.markdown("### ⚔️ Análisis de la Contienda")
        col_jug, col_vs, col_jefe_stat = st.columns([2, 1, 2])
        
        with col_jug:
            st.write("**Tu Potencial de Daño**")
            st.title(f"{total_jugador}")
            st.caption(f"Mesa ({daño_mesa}) + Activa ({daño_activa})")
            
        with col_vs:
            st.write("")
            st.subheader("VS")
            
        with col_jefe_stat:
            st.write("**Ataque del Keyraken**")
            st.title(f"{ataque_fijo_jefe}")
            st.caption("Daño constante por turno")

        # Comparativa de HP del Jefe
        st.divider()
        hp_restante = st.session_state.vida_jefe
        st.write(f"🎯 **Vida del Jefe:** {hp_restante} HP")
        
        # Barra de progreso de victoria
        progreso_victoria = max(0.0, min(total_jugador / hp_restante, 1.0)) if hp_restante > 0 else 1.0
        st.progress(progreso_victoria, text=f"Presión sobre el Jefe: {int(progreso_victoria*100)}%")

    st.divider()

    # --- 3. ZONA DE CARTA ACTIVA ---
    if st.session_state.carta_activa:
        c = st.session_state.carta_activa
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            img_path = RUTA_BASE + c['img']
            if os.path.exists(img_path):
                st.image(img_path, caption="NUEVA CARTA REVELADA", use_container_width=True)
    
    # --- 4. TABLERO DE JUEGO ---
    # ... (Mantenemos el carril de cartas y botones de daño que ya tenías)
