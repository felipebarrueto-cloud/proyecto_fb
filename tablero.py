import streamlit as st
import os

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- 1. BOTÓN DE REVELADO (Mecánica de Cascada) ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        if st.session_state.mazo:
            # Antes de sacar la nueva, movemos la actual a su destino
            if st.session_state.carta_activa:
                c_vieja = st.session_state.carta_activa
                
                if c_vieja['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_vieja['def_actual'] = c_vieja.get('defensa', 0)
                    st.session_state.mesa.append(c_vieja)
                else:
                    # Las Acciones se resuelven y van al descarte
                    st.session_state.descarte.append(c_vieja)
            
            # Sacamos la nueva carta del mazo
            st.session_state.carta_activa = st.session_state.mazo.pop(0)
            st.rerun()
        else:
            st.error("El mazo de aventura está vacío.")

    # --- 2. ÁREA DE CARTA ACTIVA (RECIÉN REVELADA) ---
    # Esta es la carta que el jugador debe leer y ejecutar su efecto "Play"
    if st.session_state.carta_activa:
        st.divider()
        c_activa = st.session_state.carta_activa
        
        # Centramos la carta revelada para que sea la protagonista
        col_izq, col_img, col_der = st.columns([1, 1, 1])
        with col_img:
            ruta_activa = RUTA_BASE + c_activa['img']
            if os.path.exists(ruta_activa):
                st.image(ruta_activa, caption="EFECTO ACTUAL", use_container_width=True)
            else:
                st.error(f"Falta imagen: {c_activa['img']}")
    
    st.divider()

    # --- 3. MESA DE COMBATE (CARRIL DE CARTAS) ---
    st.subheader("Criaturas en mesa")
    
    if st.session_state.mesa:
        # Mostramos las cartas en una cuadrícula de 6 columnas
        columnas = st.columns(6)
        
        for i, carta in enumerate(st.session_state.mesa):
            with columnas[i % 6]:
                with st.container(border=True):
                    ruta_mesa = RUTA_BASE + carta['img']
                    
                    if os.path.exists(ruta_mesa):
                        st.image(ruta_mesa, use_container_width=True)
                    
                    # Lógica de interacción para Criaturas
                    if carta['tipo'] == "CRIATURA":
                        st.write(f"❤️ HP: **{carta['def_actual']}**")
                        
                        # Input de daño simplificado
                        daño = st.number_input("Dmg", min_value=0, max_value=20, key=f"atq_{i}", label_visibility="collapsed")
                        
                        if st.button("Atacar", key=f"btn_{i}"):
                            carta['def_actual'] -= daño
                            if carta['def_actual'] <= 0:
                                # Regla automática: Al morir una criatura, el Jefe recibe 3 de daño
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                                st.toast(f"¡{carta['nombre']} eliminada! -3 HP al Jefe")
                            st.rerun()
                    else:
                        st.caption("💠 ARTEFACTO")
    else:
        st.info("La mesa está limpia por ahora.")
