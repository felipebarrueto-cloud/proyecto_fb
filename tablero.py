import streamlit as st
import os
import marea

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- CSS CORREGIDO ---
    st.markdown("""
        <style>
            div.stButton > button {
                background-color: #ff4b4b !important;
                color: white !important;
                font-weight: bold !important;
                border-radius: 10px !important;
                height: 3em !important;
                margin-top: 10px !important;
            }
            .main .block-container { padding-top: 1rem !important; }
            .compact-table { width: 100%; border-collapse: collapse; margin-bottom: 8px; }
            .compact-table td { border: 1px solid #333; padding: 6px; text-align: center; background: #1a1c23; }
            .label { color: #888; font-size: 10px; display: block; }
            .val-red { color: #ff4b4b; font-size: 18px; font-weight: bold; }
            .texto-blanco { color: #ffffff; font-size: 18px; font-weight: bold; vertical-align: middle; }
            .gema { font-size: 18px; vertical-align: middle; }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. BOTÓN REVELAR (HABILIDAD BASE EXCLUSIVA) ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        
        marea_inicial = st.session_state.marea
        
        # PASO A: El Keyraken intenta avanzar
        marea.gestionar_avance_keyraken()
        marea_ya_cambio = st.session_state.marea != marea_inicial
        
        if st.session_state.get('penalizacion_robo', 0) > 0:
            st.session_state.penalizacion_robo -= 1

        if st.session_state.mazo:
            # PASO B: Gestión de carta activa anterior
            if st.session_state.carta_activa:
                c_v = st.session_state.carta_activa
                if c_v['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_v['def_actual'] = c_v.get('defensa', 0)
                    st.session_state.mesa.append(c_v)
                else:
                    st.session_state.descarte.append(c_v)
            
            # PASO C: Revelar nueva carta
            nueva_c = st.session_state.mazo.pop(0)
            st.session_state.carta_activa = nueva_c
            
            # --- LÓGICA DE HABILIDAD EXCLUSIVA ---
            # Si es presa: Ataca. Si NO es presa: Genera 1 AE.
            if nueva_c.get("presa") == True:
                # El jefe final ataca con 3 de daño
                st.error("🦈 ¡HABILIDAD PRESA! El Jefe ataca con 3 de daño base.")
                # (Opcional: aquí puedes restar vida a una variable de jugador)
            else:
                # El jefe no ataca, genera 1 ambar
                st.session_state.recursos_jefe += 1
                st.toast("🟡 Habilidad Base: El Jefe genera 1 Æmbar.")

            # --- PASO D: PROCESAR HABILIDADES ADICIONALES ---
            hab = nueva_c.get("habilidad")
            valor = nueva_c.get("valor", 0)

            # Archivar
            if hab == "archivar":
                for _ in range(valor):
                    if st.session_state.mazo:
                        st.session_state.archivo_jefe.append(st.session_state.mazo.pop(0))
                st.toast(f"📦 Archivadas {valor} cartas.")

            # Forzar marea baja
            if hab == "forzar_marea_baja" and st.session_state.marea == "Alta":
                if not marea_ya_cambio:
                    st.session_state.marea = "Baja"
                    marea_ya_cambio = True
                    st.toast("📉 Marea baja por efecto.")

            # Penalización robo
            if hab == "penalizar_robo":
                st.session_state.penalizacion_robo = st.session_state.get('penalizacion_robo', 0) + valor

            # Subir marea estándar
            if nueva_c.get('sube_marea') == True and not marea_ya_cambio:
                st.session_state.marea = "Alta"
                st.toast("🌊 Marea ALTA")
            
            # Sumar ambar de regalo propio de la carta (si tiene)
            st.session_state.recursos_jefe += nueva_c.get('ambar_regalo', 0)
            
            st.rerun()

    # --- 2. TABLA DE RESUMEN ---
    daño_mesa = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo'] == "CRIATURA")
    poder_total = 3 + daño_mesa

    st.markdown(f"""
        <table class="compact-table">
            <tr>
                <td style="width: 45%;">
                    <span class="label">💥 PODER TOTAL</span>
                    <span class="val-red">{poder_total}</span>
                </td>
                <td style="width: 55%;">
                    <span class="label">RECURSOS Y MAREA</span>
                    <span class="gema">💎</span> 
                    <span class="texto-blanco">{st.session_state.recursos_jefe} Æ</span>
                    <span style="color:white; font-weight:bold;"> | 🌊 {st.session_state.marea}</span>
                    <br><span style="font-size:10px; color:#666;">Avances: <b>{st.session_state.avances_jefe}/4</b></span>
                </td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

    # El resto del renderizado de imágenes y mesa sigue igual...
    if st.session_state.carta_activa:
        c = st.session_state.carta_activa
        if os.path.exists(RUTA_BASE + c['img']):
            st.image(RUTA_BASE + c['img'], use_container_width=True)
