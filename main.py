import streamlit as st
import random
import os

st.set_page_config(page_title="Keyraken Adventure", layout="wide")

RUTA_BASE = "proyecto_keyforge/"

# --- CONFIGURACIÓN DE MAZO Y ASOCIACIONES ---
def inicializar_mazo():
    pool = [
        {"nombre": "Crushing Arm", "tipo": "CRIATURA", "defensa": 9, "img": "1.png", "efecto": "Destroyed: -3 HP al Jefe"},
        {"nombre": "Grappling Tentacle", "tipo": "CRIATURA", "defensa": 6, "img": "3.png", "efecto": "Play: Captura recursos"},
        {"nombre": "Lashing Tentacle", "tipo": "CRIATURA", "defensa": 3, "img": "5.png", "efecto": "Skirmish"},
        {"nombre": "Shield Arm", "tipo": "CRIATURA", "defensa": 6, "img": "8.png", "efecto": "Taunt"},
        {"nombre": "Beast of Dark Legend", "tipo": "ACCION", "img": "14.png", "efecto": "Jefe gana recursos"}
    ]
    # Generamos el mazo de 43 cartas
    return random.choices(pool, k=43)

# --- INICIALIZACIÓN DE ESTADOS ---
if 'log' not in st.session_state: st.session_state.log = []
if 'mesa' not in st.session_state: st.session_state.mesa = []
if 'descarte' not in st.session_state: st.session_state.descarte = []
if 'reserva_daño' not in st.session_state: st.session_state.reserva_daño = 0

if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

# --- PANTALLA DE INICIO ---
if not st.session_state.juego_iniciado:
    st.title("🐙 Configuración Keyraken")
    n_jug = st.number_input("Número de Jugadores", min_value=1, value=1)
    if st.button("Iniciar Batalla"):
        st.session_state.vida_max = 30 * n_jug
        st.session_state.vida_actual = st.session_state.vida_max
        st.session_state.llaves_unforged = 3
        st.session_state.armadura_actual = 6
        st.session_state.recursos_jefe = 0
        st.session_state.llaves_jefe = 0
        st.session_state.mazo = inicializar_mazo()
        st.session_state.log.append("--- Inicio de la Partida ---")
        st.session_state.juego_iniciado = True
        st.rerun()

# --- INTERFAZ DE BATALLA ---
else:
    # 1. BARRA LATERAL (Log e Historial de Descarte)
    with st.sidebar:
        st.header("📜 Log de Batalla")
        for e in reversed(st.session_state.log[-10:]):
            st.caption(e)
        
        st.divider()
        st.header("🗑️ Zona de Descarte")
        if st.session_state.descarte:
            for d in reversed(st.session_state.descarte):
                st.write(f"• {d['nombre']} ({d['tipo']})")
        else:
            st.write("Vacío")

    # 2. CUERPO PRINCIPAL
    col_jefe, col_ataque = st.columns([1, 2])

    with col_jefe:
        # Visualización fija del Jefe
        img_jefe = RUTA_BASE + "kf_adv_keyraken_keyraken.pdf.png"
        if os.path.exists(img_jefe):
            st.image(img_jefe, use_container_width=True)
        
        st.metric("Vida del Jefe", f"{st.session_state.vida_actual} HP")
        st.metric("Armadura Temporal", f"{st.session_state.armadura_actual}")
        st.write(f"🔑 Llaves: {st.session_state.llaves_jefe}/3 | 💎 Recursos: {st.session_state.recursos_jefe}/6")
        
        if st.button("🎴 Revelar Carta (Turno Jefe)"):
            if st.session_state.mazo:
                st.session_state.armadura_actual = 2 * st.session_state.llaves_unforged
                carta = st.session_state.mazo.pop(0)
                if carta['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    carta['def_actual'] = carta['defensa']
                    st.session_state.mesa.append(carta)
                    st.session_state.log.append(f"Jefe jugó {carta['nombre']}")
                else:
                    st.session_state.recursos_jefe += 2
                    st.session_state.descarte.append(carta) # Las acciones van al descarte
                    st.session_state.log.append(f"Acción: {carta['nombre']} ejecutada")
                st.rerun()

    with col_ataque:
        st.subheader("⚔️ Gestión de Daño")
        c1, c2 = st.columns(2)
        with c1:
            carga = st.number_input("Cargar daño a la reserva:", min_value=0, step=1)
            if st.button("Añadir Daño"):
                st.session_state.reserva_daño += carga
                st.rerun()
        with c2:
            st.info(f"Puntos Disponibles: **{st.session_state.reserva_daño}**")
            if st.button("Vaciar Reserva"):
                st.session_state.reserva_daño = 0
                st.rerun()

        # Selector Único de Objetivo
        if st.session_state.reserva_daño > 0:
            objetivos = ["El Jefe (Keyraken)"] + [f"{c['nombre']} (HP: {c['def_actual']})" for c in st.session_state.mesa]
            target = st.selectbox("Selecciona objetivo del ataque:", objetivos)
            
            if st.button("CONFIRMAR ATAQUE"):
                if target == "El Jefe (Keyraken)":
                    daño = st.session_state.reserva_daño
                    if st.session_state.armadura_actual > 0:
                        abs = min(daño, st.session_state.armadura_actual)
                        st.session_state.armadura_actual -= abs
                        daño -= abs
                    st.session_state.vida_actual -= daño
                    st.session_state.log.append(f"Ataque al Jefe por {st.session_state.reserva_daño}")
                    st.session_state.reserva_daño = 0
                else:
                    idx = objetivos.index(target) - 1
                    c = st.session_state.mesa[idx]
                    necesario = c['def_actual']
                    usado = min(st.session_state.reserva_daño, necesario)
                    c['def_actual'] -= usado
                    st.session_state.reserva_daño -= usado
                    st.session_state.log.append(f"{usado} daño a {c['nombre']}")
                    
                    if c['def_actual'] <= 0:
                        st.session_state.vida_actual -= 3
                        st.session_state.descarte.append(st.session_state.mesa.pop(idx))
                        st.session_state.log.append(f"{c['nombre']} DESTRUIDO")
                st.rerun()

    st.divider()

    # --- CARRIL DE CARTAS (Mesa horizontal) ---
    st.subheader("🏟️ Tablero del Keyraken")
    if st.session_state.mesa:
        # Usamos un contenedor con columnas para simular el carril
        cols = st.columns(len(st.session_state.mesa) if len(st.session_state.mesa) < 6 else 6)
        for i, carta in enumerate(st.session_state.mesa):
            with cols[i % 6]:
                with st.container(border=True):
                    p = RUTA_BASE + carta['img']
                    if os.path.exists(p):
                        st.image(p, use_container_width=True)
                    else:
                        st.warning(f"Falta: {carta['img']}")
                    
                    st.markdown(f"**{carta['nombre']}**")
                    if carta['defensa'] > 0:
                        st.progress(max(0.0, float(carta['def_actual'] / carta['defensa'])))
                        st.caption(f"HP: {carta['def_actual']} / {carta['defensa']}")
    else:
        st.info("La mesa está despejada.")

    # Regla recursos jefe
    if st.session_state.recursos_jefe >= 6:
        st.session_state.recursos_jefe -= 6
        st.session_state.llaves_jefe += 1
        st.rerun()

