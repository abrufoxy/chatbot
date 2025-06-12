import streamlit as st
import groq as gq
# TENER MODELOS DE IA

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192']

#CONFIGURAR PÁGINA
def configurar_pagina():

    st.set_page_config(page_title="Chatbot con Python" , page_icon="🤖") #cambia el nombre de la ventana del navegador
    st.title("Bienvenidos a mi chatbot:3")



 # MOSTRAR EL SIDEBAR CON LOS MODELOS
def mostrar_sidebar():
    st.sidebar.title('Elegí tu modelo de IA')
    modelo = st.sidebar.selectbox('¿Cuál elejís?', MODELOS,index=0)
    st.write(f'**Elejiste el modelo:** {modelo}')
    return modelo

#  UN CLIENTE GROQ

def crear_cliente_groq():
    groq_api_key= st.secrets['GROQ_APT_KEY'] #almacena la api key de groq
    return gq.Groq(api_key=groq_api_key)

# INICIALIZAR EL ESTADO DE LOS MENSAJES
def inicializacion_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


# HISTORIAL DEL CHAT
def mostrar_historial_chat():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):     #context manager
            st.markdown(mensaje["content"])


# INPUT USUARIO
def obtener_mensaje_usuario():
    return st.chat_input('Escribí tu mensaje')

# AGREGAR LOS MENSAJES AL HISTORIAL
def agregar_mensajes_historial(role, content):
    st.session_state.mensajes.append({"role":role, "content": content})


# MOSTRAR LOS MENSAJES EN PENTALLA
def  mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

# LLAMAR AL MODELO DE GROQ
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream = False
    )
    return respuesta.choices[0].message.content

# EJECUTAMIENTO DE PÁGINA
def ejecutar_app():
    configurar_pagina()
    modelo = mostrar_sidebar()
    cliente = crear_cliente_groq()
    inicializacion_estado_chat()
    mostrar_historial_chat()
    mensaje_usuario = obtener_mensaje_usuario()

    if mensaje_usuario:
        agregar_mensajes_historial("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)

        mensaje_modelo = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)

        agregar_mensajes_historial("assistant", mensaje_modelo)
        mostrar_mensaje("assistant", mensaje_modelo)


if __name__== '__main__': # si este archivo es el principal, ejecutá
    ejecutar_app()