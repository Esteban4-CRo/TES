import streamlit as st
import psycopg2
import base64
from PIL import Image
import Utils as util

util.spawn_menu()

# Bloquear acceso si no está logueado
if not st.session_state.get('logged_in', False):
    st.warning("Debes iniciar sesión primero.")
    st.switch_page("Login.py")
    st.stop()

documento_identidad = st.session_state.get("documento_usuario")
nombre_usuario = st.session_state.get("nombre_usuario")

# Función para la conexión con la base de datos
def conectar_db():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='your_user',
            password='your_password',
            dbname='emotionalai'
        )
        return connection
    
    except Exception as ex:
        st.error(f"Error al conectar la base de datos: {ex}")
        return None

# Función para obtener el ID y nombre del usuario
def obtener_id_usuario(documento_identidad):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id_usuario, nombre FROM usuarios WHERE documento_identidad = %s
                """,
                (documento_identidad,)
            )
            result = cursor.fetchone()
            if result:
                return result[0], result[1]  # id_usuario, nombre_usuario
            else:
                return None, None
        except Exception as ex:
            st.error(f"Error al obtener el ID del usuario: {ex}")
            return None, None
        finally:
            cursor.close()
            connection.close()
    return None, None

# Función para obtener el ID, nombre y perfil del profesional
def get_id_pro(documento_identidad):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id_profesional, nombre, perfil FROM profesionales WHERE documento_identidad = %s
                """,
                (documento_identidad,)
            )
            result = cursor.fetchone()
            if result:
                return result[0], result[1], result[2]  # id_profesional, nombre_profesional, perfil_profesional
            else:
                return None, None, None
        except Exception as ex:
            st.error(f"Error al obtener el ID del profesional: {ex}")
            return None, None, None
        finally:
            cursor.close()
            connection.close()
    return None, None, None

# Función para actualizar los datos del perfil 
def save_profile(id_usuario, id_profesional, nombre, correo, certificado, descripcion, perfil):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Actualizar los datos del profesional 
            if id_profesional:
                certificado_bytes = certificado.read() if certificado else None
                perfil_bytes = perfil.read() if perfil else None

                cursor.execute(
                    """
                    UPDATE profesionales 
                    SET nombre = %s, correo = %s, certificado = %s, descripcion = %s, perfil = %s
                    WHERE id_profesional = %s
                    """,
                    (nombre, correo, certificado_bytes, descripcion, perfil_bytes, id_profesional)
                )

            # Actualizar los datos del usuario 
            else:
                cursor.execute(
                    """
                    UPDATE usuarios
                    SET nombre = %s, correo = %s
                    WHERE id_usuario = %s
                    """,
                    (nombre, correo, id_usuario)
                )
            
            connection.commit()
            st.success("Perfil actualizado correctamente!")

        except Exception as ex:
            connection.rollback()
            st.error(f"Error al actualizar el perfil: {ex}")

        finally:
            cursor.close()
            connection.close()

# Convertir la imagen local a base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Interfaz de Streamlit
def main():
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

    st.markdown(
        "<h1 style='text-align:center;'>EDITAR PERFIL</h1>",
        unsafe_allow_html=True
    )

    tipo_usuario = st.session_state.get("tipo_usuario")

    if tipo_usuario == "usuario":
        id_usuario, nombre_usuario = obtener_id_usuario(documento_identidad)
        id_profesional = None
        perfil_profesional = None
    elif tipo_usuario == "profesional":
        id_profesional, nombre_profesional, perfil_profesional = get_id_pro(documento_identidad)
        id_usuario = None
        nombre_usuario = None
    else:
        st.error("Tipo de usuario desconocido.")
        st.stop()
        
    if documento_identidad:
        # Obtener el ID del usuario o profesional
        id_usuario, nombre_usuario = obtener_id_usuario(documento_identidad)
        id_profesional, nombre_profesional, perfil_profesional = get_id_pro(documento_identidad)

        if id_usuario or id_profesional:
            nombre = nombre_usuario if id_usuario else nombre_profesional
            st.write(f"Bienvenid@, {nombre}")

            # Campos editables
            nombre = st.text_input("Nombre", value=nombre)
            correo = st.text_input("Correo electrónico", value="usuario@example.com")

            if id_profesional:
                # Campos adicionales para profesionales
                certificado = st.file_uploader("Subir certificado (opcional)", type=["pdf", "png", "jpg"])
                descripcion = st.text_area("Descripción", value="Soy un profesional en...")
                perfil = st.file_uploader("Subir imagen de perfil (opcional)", type=["png", "jpg", "jpeg"])
            else:
                certificado = None
                descripcion = None
                perfil = None

            # Botón para guardar los cambios
            if st.button("Guardar cambios"):
                if id_profesional and certificado is None:
                    st.error("El certificado es obligatorio para los profesionales.")
                else:

                    save_profile(id_usuario, id_profesional, nombre, correo, certificado, descripcion, perfil)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()