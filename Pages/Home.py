import streamlit as st
import Utils as util
import base64

# Mostrar menú
util.spawn_menu()

# Verificar si hay sesión activa
if not st.session_state.get("logged_in", False):
    st.warning("Debes iniciar sesión primero.")
    st.switch_page("Login.py")
    st.stop()

# Cargar datos de sesión
nombre = st.session_state.get("nombre_usuario", "Usuario")
tipo_usuario = st.session_state.get("tipo_usuario")

# Función para convertir imágenes locales a base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Fondo de pantalla
image_path = "Backgrounds/BackgroundComments.png"
base64_image = get_base64_of_image(image_path)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_image}"); 
        background-size: cover; 
        background-position: center;  
        background-repeat: no-repeat; 
        background-attachment: fixed; 
        color: #ffffff;
    }}
    .content-box {{
        background-color: rgba(0, 0, 0, 0.6);
        padding: 2rem;
        border-radius: 15px;
        margin: auto;
        width: 80%;
        text-align: justify;
        font-size: 18px;
    }}
    h1, h2 {{
        text-align: center;
        color: #ffffff;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Contenido de bienvenida
st.markdown("<h1>Bienvenido a TES</h1>", unsafe_allow_html=True)
st.write(f"Hola **{nombre}**, selecciona una opción del menú a la izquierda para comenzar.")

# Información principal
st.markdown(f"""
<div class='content-box'>
    <h2>¿Por qué nació TES?</h2>
    <p>
        En los últimos años, los problemas mentales y emocionales han aumentado drásticamente, 
        afectando a personas de todas las edades. La ansiedad, la depresión y el estrés se han convertido 
        en compañeros constantes de vida para muchos, y muchas veces estas situaciones no se atienden a tiempo 
        por falta de acompañamiento profesional o miedo al estigma social.
    </p>
    <p>
        TES nace como una herramienta tecnológica diseñada para brindar un espacio seguro, de apoyo y orientación 
        a quienes enfrentan dificultades emocionales. Nuestro objetivo es facilitar el acceso a la ayuda psicológica 
        y fomentar el autocuidado, utilizando la tecnología como medio para conectar a las personas con recursos útiles 
        y profesionales dispuestos a ayudar.
    </p>
    <p>
        Aquí podrás expresar lo que sientes, obtener consejos, contactar profesionales y ser parte de una comunidad que 
        te comprende. Recuerda: no estás solo. En TES, estamos contigo.
    </p>
</div>
""", unsafe_allow_html=True)

# Puedes añadir más imágenes con base64 así:
# imagen de apoyo (puedes reemplazar con otras rutas como "Images/tes_logo.png")
image_path_logo = "Backgrounds/Reference.png"
base64_logo = get_base64_of_image(image_path_logo)

st.markdown(f"""
    <div style='text-align:center; margin-top: 30px;'>
        <img src="data:image/png;base64,{base64_logo}" width="200">
    </div>
""", unsafe_allow_html=True)

documento = st.session_state.get("documento_usuario")
print(documento)
print(tipo_usuario)
