import streamlit as st
import random
import os

st.set_page_config(page_title="Keyraken Adventure - Combo Mode", layout="wide")

RUTA_BASE = "proyecto_keyforge/"

def inicializar_mazo():
    pool = [
        {"nombre": "Crushing Arm", "tipo": "CRIATURA", "defensa": 9, "img": "1.png", "efecto": "Destroyed: -3 HP al Jefe"},
        {"nombre": "Grappling Tentacle", "tipo": "CRIATURA", "defensa": 6, "img": "kf_adv_keyraken_004.png", "efecto": "Play: Captura recursos"},
        {"nombre": "Shield Arm", "tipo": "CRIATURA", "defensa": 6, "img": "kf_adv_keyraken_008.png", "efecto": "Taunt. Destroyed: -3 HP al Jefe"},
        {"nombre": "Beast of Dark Legend", "tipo": "ACCION", "img": "kf_adv_keyraken_014.png", "efecto": "Jefe gana recursos"},
    ]
    return random.choices(pool, k=43)

# --- ESTADO INICIAL ---
if 'reserva_daño' not in st.session_state: st.session_state.reserva_daño = 0
if 'log' not in st.session_state: st.session_state.log = []
if 'turno' not in st.session_state: st.session_state.turno = 1

if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Configuración Keyraken")
    n_jug = st.number_input("Jugadores", min_value=1, value=1)
    if st.button("Empezar Batalla"):
        st.session_state.vida_max = 30 * n_jug
        st.session_state.vida_actual = st.session_state.vida_max
        st.session_state.llaves_unforged = 3
        st.session_state.armadura_base = 2 * st.session_state.llaves_unforged
        st.session_state.armadura_actual = st.session_state.armadura_base
        st.session_state.recursos_jefe = 0
        st.session_state.llaves_jefe = 0
        st.session_state.mesa = []
        st.session_state.mazo = inicializar_mazo()
        st.session_state.juego_iniciado = True
        st.rerun()
else:
    # --- INTERFAZ ---
    col_jefe, col_mesa, col_log = st.columns([1, 1.5, 1])

    with col_jefe:
        st.subheader(f"Turno {st.session_state.turno}")
        path_jefe = RUTA_BASE + "kf_adv_keyraken_keyraken.pdf.png"
        if os.path.exists(path_jefe): st.image(path_jefe)
        
        st.metric("Vida Jefe", f"{st.session_state.vida_actual} HP")
        st.metric("Armadura Temporal", f"{st.session_state.armadura_actual} / {st.session_state.armadura_base}")
        st.write(f"🔑 Llaves: {st.session_state.llaves_jefe} | 💎: {st.session_state.recursos_jefe}")

    with col_mesa:
        st.subheader("Acciones del Jefe")
        if st.button("🔥 Revelar Carta (Nueva Amenaza)"):
            if st.session_state.mazo:
                st.session_state.turno += 1
                st.session_state.armadura_base = 2 * st.session_state.llaves_unforged
                st.session_state.armadura_actual = st.session_state.armadura_base
                st.session_state.reserva_daño = 0 # El daño no usado se pierde al cambiar de turno
                carta = st.session_state.mazo.pop(0)
                if carta['tipo'] == "CRIATURA":
                    carta['def_actual'] = carta['defensa']
                    st.session_state.mesa.append(carta)
                    st.session_state.log.append(f"T{st.session_state.turno}: Aparece {carta['nombre']}")
                else:
                    st.session_state.recursos_jefe += 2
                    st.session_state.log.append(f"T{st.session_state.turno}: Acción {carta['nombre']} activada")
                st.rerun()

        st.divider()
        st.subheader("⚔️ Panel de Combate")
        
        # 1. CARGAR DAÑO
        col_input, col_status = st.columns([1, 1])
        with col_input:
            nuevo_daño = st.number_input("Cargar daño total del ataque:", min_value=0, step=1, key="carga_daño")
            if st.button("Cargar a la Reserva"):
                st.session_state.reserva_daño += nuevo_daño
                st.session_state.log.append(f"T{st.session_state.turno}: Cargaste {nuevo_daño} de daño.")
                st.rerun()
        
        with col_status:
            st.info(f"Daño Disponible: **{st.session_state.reserva_daño}**")
            if st.button("Vaciar Reserva"):
                st.session_state.reserva_daño = 0
                st.rerun()

        # 2. SELECTOR DE OBJETIVOS (Solo si hay daño en reserva)
        if st.session_state.reserva_daño > 0:
            nombres_criaturas = [f"Criatura: {c['nombre']} (HP:{c['def_actual']})" for c in st.session_state.mesa]
            objetivo = st.selectbox("¿A quién aplicar el daño?", ["El Keyraken"] + nombres_criaturas)
            
            puntos_a_usar = st.number_input("Puntos de daño a usar:", min_value=1, max_value=st.session_state.reserva_daño, value=min(st.session_state.reserva_daño, 1))

            if st.button("Aplicar Daño"):
                if objetivo == "El Keyraken":
                    # Lógica armadura -> vida
                    puntos_restantes = puntos_a_usar
                    if st.session_state.armadura_actual > 0:
                        abs = min(puntos_restantes, st.session_state.armadura_actual)
                        st.session_state.armadura_actual -= abs
                        puntos_restantes -= abs
                        st.session_state.log.append(f"T{st.session_state.turno}: {abs} de armadura reducida.")
                    
                    if puntos_restantes > 0:
                        st.session_state.vida_actual -= puntos_restantes
                        st.session_state.log.append(f"T{st.session_state.turno}: {puntos_restantes} de vida restada al Jefe.")
                
                else:
                    # Atacar criatura
                    idx = nombres_criaturas.index(objetivo)
                    criatura = st.session_state.mesa[idx]
                    daño_real = min(puntos_a_usar, criatura['def_actual'])
                    criatura['def_actual'] -= puntos_a_usar # Aplicamos todo el daño elegido
                    
                    st.session_state.log.append(f"T{st.session_state.turno}: {puntos_a_usar} daño a {criatura['nombre']}")
                    
                    if criatura['def_actual'] <= 0:
                        st.session_state.vida_actual -= 3
                        st.session_state.log.append(f"T{st.session_state.turno}: {criatura['nombre']} DESTRUIDA (-3 HP al Jefe)")
                        st.session_state.mesa.pop(idx)
                
                # Descontar de la reserva global
                st.session_state.reserva_daño -= puntos_a_usar
                st.rerun()

    with col_log:
        st.subheader("📜 Log")
        for e in reversed(st.session_state.log[-15:]):
            st.write(f"- {e}")

    # Forjado automático
    if st.session_state.recursos_jefe >= 6:
        st.session_state.recursos_jefe -= 6
        st.session_state.llaves_jefe += 1
        st.session_state.log.append(f"T{st.session_state.turno}: JEFE FORJÓ LLAVE")
        st.rerun()

    if st.session_state.vida_actual <= 0:
        st.success("¡VICTORIA!")
        st.balloons()
