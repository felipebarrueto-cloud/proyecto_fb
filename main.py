import streamlit as st
import random
import os

st.set_page_config(page_title="Keyraken Adventure", layout="wide")

RUTA_BASE = "proyecto_keyforge/"

# --- CONFIGURACIÓN DE MAZO ---
def inicializar_mazo():
    pool = [
        {"nombre": "Crushing Arm", "tipo": "CRIATURA", "defensa": 9, "img": "1.png", "efecto": "Al morir: -3 HP al Jefe"},
        {"nombre": "Grappling Tentacle", "tipo": "CRIATURA", "defensa": 6, "img": "kf_adv_keyraken_004.png", "efecto": "Captura recursos"},
        {"nombre": "Shield Arm", "tipo": "CRIATURA", "defensa": 6, "img": "kf_adv_keyraken_008.png", "efecto": "Taunt (Protege al Jefe)"},
        {"nombre": "Lashing Tentacle", "tipo": "CRIATURA", "defensa": 3, "img": "kf_adv_keyraken_006.png", "efecto": "-3 HP al Jefe"},
        {"nombre": "Ascending Jet", "tipo": "ARTEFACTO", "defensa": 0, "img": "kf_adv_keyraken_038.png", "efecto": "Efecto de soporte"}
    ]
    return random.choices(pool, k=43)

# --- INICIALIZACIÓN ---
if 'reserva_daño' not in st.session_state: st.session_state.reserva_daño = 0
if 'mesa' not in st.session_state: st.session_state.mesa = []

if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Configuración")
    n_jug = st.number_input("Jugadores", min_value=1, value=1)
    if st.button("Iniciar Batalla"):
        st.session_state.vida_max = 30 * n_jug
        st.session_state.vida_actual = st.session_state.vida_max
        st.session_state.llaves_unforged = 3
        st.session_state.armadura_actual = 6
        st.session_state.recursos_jefe = 0
        st.session_state.llaves_jefe = 0
        st.session_state.mazo = inicializar_mazo()
        st.session_state.juego_iniciado = True
        st.rerun()
else:
    # --- INTERFAZ ---
    col_jefe, col_tablero = st.columns([1, 2.5])

    with col_jefe:
        # 1. IMAGEN DEL JEFE (Arriba de los valores)
        img_jefe = RUTA_BASE + "kf_adv_keyraken_keyraken.pdf.png"
        if os.path.exists(img_jefe):
            st.image(img_jefe, caption="EL KEYRAKEN", use_container_width=True)
        
        # 2. VALORES DEL JEFE
        st.metric("Vida Restante", f"{st.session_state.vida_actual} HP")
        st.metric("Armadura Temporal", f"{st.session_state.armadura_actual}")
        st.write(f"🔑 Llaves: {st.session_state.llaves_jefe}/3 | 💎 {st.session_state.recursos_jefe}/6")
        
        st.divider()
        
        # 3. CONTROL DE DAÑO
        st.subheader("⚔️ Tu Ataque")
        carga = st.number_input("Cargar daño:", min_value=0, step=1)
        if st.button("Sumar Daño a Reserva"):
            st.session_state.reserva_daño += carga
            st.rerun()
        
        st.warning(f"Tienes **{st.session_state.reserva_daño}** puntos para usar.")
        if st.button("Vaciar Reserva"):
            st.session_state.reserva_daño = 0
            st.rerun()

    with col_tablero:
        st.subheader("🏟️ Tablero y Acciones")
        
        # Botón para turno del jefe
        if st.button("🎴 Revelar Carta del Jefe"):
            if st.session_state.mazo:
                st.session_state.armadura_actual = 2 * st.session_state.llaves_unforged
                carta = st.session_state.mazo.pop(0)
                if carta['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    carta['def_actual'] = carta['defensa']
                    st.session_state.mesa.append(carta)
                else:
                    st.session_state.recursos_jefe += 2
                st.rerun()

        # SELECTOR DE ATAQUE SIMPLIFICADO
        if st.session_state.reserva_daño > 0:
            st.write("---")
            opciones = ["Al Jefe (Keyraken)"] + [f"A {c['nombre']} (HP: {c['def_actual']})" for i, c in enumerate(st.session_state.mesa)]
            target = st.selectbox("¿A quién quieres atacar?", opciones)
            
            if st.button("💥 ATACAR"):
                if target == "Al Jefe (Keyraken)":
                    # Gasta todo el daño en el jefe
                    daño = st.session_state.reserva_daño
                    if st.session_state.armadura_actual > 0:
                        absorbe = min(daño, st.session_state.armadura_actual)
                        st.session_state.armadura_actual -= absorbe
                        daño -= absorbe
                    st.session_state.vida_actual -= daño
                    st.session_state.reserva_daño = 0
                else:
                    # Gasta solo lo necesario para la criatura
                    idx = opciones.index(target) - 1
                    c = st.session_state.mesa[idx]
                    necesario = c['def_actual']
                    daño_usado = min(st.session_state.reserva_daño, necesario)
                    
                    c['def_actual'] -= daño_usado
                    st.session_state.reserva_daño -= daño_usado
                    
                    if c['def_actual'] <= 0:
                        st.session_state.vida_actual -= 3
                        st.session_state.mesa.pop(idx)
                        st.toast(f"{c['nombre']} destruida!")
                st.rerun()

        # VISUALIZACIÓN DE CARTAS EN MESA
        st.write("---")
        if st.session_state.mesa:
            cols = st.columns(3)
            for i, carta in enumerate(st.session_state.mesa):
                with cols[i % 3]:
                    with st.container(border=True):
                        p = RUTA_BASE + carta['img']
                        if os.path.exists(p): st.image(p)
                        st.write(f"**{carta['nombre']}**")
                        if carta['defensa'] > 0:
                            st.write(f"❤️ {carta['def_actual']} / {carta['defensa']}")
                        st.caption(carta['efecto'])
        else:
            st.info("Mesa libre. Carga daño y ataca al jefe.")

    # Regla de llaves del jefe
    if st.session_state.recursos_jefe >= 6:
        st.session_state.recursos_jefe = 0
        st.session_state.llaves_jefe += 1
        st.rerun()
