import streamlit as st
import psycopg2
from PIL import Image
import io
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

# Función para conectar a la base de datos
def conectar_db():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='94410404Juan', 
            dbname='emotionalai'     
        )
        return connection
    except Exception as ex:
        st.error(f"Error al conectar a la base de datos: {ex}")
        return None

# Función para obtener los profesionales de la base de datos
def obtener_profesionales():
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT nombre, especialidad,correo, descripcion,perfil FROM profesionales")
            profesionales = cursor.fetchall()
            cursor.close()
            connection.close()
            return profesionales
        except Exception as ex:
            st.error(f"Error al obtener los profesionales: {ex}")
            return []

# Función para convertir bytes a base64
def bytes_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode()

# Función para mostrar una tarjeta de profesional
def mostrar_tarjeta(nombre, correo, especialidad,descripcion,perfil_bytes):
    # Convertir la imagen de perfil a base64
    perfil_base64 = bytes_to_base64(perfil_bytes) if perfil_bytes else ""

    # HTML y CSS para la tarjeta
    tarjeta_html = f"""
<div style="
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: none;
    display: flex;
    align-items: center;
">
    <div style="margin-right: 15px;">
        <img src="data:image/png;base64,{perfil_base64}" 
             style="border-radius: 50%; width: 80px; height: 80px; object-fit: cover;">
    </div>
    <div>
        <div style="display: flex; align-items: baseline;">
            <h3 style="margin: 0; color: white; font-size: 18px;">{nombre}</h3>
            <span style="margin: 0 5px; color: white; font-size: 14px;"></span>
            <p style="margin: 0; color: white; font-size: 14px;">{correo}</p>
             <span style="margin: 0 5px; color: white; font-size: 14px;">-</span>
            <p style="margin: 0; color: white; font-size: 14px;">{especialidad}</p>
        </div>
        <p style="margin: 10px 0 0 0; color: white; font-size: 14px; line-height: 1.4;">{descripcion}</p>
    </div>
</div>
"""

# Mostrar la tarjeta en Streamlit
    st.markdown(tarjeta_html, unsafe_allow_html=True)   

# Convertir la imagen local a base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
# Interfaz de Streamlit
def main():

    st.markdown(
    "<h1 style='text-align:center;'>PROFESIONALES DISPONIBLES</h1>",
    unsafe_allow_html=True
)
    
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
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Obtener los profesionales de la base de datos
    profesionales = obtener_profesionales()

    if profesionales:
        for profesional in profesionales:
            nombre, correo,especialidad, descripcion, perfil_bytes = profesional
            mostrar_tarjeta(nombre, correo, especialidad,descripcion, perfil_bytes)
    else:
        st.info("No hay profesionales registrados.")

if __name__ == "__main__":
    main()