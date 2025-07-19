import streamlit as st
import requests

st.title("My AI app")

api_key = st.sidebar.text_input("API Key", type="password").strip()
prompt = st.text_area("Enter your prompt:", "Explain how AI works in a few words")

def gemini_response(api_key, prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "No answer received: " + str(result)
    else:
        return f"Error: {response.status_code} - {response.text}"

if not api_key:
    st.warning("Please enter your API key!", icon="⚠️")

if st.button("Send"):
    if not api_key:
        st.warning("Please enter your API key!", icon="⚠️")
    elif not prompt.strip():
        st.error("❌ Prompt field cannot be empty!")
    else:
        answer = gemini_response(api_key, prompt)
        st.info(answer)