import streamlit as st
import random
import os

# Configuración de la página para que se vea bien en web y móvil
st.set_page_config(page_title="Keyraken Adventure", layout="wide")

# --- RUTA DE LA IMAGEN (Corregida según tu repo) ---
# Como tu imagen está dentro de una carpeta, debemos incluirla en la ruta
RUTA_IMAGEN = "proyecto_keyforge/kf_adv_keyraken_keyraken.pdf.png"

# --- LÓGICA DE CARTAS (Mapeo de tus PDF) ---
def inicializar_mazo():
    pool = [
        {"nombre": "Crushing Arm", "tipo": "CRIATURA", "defensa": 9, "efecto": "Destroyed: -3 HP al Jefe (ignora armadura)"},
        {"nombre": "Shield Arm", "tipo": "CRIATURA", "defensa": 6, "efecto": "Taunt: Debes atacarlo antes que al Jefe"},
        {"nombre": "Grappling Tentacle", "tipo": "CRIATURA", "defensa": 6, "efecto": "Play: Captura recursos del jugador"},
        {"nombre": "Beast of Dark Legend", "tipo": "ACCION", "efecto": "Jefe gana recursos por cada llave no forjada"},
        {"nombre": "Ascending Jet", "tipo": "ARTEFACTO", "efecto": "Soporte: +3 poder a la criatura más débil"}
    ]
    # Creamos el mazo de 43 cartas
    mazo = random.choices(pool, k=43)
    random.shuffle(mazo)
    return mazo

# --- INICIALIZACIÓN DE ESTADO ---
if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Keyraken Adventure")
    num_jugadores = st.number_input("¿Cuántos jugadores?", min_value=1, value=1)
    if st.button("Empezar Batalla"):
        st.session_state.num_jugadores = num_jugadores
        st.session_state.vida_max = 30 * num_jugadores
        st.session_state.vida_actual = st.session_state.vida_max
        st.session_state.llaves_unforged = 3
        st.session_state.recursos_jefe = 0
        st.session_state.llaves_jefe = 0
        st.session_state.mesa = []
        st.session_state.mazo = inicializar_mazo()
        st.session_state.juego_iniciado = True
        st.rerun()

else:
    # --- CÁLCULO DE ARMADURA DINÁMICA ---
    # +2 por cada llave que el jugador no ha forjado aún
    armadura_jefe = 2 * st.session_state.llaves_unforged

    st.title("Batalla contra el Keyraken")

    col_izq, col_der = st.columns([1, 2])

    with col_izq:
        st.subheader("El Jefe")
        # Mostrar imagen desde la subcarpeta
        if os.path.exists(RUTA_IMAGEN):
            st.image(RUTA_IMAGEN, use_container_width=True)
        else:
            st.error(f"No se encuentra: {RUTA_IMAGEN}")
            st.info("Asegúrate de que la carpeta se llame 'proyecto_keyforge' en GitHub.")

        st.metric("Vida", f"{st.session_state.vida_actual} HP")
        st.metric("Armadura Activa", f"{armadura_jefe}")
        st.write(f"💎 Recursos: {st.session_state.recursos_jefe} / 6")
        st.write(f"🔑 Llaves Jefe: {st.session_state.llaves_jefe} / 3")

    with col_der:
        st.subheader("Mesa y Acciones")
        
        # Botón para robar carta del mazo de 43
        if st.button("Revelar Carta (Turno del Jefe)"):
            if st.session_state.mazo:
                carta = st.session_state.mazo.pop(0)
                if carta['tipo'] == "ACCION":
                    st.warning(f"ACCIÓN: {carta['nombre']} - {carta['efecto']}")
                    st.session_state.recursos_jefe += 2
                else:
                    st.session_state.mesa.append(carta)
                
                # Regla de forjado de llaves
                if st.session_state.recursos_jefe >= 6:
                    st.session_state.recursos_jefe -= 6
                    st.session_state.llaves_jefe += 1
            st.rerun()

        # Visualización de criaturas en mesa
        if st.session_state.mesa:
            st.write("--- Criaturas/Artefactos en juego ---")
            cols_mesa = st.columns(2)
            for idx, c in enumerate(st.session_state.mesa):
                with cols_mesa[idx % 2]:
                    with st.container(border=True):
                        st.write(f"**{c['nombre']}** ({c['tipo']})")
                        st.write(f"DEF: {c['defensa']}" if 'defensa' in c else "")
                        st.caption(c['efecto'])
                        if st.button(f"Destruir {idx}", key=f"del_{idx}"):
                            # Al destruir partes, el jefe recibe 3 de daño directo
                            st.session_state.vida_actual -= 3
                            st.session_state.mesa.pop(idx)
                            st.rerun()

        st.divider()
        # Ataque directo al Jefe
        daño_atq = st.number_input("Tu daño de ataque:", min_value=0)
        if st.button("Atacar al Keyraken"):
            if daño_atq > armadura_jefe:
                daño_real = daño_atq - armadura_jefe
                st.session_state.vida_actual -= daño_real
                st.success(f"¡Golpeaste al jefe por {daño_real}!")
            else:
                st.error("Daño insuficiente para atravesar la armadura.")
            st.rerun()

    # Condiciones de victoria / derrota
    if st.session_state.vida_actual <= 0:
        st.balloons()
        st.success("¡VICTORIA! El Keyraken ha sido derrotado.")
        if st.button("Reiniciar"): st.session_state.clear()
    
    if st.session_state.llaves_jefe >= 3:
        st.error("DERROTA: El Jefe ha forjado 3 llaves.")
        if st.button("Reiniciar"): st.session_state.clear()
