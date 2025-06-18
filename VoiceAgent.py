import speech_recognition as sr
import pyttsx3
import psycopg2
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

# Cargar el modelo de IA desde Ollama
llm = OllamaLLM(model="mistral")

# Inicializar historial de conversación
chat_history = ChatMessageHistory()

# Inicializar motor de voz
engine = pyttsx3.init()
engine.setProperty("rate", 160)

recognizer = sr.Recognizer()

# Función para hablar
def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

# Función para escuchar
def escuchar():
    with sr.Microphone() as source:
        print("\nEscuchando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        consulta = recognizer.recognize_google(audio, language="es-ES")
        print(f"Dijiste: {consulta}")
        return consulta.lower()
    except sr.UnknownValueError:
        print("No entendí. Inténtalo de nuevo.")
        return ""
    except sr.RequestError:
        print("Error con el servicio de reconocimiento.")
        return ""

# Obtener profesionales de la base de datos
def obtener_profesionales():
    try:
        conexion = psycopg2.connect(
             host='localhost',
            user='your_user',
            password='your_password',
            dbname='emotionalai'
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, especialidad FROM profesionales")
        resultados = cursor.fetchall()
        conexion.close()

        if resultados:
            return "\n".join([f"- {nombre}, especialista en {especialidad}" for nombre, especialidad in resultados])
        else:
            return "No hay profesionales registrados aún."
    except Exception as e:
        return f"No se pudieron obtener los profesionales. Error: {str(e)}"

# Plantilla de prompt
plantilla = PromptTemplate(
    input_variables=["chat_history", "question", "contexto"],
    template="""
Eres TES, un asistente virtual para la salud mental. 
Funciones disponibles: enviar mensajes en foros, contactar profesionales o conversar contigo.

Profesionales disponibles:
{contexto}

Conversación previa:
{chat_history}

Usuario: {question}
TES:"""
)

# Procesar la pregunta
def ejecutar_cadena(pregunta):
    historial_texto = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages])
    contexto = obtener_profesionales()
    respuesta = llm.invoke(plantilla.format(chat_history=historial_texto, question=pregunta, contexto=contexto))
    chat_history.add_user_message(pregunta)
    chat_history.add_ai_message(respuesta)
    return respuesta

# Bucle principal
if __name__ == "__main__":
    hablar("¡Hola! Soy TES, tu asistente de salud mental. ¿En qué puedo ayudarte?")
    while True:
        consulta = escuchar()
        if "salir" in consulta or "detener" in consulta:
            hablar("¡Hasta luego! Que tengas un buen día.")
            break
        if consulta:
            respuesta = ejecutar_cadena(consulta)
            print(f"\nTES: {respuesta}")
            hablar(respuesta)
