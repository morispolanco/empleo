import streamlit as st
import requests
import json

def get_groq_response(user_input):
    api_key = st.secrets["GROQ_API_KEY"]  # Obtener la API key desde los secrets de Streamlit
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are an expert career counselor assisting unemployed individuals with job recommendations."},
            {"role": "user", "content": user_input}
        ],
        "model": "deepseek-r1-distill-llama-70b",
        "temperature": 0.6,
        "max_completion_tokens": 4096,
        "top_p": 0.95,
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error: No response received.")

# Configurar la interfaz de Streamlit
st.set_page_config(page_title="Career Chatbot", page_icon="💼")
st.title("Career Guidance Chatbot 🤖")

st.write("Bienvenido/a. Estoy aquí para ayudarte a encontrar oportunidades laborales que se ajusten a tu perfil. Responde algunas preguntas para que pueda ofrecerte recomendaciones personalizadas.")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Mostrar el historial del chat
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input del usuario
user_input = st.chat_input("Escribe tu mensaje aquí...")
if user_input:
    # Agregar mensaje del usuario al historial
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Obtener respuesta de la API
    response = get_groq_response(user_input)
    
    # Agregar respuesta del chatbot al historial
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
