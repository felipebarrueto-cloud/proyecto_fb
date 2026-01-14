import streamlit as st

def mostrar_descarte():
    st.header("Zona de Descarte")
    if st.session_state.descarte:
        for carta in st.session_state.descarte:
            st.write(f"❌ **{carta['nombre']}** - ({carta['tipo']})")
    else:
        st.info("El descarte está vacío.")
