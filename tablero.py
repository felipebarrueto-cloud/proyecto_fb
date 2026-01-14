import streamlit as st
import os
import marea

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- CSS PARA TABLA Y COMPACTACIÓN ---
    st.markdown("""
        <style>
            .compact-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 10px; }
            .compact-table td { border: 1px solid #444; padding: 5px; text-align: center; vertical-align: middle; }
            .label-text { color: #888; font-size: 11px; display: block; margin-bottom: 2px; }
            .value-text { font-weight: bold; font-size: 18px; color: #ff4b4b; }
            .value-text-blue { font-weight: bold; font-size: 18px; color: #00d2ff; }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. BOTÓN DE REVELADO ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        marea.gestionar_avance_keyraken() # Procesa avance antes de la nueva carta
        
        if st.session_state.mazo:
            if st.session_state.carta_activa:
                c_v = st.session_state.carta_activa
                if c_v['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_v['def_actual'] = c_v.get('defensa', 0)
                    st.session_state.mesa.append(c_v)
                else:
                    st.session_state.descarte.append(c_v)
            
            st.session_state.carta_activa = st.session_state.mazo.pop(0)
            
            # Suma de Ámbar automático (Sin forjado de llaves)
            regalo = st.session_state.carta_activa.get('ambar_regalo', 0)
            if regalo > 0:
                st.session_state.recursos_jefe += regalo
            
            st.rerun()

    # --- 2. TABLA DE RESUMEN DE COMBATE Y ESTADO ---
    daño_base = 3
    daño_mesa = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo'] == "CRIATURA")
    daño_activa = 0
    if st.session_state.carta_activa and st.session_state.carta_activa['tipo'] == "CRIATURA":
        daño_activa = st.session_state.carta_activa.get('defensa', 0)
    
    poder_total = daño_base + daño_mesa + daño_activa

    # Renderizado de la tabla HTML
    st.markdown(f"""
        <table class="compact-table">
            <tr>
                <td style="width: 50%;">
                    <span class="label-text">⚔️ PODER ENEMIGO</span>
                    <span class="value-text">{poder_total}</span>
                    <br><span style="font-size:10px; color:#666;">(3 Base + {daño_mesa} Mesa + {daño_activa} Act)</span>
                </td>
                <td style="width: 50%;">
                    <span class="label-text">💎 ÆMBAR | 🌊 MAREA</span>
                    <span class="value-text-blue">{st.session_state.recursos_jefe} Æ</span> | 
                    <span style="color:white; font-weight:bold;">{st.session_state.marea}</span>
                    <br><span style="font-size:10px; color:#666;">Avances: {st.session_state.avances_jefe}/4</span>
                </td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

    # --- 3. ZONA DE CARTA ACTIVA ---
    if st.session_state.carta_activa:
        c = st.session_state.carta_activa
        col_izq, col_img, col_der = st.columns([1, 1.3, 1])
        with col_img:
            ruta = RUTA_BASE + c['img']
            if os.path.exists(ruta):
                st.image(ruta, use_container_width=True)
            else:
                st.error(f"Falta imagen: {c['img']}")
    
    st.divider()

    # --- 4. MESA (CARRIL) ---
    st.subheader("Mesa (Tentáculos y Amenazas)")
    if st.session_state.mesa:
        cols = st.columns(6)
        for i, carta in enumerate(st.session_state.mesa):
            with cols[i % 6]:
                with st.container(border=True):
                    pm = RUTA_BASE + carta['img']
                    if os.path.exists(pm): st.image(pm, use_container_width=True)
                    if carta['tipo'] == "CRIATURA":
                        st.write(f"❤️ {carta['def_actual']}")
                        if st.button("💥-1", key=f"d_{i}"):
                            carta['def_actual'] -= 1
                            if carta['def_actual'] <= 0:
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                            st.rerun()
