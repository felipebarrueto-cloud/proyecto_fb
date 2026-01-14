import streamlit as st
import os
from cartas import obtener_mazo_oficial

st.set_page_config(page_title="Keyraken Adventure", layout="wide")
RUTA_BASE = "proyecto_keyforge/"

# --- INICIALIZACIÓN ---
if 'juego_iniciado' not in st.session_state:
    st.session_state.juego_iniciado = False

if not st.session_state.juego_iniciado:
    st.title("🐙 Keyraken Adventure")
    n_jug = st.number_input("Número de Jugadores", min_value=1, value=1)
    if st.button("Empezar Batalla"):
        st.session_state.mazo = obtener_mazo_oficial()
        st.session_state.mesa = []
        st.session_state.descarte = []
        st.session_state.carta_activa = None
        st.session_state.vida_jefe = 30 * n_jug
        st.session_state.armadura_jefe = 6 # Valor inicial aproximado
        st.session_state.juego_iniciado = True
        st.rerun()

else:
    # --- PANEL SUPERIOR: ESTADÍSTICAS DEL JEFE ---
    st.header("Estado del Keyraken")
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    stat_col1.metric("HP Keyraken", f"{st.session_state.vida_jefe}")
    stat_col2.metric("Armadura", f"{st.session_state.armadura_jefe}")
    stat_col3.metric("Mazo Aventura", f"{len(st.session_state.mazo)} cartas")

    # --- BOTÓN DE REVELAR (CASCADA) ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        if st.session_state.mazo:
            if st.session_state.carta_activa:
                c_v = st.session_state.carta_activa
                if c_v['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_v['def_actual'] = c_v.get('defensa', 0)
                    st.session_state.mesa.append(c_v)
                else:
                    st.session_state.descarte.append(c_v)
            
            st.session_state.carta_activa = st.session_state.mazo.pop(0)
            st.rerun()

    # --- CARTA ACTIVA REVELADA ---
    if st.session_state.carta_activa:
        st.divider()
        c_activa = st.session_state.carta_activa
        col_esp1, col_img, col_esp2 = st.columns([1, 1, 1])
        with col_img:
            ruta = RUTA_BASE + c_activa['img']
            if os.path.exists(ruta):
                st.image(ruta, caption="NUEVA AMENAZA REVELADA", use_container_width=True)
            else:
                st.error(f"Imagen {c_activa['img']} no encontrada")

    # --- MESA DE COMBATE (CRIATURAS Y ARTEFACTOS) ---
    st.divider()
    st.subheader("Amenazas en Juego")
    
    if st.session_state.mesa:
        filas = st.columns(5)
        for i, c in enumerate(st.session_state.mesa):
            with filas[i % 5]:
                with st.container(border=True):
                    ruta_m = RUTA_BASE + c['img']
                    if os.path.exists(ruta_m):
                        st.image(ruta_m, use_container_width=True)
                    
                    if c['tipo'] == "CRIATURA":
                        st.write(f"❤️ Vida: {c['def_actual']} / {c['defensa']}")
                        # Selector de daño rápido
                        d_atq = st.number_input("Daño recibido", min_value=0, max_value=20, key=f"atq_{i}")
                        if st.button("Aplicar Daño", key=f"btn_{i}"):
                            c['def_actual'] -= d_atq
                            if c['def_actual'] <= 0:
                                # Regla: -3 HP al Jefe cuando una criatura muere
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                                st.toast(f"{c['nombre']} destruida! -3 HP al Keyraken")
                            st.rerun()
                    else:
                        st.caption("💠 ARTEFACTO")
    else:
        st.info("No hay criaturas ni artefactos en mesa.")

    # --- ATAQUE DIRECTO AL KEYRAKEN ---
    st.divider()
    with st.expander("Ataque Directo al Jefe"):
        d_directo = st.number_input("Daño total al Jefe:", min_value=0)
        if st.button("Atacar al Keyraken"):
            if d_directo > st.session_state.armadura_jefe:
                real_dmg = d_directo - st.session_state.armadura_jefe
                st.session_state.vida_jefe -= real_dmg
                st.success(f"Infligiste {real_dmg} de daño!")
            else:
                st.warning("La armadura absorbió todo el daño.")
            st.rerun()

