import streamlit as st
import random
import os

# Configuración de la página
st.set_page_config(page_title="Keyraken Adventure", layout="centered")

# --- LÓGICA DE DATOS (Basado en tus documentos) ---
def inicializar_mazo():
    # Mapeo de cartas del pool [cite: 2, 20, 42, 63, 131, 339]
    pool = [
        {"nombre": "Crushing Arm", "tipo": "criatura", "defensa": 9, "efecto": "Destrucción: -3 HP al Jefe [cite: 5]"},
        {"nombre": "Grappling Tentacle", "tipo": "criatura", "defensa": 6, "efecto": "Play: Captura recursos [cite: 23]"},
        {"nombre": "Shield Arm", "tipo": "criatura", "defensa": 6, "efecto": "Taunt: Debes destruirla primero [cite: 68]"},
        {"nombre": "Beast of Dark Legend", "tipo": "accion", "efecto": "Jefe gana recursos por llaves [cite: 133]"},
        {"nombre": "Ascending Jet", "tipo": "artefacto", "efecto": "Soporte: Potencia criaturas [cite: 342]"},
    ]
    mazo = random.choices(pool, k=43)
    random.shuffle(mazo)
    return mazo

# --- ESTADO DEL JUEGO (Session State) ---
if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

# --- PANTALLA DE INICIO ---
if not st.session_state.juego_iniciado:
    st.title("🐙 Keyraken Adventure")
    st.write("Configura la partida para comenzar")
    num_jugadores = st.number_input("Cantidad de jugadores", min_value=1, value=1)
    
    if st.button("Iniciar Juego"):
        st.session_state.num_jugadores = num_jugadores
        st.session_state.vida_max = 30 * num_jugadores  # 
        st.session_state.vida_jefe = st.session_state.vida_max
        st.session_state.llaves_unforged = 3
        st.session_state.recursos_jefe = 0
        st.session_state.llaves_jefe = 0
        st.session_state.criaturas_mesa = []
        st.session_state.mazo = inicializar_mazo()
        st.session_state.log = ["¡El Keyraken ha emergido!"]
        st.session_state.juego_iniciado = True
        st.rerun()

# --- PANTALLA DE JUEGO ---
else:
    # Calcular Armadura: +2 por cada llave no forjada del jugador 
    armadura = 2 * st.session_state.llaves_unforged

    st.title("Batalla contra el Keyraken")
    
    col1, col2 = st.columns([1, 1])

    with col1:
        # Mostrar imagen del jefe
        if os.path.exists("kf_adv_keyraken_keyraken.pdf.png"):
            st.image("kf_adv_keyraken_keyraken.pdf.png", caption="The Keyraken [cite: 432]")
        else:
            st.warning("Imagen 'kf_adv_keyraken_keyraken.pdf.png' no encontrada en el repositorio.")
        
        # Barra de vida
        progreso_vida = max(0, st.session_state.vida_jefe / st.session_state.vida_max)
        st.progress(progreso_vida)
        st.metric("Vida del Jefe", f"{st.session_state.vida_jefe} HP")
        st.metric("Armadura Activa", f"{armadura}")

    with col2:
        st.subheader("Estado del Jefe")
        st.write(f"🔑 Llaves del Jefe: {st.session_state.llaves_jefe} / 3")
        st.write(f"💎 Recursos: {st.session_state.recursos_jefe} / 6")
        
        st.divider()
        
        # Acciones del Jugador
        st.subheader("Tu Turno")
        daño_jugador = st.number_input("Daño total de tu ataque", min_value=0, value=0)
        
        # Selección de objetivo
        objetivo = st.selectbox("Objetivo del ataque", ["Keyraken"] + [c['nombre'] for c in st.session_state.criaturas_mesa])

        if st.button("Ejecutar Ataque"):
            if objetivo == "Keyraken":
                # Verificar Taunt
                if any(c['nombre'] == "Shield Arm" for c in st.session_state.criaturas_mesa):
                    st.error("¡Bloqueado! Debes destruir el Shield Arm primero[cite: 68].")
                else:
                    if daño_jugador > armadura:
                        daño_real = daño_jugador - armadura
                        st.session_state.vida_jefe -= daño_real
                        st.session_state.log.append(f"Atacaste al Jefe por {daño_real} de daño.")
                    else:
                        st.session_state.log.append("El ataque rebotó en la armadura.")
            else:
                # Atacar criatura
                idx = [i for i, c in enumerate(st.session_state.criaturas_mesa) if c['nombre'] == objetivo][0]
                st.session_state.criaturas_mesa[idx]['defensa'] -= daño_jugador
                if st.session_state.criaturas_mesa[idx]['defensa'] <= 0:
                    st.session_state.log.append(f"¡Destruiste {objetivo}! El jefe recibe 3 de daño extra[cite: 5].")
                    st.session_state.vida_jefe -= 3
                    st.session_state.criaturas_mesa.pop(idx)
            st.rerun()

    # Turno del Jefe
    if st.button("Pasar Turno (Turno del Jefe)"):
        if st.session_state.mazo:
            carta = st.session_state.mazo.pop(0)
            st.session_state.log.append(f"Jefe revela: {carta['nombre']}")
            if carta['tipo'] == "criatura":
                st.session_state.criaturas_mesa.append(carta)
            else:
                st.session_state.recursos_jefe += 2
            
            # Forjar llaves del jefe
            if st.session_state.recursos_jefe >= 6:
                st.session_state.recursos_jefe -= 6
                st.session_state.llaves_jefe += 1
                st.session_state.log.append("¡El Jefe forjó una llave!")
        st.rerun()

    # Historial
    st.divider()
    with st.expander("Ver Historial de Batalla"):
        for l in reversed(st.session_state.log):
            st.write(l)

    # Condiciones de fin
    if st.session_state.vida_jefe <= 0:
        st.balloons()
        st.success("¡VICTORIA! Han destruido al Keyraken[cite: 437].")
        if st.button("Reiniciar"): st.session_state.clear()
        
    if st.session_state.llaves_jefe >= 3:
        st.error("DERROTA: El Keyraken ha forjado las 3 llaves.")
        if st.button("Reiniciar"): st.session_state.clear()