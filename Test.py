#Importing all the necessary libraries
import random
import google.generativeai as genai
import streamlit as st
import time
import base64
#Setting the page configuration
st.set_page_config(
    page_title="AgriBot",
    layout="wide",
    page_icon=":chart_with_upwards_trend:",
    
)
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("/Users/srimanthdhondy/Programs/Project_SenseGrass/HD-wallpaper-grass-wicker-texture-grass-weave-texture-macro-green-background-grass-textures-green-grass-texture-grass-from-top-grass-background-green-grass.jpg")
pg_bg = """<style>
[data-testid="stApp"]
{
    background-image: url("data:image/jpg;base64,{img}")
    background-position: center;
    background-color: #f6fff9;
}
[data-testid="stSidebar"] > div:first-child
{{
   background-image: url("data:image/jpg;base64,""" + img + """")
   background-position: center;
}}
</style>"""
st.markdown(pg_bg, unsafe_allow_html=True)
#Setting the header and subheader
st.header("Gemini LLM Powered Chat Bot",divider="rainbow")
st.subheader("Ask me anything about anything and I will try to help you out.")
#Checking if the generative model is in the session state
if "genai_model" not in st.session_state:
    st.session_state["genai_model"] = genai.GenerativeModel('gemini-pro')
#Checking if the sidebar state is in the session state
if "sidebar_state" not in st.session_state:
        st.session_state.sidebar_state = False
#Checking if the chat is in the session state
if 'chat' not in st.session_state:
    st.session_state.chat = st.session_state["genai_model"].start_chat(history=[])
      
#Function to confirm clearing the chat history
def confirm_clear_history():#Perfectly working
    with st.sidebar:
        confirmation = st.button("Clear Chat History")
        if confirmation:
            st.session_state.chat = st.session_state["genai_model"].start_chat(history=[])
            msg = st.empty()
            msg.success("Chat history cleared.", icon='✅')
            time.sleep(2)
            msg.empty()
#Creating the sidebar
with st.sidebar:
    gemini_api_key = st.text_input("Enter your Gemini API Key", key="chatbot_api_key", type="password",)
    if gemini_api_key != '':
        msg = st.empty()
        msg.success('Thank You for providing API key.', icon='✅')
        confirm_clear_history()
        st.markdown("---")
        st.write("Powered by [GenerativeAI](https://generativeai.com/)")
        st.warning("NOTE: This model may generate inaccurate responses. Kindly use with caution. Do not enter any sensitive information.", icon="⚠️")
        #st.session_state.chat_history = st.session_state.chat_history.append[st.session_state.chat]
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#Checking if the API key is empty
if gemini_api_key == "":
        st.info("""Please enter your Gemini API key before you continue.
                [**Click here to create/get a Gemini API key**](https://aistudio.google.com/app/apikey)""")
        st.chat_input()
#Configuring the generative model
client = genai.configure(api_key=gemini_api_key)
#print(st.session_state['chat'].history[3].parts[0].text)
#print(st.session_state['chat'].history)
with st.chat_message("assistant",avatar='🤖'):
    st.markdown("How can I help you today?You can ask me anything about agriculture or any topic of your choice.")

for message in st.session_state['chat'].history:
    with st.chat_message(message.role,avatar='🤖'if message.role=='model' else None):
        st.markdown(message.parts[0].text)

if gemini_api_key != "":
    if prompt := st.chat_input():
    #client = genai.configure(api_key=gemini_api_key)
        with st.chat_message("user"):
             st.markdown(prompt)
        with st.chat_message("ai", avatar='🤖'):
            with st.spinner(random.choice([x for x in ["Generating your response...", "Thinking...", "I'm on it!", "Just a sec...", "Let me think...", "Hang On...", "The answer is getting ready...", "......"]])):
                 stream = st.session_state.chat.send_message(prompt)
                 response = st.write(stream.text)
