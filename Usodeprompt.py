import streamlit as st
from openai import OpenAI



def preguntar(pregunta, modelo, prompt):
    try:
        cliente = OpenAI(api_key=st.session_state.api)
        response = cliente.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Escribe informacion optimizada sobre: {pregunta}"}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Introduce tu API para chatear: {str(e)}")
        return None

def sidebar():
    with (st.sidebar):
        st.sidebar.image("lion-head-logo.png", width=200)  # agrega icono
        st.page_link("Usodeprompt.py", label="Inicio", icon=":material/home:")
        st.page_link("pages/Guardados.py", label="Chats Guardados", icon=":material/file_present:")
        st.write("Entrada de datos")
        modelo = st.sidebar.selectbox("Selecciona un modelo", st.session_state.modelo)
        st.success(modelo)
        nuevoModelo = st.text_input("Introduce el modelo")
        if nuevoModelo:
            st.session_state.modelo.append(nuevoModelo)
        prompt = st.sidebar.selectbox("Selecciona una Plantilla", st.session_state.plantilla)
        st.success(prompt)
        with st.form("Crear Plantilla"):
            plantilla = st.text_input("Crea una nueva Plantilla")
            if st.form_submit_button("Crear", use_container_width=True):
                 st.session_state.plantilla.append(plantilla)

    return modelo, prompt



def main():
    if "plantilla" not in st.session_state:
        st.session_state.plantilla = ["Eres un experto en redacción de articulos SEO", "Eres un experto en redacción de twitter con no mas de 140 caracteres", "Eres un experto en redacción de recetas de cocina", "Eres un programador Python. Proporciona el codigo Python, sin explicaciones ni comentarios adicionales."]

    if "api" not in st.session_state:
        st.session_state.api = None

    if "Historial" not in st.session_state:
        st.session_state.historial = ["Historial de Chat"]

    if "respuesta" not in st.session_state:
        st.session_state.respuesta = ""

    if "modelo" not in st.session_state:
        st.session_state.modelo = ["gpt-4.1-mini", "gpt-4.1-nano"]

    api = st.text_input("Introduce tu api de OpenAI")
    if api:
        st.session_state.api = api

    modelo, prompt = sidebar()

    if pregunta := st.chat_input("Ingresa tu pregunta"):
        respuesta = preguntar(pregunta, modelo, prompt)
        st.session_state.respuesta = respuesta
        st.write(st.session_state.respuesta)
        st.session_state.historial.append(respuesta)
        #st.write(st.session_state)



if __name__ == "__main__":
    # configuracion de la app
    st.set_page_config(page_title="Prueba tus Modelos y Prompt", layout="wide", page_icon="lion-head-logo.png")
    main()
