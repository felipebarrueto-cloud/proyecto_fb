import streamlit as st
import os
import marea

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- CSS MANTENIDO ---
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
            .texto-blanco { color: #ffffff; font-size: 18px; font-weight: bold; vertical-align: middle; }
            .gema { font-size: 18px; vertical-align: middle; }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. BOTÓN REVELAR ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        marea_inicial = st.session_state.marea
        marea.gestionar_avance_keyraken()
        marea_ya_cambio = st.session_state.marea != marea_inicial
        
        if st.session_state.mazo:
            if st.session_state.carta_activa:
                c_v = st.session_state.carta_activa
                if c_v['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_v['def_actual'] = c_v.get('defensa', 0)
                    st.session_state.mesa.append(c_v)
                else:
                    st.session_state.descarte.append(c_v)
            
            nueva_c = st.session_state.mazo.pop(0)
            st.session_state.carta_activa = nueva_c
            
            # Lógica de Presa: Solo se evalúa al revelar
            presa_en_mesa = any(carta.get('presa') == True for carta in st.session_state.mesa if carta['tipo'] == "CRIATURA")
            presa_revelada = nueva_c.get('presa') == True

            if not (presa_revelada or presa_en_mesa):
                st.session_state.recursos_jefe += 1
                st.toast("💎 Sin Presa: +1 Æmbar.")

            if nueva_c.get('sube_marea') == True and not marea_ya_cambio:
                st.session_state.marea = "Alta"
            
            st.session_state.recursos_jefe += nueva_c.get('ambar_regalo', 0)
            st.rerun()

    # --- 2. CÁLCULO DE PODER (CORREGIDO: Solo si hay carta activa) ---
    poder_total = 0
    detalle_base = ""

    if st.session_state.carta_activa:
    # A. Comprobar si hay PRESA (activa el daño base del jefe inmediatamente)
        presa_en_mesa = any(c.get('presa') == True for c in st.session_state.mesa if c['tipo'] == "CRIATURA")
        presa_activa = st.session_state.carta_activa.get('presa') == True
    
    # El daño base de 3 se aplica SIEMPRE que haya una presa (incluso si acaba de aparecer)
    daño_base = 3 if (presa_en_mesa or presa_activa) else 0
    
    # B. Daño de criaturas en mesa (Criaturas de turnos anteriores)
    daño_mesa = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo'] == "CRIATURA")
    
    # C. Daño de la criatura activa (REGLA: Es 0 porque acaba de ser revelada)
    # Solo sumará su poder cuando el jugador pulse "Revelar" otra vez y pase a la mesa
    daño_activa_inmediato = 0 
    
    poder_total = daño_base + daño_mesa + daño_activa_inmediato
    
    if daño_base > 0:
        detalle_base = f"(Base 3 por Presa + {daño_mesa} Mesa)"
    else:
        detalle_base = f"(Solo Mesa: {daño_mesa} | Jefe: +1 Æ por falta de Presa)"
    else:
        detalle_base = "Esperando primer turno..."

    st.markdown(f"""
        <table class="compact-table">
            <tr>
                <td style="width: 45%;">
                    <span class="label">💥 PODER TOTAL</span>
                    <span class="val-red">{poder_total}</span>
                    <br><span style="font-size:9px; color:#888;">{detalle_base}</span>
                </td>
                <td style="width: 55%;">
                    <span class="label">RECURSOS Y MAREA</span>
                    <span class="gema">💎</span> 
                    <span class="texto-blanco">{st.session_state.recursos_jefe} Æ</span>
                    <span style="color:white; font-weight:bold;"> | 🌊 {st.session_state.marea}</span>
                    <br><span style="font-size:10px; color:#666;">Avances: <b>{st.session_state.avances_jefe}/4</b></span>
                </td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

    # --- 3. RENDERIZADO DE CARTAS ---
    if st.session_state.carta_activa:
        c = st.session_state.carta_activa
        if os.path.exists(RUTA_BASE + c['img']):
            st.image(RUTA_BASE + c['img'], use_container_width=True)

    st.divider()

    if st.session_state.mesa:
        st.subheader("Mesa (Criaturas y Artefactos)")
        cols = st.columns(2)
        for i, carta in enumerate(st.session_state.mesa):
            with cols[i % 2]:
                with st.container(border=True):
                    if os.path.exists(RUTA_BASE + carta['img']):
                        st.image(RUTA_BASE + carta['img'], use_container_width=True)
                    if carta['tipo'] == "CRIATURA":
                        st.write(f"❤️ **{carta['def_actual']}** {'(⛓️ Presa)' if carta.get('presa') else ''}")
                        if st.button(f"Atacar {i}", key=f"atq_{i}", use_container_width=True):
                            carta['def_actual'] -= 1
                            if carta['def_actual'] <= 0:
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                            st.rerun()
                    else:
                        st.caption("💠 ARTEFACTO")
