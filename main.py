import streamlit as st
import random
import os

st.set_page_config(page_title="Keyraken Adventure - Battle Board", layout="wide")

# Configuración de carpetas
RUTA_BASE = "proyecto_keyforge/"

def inicializar_mazo():
    pool = [
        {"nombre": "Crushing Arm", "tipo": "CRIATURA", "defensa": 9, "img": "1.png", "efecto": "Destroyed: -3 HP al Jefe"},
        {"nombre": "Grappling Tentacle", "tipo": "CRIATURA", "defensa": 6, "img": "kf_adv_keyraken_004.png", "efecto": "Play: Captura recursos"},
        {"nombre": "Shield Arm", "tipo": "CRIATURA", "defensa": 6, "img": "kf_adv_keyraken_008.png", "efecto": "Taunt. Destroyed: -3 HP al Jefe"},
        {"nombre": "Lashing Tentacle", "tipo": "CRIATURA", "defensa": 3, "img": "kf_adv_keyraken_006.png", "efecto": "Skirmish. -3 HP al Jefe"},
        {"nombre": "Ascending Jet", "tipo": "ARTEFACTO", "defensa": 0, "img": "kf_adv_keyraken_038.png", "efecto": "Soporte: Potencia criaturas"},
    ]
    return random.choices(pool, k=43)

# --- INICIALIZACIÓN ---
if 'reserva_daño' not in st.session_state: st.session_state.reserva_daño = 0
if 'log' not in st.session_state: st.session_state.log = []
if 'mesa' not in st.session_state: st.session_state.mesa = []

if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Preparando el Keyraken")
    n_jug = st.number_input("Jugadores", min_value=1, value=1)
    if st.button("Iniciar"):
        st.session_state.vida_max = 30 * n_jug
        st.session_state.vida_actual = st.session_state.vida_max
        st.session_state.llaves_unforged = 3
        st.session_state.armadura_actual = 2 * st.session_state.llaves_unforged
        st.session_state.recursos_jefe = 0
        st.session_state.llaves_jefe = 0
        st.session_state.mazo = inicializar_mazo()
        st.session_state.juego_iniciado = True
        st.rerun()
else:
    # --- CABECERA DE ESTADO ---
    st.title("Batalla contra el Keyraken")
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    col_stat1.metric("HP Jefe", f"{st.session_state.vida_actual}")
    col_stat2.metric("Armadura", f"{st.session_state.armadura_actual}")
    col_stat3.metric("Llaves Jefe", f"{st.session_state.llaves_jefe}/3")
    col_stat4.info(f"💥 Reserva Daño: {st.session_state.reserva_daño}")

    st.divider()

    # --- CUERPO DEL JUEGO ---
    col_panel, col_tablero = st.columns([1, 2.5])

    with col_panel:
        st.subheader("Turno del Jefe")
        if st.button("🎴 REVELAR CARTA"):
            if st.session_state.mazo:
                st.session_state.armadura_actual = 2 * st.session_state.llaves_unforged
                carta = st.session_state.mazo.pop(0)
                if carta['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    carta['def_actual'] = carta['defensa']
                    st.session_state.mesa.append(carta)
                    st.session_state.log.append(f"Jefe jugó: {carta['nombre']}")
                else:
                    st.session_state.recursos_jefe += 2
                    st.session_state.log.append(f"Acción: {carta['nombre']} (+2 recursos)")
                st.rerun()

        st.divider()
        st.subheader("Tu Ataque")
        nuevo_d = st.number_input("Cargar Daño:", min_value=0, step=1)
        if st.button("Sumar a Reserva"):
            st.session_state.reserva_daño += nuevo_d
            st.rerun()

        # Selector de objetivo basado en lo que hay en mesa
        nombres_targets = ["Keyraken"] + [f"{c['nombre']} (ID:{i})" for i, c in enumerate(st.session_state.mesa)]
        target = st.selectbox("Objetivo:", nombres_targets)
        puntos = st.number_input("Puntos a usar:", min_value=1, max_value=max(1, st.session_state.reserva_daño))
        
        if st.button("CONFIRMAR DAÑO"):
            if st.session_state.reserva_daño >= puntos:
                if target == "Keyraken":
                    # Desgaste de armadura primero
                    if st.session_state.armadura_actual > 0:
                        abs = min(puntos, st.session_state.armadura_actual)
                        st.session_state.armadura_actual -= abs
                        sobrante = puntos - abs
                        if sobrante > 0: st.session_state.vida_actual -= sobrante
                    else:
                        st.session_state.vida_actual -= puntos
                else:
                    # Daño a criatura
                    idx = int(target.split("ID:")[1].replace(")", ""))
                    st.session_state.mesa[idx]['def_actual'] -= puntos
                    if st.session_state.mesa[idx]['def_actual'] <= 0:
                        st.session_state.vida_actual -= 3
                        st.session_state.mesa.pop(idx)
                        st.toast("¡Criatura destruida! -3 HP al Jefe")
                
                st.session_state.reserva_daño -= puntos
                st.rerun()

    with col_tablero:
        st.subheader("🏟️ Mesa del Keyraken")
        if st.session_state.mesa:
            # Creamos una cuadrícula dinámica
            cols_mesa = st.columns(3)
            for idx, carta in enumerate(st.session_state.mesa):
                with cols_mesa[idx % 3]:
                    with st.container(border=True):
                        # Mostrar imagen de la carta
                        img_path = RUTA_BASE + carta['img']
                        if os.path.exists(img_path):
                            st.image(img_path, use_container_width=True)
                        else:
                            st.warning(f"No image: {carta['img']}")
                        
                        st.write(f"**{carta['nombre']}**")
                        if carta['tipo'] == "CRIATURA":
                            st.write(f"❤️ Vida: {carta['def_actual']} / {carta['defensa']}")
                            progreso = max(0.0, float(carta['def_actual'] / carta['defensa']))
                            st.progress(progreso)
                        else:
                            st.caption("💠 ARTEFACTO")
                        st.write(f"*{carta['efecto']}*")
        else:
            st.info("La mesa está limpia. ¡Ataca directamente al Keyraken!")

    # Forjado
    if st.session_state.recursos_jefe >= 6:
        st.session_state.recursos_jefe -= 6
        st.session_state.llaves_jefe += 1
        st.rerun()

    # Historial flotante al final
    with st.expander("Ver Historial de Batalla"):
        for l in reversed(st.session_state.log):
            st.write(l)
