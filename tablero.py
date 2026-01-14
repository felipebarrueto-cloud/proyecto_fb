import streamlit as st
import os

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- BOTÓN DE REVELADO CON LÓGICA DE MOVIMIENTO ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        if st.session_state.mazo:
            # A. MOVER CARTA ANTERIOR (Si existe)
            if st.session_state.carta_activa:
                c_vieja = st.session_state.carta_activa
                if c_vieja['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_vieja['def_actual'] = c_vieja.get('defensa', 0)
                    st.session_state.mesa.append(c_vieja)
                else:
                    # Las acciones se van al descarte al ser desplazadas
                    st.session_state.descarte.append(c_vieja)
            
            # B. REVELAR NUEVA CARTA
            nueva = st.session_state.mazo.pop(0)
            
            # C. SUMAR ÁMBAR AUTOMÁTICO (Si la carta lo indica)
            regalo = nueva.get('ambar_regalo', 0)
            if regalo > 0:
                st.session_state.recursos_jefe += regalo
                st.toast(f"✨ +{regalo} Ámbar generado por {nueva['nombre']}")

            # D. CHEQUEO DE FORJA AUTOMÁTICA
            if st.session_state.recursos_jefe >= 6:
                st.session_state.recursos_jefe -= 6
                st.session_state.llaves_jefe += 1
                st.toast("⚠️ EL JEFE HA FORJADO UNA LLAVE")

            # E. ACTUALIZAR ESTADO
            st.session_state.carta_activa = nueva
            st.rerun()
        else:
            st.error("El mazo se ha agotado.")

    # --- ZONA DE CARTA ACTIVA (REVELADA) ---
    if st.session_state.carta_activa:
        st.divider()
        c = st.session_state.carta_activa
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            img_path = RUTA_BASE + c['img']
            if os.path.exists(img_path):
                st.image(img_path, caption="CARTA REVELADA - RESUELVE SUS EFECTOS", use_container_width=True)
            else:
                st.error(f"Falta imagen: {c['img']}")
    
    # --- MESA DE JUEGO ---
    st.divider()
    st.subheader("🏟️ Mesa (Criaturas y Artefactos)")
    if st.session_state.mesa:
        cols = st.columns(6)
        for i, carta in enumerate(st.session_state.mesa):
            with cols[i % 6]:
                with st.container(border=True):
                    p = RUTA_BASE + carta['img']
                    if os.path.exists(p):
                        st.image(p, use_container_width=True)
                    
                    if carta['tipo'] == "CRIATURA":
                        st.write(f"❤️ **{carta['def_actual']}** / {carta['defensa']}")
                        # Botón para daño rápido
                        if st.button("💥 -1", key=f"dmg_{i}"):
                            carta['def_actual'] -= 1
                            if carta['def_actual'] <= 0:
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                            st.rerun()
    else:
        st.caption("Aún no hay cartas en el tablero.")
