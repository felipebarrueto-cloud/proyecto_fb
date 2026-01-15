import streamlit as st
import os
import marea

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- SEGURIDAD: Inicialización de emergencia ---
    if 'marea' not in st.session_state: st.session_state.marea = "Baja"
    if 'avances_jefe' not in st.session_state: st.session_state.avances_jefe = 0
    if 'recursos_jefe' not in st.session_state: st.session_state.recursos_jefe = 0

    # --- ESTILOS CSS COMPACTOS ---
    st.markdown("""
        <style>
            [data-testid="stMetricValue"] { font-size: 22px !important; line-height: 1 !important; }
            .block-container { padding-top: 1rem !important; }
            .compact-table { width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 5px; }
            .compact-table td { border: 1px solid #444; padding: 4px; text-align: center; }
            .label-text { color: #888; font-size: 10px; display: block; }
            .value-text { font-weight: bold; font-size: 16px; color: #ff4b4b; }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. BOTÓN DE REVELADO CON LÓGICA DE MAREA ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        # El jefe intenta avanzar ANTES de revelar la nueva carta
        marea.gestionar_avance_keyraken()
        
        if st.session_state.mazo:
            # Desplazar la carta que estaba activa
            if st.session_state.carta_activa:
                c_v = st.session_state.carta_activa
                if c_v['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_v['def_actual'] = c_v.get('defensa', 0)
                    st.session_state.mesa.append(c_v)
                else:
                    st.session_state.descarte.append(c_v)
            
            # Sacar nueva carta
            st.session_state.carta_activa = st.session_state.mazo.pop(0)
            
            # Sumar ámbar de regalo si lo tiene
            regalo = st.session_state.carta_activa.get('ambar_regalo', 0)
            if regalo > 0:
                st.session_state.recursos_jefe += regalo
            
            st.rerun()

    # --- 2. TABLA DE RESUMEN (PODER + ÆMBAR + MAREA) ---
    daño_base = 3
    daño_mesa = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo'] == "CRIATURA")
    daño_activa = 0
    if st.session_state.carta_activa and st.session_state.carta_activa['tipo'] == "CRIATURA":
        daño_activa = st.session_state.carta_activa.get('defensa', 0)
    
    poder_total = daño_base + daño_mesa + daño_activa

    st.markdown(f"""
        <table class="compact-table">
            <tr>
                <td style="width: 45%;">
                    <span class="label-text">⚔️ PODER TOTAL</span>
                    <span class="value-text">{poder_total}</span>
                </td>
                <td style="width: 55%;">
                    <span class="label-text">💎 {st.session_state.recursos_jefe} Æ | 🌊 {st.session_state.marea}</span>
                    <span style="color:white; font-size:11px;">Avances: <b>{st.session_state.avances_jefe}/4</b></span>
                </td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

    # --- 3. CARTA ACTIVA ---
    if st.session_state.carta_activa:
        c = st.session_state.carta_activa
        col_izq, col_img, col_der = st.columns([0.2, 2, 0.2])
        with col_img:
            ruta = RUTA_BASE + c['img']
            if os.path.exists(ruta):
                st.image(ruta, use_container_width=True)
    
    st.divider()

    # --- 4. CARRIL DE CARTAS (TABLERO) ---
    if st.session_state.mesa:
        cols = st.columns(3)
        for i, carta in enumerate(st.session_state.mesa):
            with cols[i % 3]:
                with st.container(border=True):
                    img_m = RUTA_BASE + carta['img']
                    if os.path.exists(img_m):
                        st.image(img_m, use_container_width=True)
                    
                    if carta['tipo'] == "CRIATURA":
                        # Botón de vida/daño compacto
                        if st.button(f"💥 {carta['def_actual']}", key=f"btn_{i}", use_container_width=True):
                            carta['def_actual'] -= 1
                            if carta['def_actual'] <= 0:
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                            st.rerun()
                    
