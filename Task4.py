import streamlit as st
import requests

def is_on_topic(user_input, domain):
    prompt = f"Is the following question related to {domain}? Answer only 'yes' or 'no'.\n\nQuestion: {user_input}"
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        data = response.json()
        result = data.get("response", "").strip().lower()
        return "yes" in result
    except Exception as e:
        st.error(f"Error checking domain relevance: {e}")
        return False




st.set_page_config(page_title="Ollama ChatBot", layout="centered")
st.title("🤖 Ollama ChatBot UI")


with st.sidebar:
    st.header("⚙️ Settings")
    model = st.selectbox("Choose LLM Model", ["deepseek-r1:1.5b", "qwen3:0.6b"], index=0)
    domain = st.text_input("Domain ", "Finance")




if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"You are a knowledgeable and helpful assistant with expertise only in {domain}. Your job is to answer only questions that are clearly related to {domain}. Do not attempt to answer unrelated questions."}

    ]
    st.session_state.previous_domain = domain
    st.session_state.previous_model = model

if (domain != st.session_state.previous_domain) or (model != st.session_state.previous_model):
    st.session_state.messages = [
       {"role": "system", "content": f"You are a knowledgeable and helpful assistant with expertise only in {domain}. Your job is to answer only questions that are clearly related to {domain}.  Do not attempt to answer unrelated questions."}

    ]
    st.session_state.previous_domain = domain
    st.session_state.previous_model = model




for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])



prompt = st.chat_input("Type your message here...")

if prompt:
    with st.chat_message("user"):
            st.markdown(prompt)
    if (is_on_topic(prompt,domain)):
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            

        
            formatted_prompt = "\n".join([
                f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages
                if m["role"] != "system"
            ])
            system_message = st.session_state.messages[0]["content"]
            full_prompt = f"System: {system_message}\n{formatted_prompt}\nAssistant:"

            
            response = requests.post("http://localhost:11434/api/generate", json={
                "model": model,
                "prompt": full_prompt,
                "stream": False
            })


           
            output = response.json().get("response", "[Error: No response from model]")
            st.session_state.messages.append({"role": "assistant", "content": output})

            with st.chat_message("assistant"):
                st.markdown(output)
    else:
        with st.chat_message("assistant"):
                st.markdown(f" 'I'm sorry, I can only help with questions related to {domain}")

