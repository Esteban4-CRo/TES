import psycopg2
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from smtplib import SMTP

EMAIL_CONFIG = {
    "sender_email": "juancampinoc@gmail.com",
    "password": "6628651DianaJames",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}

def enviar_recordatorio(correo, nombre):
    mensaje = MIMEText(f"Hola {nombre}, han pasado 10 días desde tu registro. ¡Vuelve a visitarnos!")
    mensaje["Subject"] = "Te extrañamos en la plataforma"
    mensaje["From"] = EMAIL_CONFIG["sender_email"]
    mensaje["To"] = correo

    with SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as servidor:
        servidor.starttls()
        servidor.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["password"])
        servidor.send_message(mensaje)

def verificar_y_enviar():
    conn = psycopg2.connect(
        host='db.rbenrvkegphjaftoekjk.supabase.co',
        user='postgres',
        password='94410404Juan',
        dbname='postgres',
        port='5432'
    )
    cursor = conn.cursor()
    diez_dias_atras = datetime.now() - timedelta(days=10)

    # Ver usuarios
    cursor.execute("SELECT nombre, correo, fecha_registro FROM usuarios")
    for nombre, correo, fecha in cursor.fetchall():
        if fecha.date() == diez_dias_atras.date():
            enviar_recordatorio(correo, nombre)

    # Ver profesionales
    cursor.execute("SELECT nombre, correo, fecha_registro FROM profesionales")
    for nombre, correo, fecha in cursor.fetchall():
        if fecha.date() == diez_dias_atras.date():
            enviar_recordatorio(correo, nombre)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    verificar_y_enviar()
