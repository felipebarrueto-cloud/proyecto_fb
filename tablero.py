import streamlit as st
import os
import marea  # Importamos el nuevo script de lógica de marea

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- ESTILOS CSS PARA COMPACTAR ---
    st.markdown("""
        <style>
            [data-testid="stMetricValue"] { font-size: 24px !important; line-height: 1 !important; }
            [data-testid="stMetricLabel"] { font-size: 14px !important; }
            .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
            h1, h2, h3 { margin-top: -15px !important; margin-bottom: 5px !important; font-size: 18px !important; }
            .stCaption { font-size: 11px !important; line-height: 1.1 !important; }
            hr { margin: 0.5em 0px !important; }
            [data-testid="stVerticalBlock"] > div { padding-top: 0.1rem !important; padding-bottom: 0.1rem !important; }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. LÓGICA DE REVELADO (CASCADA) ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        # A. NUEVA REGLA: El Keyraken intenta avanzar pagando Æmbar ANTES de revelar
        marea.gestionar_avance_keyraken()

        if st.session_state.mazo:
            # B. Desplazar carta activa anterior a su destino
            if st.session_state.carta_activa:
                c_vieja = st.session_state.carta_activa
                if c_vieja['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_vieja['def_actual'] = c_vieja.get('defensa', 0)
                    st.session_state.mesa.append(c_vieja)
                else:
                    st.session_state.descarte.append(c_vieja)
            
            # C. Revelar la nueva carta
            st.session_state.carta_activa = st.session_state.mazo.pop(0)
            
            # D. Suma de Ámbar automático
            regalo = st.session_state.carta_activa.get('ambar_regalo', 0)
            if regalo > 0:
                st.session_state.recursos_jefe += regalo
            
            # E. Chequeo de forjado (opcional, por si el regalo completó la llave)
            if st.session_state.recursos_jefe >= 6:
                st.session_state.recursos_jefe -= 6
                st.session_state.llaves_jefe += 1
                st.toast("⚠️ EL KRAKEN FORJÓ UNA LLAVE")

            st.rerun()

    # --- 2. CÁLCULO DE PODER UNIFICADO ---
    daño_base_jefe = 3
    daño_mesa = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo'] == "CRIATURA")
    daño_activa = 0
    if st.session_state.carta_activa and st.session_state.carta_activa['tipo'] == "CRIATURA":
        daño_activa = st.session_state.carta_activa.get('defensa', 0)
    
    poder_total_enemigo = daño_base_jefe + daño_mesa + daño_activa

    # PANEL DE AMENAZA COMPACTO
    if st.session_state.carta_activa:
        with st.container(border=True):
            col_t, col_d = st.columns([1, 1.5])
            with col_t:
                st.metric("⚔️ PODER TOTAL", f"{poder_total_enemigo}")
            with col_d:
                st.markdown(f"""
                    <div style='font-size: 12px; line-height: 1.2; color: #888;'>
                        <b>Base:</b> 3 | <b>Mesa:</b> {daño_mesa} | <b>Revelada:</b> {daño_activa}
                    </div>
                """, unsafe_allow_html=True)
                st.progress(min(poder_total_enemigo / 25, 1.0))

    st.divider()

    # --- 3. ZONA DE CARTA ACTIVA ---
    if st.session_state.carta_activa:
        c = st.session_state.carta_activa
        col_izq, col_img, col_der = st.columns([1, 1.2, 1])
        with col_img:
            ruta_p = RUTA_BASE + c['img']
            if os.path.exists(ruta_p):
                st.image(ruta_p, caption=f"AMENAZA ACTUAL: {c['nombre']}", use_container_width=True)
            else:
                st.error(f"Falta imagen: {c['img']}")
    
    # --- 4. CARRIL DE CARTAS (TABLERO) ---
    st.subheader("Mesa (Amenazas Permanentes)")
    if st.session_state.mesa:
        filas_mesa = st.columns(6)
        for i, carta in enumerate(st.session_state.mesa):
            with filas_mesa[i % 6]:
                with st.container(border=True):
                    p_mesa = RUTA_BASE + carta['img']
                    if os.path.exists(p_mesa):
                        st.image(p_mesa, use_container_width=True)
                    
                    if carta['tipo'] == "CRIATURA":
                        st.write(f"❤️ HP: **{carta['def_actual']}**")
                        if st.button("💥 -1", key=f"dmg_{i}"):
                            carta['def_actual'] -= 1
                            if carta['def_actual'] <= 0:
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                                st.toast(f"¡{carta['nombre']} destruida! -3 HP al Jefe")
                            st.rerun()
                    else:
                        st.caption("💠 ARTEFACTO")
    elif st.session_state.carta_activa:
        st.caption("La mesa está limpia, pero la carta activa está atacando.")
