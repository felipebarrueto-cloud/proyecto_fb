import streamlit as st
import random
import os

st.set_page_config(page_title="Keyraken Adventure", layout="wide")

# Ruta de la carpeta en tu repositorio de GitHub
RUTA_BASE = "proyecto_keyforge/"

def inicializar_mazo():
    # Definimos el pool de cartas
    # Nota: Aquí asociamos Crushing Arm con 1.png
    pool = [
        {"nombre": "Crushing Arm", "tipo": "CRIATURA", "defensa": 9, "img": "1.png", "efecto": "Destroyed: Deal 3 to the Keyraken (Ignore Armor)"},
        {"nombre": "Grappling Tentacle", "tipo": "CRIATURA", "defensa": 6, "img": "kf_adv_keyraken_004.png", "efecto": "Play: Captura recursos"},
        {"nombre": "Shield Arm", "tipo": "CRIATURA", "defensa": 6, "img": "kf_adv_keyraken_008.png", "efecto": "Taunt (Protege al Jefe)"},
        {"nombre": "Beast of Dark Legend", "tipo": "ACCION", "img": "kf_adv_keyraken_014.png", "efecto": "Jefe gana recursos por llaves"},
    ]
    # Generamos las 43 cartas del mazo de aventura
    mazo = random.choices(pool, k=43)
    random.shuffle(mazo)
    return mazo

if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

# --- CONFIGURACIÓN INICIAL ---
if not st.session_state.juego_iniciado:
    st.title("🐙 Keyraken Adventure")
    n_jugadores = st.number_input("Número de jugadores", min_value=1, value=1)
    if st.button("Comenzar Partida"):
        st.session_state.vida_max = 30 * n_jugadores
        st.session_state.vida_actual = st.session_state.vida_max
        st.session_state.llaves_unforged = 3
        st.session_state.armadura_actual = 2 * st.session_state.llaves_unforged
        st.session_state.recursos_jefe = 0
        st.session_state.llaves_jefe = 0
        st.session_state.mesa = []
        st.session_state.mazo = inicializar_mazo()
        st.session_state.juego_iniciado = True
        st.rerun()

# --- INTERFAZ DE JUEGO ---
else:
    st.title("Batalla contra el Keyraken")
    col_jefe, col_mesa = st.columns([1, 2])

    with col_jefe:
        st.subheader("Estado del Jefe")
        # Imagen principal del jefe
        path_jefe = RUTA_BASE + "kf_adv_keyraken_keyraken.pdf.png"
        if os.path.exists(path_jefe):
            st.image(path_jefe, use_container_width=True)
        
        st.metric("Vida del Keyraken", f"{st.session_state.vida_actual} HP")
        
        # EFECTO VISUAL DE ARMADURA
        color_armadura = "normal" if st.session_state.armadura_actual > 0 else "inverse"
        if st.session_state.armadura_actual == 0:
            st.error("¡ARMADURA DESTRUIDA! El daño va directo a la vida.")
        
        st.metric("Armadura Temporal", f"{st.session_state.armadura_actual}")
        st.write(f"🔑 Llaves Jefe: {st.session_state.llaves_jefe}/3 | 💎: {st.session_state.recursos_jefe}/6")

    with col_mesa:
        # Botón para revelar carta: Restaura armadura y saca carta
        if st.button("Revelar Carta (Restaura Armadura)"):
            if st.session_state.mazo:
                # Restauramos al valor original basado en llaves
                st.session_state.armadura_actual = 2 * st.session_state.llaves_unforged
                carta = st.session_state.mazo.pop(0)
                if carta['tipo'] == "CRIATURA":
                    carta['def_actual'] = carta['defensa']
                    st.session_state.mesa.append(carta)
                elif carta['tipo'] == "ACCION":
                    st.session_state.recursos_jefe += 2
                st.rerun()

        # Mostrar criaturas con su imagen respectiva (1.png para Crushing Arm)
        if st.session_state.mesa:
            st.write("### Criaturas en combate")
            filas = st.columns(3)
            for i, c in enumerate(st.session_state.mesa):
                with filas[i % 3]:
                    with st.container(border=True):
                        # Cargar imagen de la criatura (ej: proyecto_keyforge/1.png)
                        path_img = RUTA_BASE + c['img']
                        if os.path.exists(path_img):
                            st.image(path_img, use_container_width=True)
                        
                        st.markdown(f"**{c['nombre']}**")
                        st.write(f"❤️ {c['def_actual']} / {c['defensa']}")
                        
                        dmg_c = st.number_input("Daño a criatura", min_value=0, key=f"d_{i}")
                        if st.button("Atacar", key=f"b_{i}"):
                            c['def_actual'] -= dmg_c
                            if c['def_actual'] <= 0:
                                st.session_state.vida_actual -= 3 # Daño directo al morir
                                st.session_state.mesa.pop(i)
                            st.rerun()

    # ATAQUE AL JEFE
    st.divider()
    atq_total = st.number_input("Tu ataque total este turno:", min_value=0)
    if st.button("💥 Ejecutar Ataque al Jefe"):
        if st.session_state.armadura_actual > 0:
            # Primero consume armadura
            absorbido = min(atq_total, st.session_state.armadura_actual)
            st.session_state.armadura_actual -= absorbido
            atq_total -= absorbido
            st.info(f"Armadura reducida en {absorbido}")
        
        if atq_total > 0:
            # El resto va a la vida
            st.session_state.vida_actual -= atq_total
            st.success(f"¡Daño directo al Jefe: {atq_total}!")
        st.rerun()

    # Regla de llaves del jefe
    if st.session_state.recursos_jefe >= 6:
        st.session_state.recursos_jefe -= 6
        st.session_state.llaves_jefe += 1
        st.warning("¡El Jefe ha forjado una llave!")
        st.rerun()
