import streamlit as st
import psycopg2
import base64
from datetime import datetime
import Utils as util

util.spawn_menu()

# Bloquear acceso si no está logueado
if not st.session_state.get('logged_in', False):
    st.warning("Debes iniciar sesión primero.")
    st.switch_page("Login.py")
    st.stop()

# Obtener datos de sesión
documento_identidad = st.session_state.get("documento_usuario")
tipo_usuario = st.session_state.get("tipo_usuario")

# Función para conectar a la base de datos
def conectar_db():
    try:
        return psycopg2.connect(
            host='db.rbenrvkegphjaftoekjk.supabase.co',
            user='postgres',
            password='94410404Juan',
            dbname='postgres',
            port='5432'
        )
    except Exception as ex:
        st.error(f"Error al conectar a la base de datos: {ex}")
        return None

# Obtener datos de usuario
def obtener_id_usuario(documento):
    conn = conectar_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id_usuario, nombre FROM usuarios WHERE documento_identidad = %s", (documento,))
            res = cur.fetchone()
            return res if res else (None, None)
        except Exception as ex:
            st.error(f"Error al consultar usuario: {ex}")
            return None, None
        finally:
            cur.close()
            conn.close()

# Obtener datos de profesional
def get_id_pro(documento):
    conn = conectar_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id_profesional, nombre, perfil FROM profesionales WHERE documento_identidad = %s", (documento,))
            res = cur.fetchone()
            return res if res else (None, None, None)
        except Exception as ex:
            st.error(f"Error al consultar profesional: {ex}")
            return None, None, None
        finally:
            cur.close()
            conn.close()

# Guardar comentario
def guardar_comentario(id_usuario, id_profesional, contenido, archivo):
    conn = conectar_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO comentarios (contenido, id_usuario, id_profesional, archivo) VALUES (%s, %s, %s, %s)",
                (contenido, id_usuario, id_profesional, archivo)
            )
            conn.commit()
            st.success("Comentario guardado correctamente.")
            return True
        except Exception as ex:
            st.error(f"Error al guardar el comentario: {ex}")
            return False
        finally:
            cur.close()
            conn.close()

# Obtener comentarios del foro
def obtener_comentarios():
    conn = conectar_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.id_comentario, c.contenido, c.fecha, 
                       COALESCE(u.nombre, p.nombre) AS nombre, 
                       c.archivo, p.perfil
                FROM comentarios c
                LEFT JOIN usuarios u ON c.id_usuario = u.id_usuario
                LEFT JOIN profesionales p ON c.id_profesional = p.id_profesional
                ORDER BY c.fecha DESC
            """)
            return cur.fetchall()
        except Exception as ex:
            st.error(f"Error al obtener los comentarios: {ex}")
            return []
        finally:
            cur.close()
            conn.close()

# Convertir bytes a base64
def bytes_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode()

# Fondo personalizado
def fondo():
    def get_base64_of_image(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    img = get_base64_of_image("Backgrounds/BackgroundComments.png")
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img}"); 
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

# Página principal
def main():
    fondo()
    
    st.markdown("<h1 style='text-align:center;'>FORO TES</h1>", unsafe_allow_html=True)

    # Determinar si es usuario o profesional
    id_usuario = id_profesional = None
    nombre_usuario = nombre_profesional = perfil_profesional = None

    if tipo_usuario == "usuario":
        id_usuario, nombre_usuario = obtener_id_usuario(documento_identidad)
    elif tipo_usuario == "profesional":
        id_profesional, nombre_profesional, perfil_profesional = get_id_pro(documento_identidad)
    else:
        st.error("Tipo de usuario desconocido.")
        st.stop()

    if not (id_usuario or id_profesional):
        st.error("Usuario o profesional no encontrado.")
        st.stop()

    nombre = nombre_usuario if id_usuario else nombre_profesional
    st.write(f"Bienvenid@, {nombre}")

    # Campo comentario
    comentario = st.text_area("Escribe tu comentario (máximo 300 caracteres):", max_chars=300)

    # Archivo
    archivo = st.file_uploader("Sube un archivo (opcional):", type=["pdf", "jpg", "png", "txt"])

    if st.button("Enviar comentario"):
        if comentario.strip():
            archivo_bytes = archivo.read() if archivo else None
            guardar_comentario(id_usuario, id_profesional, comentario, archivo_bytes)
        else:
            st.error("Por favor, escribe un comentario.")

    # Mostrar comentarios del foro
    st.subheader("------------------------------------------------------------------------------")
    comentarios = obtener_comentarios()
    if comentarios:
        for com in comentarios:
            if com[5]:  # Imagen perfil
                try:
                    perfil_bytes = bytes(com[5]) if isinstance(com[5], memoryview) else com[5]
                    perfil_base64 = bytes_to_base64(perfil_bytes)
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <img src="data:image/png;base64,{perfil_base64}" 
                            style="border-radius: 50%; width: 50px; height: 50px; margin-right: 10px;">
                        <div>
                            <strong>{com[3]}</strong><br>
                            <small>{com[2]}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    st.warning("No se pudo cargar la imagen de perfil.")
            else:
                st.write(f"**{com[3]}**, {com[2]}")

            st.write(com[1])  # Contenido

            if com[4]:  # Archivo adjunto
                archivo_bytes = bytes(com[4]) if isinstance(com[4], memoryview) else com[4]
                if archivo_bytes:
                    try:
                        if archivo_bytes.startswith(b'%PDF'):
                            st.text("Archivo PDF (no se puede mostrar directamente).")
                        elif archivo_bytes[:4] in (b'\xFF\xD8\xFF\xE0', b'\x89PNG'):
                            st.image(archivo_bytes, width=300)
                        else:
                            try:
                                texto = archivo_bytes.decode('utf-8')
                                st.text(texto)
                            except:
                                st.write("Archivo en formato no compatible.")
                    except Exception as ex:
                        st.error(f"No se pudo mostrar el archivo: {ex}")
                    st.download_button("Descargar archivo", archivo_bytes, file_name=f"archivo_{com[2]}.bin", mime="application/octet-stream", key=f"dl_{com[0]}")
            st.write("---")
    else:
        st.info("No hay comentarios aún.")

if __name__ == "__main__":
    main()
