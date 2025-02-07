import streamlit as st
import requests
import json

# Configura la API key desde los secretos de Streamlit
api_key = st.secrets["GROQ_API_KEY"]

# Función para interactuar con la API de Groq
def obtener_respuesta(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "deepseek-r1-distill-llama-70b",
        "temperature": 0.6,
        "max_completion_tokens": 4096,
        "top_p": 0.95,
        "stream": True,
        "stop": None
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)

    # Procesar la respuesta en streaming
    respuesta_completa = ""
    for chunk in response.iter_lines():
        if chunk:
            decoded_chunk = chunk.decode('utf-8')
            if decoded_chunk.strip() != "data: [DONE]":
                json_chunk = json.loads(decoded_chunk.split("data: ")[1])
                if "choices" in json_chunk:
                    content = json_chunk["choices"][0]["delta"].get("content", "")
                    respuesta_completa += content

    return respuesta_completa

# Interfaz de usuario de Streamlit
st.title("Chatbot de Asesoramiento Laboral")

# Introducción
st.write("¡Hola! Soy un chatbot diseñado para ayudarte a encontrar empleo. Vamos a recopilar algo de información para ofrecerte recomendaciones personalizadas.")

# Recopilación de información
genero = st.text_input("¿Cuál es tu género?")
edad = st.text_input("¿Cuántos años tienes?")
condicion_salud = st.text_input("¿Tienes alguna condición de salud que pueda afectar tu empleo?")
situacion_economica = st.text_input("¿Cuál es tu situación económica actual?")
intereses = st.text_input("¿Cuáles son tus intereses y preferencias?")
antecedentes_profesionales = st.text_input("¿Cuál es tu historial profesional?")
habilidades = st.text_input("¿Tienes alguna habilidad o certificación específica?")
educacion = st.text_input("¿Cuál es tu nivel educativo más alto?")
industrias_interes = st.text_input("¿Hay alguna industria o trabajo específico que te interese?")

# Botón para enviar la consulta
if st.button("Obtener Recomendaciones"):
    # Construir el prompt con la información recopilada
    prompt = (f"Context: Eres un experto en orientación profesional y colocación laboral con más de dos décadas de experiencia.\n"
              f"Role: Ayudar a personas desempleadas a encontrar trabajo.\n"
              f"Action:\n"
              f"1. Saludo y presentación:\n"
              f"   - Saludo cálido y empático.\n"
              f"   - Breve introducción del propósito del chatbot.\n"
              f"2. Recopilación de información:\n"
              f"   - Género: {genero}\n"
              f"   - Edad: {edad}\n"
              f"   - Condición de salud: {condicion_salud}\n"
              f"   - Situación económica: {situacion_economica}\n"
              f"   - Intereses y preferencias: {intereses}\n"
              f"   - Antecedentes profesionales: {antecedentes_profesionales}\n"
              f"   - Habilidades o certificaciones: {habilidades}\n"
              f"   - Nivel educativo: {educacion}\n"
              f"   - Industrias o trabajos de interés: {industrias_interes}\n"
              f"3. Análisis de datos:\n"
              f"   - Identificar fortalezas, limitaciones y preferencias del usuario.\n"
              f"4. Recomendaciones de empleo:\n"
              f"   - Proporcionar una lista de recomendaciones de empleo que coincidan con el perfil del usuario.\n"
              f"5. Plan de acción:\n"
              f"   - Desarrollar un plan de acción personalizado para el usuario.\n"
              f"6. Seguimiento:\n"
              f"   - Ofrecer opciones de apoyo y recursos adicionales.\n"
              f"Format: Las respuestas del chatbot deben presentarse en un formato conversacional, usando texto sin formato.\n"
              f"Target Audience: Personas desempleadas que buscan recomendaciones de empleo.")

    # Obtener la respuesta del modelo
    respuesta = obtener_respuesta(prompt)

    # Mostrar la respuesta
    st.write("### Recomendaciones Personalizadas")
    st.write(respuesta)
