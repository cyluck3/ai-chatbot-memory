import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Para cargar variables de entorno
from dotenv import load_dotenv
load_dotenv(dotenv_path="config.env")


# para MCP
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType

# Con Gemma 3 no puedo predefinir cómo debe comportarse el agente con una instrucción de base
# Pero con otros modelos superiores sí puedo 

# Configurar API del MODElO de IA a usar
google_api_key = os.environ.get("GOOGLE_API_KEY")

# Instanciar Modelo
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=google_api_key)


def maketxt(texto):
    with open(f"1.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    print("Archivo guardado con éxito.")

# Crear un prompt para el modelo
prompt = ChatPromptTemplate.from_messages([
    ("system", f"Actúa como si fueras Sebastian Michaelis de Kuroshitsuji, el usuario es Ciel Phantomhive"), #quitar o comentar esta línea si uso Gemma 3
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Crear cadena de conversación
chain = prompt | llm

def run():
    print("Bienvenido a la IA de Google")

    capaelegido = "" # acción a hacer seleccionada

    # Para mantener el historial de la conversación
    chat_history = []
    interacciones = 0 # Variable que cuenta las interacciones
    max_interacciones = 25 # Numero maximo de interacciones antes de resetear


    while True:
        # Obtener la entrada del usuario
        user_input = input("Tú: ")

        # Salir si el usuario escribe 'salir'
        if user_input.lower() == "salir":
            print("¡Hasta luego!")
            break
            
        # **Resetear la memoria si el usuario escribe 'resetear'**
        if user_input.lower() == "resetear":
            chat_history = []
            interacciones = 0 # Resetear el contador de interacciones
            print("Memoria reseteada.")
            continue  # Ir a la siguiente iteración del bucle
        
        # Resetear la memoria si se llega al numero maximo de interacciones
        if interacciones >= max_interacciones:
            chat_history = []
            interacciones = 0 # Resetear el contador de interacciones
            print("Memoria reseteada por numero maximo de interacciones.")

        # Crear un mensaje humano y agregarlo al historial
        human_message = HumanMessage(content=user_input)
        chat_history.append(human_message)

        # Ejecutar la cadena y obtener la respuesta de la IA
        response = chain.invoke({
            "input": user_input,
            "chat_history": chat_history
        })

        # Agregar el mensaje de la IA al historial
        # Guardar el historial de la conversación en un archivo y en la lista historial
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response.content))
        interacciones += 1 # Sumar una interaccion


        #with open("historial_conversacion.txt", "a") as f:
        #    f.write(f"Tú: {user_input}\n")
        #    f.write(f"IA: {response['text']}\n")
        
        # Imprimir la respuesta de la IA
        print("IA:", response.content)

if __name__ == "__main__":
    run()


# Tutorial: https://www.youtube.com/watch?v=9EWR5T7QyBU&ab_channel=C%C3%B3digoEspinoza-IAyMachineLearning

# para generación de imágenes https://python.langchain.com/docs/integrations/tools/google_imagen/


### PROMPTS 
# Actúa como si fueras Sebastian Michaelis de Kuroshitsuji, el usuario es Ciel Phantomhive

