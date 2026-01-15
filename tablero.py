import streamlit as st
import os
import marea

RUTA_BASE = "proyecto_keyforge/"

def mostrar_tablero():
    # --- CSS MANTENIDO ---
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

    # --- 1. BOTÓN REVELAR ---
    if st.button("🎴 REVELAR SIGUIENTE CARTA", use_container_width=True):
        
        marea_inicial = st.session_state.marea
        
        # PASO A: El Keyraken intenta avanzar
        marea.gestionar_avance_keyraken()
        marea_ya_cambio = st.session_state.marea != marea_inicial
        
        if st.session_state.get('penalizacion_robo', 0) > 0:
            st.session_state.penalizacion_robo -= 1

        if st.session_state.mazo:
            # PASO B: Gestión de carta activa anterior (Mover a la mesa)
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
            
            # --- LÓGICA DE PRESA Y ÁMBAR CONDICIONAL ---
            # Comprobamos Presa en las cartas ya en mesa y en la nueva revelada
            presa_en_mesa = any(carta.get('presa') == True for carta in st.session_state.mesa if carta['tipo'] == "CRIATURA")
            presa_revelada = nueva_c.get('presa') == True

            if presa_revelada or presa_en_mesa:
                # El jefe ataca (El daño base 3 se activará en la tabla)
                st.error("🐙 ¡PRESA DETECTADA! El Jefe infligirá su daño base de 3.")
            else:
                # El jefe no ataca con el base, genera 1 ambar
                st.session_state.recursos_jefe += 1
                st.toast("💎 Sin Presa: El Jefe genera 1 Æmbar en lugar de atacar.")

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
                    st.toast("🌊 Marea baja por efecto.")

            # Penalización robo
            if hab == "penalizar_robo":
                st.session_state.penalizacion_robo = st.session_state.get('penalizacion_robo', 0) + valor

            # Subir marea estándar de la carta
            if nueva_c.get('sube_marea') == True and not marea_ya_cambio:
                st.session_state.marea = "Alta"
                st.toast("🌊 Marea Alta")
            
            # Ámbar de regalo extra de la carta
            st.session_state.recursos_jefe += nueva_c.get('ambar_regalo', 0)
            
            st.rerun()

    # --- 2. CÁLCULO DE PODER Y TABLA DE RESUMEN ---
    # Revisamos si hay Presa para aplicar el daño base de 3
    presa_en_mesa = any(carta.get('presa') == True for carta in st.session_state.mesa if carta['tipo'] == "CRIATURA")
    presa_activa = False
    if st.session_state.carta_activa and st.session_state.carta_activa.get('presa') == True:
        presa_activa = True

    # Daño base condicional
    daño_base = 3 if (presa_en_mesa or presa_activa) else 0
    
    # Daño de criaturas en mesa
    daño_mesa = sum(c.get('defensa', 0) for c in st.session_state.mesa if c['tipo'] == "CRIATURA")
    
    # Daño de la criatura activa (si es criatura)
    daño_activa = 0
    if st.session_state.carta_activa and st.session_state.carta_activa['tipo'] == "CRIATURA":
        daño_activa = st.session_state.carta_activa.get('defensa', 0)

    poder_total = daño_base + daño_mesa + daño_activa

    st.markdown(f"""
        <table class="compact-table">
            <tr>
                <td style="width: 45%;">
                    <span class="label">💥 PODER TOTAL</span>
                    <span class="val-red">{poder_total}</span>
                    <br><span style="font-size:9px; color:#888;">{'(Base 3 + Mesa)' if daño_base > 0 else '(Solo Mesa - Sin Presa)'}</span>
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

    # --- 3. RENDERIZADO DE CARTA ACTIVA Y MESA ---
    if st.session_state.carta_activa:
        c = st.session_state.carta_activa
        ruta_activa = RUTA_BASE + c['img']
        if os.path.exists(ruta_activa):
            st.image(ruta_activa, use_container_width=True)

    st.divider()

    if st.session_state.mesa:
        cols = st.columns(2)
        for i, carta in enumerate(st.session_state.mesa):
            with cols[i % 2]:
                with st.container(border=True):
                    ruta_m = RUTA_BASE + carta['img']
                    if os.path.exists(ruta_m):
                        st.image(ruta_m, use_container_width=True)
                    
                    if carta['tipo'] == "CRIATURA":
                        if st.button(f"💥 {carta['def_actual']}", key=f"btn_{i}", use_container_width=True):
                            carta['def_actual'] -= 1
                            if carta['def_actual'] <= 0:
                                st.session_state.vida_jefe -= 3
                                st.session_state.descarte.append(st.session_state.mesa.pop(i))
                            st.rerun()
