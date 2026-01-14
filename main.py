import streamlit as st
import random
import os

st.set_page_config(page_title="Keyraken Adventure - Deck Balanced", layout="wide")

RUTA_BASE = "proyecto_keyforge/"

# --- CONFIGURACIÓN DEL MAZO OFICIAL (43 CARTAS) ---
def inicializar_mazo_oficial():
    # Definimos las cartas con sus cantidades exactas según el set de aventura
    cartas_definidas = [
        # CRIATURAS (Brazos y Tentáculos)
        {"nombre": "Crushing Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 9, "img": "1.png", "efecto": "Destroyed: -3 HP al Jefe"},
        {"nombre": "Grappling Tentacle", "cant": 4, "tipo": "CRIATURA", "defensa": 6, "img": "3.png", "efecto": "Play: Captura recursos"},
        {"nombre": "Lashing Tentacle", "cant": 4, "tipo": "CRIATURA", "defensa": 3, "img": "5.png", "efecto": "Skirmish"},
        {"nombre": "Shield Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 6, "img": "8.png", "efecto": "Taunt"},
        {"nombre": "Tenacious Arm", "cant": 2, "tipo": "CRIATURA", "defensa": 12, "img": "12.png", "efecto": "Reap: Roba recursos"},
        
        # ARTEFACTOS
        {"nombre": "Ascending Jet", "cant": 2, "tipo": "ARTEFACTO", "defensa": 0, "img": "38.png", "efecto": "Soporte"},
        {"nombre": "Submerged Cave", "cant": 2, "tipo": "ARTEFACTO", "defensa": 0, "img": "40.png", "efecto": "Efecto de entorno"},
        
        # ACCIONES (Se van directo al descarte tras activar su efecto)
        {"nombre": "Beast of Dark Legend", "cant": 3, "tipo": "ACCION", "img": "14.png", "efecto": "Jefe gana recursos"},
        {"nombre": "The Keyraken Emerges", "cant": 3, "tipo": "ACCION", "img": "16.png", "efecto": "Añade amenazas"},
        {"nombre": "Whirlpool", "cant": 4, "tipo": "ACCION", "img": "20.png", "efecto": "Efecto de control"},
    ]

    mazo_final = []
    for c in cartas_definidas:
        for _ in range(c["cant"]):
            # Creamos una copia de la carta para el mazo
            nueva_carta = c.copy()
            del nueva_carta["cant"] # No necesitamos el contador en la carta individual
            mazo_final.append(nueva_carta)
    
    # Rellenamos hasta 43 con cartas genéricas de "Amenaza Menor" si faltan
    while len(mazo_final) < 43:
        mazo_final.append({"nombre": "Minor Threat", "tipo": "ACCION", "img": "generic.png", "efecto": "Jefe gana 1 recurso"})

    random.shuffle(mazo_final)
    return mazo_final

# --- ESTADOS DE SESIÓN ---
if 'log' not in st.session_state: st.session_state.log = []
if 'mesa' not in st.session_state: st.session_state.mesa = []
if 'descarte' not in st.session_state: st.session_state.descarte = []
if 'reserva_daño' not in st.session_state: st.session_state.reserva_daño = 0

if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

# --- LÓGICA DE INICIO ---
if not st.session_state.juego_iniciado:
    st.title("🐙 Keyraken Adventure - Deck Setup")
    n_jug = st.number_input("Número de Jugadores", min_value=1, value=1)
    if st.button("Generar Mazo de 43 Cartas e Iniciar"):
        st.session_state.vida_max = 30 * n_jug
        st.session_state.vida_actual = st.session_state.vida_max
        st.session_state.llaves_unforged = 3
        st.session_state.armadura_actual = 6
        st.session_state.recursos_jefe = 0
        st.session_state.llaves_jefe = 0
        st.session_state.mazo = inicializar_mazo_oficial()
        st.session_state.juego_iniciado = True
        st.rerun()

# --- INTERFAZ DE BATALLA ---
else:
    col_izq, col_der = st.columns([1, 2.5])

    with col_izq:
        # Visualización del Jefe
        img_jefe = RUTA_BASE + "kf_adv_keyraken_keyraken.pdf.png"
        if os.path.exists(img_jefe): st.image(img_jefe)
        
        st.metric("HP Jefe", f"{st.session_state.vida_actual}")
        st.metric("Armadura", f"{st.session_state.armadura_actual}")
        st.write(f"Mazo: {len(st.session_state.mazo)} cartas restantes")
        
        st.divider()
        # Gestión de Daño
        val = st.number_input("Cargar Daño:", min_value=0, step=1)
        if st.button("Añadir Daño"):
            st.session_state.reserva_daño += val
            st.rerun()
        st.info(f"Reserva: {st.session_state.reserva_daño}")

    with col_der:
        # ACCIÓN: REVELAR CARTA
        if st.button("🎴 Revelar Carta del Mazo"):
            if st.session_state.mazo:
                # Reset Armadura
                st.session_state.armadura_actual = 2 * st.session_state.llaves_unforged
                
                carta = st.session_state.mazo.pop(0)
                if carta['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    carta['def_actual'] = carta.get('defensa', 0)
                    st.session_state.mesa.append(carta)
                    st.session_state.log.append(f"REVELADO: {carta['nombre']} (Quedan {len(st.session_state.mazo)})")
                else:
                    st.session_state.recursos_jefe += 2
                    st.session_state.descarte.append(carta)
                    st.session_state.log.append(f"ACCION: {carta['nombre']} - Ejecutada y Descartada")
                st.rerun()

        # ATAQUE SIMPLIFICADO
        if st.session_state.reserva_daño > 0:
            objs = ["Keyraken"] + [f"{c['nombre']} (ID:{i})" for i, c in enumerate(st.session_state.mesa)]
            target = st.selectbox("Objetivo:", objs)
            if st.button("EJECUTAR ATAQUE"):
                if target == "Keyraken":
                    d = st.session_state.reserva_daño
                    if st.session_state.armadura_actual > 0:
                        a = min(d, st.session_state.armadura_actual)
                        st.session_state.armadura_actual -= a
                        d -= a
                    st.session_state.vida_actual -= d
                    st.session_state.reserva_daño = 0
                else:
                    idx = int(target.split("ID:")[1].replace(")", ""))
                    c = st.session_state.mesa[idx]
                    coste = min(st.session_state.reserva_daño, c['def_actual'])
                    c['def_actual'] -= coste
                    st.session_state.reserva_daño -= coste
                    if c['def_actual'] <= 0:
                        st.session_state.vida_actual -= 3
                        st.session_state.descarte.append(st.session_state.mesa.pop(idx))
                st.rerun()

        # CARRIL DE CARTAS
        st.subheader("Tablero")
        if st.session_state.mesa:
            cols = st.columns(min(len(st.session_state.mesa), 5))
            for i, carta in enumerate(st.session_state.mesa):
                with cols[i % 5]:
                    with st.container(border=True):
                        p = RUTA_BASE + carta['img']
                        if os.path.exists(p): st.image(p)
                        st.write(f"**{carta['nombre']}**")
                        if carta['tipo'] == "CRIATURA":
                            st.caption(f"HP: {carta['def_actual']}/{carta['defensa']}")
        
        with st.expander("Ver Historial (Log)"):
            for l in reversed(st.session_state.log): st.write(l)

    # Forjado automático
    if st.session_state.recursos_jefe >= 6:
        st.session_state.recursos_jefe -= 6
        st.session_state.llaves_jefe += 1
        st.rerun()
