import streamlit as st
import os
import marea

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- CSS CORREGIDO PARA MÓVIL ---
    st.markdown("""
        <style>
            /* Asegurar visibilidad del botón */
            div.stButton > button {
                background-color: #ff4b4b !important;
                color: white !important;
                font-weight: bold !important;
                border-radius: 10px !important;
                height: 3em !important;
                margin-top: 10px !important;
            }
            /* Reducir espacios de Streamlit */
            .main .block-container { padding-top: 1rem !important; }
            .compact-table { width: 100%; border-collapse: collapse; margin-bottom: 8px; }
            .compact-table td { border: 1px solid #333; padding: 6px; text-align: center; background: #1a1c23; }
            .label { color: #888; font-size: 10px; display: block; }
            .val-red { color: #ff4b4b; font-size: 18px; font-weight: bold; }
            .val-blue { color: #00d2ff; font-size: 18px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. BOTÓN REVELAR (Visible y Prioritario) ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        marea.gestionar_avance_keyraken()
        if st.session_state.mazo:
            if st.session_state.carta_activa:
                c_v = st.session_state.carta_activa
                if c_v['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_v['def_actual'] = c_v.get('defensa', 0)
                    st.session_state.mesa.append(c_v)
                else:
                    st.session_state.descarte.append(c_v)
            
            st.session_state.carta_activa = st.session_state.mazo.pop(0)
            regalo = st.session_state.carta_activa.get('ambar_regalo', 0)
            st.session_state.recursos_jefe += regalo
            st.rerun()

    # --- 2. TABLA DE RESUMEN ---
    daño_mesa = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo'] == "CRIATURA")
    daño_activa = 0
    if st.session_state.carta_activa and st.session_state.carta_activa['tipo'] == "CRIATURA":
        daño_activa = st.session_state.carta_activa.get('defensa', 0)
    
    poder_total = 3 + daño_mesa + daño_activa

    st.markdown(f"""
        <table class="compact-table">
            <tr>
                <td style="width: 45%;">
                    <span class="label">⚔️ PODER TOTAL</span>
                    <span class="val-red">{poder_total}</span>
                </td>
                <td style="width: 55%;">
                    <span class="label">💎 {st.session_state.recursos_jefe} Æ | 🌊 {st.session_state.marea}</span>
                    <span style="color:white; font-size:12px;">Avances: <b>{st.session_state.avances_jefe}/4</b></span>
                </td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

    # --- 3. CARTA ACTIVA ---
    if st.session_state.carta_activa:
        c = st.session_state.carta_activa
        ruta = RUTA_BASE + c['img']
        if os.path.exists(ruta):
            st.image(ruta, use_container_width=True)
    
    st.divider()

    # --- 4. MESA (CARRIL) ---
    if st.session_state.mesa:
        cols = st.columns(2) # En móvil 2 columnas es más cómodo que 3
        for i, carta in enumerate(st.session_state.mesa):
            with cols[i % 2]:
                with st.container(border=True):
                    im_m = RUTA_BASE + carta['img']
                    if os.path.exists(im_m): st.image(im_m, use_container_width=True)
                    if carta['tipo'] == "CRIATURA":
                        if st.button(f"💥 {carta['def_actual']}", key=f"btn_{i}", use_container_width=True):
                            carta['def_actual'] -= 1
                            if carta['def_actual'] <= 0:
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                            st.rerun()
            
