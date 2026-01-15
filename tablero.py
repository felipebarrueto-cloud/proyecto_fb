import streamlit as st
import os
import marea

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- CSS CORREGIDO PARA MÓVIL Y GEMA DORADA ---
    st.markdown("""
        <style>
            div.stButton > button {
                background-color: #ff4b4b !important;
                color: white !important;
                font-weight: bold !important;
                border-radius: 10px !important;
                height: 3em !important;
                margin-top: 10px !important;
            }
            .main .block-container { padding-top: 1rem !important; }
            .compact-table { width: 100%; border-collapse: collapse; margin-bottom: 8px; }
            .compact-table td { border: 1px solid #333; padding: 6px; text-align: center; background: #1a1c23; }
            .label { color: #888; font-size: 10px; display: block; }
            .val-red { color: #ff4b4b; font-size: 18px; font-weight: bold; }
            .gema-dorada {
                display: inline-block;
                background: radial-gradient(circle at 30% 30%, #FFF5A5 0%, #FFD700 50%, #B8860B 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                filter: drop-shadow(0px 0px 5px rgba(255, 215, 0, 0.7));
                font-weight: bold;
            }
            .texto-recurso { color: #FFEC8B; font-size: 18px; font-weight: bold; vertical-align: middle; }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. BOTÓN REVELAR (CON REGLA DE 1 CAMBIO DE MAREA POR TURNO) ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        
        # Guardamos el estado inicial para detectar cambios
        marea_inicial = st.session_state.marea
        
        # PASO 1: El Keyraken intenta avanzar con los recursos actuales
        # Si tiene éxito y la marea estaba alta, esta bajará aquí.
        marea.gestionar_avance_keyraken()
        
        # Verificamos si la marea ya cambió (bajó por pago)
        marea_ya_cambio = st.session_state.marea != marea_inicial
        
        if st.session_state.mazo:
            # PASO 2: Mover la carta activa anterior a la mesa
            if st.session_state.carta_activa:
                c_v = st.session_state.carta_activa
                if c_v['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_v['def_actual'] = c_v.get('defensa', 0)
                    st.session_state.mesa.append(c_v)
                else:
                    st.session_state.descarte.append(c_v)
            
            # PASO 3: Revelar la nueva carta del mazo
            nueva_c = st.session_state.mazo.pop(0)
            st.session_state.carta_activa = nueva_c
            
            # PASO 4: Aplicar efectos de la nueva carta
            # REGLA: Solo sube si la marea NO ha cambiado ya en este turno (paso 1)
            if nueva_c.get('sube_marea') == True:
                if not marea_ya_cambio:
                    st.session_state.marea = "Alta"
                    st.toast("🌊 ¡La Marea ha subido a ALTA!")
                else:
                    st.toast("🚫 Marea bloqueada: ya cambió este turno.")
            
            # Cobrar Ámbar de regalo
            regalo = nueva_c.get('ambar_regalo', 0)
            st.session_state.recursos_jefe += regalo
            
            st.rerun()

    # --- 2. TABLA DE RESUMEN ---
    daño_mesa = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo'] == "CRIATURA")
    poder_total = 3 + daño_mesa

    st.markdown(f"""
        <table class="compact-table">
            <tr>
                <td style="width: 45%;">
                    <span class="label">💥 PODER TOTAL</span>
                    <span class="val-red">{poder_total}</span>
                </td>
                <td style="width: 55%;">
                    <span class="label">RECURSOS Y MAREA</span>
                    <span class="gema">💎</span> 
                    <span class="texto-recurso">{st.session_state.recursos_jefe} Æ</span>
                    <span style="color:white; font-weight:bold;"> | 🌊 {st.session_state.marea}</span>
                    <br><span style="font-size:10px; color:#666;">Avances: <b>{st.session_state.avances_jefe}/4</b></span>
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
            if c['tipo'] == "CRIATURA":
                st.caption(f"⚠️ Recién llegada: Hará {c.get('defensa')} de daño al próximo turno.")
    
    st.divider()

    # --- 4. MESA (CARRIL) ---
    if st.session_state.mesa:
        cols = st.columns(2)
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
