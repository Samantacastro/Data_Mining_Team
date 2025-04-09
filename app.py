import streamlit as st
import os
import requests

st.set_page_config(page_title="Together AI Code Generator", page_icon="🤖")

st.title("🤖 Together AI Python Code Generator")
st.markdown("Describe what you want the Python code to do, and Together AI will generate it for you!")

prompt = st.text_area("📝 Enter your prompt here", placeholder="e.g. Write a Python function to reverse a string")

if st.button("🚀 Generate Code"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            st.error("API key not found. Please add TOGETHER_API_KEY in Secrets.")
        else:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "mistralai/Mistral-7B-Instruct-v0.1",
                "prompt": prompt,
                "max_tokens": 256,
                "temperature": 0.7,
                "top_p": 0.9,
                "repetition_penalty": 1.2
            }

            response = requests.post(
                "https://api.together.xyz/inference",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                code = result.get("output", "No output returned.")
                st.subheader("💡 Generated Code")
                st.code(code, language='python')
            else:
                st.error(f"❌ Request failed with status code {response.status_code}")
                st.json(response.json())

