import streamlit as st
import psycopg2
import bcrypt
import base64   
import Utils as util
from sqlalchemy.engine import URL

util.spawn_menu()

# Función para conectar a la base de datos
def conectar_db():
    try:
        connection = psycopg2.connect(
            host='db.rbenrvkegphjaftoekjk.supabase.co',
            user='postgres',
            password='94410404Juan',
            dbname='postgres',
            port='5432'
        )
        return connection
    except Exception as ex:
        st.error(f"Error al conectar a la base de datos: {ex}")
        return None

# Función para verificar las credenciales del usuario
def verificar_usuario(nombre, documento_identidad, password):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            # Obtener la contraseña encriptada de la base de datos
            cursor.execute(
                "SELECT contrasena FROM usuarios WHERE nombre = %s AND documento_identidad = %s",
                (nombre, documento_identidad)
            )
            resultado = cursor.fetchone()

            cursor.close()
            connection.close()

            if resultado:
                # Verificar la contraseña encriptada
                if bcrypt.checkpw(password.encode('utf-8'), resultado[0].encode('utf-8')):
                    return True
            return False

        except Exception as ex:
            st.error(f"Error al verificar el usuario: {ex}")
            return False

# Función para registrar un nuevo profesional
def register_pro(nombre_pro, documento_identidad_pro, especialidad, email_pro, password_pro, certificado_pro, perfil_pro):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Verificar si el documento de identidad ya está en uso
            cursor.execute("SELECT * FROM profesionales WHERE documento_identidad = %s", (documento_identidad_pro,))
            if cursor.fetchone():
                st.error("El documento de identidad ya está registrado.")
                return False

            # Insertar en personas
            cursor.execute("INSERT INTO personas (documento_identidad) VALUES (%s)", (documento_identidad_pro,))
            # Encriptar la contraseña antes de guardarla
            hashed_password = bcrypt.hashpw(password_pro.encode('utf-8'), bcrypt.gensalt())

            # Leer los archivos como bytes
            certificado_bytes = certificado_pro.read() if certificado_pro else None
            perfil_bytes = perfil_pro.read() if perfil_pro else None

            # Insertar el nuevo profesional en la base de datos
            cursor.execute(
                "INSERT INTO profesionales (nombre, documento_identidad,especialidad, correo, contrasena, certificado, perfil) VALUES (%s, %s,%s, %s, %s, %s, %s)",
                (nombre_pro, documento_identidad_pro, especialidad,email_pro, hashed_password.decode('utf-8'), certificado_bytes, perfil_bytes)
            )
            connection.commit()
            cursor.close()
            connection.close()

            st.success("¡Registro exitoso! Ahora puedes iniciar sesión.")
            return True

        except Exception as ex:
            st.error(f"Error al registrar el profesional: {ex}")
            return False

# Función para verificar las credenciales del profesional
def check_pro(nombre, documento_identidad, password):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()
            # Obtener la contraseña encriptada de la base de datos
            cursor.execute(
                "SELECT contrasena FROM profesionales WHERE nombre = %s AND documento_identidad = %s",
                (nombre, documento_identidad)
            )
            resultado = cursor.fetchone()

            cursor.close()
            connection.close()

            if resultado:
                # Verificar la contraseña encriptada
                if bcrypt.checkpw(password.encode('utf-8'), resultado[0].encode('utf-8')):
                    return True
            return False

        except Exception as ex:
            st.error(f"Error al verificar el profesional: {ex}")
            return False

# Función para registrar un nuevo usuario
def registrar_usuario(nombre, documento_identidad, email, password):
    connection = conectar_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Verificar si el documento de identidad ya está en uso
            cursor.execute("SELECT * FROM usuarios WHERE documento_identidad = %s", (documento_identidad,))
            if cursor.fetchone():
                st.error("El documento de identidad ya está registrado.")
                return False

              # Insertar en personas
            cursor.execute("INSERT INTO personas (documento_identidad) VALUES (%s)", (documento_identidad,))

            # Encriptar la contraseña antes de guardarla
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insertar el nuevo usuario en la base de datos
            cursor.execute(
                "INSERT INTO usuarios (nombre, documento_identidad, correo, contrasena) VALUES (%s, %s, %s, %s)",
                (nombre, documento_identidad, email, hashed_password.decode('utf-8'))
            )
            connection.commit()

            cursor.close()
            connection.close()

            st.success("¡Registro exitoso! Ahora puedes iniciar sesión.")
            return True

        except Exception as ex:
            st.error(f"Error al registrar el usuario: {ex}")
            return False

# Convertir la imagen local a base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Interfaz de Streamlit
def main():
    # Configuración del fondo
    image_path = "Backgrounds/BackgroundComments.png"
    base64_image = get_base64_of_image(image_path)

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}"); 
            background-size: cover; 
            background-position:center;  
            background-repeat: no-repeat; 
            background-attachment: fixed; 
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<h1 style='text-align:center;'>TES</h1>",
        unsafe_allow_html=True
    )


    opcion = st.radio("", ( "Iniciar sesión","Registrarse", "Registro - PRO"), horizontal=True)

    
    if opcion == "Iniciar sesión":
        st.subheader("Iniciar sesión")

        #Campos de entrada para el nombre, documento de identidad y contraseña
        nombre = st.text_input("Nombre")
        documento_identidad = st.text_input("Documento de identidad")
        password = st.text_input("Contraseña", type="password")

        # Botón de login
        if st.button("Iniciar sesión"):
            if verificar_usuario(nombre, documento_identidad, password):
                st.session_state.logged_in = True
                st.session_state.nombre_usuario = nombre
                st.session_state.documento_usuario = documento_identidad
                st.session_state.tipo_usuario ="usuario" 
                st.success("¡Inicio de sesión exitoso!")
                st.write(f"Bienvenido, {nombre}!")
                st.switch_page("Pages/Home.py")
                
              

            elif check_pro(nombre, documento_identidad, password):
               st.session_state.logged_in = True
               st.success("¡Inicio de sesión exitoso!")
               st.write(f"Bienvenido, {nombre}!")
               st.session_state.nombre_usuario = nombre
               st.session_state.documento_usuario = documento_identidad
               st.session_state.tipo_usuario = "profesional"  
               st.switch_page("Pages/Home.py")

            else:
               st.error("Nombre, documento de identidad o contraseña incorrectos.")
        
    elif opcion == "Registrarse":
        st.subheader("Registrarse")

        # Campos de entrada para el registro
        new_nombre = st.text_input("Nombre completo")
        new_documento_identidad = st.text_input("Documento de identidad")
        new_email = st.text_input("Correo electrónico")
        new_password = st.text_input("Elige una contraseña", type="password")
        confirm_password = st.text_input("Confirma tu contraseña", type="password")

        # Botón de registro
        if st.button("Registrarse"):
            if new_password == confirm_password:
                if registrar_usuario(new_nombre, new_documento_identidad, new_email, new_password):
                    st.success("¡Registro exitoso! Ahora puedes iniciar sesión.")
            else:
                st.error("Las contraseñas no coinciden.")

    elif opcion == "Registro - PRO":
        st.subheader("Registro - PRO")

        # Campos de entrada para el registro profesional
        new_nombre_pro = st.text_input("Nombre completo")
        new_documento_identidad_pro = st.text_input("Documento de identidad")
        especialidad = st.text_input("Especialidad")
        new_email_pro = st.text_input("Correo electrónico")
        new_password_pro = st.text_input("Elige una contraseña", type="password")
        confirm_password_pro = st.text_input("Confirma tu contraseña", type="password")
        new_certificado_pro = st.file_uploader("Certificado", type=["pdf", "jpg", "png", "txt"])
        new_perfil_photo_pro = st.file_uploader("Foto de perfil", type=["jpg", "png"])

        # Botón de registro
        if st.button("Registrarse"):
            if new_password_pro == confirm_password_pro:
                if register_pro(new_nombre_pro, new_documento_identidad_pro, especialidad,new_email_pro, new_password_pro, new_certificado_pro, new_perfil_photo_pro):
                    st.success("¡Registro exitoso! Ahora puedes iniciar sesión.")
            else:
                st.error("Las contraseñas no coinciden.")

if __name__ == "__main__":
    main()