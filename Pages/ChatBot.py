import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import base64

import Utils as util

util.spawn_menu()

# Bloquear acceso si no está logueado
if not st.session_state.get('logged_in', False):
    st.warning("Debes iniciar sesión primero.")
    st.switch_page("Login.py")
    st.stop()

documento_identidad = st.session_state.get("documento_usuario")
nombre_usuario = st.session_state.get("nombre_usuario")

# Convertir la imagen local a base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_path = "Backgrounds/BackgroundComments.png"
base64_image = get_base64_of_image(image_path)
# CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("data:image/png;base64,{base64_image}"); 
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }

    .stChatMessage {
        background-color: rgba(0, 0, 0, 0); /* fondo transparente */
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); /* sombra para legibilidad */
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }

    .stMarkdown {
        font-size: 1.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("ChatBot TES ")

# Cargar modelo de Ollama
llm = OllamaLLM(model="mistral")

# Inicializar historial si no está presente
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

# Mostrar historial
for msg in st.session_state.chat_history.messages:
    if msg.type == "human":
        with st.chat_message("user", avatar="Backgrounds/User.jpg"):
            st.markdown(msg.content)
    else:
        with st.chat_message("assistant", avatar="Backgrounds/Logo.png"):
            st.markdown(msg.content)

if len(st.session_state.chat_history.messages) == 0:
    bienvenida = (
        "¡Hola! Bienvenido al **ChatBot TES**. Estoy aquí para escucharte y ayudarte con cualquier "
        "problema emocional o situación difícil por la que estés pasando. No estás solo. "
        "Cuéntame cómo te sientes o en qué puedo acompañarte. "
    )
    st.session_state.chat_history.add_ai_message(bienvenida)
    with st.chat_message("assistant", avatar="Backgrounds/Logo.png"):
        st.markdown(bienvenida)

# Plantilla de prompt
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="Conversación previa:\n{chat_history}\nUsuario: {question}\nAI:"
)

# Función de interacción
def run_chain(question):
    history_text = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages])
    full_prompt = prompt.format(chat_history=history_text, question=question)
    response = llm.invoke(full_prompt)

    # Guardar mensajes
    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)

    return response


if user_input := st.chat_input("Escribe tu mensaje..."):
    st.session_state.chat_history.add_user_message(user_input)
    with st.chat_message("user", avatar="Backgrounds/User.jpg"):
        st.markdown(user_input)

    response = run_chain(user_input)

    with st.chat_message("assistant", avatar="Backgrounds/Logo.png"):
        st.markdown(response)
