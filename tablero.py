import streamlit as st
import os

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- 1. LÓGICA DE REVELADO (CASCADA) ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        if st.session_state.mazo:
            # Antes de sacar la nueva, movemos la actual a su destino
            if st.session_state.carta_activa:
                c_vieja = st.session_state.carta_activa
                if c_vieja['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_vieja['def_actual'] = c_vieja.get('defensa', 0)
                    st.session_state.mesa.append(c_vieja)
                else:
                    st.session_state.descarte.append(c_vieja)
            
            # Sacamos la nueva carta del mazo
            st.session_state.carta_activa = st.session_state.mazo.pop(0)
            
            # Suma de Ámbar automático (si la carta tiene 'ambar_regalo')
            regalo = st.session_state.carta_activa.get('ambar_regalo', 0)
            if regalo > 0:
                st.session_state.recursos_jefe += regalo
            
            # Chequeo de forjado inmediato
            if st.session_state.recursos_jefe >= 6:
                st.session_state.recursos_jefe -= 6
                st.session_state.llaves_jefe += 1
                st.toast("⚠️ EL KRAKEN FORJÓ UNA LLAVE")

            st.rerun()

    # --- 2. CÁLCULO DE PODER UNIFICADO (KRAKEN + EQUIPO) ---
    daño_base_jefe = 3
    daño_mesa = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo'] == "CRIATURA")
    daño_activa = 0
    if st.session_state.carta_activa and st.session_state.carta_activa['tipo'] == "CRIATURA":
        daño_activa = st.session_state.carta_activa.get('defensa', 0)
    
    poder_total_enemigo = daño_base_jefe + daño_mesa + daño_activa

    with st.container(border=True):
        col_t, col_d = st.columns([1, 2])
        with col_t:
            st.metric("⚔️ PODER ENEMIGO TOTAL", f"{poder_total_enemigo}")
        with col_d:
            st.caption(f"Desglose: Base(3) + Mesa({daño_mesa}) + Activa({daño_activa})")
            progreso = min(poder_total_enemigo / 25, 1.0)
            st.progress(progreso)

    st.divider()

    # --- 3. ZONA DE CARTA ACTIVA (LA REVELADA) ---
    if st.session_state.carta_activa:
        c = st.session_state.carta_activa
        col_izq, col_img, col_der = st.columns([1, 1.2, 1])
        with col_img:
            ruta_p = RUTA_BASE + c['img']
            if os.path.exists(ruta_p):
                st.image(ruta_p, caption="CARTA ACTIVA (RECIÉN REVELADA)", use_container_width=True)
            else:
                st.error(f"Falta imagen: {c['img']}")
    
    st.divider()

    # --- 4. CARRIL DE CARTAS (EL TABLERO) ---
    st.subheader("Amenazas en la Mesa")
    
    if st.session_state.mesa:
        # Mostramos las cartas en una cuadrícula de 6 columnas
        filas_mesa = st.columns(6)
        
        for i, carta in enumerate(st.session_state.mesa):
            with filas_mesa[i % 6]:
                with st.container(border=True):
                    p_mesa = RUTA_BASE + carta['img']
                    if os.path.exists(p_mesa):
                        st.image(p_mesa, use_container_width=True)
                    
                    # Interacción según el tipo
                    if carta['tipo'] == "CRIATURA":
                        st.write(f"❤️ HP: **{carta['def_actual']}**")
                        # Botón para daño manual
                        if st.button("💥 -1", key=f"dmg_{i}"):
                            carta['def_actual'] -= 1
                            if carta['def_actual'] <= 0:
                                # Regla: Al morir criatura, -3 HP al Jefe
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                                st.toast(f"¡{carta['nombre']} destruida! -3 HP al Jefe")
                            st.rerun()
                    else:
                        st.caption("💠 ARTEFACTO")
    else:
        st.info("La mesa está despejada. Revela una carta para empezar.")
