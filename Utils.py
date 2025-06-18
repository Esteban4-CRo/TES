import streamlit as st
import subprocess
import time

def mostrar_icono_microfono():
    # CSS 
    st.markdown("""
        <style>
            .microfono-img {
                border-radius: 50%;
                width: 50px;
                height: 50px;
                transition: transform 0.3s ease-in-out;
            }
            .microfono-animado {
                animation: pulsar 1s infinite;
            }
            @keyframes pulsar {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
        </style>
    """, unsafe_allow_html=True)

    if "voice_active" not in st.session_state:
        st.session_state.voice_active = False

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🎤", key="micro_btn"):
            st.session_state.voice_active = True
            subprocess.Popen(["python", "VoiceAgent.py"])  # Llama al asistente por voz
            time.sleep(1.5)
            st.session_state.voice_active = False

    

def spawn_menu():
    with st.sidebar:
        if st.session_state.get('logged_in', False):
            st.page_link('Pages/Home.py', label="Home 🏡")
            st.page_link('Pages/ChatBot.py', label="ChatBot 🤖")
            st.page_link('Pages/Comments.py', label="Comentarios 📨")
            st.page_link('Pages/Profesionals.py', label="Profesionales 🧑🏻‍⚕️")
            st.page_link('Pages/ProfileEdit.py', label="Perfil 🙋🏻")

            if st.button("Cerrar sesión 🚪"):
                st.session_state.logged_in = False
                st.session_state.nombre_usuario = ""
                st.session_state.documento_usuario = ""
                st.success("Sesión cerrada.")
                st.switch_page("Login.py")
        else:
            st.page_link('Login.py', label="Login / Registro 🏡")

        # Mostrar ícono del micrófono al final
        mostrar_icono_microfono()
