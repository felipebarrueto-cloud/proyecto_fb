import streamlit as st
import os
import marea

RUTA_BASE = "proyecto_keyforge/"

def procesar_habilidades_carta(carta, marea_ya_cambio):
    """Procesa ámbar, marea y habilidades de cartas"""
    if 'archivo_jefe' not in st.session_state:
        st.session_state.archivo_jefe = []
        
    st.session_state.recursos_jefe += carta.get('ambar_regalo', 0)
    if carta.get('sube_marea') == True and not marea_ya_cambio:
        st.session_state.marea = "Alta"
        marea_ya_cambio = True
    if carta.get("habilidad") == "archivar":
        valor = carta.get("valor", 0)
        for _ in range(valor):
            if st.session_state.mazo:
                st.session_state.archivo_jefe.append(st.session_state.mazo.pop(0))
    return marea_ya_cambio

def mostrar_tablero():
    if 'archivo_jefe' not in st.session_state:
        st.session_state.archivo_jefe = []
    if 'ultimas_desarchivadas' not in st.session_state:
        st.session_state.ultimas_desarchivadas = []

    # --- CSS ---
    st.markdown("""
        <style>
            div.stButton > button {
                background-color: #1a1c23 !important;
                color: #ffffff !important;
                border: 1px solid #333 !important;
                border-radius: 8px !important;
                height: 2.8em !important;
            }
            .compact-table { width: 100%; border-collapse: collapse; background: #1a1c23; border: 1px solid #333; border-radius: 8px; overflow: hidden; }
            .compact-table td { border: 1px solid #333; padding: 8px 4px; text-align: center; }
            .label-top { color: #888; font-size: 10px; font-weight: bold; text-transform: uppercase; display: block; margin-bottom: 2px; }
            .value-bottom { color: #ffffff; font-size: 18px; font-weight: bold; display: block; }
            .sub-info { color: #666; font-size: 9px; display: block; margin-top: 1px; }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. LÓGICA DE REVELADO ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        st.session_state.ultimas_desarchivadas = []
        marea.gestionar_avance_keyraken()
        
        recursos_ganados = sum(c['ambar_generado'] for c in st.session_state.mesa if c.get('no_hace_danio') and c.get('ambar_generado'))
        st.session_state.recursos_jefe += recursos_ganados

        if st.session_state.archivo_jefe:
            cartas_a_desarchivar = st.session_state.archivo_jefe.copy()
            st.session_state.archivo_jefe = [] 
            for c_arc in cartas_a_desarchivar:
                procesar_habilidades_carta(c_arc, False)
                if c_arc['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_arc['def_actual'] = c_arc.get('defensa', 0)
                    st.session_state.mesa.append(c_arc)
                else:
                    st.session_state.descarte.append(c_arc)
            st.session_state.ultimas_desarchivadas = cartas_a_desarchivar

        if st.session_state.carta_activa:
            c_v = st.session_state.carta_activa
            if c_v['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                c_v['def_actual'] = c_v.get('defensa', 0)
                st.session_state.mesa.append(c_v)
            else:
                st.session_state.descarte.append(c_v)

        if st.session_state.mazo:
            nueva = st.session_state.mazo.pop(0)
            st.session_state.carta_activa = nueva
            procesar_habilidades_carta(nueva, False)
            st.rerun()

    # --- 2. TABLA RESUMEN ---
    poder_total = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo']=="CRIATURA" and not c.get('no_hace_danio'))
    p_mesa = any(c.get('presa') for c in st.session_state.mesa if c['tipo']=="CRIATURA")
    p_act = st.session_state.carta_activa.get('presa') if st.session_state.carta_activa else False
    if p_mesa or p_act: poder_total += 3

    st.markdown(f"""
        <table class="compact-table">
            <tr>
                <td style="width: 30%;"><span class="label-top">💥 PODER</span><span class="value-bottom">{poder_total}</span></td>
                <td style="width: 40%;"><span class="label-top">💎 RECURSOS</span><span class="value-bottom">{st.session_state.recursos_jefe} Æ | 🌊 {st.session_state.marea}</span><span class="sub-info">Avances: {st.session_state.avances_jefe}/4</span></td>
                <td style="width: 30%;"><span class="label-top">📦 ARCHIVO</span><span class="value-bottom">{len(st.session_state.archivo_jefe)}</span></td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

    c_esp1, c_btn1, c_btn2, c_esp2 = st.columns([1, 1, 1, 1])
    with c_btn1:
        st.button("➖ Æ", key="btn_manual_sub", use_container_width=True, on_click=lambda: st.session_state.update({"recursos_jefe": max(0, st.session_state.recursos_jefe - 1)}))
    with c_btn2:
        st.button("➕ Æ", key="btn_manual_add", use_container_width=True, on_click=lambda: st.session_state.update({"recursos_jefe": st.session_state.recursos_jefe + 1}))

    st.divider()

    # --- 3. ÁREA DE REVELADO (LO QUE FALTABA) ---
    ultimas = st.session_state.get('ultimas_desarchivadas', [])
    if ultimas:
        col_revelada, col_archivo = st.columns(2)
        with col_revelada:
            if st.session_state.carta_activa:
                st.caption("🆕 REVELADA")
                st.image(RUTA_BASE + st.session_state.carta_activa['img'], use_container_width=True)
        with col_archivo:
            st.caption("📤 DESARCHIVADA/S")
            for c_arc in ultimas:
                st.image(RUTA_BASE + c_arc['img'], use_container_width=True)
    else:
        if st.session_state.carta_activa:
            st.image(RUTA_BASE + st.session_state.carta_activa['img'], use_container_width=True)

    st.divider()

    # --- 4. MESA DE JUEGO ---
    if st.session_state.mesa:
        st.markdown("<p style='font-size: 14px; color: #888; font-weight: bold; margin-bottom: 5px;'>Criaturas y Artefactos desplegados</p>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, carta in enumerate(st.session_state.mesa):
            with cols[i % 2]:
                with st.container(border=True):
                    st.image(RUTA_BASE + carta['img'], use_container_width=True)
                    if carta['tipo'] == "CRIATURA":
                        st.write(f"❤️ {carta['def_actual']}")
                        if st.button(f"Atacar {i}", key=f"atq_{i}", use_container_width=True):
                            carta['def_actual'] -= 1
                            if carta['def_actual'] <= 0:
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                            st.rerun()
                    elif carta['tipo'] == "ARTEFACTO":
                        st.caption("🏺 Artefacto")
                        if st.button(f"Eliminar {i}", key=f"del_art_{i}", use_container_width=True):
                            st.session_state.descarte.append(st.session_state.mesa.pop(i))
                            st.rerun()
