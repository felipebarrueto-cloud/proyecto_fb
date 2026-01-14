# tablero.py

import streamlit as st
import os

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        if st.session_state.mazo:
            # 1. Limpiar carta activa anterior (Mover a Mesa o Descarte)
            if st.session_state.carta_activa:
                c_v = st.session_state.carta_activa
                if c_v['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_v['def_actual'] = c_v.get('defensa', 0)
                    st.session_state.mesa.append(c_v)
                else:
                    st.session_state.descarte.append(c_v)
            
            # 2. Revelar la nueva
            nueva_carta = st.session_state.mazo.pop(0)
            
            # 3. LÓGICA DE ÁMBAR AUTOMÁTICO
            regalo = nueva_carta.get('ambar_regalo', 0)
            if regalo > 0:
                st.session_state.recursos_jefe += regalo
                st.toast(f"✨ ¡El Jefe ganó {regalo} de Ámbar por revelar {nueva_carta['nombre']}!")
            
            # Guardamos como carta activa
            st.session_state.carta_activa = nueva_carta

            # 4. CHEQUEO AUTOMÁTICO DE FORJADO
            # Si al revelar una carta llega a 6, forja llave inmediatamente
            if st.session_state.recursos_jefe >= 6:
                st.session_state.recursos_jefe -= 6
                st.session_state.llaves_jefe += 1
                st.warning("⚠️ ¡EL KEYRAKEN HA FORJADO UNA LLAVE!")
                
            st.rerun()
