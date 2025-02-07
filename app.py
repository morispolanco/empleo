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

# Inicializar la sesión de Streamlit
if 'paso' not in st.session_state:
    st.session_state.paso = 0

# Interfaz de usuario de Streamlit
st.title("Chatbot de Asesoramiento Laboral")

# Introducción
if st.session_state.paso == 0:
    st.write("¡Hola! Soy un chatbot diseñado para ayudarte a encontrar empleo. Vamos a recopilar algo de información para ofrecerte recomendaciones personalizadas.")
    st.write("¿Cuál es tu género?")
    genero = st.text_input("", key="genero")
    if genero:
        st.session_state.paso += 1
        st.session_state.genero = genero
        st.experimental_rerun()

elif st.session_state.paso == 1:
    st.write(f"Gracias {st.session_state.genero}. ¿Cuántos años tienes?")
    edad = st.text_input("", key="edad")
    if edad:
        st.session_state.paso += 1
        st.session_state.edad = edad
        st.experimental_rerun()

elif st.session_state.paso == 2:
    st.write(f"¿Tienes alguna condición de salud que pueda afectar tu empleo?")
    condicion_salud = st.text_input("", key="condicion_salud")
    if condicion_salud:
        st.session_state.paso += 1
        st.session_state.condicion_salud = condicion_salud
        st.experimental_rerun()

elif st.session_state.paso == 3:
    st.write("¿Cuál es tu situación económica actual?")
    situacion_economica = st.text_input("", key="situacion_economica")
    if situacion_economica:
        st.session_state.paso += 1
        st.session_state.situacion_economica = situacion_economica
        st.experimental_rerun()

elif st.session_state.paso == 4:
    st.write("¿Cuáles son tus intereses y preferencias?")
    intereses = st.text_input("", key="intereses")
    if intereses:
        st.session_state.paso += 1
        st.session_state.intereses = intereses
        st.experimental_rerun()

elif st.session_state.paso == 5:
    st.write("¿Cuál es tu historial profesional?")
    antecedentes_profesionales = st.text_input("", key="antecedentes_profesionales")
    if antecedentes_profesionales:
        st.session_state.paso += 1
        st.session_state.antecedentes_profesionales = antecedentes_profesionales
        st.experimental_rerun()

elif st.session_state.paso == 6:
    st.write("¿Tienes alguna habilidad o certificación específica?")
    habilidades = st.text_input("", key="habilidades")
    if habilidades:
        st.session_state.paso += 1
        st.session_state.habilidades = habilidades
        st.experimental_rerun()

elif st.session_state.paso == 7:
    st.write("¿Cuál es tu nivel educativo más alto?")
    educacion = st.text_input("", key="educacion")
    if educacion:
        st.session_state.paso += 1
        st.session_state.educacion = educacion
        st.experimental_rerun()

elif st.session_state.paso == 8:
    st.write("¿Hay alguna industria o trabajo específico que te interese?")
    industrias_interes = st.text_input("", key="industrias_interes")
    if industrias_interes:
        st.session_state.paso += 1
        st.session_state.industrias_interes = industrias_interes
        st.experimental_rerun()

elif st.session_state.paso == 9:
    # Construir el prompt con la información recopilada
    prompt = (f"Context: Eres un experto en orientación profesional y colocación laboral con más de dos décadas de experiencia.\n"
              f"Role: Ayudar a personas desempleadas a encontrar trabajo.\n"
              f"Action:\n"
              f"1. Saludo y presentación:\n"
              f"   - Saludo cálido y empático.\n"
              f"   - Breve introducción del propósito del chatbot.\n"
              f"2. Recopilación de información:\n"
              f"   - Género: {st.session_state.genero}\n"
              f"   - Edad: {st.session_state.edad}\n"
              f"   - Condición de salud: {st.session_state.condicion_salud}\n"
              f"   - Situación económica: {st.session_state.situacion_economica}\n"
              f"   - Intereses y preferencias: {st.session_state.intereses}\n"
              f"   - Antecedentes profesionales: {st.session_state.antecedentes_profesionales}\n"
              f"   - Habilidades o certificaciones: {st.session_state.habilidades}\n"
              f"   - Nivel educativo: {st.session_state.educacion}\n"
              f"   - Industrias o trabajos de interés: {st.session_state.industrias_interes}\n"
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
