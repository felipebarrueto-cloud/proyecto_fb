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

    # --- CSS: BOTONES MANUALES RECTANGULARES / CIRCULARES ---
    st.markdown("""
        <style>
            /* Reset General de Botones */
            div.stButton > button {
                background-color: #1a1c23 !important;
                color: #ffffff !important;
                border: 1px solid #333 !important;
                transition: all 0.2s ease;
            }

            /* Configuración específica para botones de Ámbar (+ y -) */
            /* Los hacemos rectangulares compactos */
            button[key*="btn_manual"] {
                height: 45px !important;
                width: 100% !important;
                border-radius: 12px !important; /* Esquinas suaves */
                font-size: 20px !important;
                font-weight: bold !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
            }

            /* Tabla de Resumen */
            .compact-table { width: 100%; border-collapse: collapse; background: #1a1c23; border: 1px solid #333; border-radius: 8px; overflow: hidden; }
            .compact-table td { border: 1px solid #333; padding: 8px 4px; text-align: center; }
            .label-top { color: #888; font-size: 10px; font-weight: bold; text-transform: uppercase; display: block; margin-bottom: 2px; }
            .value-bottom { color: #ffffff; font-size: 18px; font-weight: bold; display: block; }
            .sub-info { color: #666; font-size: 9px; display: block; margin-top: 1px; }

            /* Forzar fila horizontal en móviles */
            [data-testid="stHorizontalBlock"]:has(button[key*="btn_manual"]) {
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                gap: 10px !important;
                justify-content: center !important;
                padding: 0 15% !important; /* Les da aire a los lados para que ocupen el centro */
            }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. BOTÓN REVELAR ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        st.session_state.ultimas_desarchivadas = []
        marea_inicial = st.session_state.marea
        marea.gestionar_avance_keyraken()
        marea_ya_cambio = st.session_state.marea != marea_inicial

        # Generación por Recolectores
        recursos_rec = sum(c['ambar_generado'] for c in st.session_state.mesa if c.get('no_hace_danio') and c.get('ambar_generado'))
        if recursos_rec > 0:
            st.session_state.recursos_jefe += recursos_rec
            st.toast(f"✨ Recolectores: +{recursos_rec} Æ")

        # Procesar Archivo
        if st.session_state.archivo_jefe:
            cartas_a_des = st.session_state.archivo_jefe.copy()
            st.session_state.archivo_jefe = [] 
            for c in cartas_a_des:
                marea_ya_cambio = procesar_habilidades_carta(c, marea_ya_cambio)
                if c['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c['def_actual'] = c.get('defensa', 0)
                    st.session_state.mesa.append(c)
                else:
                    st.session_state.descarte.append(c)
            st.session_state.ultimas_desarchivadas = cartas_a_des

        # Mover carta activa anterior
        if st.session_state.carta_activa:
            c_act = st.session_state.carta_activa
            if c_act['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                c_act['def_actual'] = c_act.get('defensa', 0)
                st.session_state.mesa.append(c_act)
            else:
                st.session_state.descarte.append(c_act)

        # Revelar nueva y regla Sin Presa
        if st.session_state.mazo:
            nueva = st.session_state.mazo.pop(0)
            st.session_state.carta_activa = nueva
            marea_ya_cambio = procesar_habilidades_carta(nueva, marea_ya_cambio)
            
            hay_p = any(c.get('presa') for c in st.session_state.mesa if c['tipo']=="CRIATURA")
            if not (nueva.get('presa') or hay_p):
                st.session_state.recursos_jefe += 1
                st.toast("💎 Sin Presa: +1 Æ")
            st.rerun()

    # --- 2. TABLA RESUMEN ---
    poder = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo']=="CRIATURA" and not c.get('no_hace_danio'))
    p_m = any(c.get('presa') for c in st.session_state.mesa if c['tipo']=="CRIATURA")
    p_a = st.session_state.carta_activa.get('presa') if st.session_state.carta_activa else False
    if p_m or p_a: poder += 3

    st.markdown(f"""
        <table class="compact-table">
            <tr>
                <td style="width: 30%;"><span class="label-top">💥 PODER</span><span class="value-bottom">{poder}</span></td>
                <td style="width: 40%;"><span class="label-top">💎 RECURSOS</span><span class="value-bottom">{st.session_state.recursos_jefe} Æ | 🌊 {st.session_state.marea}</span><span class="sub-info">Avances: {st.session_state.avances_jefe}/4</span></td>
                <td style="width: 30%;"><span class="label-top">📦 ARCHIVO</span><span class="value-bottom">{len(st.session_state.archivo_jefe)}</span></td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

    # --- 3. GESTIÓN MANUAL (Configuración Rectangular/Circular) ---
    c_e1, c_m1, c_m2, c_e2 = st.columns([1, 1, 1, 1])
    with c_m1:
        st.button("➖", key="btn_manual_sub", use_container_width=True, on_click=lambda: st.session_state.update({"recursos_jefe": max(0, st.session_state.recursos_jefe - 1)}))
    with c_m2:
        st.button("➕", key="btn_manual_add", use_container_width=True, on_click=lambda: st.session_state.update({"recursos_jefe": st.session_state.recursos_jefe + 1}))

    st.divider()

    # --- 4. ÁREA DE REVELADO ---
    ultimas = st.session_state.get('ultimas_desarchivadas', [])
    if ultimas:
        col_r, col_a = st.columns(2)
        with col_r:
            if st.session_state.carta_activa:
                st.caption("🆕 REVELADA")
                st.image(RUTA_BASE + st.session_state.carta_activa['img'], use_container_width=True)
        with col_a:
            st.caption("📤 ARCHIVO")
            for c_arc in ultimas:
                st.image(RUTA_BASE + c_arc['img'], use_container_width=True)
    elif st.session_state.carta_activa:
        st.image(RUTA_BASE + st.session_state.carta_activa['img'], use_container_width=True)

    # --- 5. MESA ---
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
