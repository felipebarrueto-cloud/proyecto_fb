import streamlit as st
import os
import marea

RUTA_BASE = "proyecto_keyforge/"

def procesar_habilidades_carta(carta, marea_ya_cambio):
    st.session_state.recursos_jefe += carta.get('ambar_regalo', 0)
    if carta.get('sube_marea') == True and not marea_ya_cambio:
        st.session_state.marea = "Alta"
        st.toast(f"🌊 Marea Alta: {carta['nombre']}")
        marea_ya_cambio = True
    if carta.get("habilidad") == "archivar":
        valor = carta.get("valor", 0)
        for _ in range(valor):
            if st.session_state.mazo:
                st.session_state.archivo_jefe.append(st.session_state.mazo.pop(0))
        st.toast(f"📦 Archivadas {valor} cartas.")
    return marea_ya_cambio

def mostrar_tablero():
    # --- CSS DE ALTA PRIORIDAD ---
    st.markdown("""
        <style>
            /* 1. Botón REVELAR (Rojo) */
            div.stButton > button:first-child { 
                background-color: #ff4b4b !important; 
                color: white !important; 
                font-weight: bold; 
                border-radius: 10px; 
            }
            
            /* 2. TABLA RESUMEN */
            .compact-table { width: 100%; border-collapse: collapse; background: #1a1c23; }
            .compact-table td { border: 1px solid #333; padding: 6px; text-align: center; }
            .label { color: #888; font-size: 10px; display: block; }
            .val-white { color: #ffffff; font-size: 18px; font-weight: bold; }

            /* 3. BOTONES DE GESTIÓN (Forzar color oscuro y eliminar rojo) */
            /* Buscamos los botones que están dentro de las columnas después de la tabla */
            div[data-testid="stHorizontalBlock"] div[data-testid="column"] button {
                background-color: #1a1c23 !important;
                color: #ffffff !important;
                border: 1px solid #444 !important;
                font-weight: normal !important;
                height: 2.5em !important;
            }

            /* 4. FORZAR COLUMNAS LADO A LADO EN MÓVIL */
            [data-testid="column"] {
                width: 48% !important;
                flex: 0 0 48% !important;
                min-width: 48% !important;
                display: inline-block !important;
            }
            div[data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                justify-content: space-between !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. BOTÓN REVELAR ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        st.session_state.ultimas_desarchivadas = []
        marea_inicial = st.session_state.marea
        marea.gestionar_avance_keyraken()
        marea_ya_cambio = st.session_state.marea != marea_inicial

        for carta_mesa in st.session_state.mesa:
            if carta_mesa.get('no_hace_danio') and carta_mesa.get('ambar_generado'):
                st.session_state.recursos_jefe += carta_mesa['ambar_generado']
                st.toast(f"✨ {carta_mesa['nombre']} generó {carta_mesa['ambar_generado']} Æ.")

        if st.session_state.get('archivo_jefe'):
            cartas_a_desarchivar = st.session_state.archivo_jefe.copy()
            st.session_state.archivo_jefe = [] 
            for c_arc in cartas_a_desarchivar:
                marea_ya_cambio = procesar_habilidades_carta(c_arc, marea_ya_cambio)
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
            marea_ya_cambio = procesar_habilidades_carta(nueva, marea_ya_cambio)
            hay_presa_mesa = any(c.get('presa') for c in st.session_state.mesa if c['tipo']=="CRIATURA")
            if not (nueva.get('presa') or hay_presa_mesa):
                st.session_state.recursos_jefe += 1
            st.rerun()

    # --- 2. TABLA DE RESUMEN ---
    n_archivo = len(st.session_state.get('archivo_jefe', []))
    poder_total = 0
    if st.session_state.carta_activa:
        p_mesa = any(c.get('presa') for c in st.session_state.mesa if c['tipo']=="CRIATURA")
        p_act = st.session_state.carta_activa.get('presa') == True
        base = 3 if (p_mesa or p_act) else 0
        dmg_mesa = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo']=="CRIATURA" and not c.get('no_hace_danio'))
        poder_total = base + dmg_mesa

    st.markdown(f"""
        <table class="compact-table">
            <tr>
                <td style="width: 30%;"><span class="label">💥 PODER</span><span class="val-white">{poder_total}</span></td>
                <td style="width: 40%;"><span class="label">💎 RECURSOS</span>
                    <span class="val-white" style="font-size:16px;">{st.session_state.recursos_jefe} Æ | 🌊 {st.session_state.marea}</span>
                    <br><span style="font-size:10px; color:#888;">Avances: {st.session_state.avances_jefe}/4</span></td>
                <td style="width: 30%;"><span class="label">📦 ARCHIVO</span><span class="val-white">{n_archivo}</span></td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

    # --- GESTIÓN MANUAL ÆMBAR (FORZADO LADO A LADO) ---
    col_izq, col_der = st.columns(2)
    with col_izq:
        if st.button("➖ Æ", use_container_width=True):
            st.session_state.recursos_jefe = max(0, st.session_state.recursos_jefe - 1)
            st.rerun()
    with col_der:
        if st.button("➕ Æ", use_container_width=True):
            st.session_state.recursos_jefe += 1
            st.rerun()

    st.divider()

    # --- 3. ÁREA DE REVELADO ---
    ultimas = st.session_state.get('ultimas_desarchivadas', [])
    if ultimas:
        c1, c2 = st.columns(2)
        with c1:
            if st.session_state.carta_activa:
                st.caption("🆕 REVELADA")
                st.image(RUTA_BASE + st.session_state.carta_activa['img'], use_container_width=True)
        with c2:
            st.caption("📤 ARCHIVO")
            for c_arc in ultimas:
                st.image(RUTA_BASE + c_arc['img'], use_container_width=True)
    else:
        if st.session_state.carta_activa:
            st.image(RUTA_BASE + st.session_state.carta_activa['img'], use_container_width=True)

    st.divider()

    # --- 4. MESA ---
    if st.session_state.mesa:
        st.subheader("🏟️ Mesa")
        cols = st.columns(2)
        for i, carta in enumerate(st.session_state.mesa):
            with cols[i % 2]:
                with st.container(border=True):
                    st.image(RUTA_BASE + carta['img'], use_container_width=True)
                    if carta['tipo'] == "CRIATURA":
                        if carta.get('no_hace_danio'):
                            st.markdown("<span style='color:white; font-size:11px;'>💎 Cosechar</span>", unsafe_allow_html=True)
                        st.write(f"❤️ {carta['def_actual']}")
                        if st.button(f"Atacar {i}", key=f"atq_{i}", use_container_width=True):
                            carta['def_actual'] -= 1
                            if carta['def_actual'] <= 0:
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                            st.rerun()
