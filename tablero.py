import streamlit as st
import os
import marea

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- CSS CORREGIDO PARA MÓVIL Y ESTILOS ---
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

    # --- 1. BOTÓN REVELAR (CON LÓGICA DE HABILIDADES, MAREA Y PRESA) ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        
        # Guardamos estado inicial para la regla de marea
        marea_inicial = st.session_state.marea
        
        # PASO 1: El Keyraken intenta avanzar (puede bajar la marea aquí)
        marea.gestionar_avance_keyraken()
        
        # Detectar si la marea ya cambió por el avance
        marea_ya_cambio = st.session_state.marea != marea_inicial
        
        # Reducir penalización de robo si existe
        if st.session_state.get('penalizacion_robo', 0) > 0:
            st.session_state.penalizacion_robo -= 1

        if st.session_state.mazo:
            # PASO 2: Gestión de carta activa anterior (Mover a la mesa)
            if st.session_state.carta_activa:
                c_v = st.session_state.carta_activa
                if c_v['tipo'] in ["CRIATURA", "ARTEFACTO"]:
                    c_v['def_actual'] = c_v.get('defensa', 0)
                    st.session_state.mesa.append(c_v)
                else:
                    st.session_state.descarte.append(c_v)
            
            # PASO 3: Revelar nueva carta
            nueva_c = st.session_state.mazo.pop(0)
            st.session_state.carta_activa = nueva_c
            
            # --- AJUSTE: HABILIDAD BASE VS PRESA ---
            # Si la carta tiene la propiedad 'presa': True, no genera ambar y hace daño.
            if nueva_c.get("presa") == True:
                st.error("🦈 ¡PRESA! El Jefe no genera Æmbar y realiza 3 de daño.")
            else:
                st.session_state.recursos_jefe += 1
                st.toast("🟡 Habilidad Base: +1 Æmbar generado.")

            # --- PASO 4: PROCESAR HABILIDADES ESPECIALES ---
            hab = nueva_c.get("habilidad")
            valor = nueva_c.get("valor", 0)

            # 1. Archivar cartas
            if hab == "archivar":
                for _ in range(valor):
                    if st.session_state.mazo:
                        st.session_state.archivo_jefe.append(st.session_state.mazo.pop(0))
                st.toast(f"📦 Archivadas {valor} cartas.")

            # 2. Forzar Marea Baja
            if hab == "forzar_marea_baja" and st.session_state.marea == "Alta":
                if not marea_ya_cambio:
                    st.session_state.marea = "Baja"
                    marea_ya_cambio = True
                    st.toast("📉 La Marea bajó por efecto de la carta.")
                else:
                    st.toast("🚫 Marea bloqueada: ya cambió este turno.")

            # 3. Penalización de Robo
            if hab == "penalizar_robo":
                st.session_state.penalizacion_robo = st.session_state.get('penalizacion_robo', 0) + valor
                st.toast(f"⏳ Penalización: Robas -1 carta por {valor} turnos.")

            # 4. Efecto estándar: Subir Marea (si no cambió ya)
            if nueva_c.get('sube_marea') == True:
                if not marea_ya_cambio:
                    st.session_state.marea = "Alta"
                    st.toast("🌊 ¡La Marea ha subido a ALTA!")
                else:
                    st.toast("🚫 Marea bloqueada: ya cambió este turno.")
            
            # Cobrar Ámbar de regalo de la carta (adicional al base)
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

    if st.session_state.get('penalizacion_robo', 0) > 0:
        st.warning(f"⚠️ Penalización de Robo activa: {st.session_state.penalizacion_robo} turnos.")

    # --- 3. CARTA ACTIVA ---
    if st.session_state.carta_activa:
        c = st.session_state.carta_activa
        ruta = RUTA_BASE + c['img']
        if os.path.exists(ruta):
            st.image(ruta, use_container_width=True)
            if c.get("presa"):
                st.error("CARÁCTER: PRESA (Ataque base de 3 daño)")
            elif c['tipo'] == "CRIATURA":
                st.caption(f"⚠️ Recién llegada: Hará {c.get('defensa')} de daño al próximo turno.")
    
    st.divider()

    # --- 4. MESA (CARRIL) ---
    if st.session_state.mesa:
        cols = st.columns(2)
        for i, carta in enumerate(st.session_state.mesa):
            with cols[i % 2]:
                with st.container(border=True):
                    im_m = RUTA_BASE + carta['img']
                    if os.path.exists(im_m): st.image(im_m, use_container_width=True)
                    if carta['tipo'] == "CRIATURA":
                        if st.button(f"💥 {carta['def_actual']}", key=f"btn_{i}", use_container_width=True):
                            carta['def_actual'] -= 1
                            if carta['def_actual'] <= 0:
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                            st.rerun()
