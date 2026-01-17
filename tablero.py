import streamlit as st
import os
import marea

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- CSS ULTRA-ESPECÍFICO PARA FORZAR LADO A LADO ---
    st.markdown("""
        <style>
            /* 1. Seleccionamos el contenedor que Streamlit crea para los botones */
            /* Forzamos que el bloque de botones NO se rompa en móvil */
            div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div.stButton {
                display: inline-block !important;
                width: auto !important;
                margin-right: 10px !important;
            }

            /* 2. Alineamos el contenedor padre para centrar los botones */
            div[data-testid="stVerticalBlock"]:has(button[key*="manual"]) {
                display: flex !important;
                flex-direction: row !important;
                justify-content: center !important;
                align-items: center !important;
                flex-wrap: nowrap !important; /* Prohibido saltar de línea */
            }

            /* 3. Estilo Cuadrado Fijo para los botones de Ámbar */
            button[key*="manual"] {
                width: 60px !important;
                height: 60px !important;
                min-width: 60px !important;
                max-width: 60px !important;
                border-radius: 10px !important;
                background-color: #1a1c23 !important;
                color: #ffffff !important;
                border: 1px solid #333 !important;
                font-size: 26px !important;
                padding: 0 !important;
            }

            /* Estilos de la Tabla Resumen */
            .compact-table { width: 100%; border-collapse: collapse; background: #1a1c23; border: 1px solid #333; border-radius: 8px; overflow: hidden; }
            .compact-table td { border: 1px solid #333; padding: 10px 4px; text-align: center; }
            .label-top { color: #888; font-size: 11px; font-weight: bold; text-transform: uppercase; display: block; margin-bottom: 2px; }
            .value-bottom { color: #ffffff; font-size: 19px; font-weight: bold; display: block; }
        </style>
    """, unsafe_allow_html=True)

    # --- LÓGICA DE REVELADO Y TABLA (Mantenemos tu lógica actual) ---
    # ... (Botón revelar y procesamiento de cartas) ...

    # --- TABLA RESUMEN ---
    st.markdown(f"""
        <table class="compact-table">
            <tr>
                <td style="width: 33%;"><span class="label-top">💥 PODER</span><span class="value-bottom">{0}</span></td>
                <td style="width: 34%;"><span class="label-top">💎 RECURSOS</span><span class="value-bottom">{st.session_state.recursos_jefe} Æ</span></td>
                <td style="width: 33%;"><span class="label-top">📦 ARCHIVO</span><span class="value-bottom">{0}</span></td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

    # --- 3. GESTIÓN MANUAL (LA SOLUCIÓN DEFINITIVA) ---
    # Colocamos ambos botones en el mismo contenedor (sin usar st.columns)
    # El CSS se encargará de ponerlos uno al lado del otro
    container = st.container()
    container.button("➖", key="btn_manual_sub", on_click=lambda: st.session_state.update({"recursos_jefe": max(0, st.session_state.recursos_jefe - 1)}))
    container.button("➕", key="btn_manual_add", on_click=lambda: st.session_state.update({"recursos_jefe": st.session_state.recursos_jefe + 1}))

    st.divider()
    # ... resto del tablero ...


    # --- 4. ÁREA DE REVELADO Y MESA ---
    if st.session_state.carta_activa:
        st.image(RUTA_BASE + st.session_state.carta_activa['img'], use_container_width=True)
    
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
