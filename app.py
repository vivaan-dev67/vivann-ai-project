import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. The AI Engine (Handles Text, Images, and Audio)
def vivann_ai_engine(prompt, file_data=None, m_type=None):
    # Using the stable 2026 model
    model = genai.GenerativeModel('gemini-1.5-flash')
    if file_data:
        # This sends the file (photo or sound) to Google
        response = model.generate_content([
            prompt, 
            {'mime_type': m_type, 'data': file_data}
        ])
    else:
        response = model.generate_content(prompt)
    return response.text

# 2. The Interface
st.set_page_config(page_title="Vivann AI Project", layout="centered")
st.title("🚀 Vivann AI Project")
st.write("Math Solver + Image & Audio Recognition")

# 3. Sidebar Settings
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
mode = st.sidebar.selectbox("Choose Mode", ["Math & General", "Identify Object/Sound"])

if api_key:
    genai.configure(api_key=api_key)
    
    if mode == "Math & General":
        u_input = st.text_input("Type your math problem:")
        u_file = st.file_uploader("Upload Math Photo (Optional)", type=["jpg", "png", "jpeg"])
        p_prefix = "Solve this step-by-step: "
    else:
        u_input = st.text_input("What is this?")
        u_file = st.file_uploader("Upload Photo or Audio (Cuckoo sound, etc.)", type=["jpg", "png", "mp3", "wav"])
        p_prefix = "Identify this object or sound source precisely: "

    if st.button("Run Vivann AI"):
        if u_file or u_input:
            try:
                with st.spinner("Vivann AI is analyzing..."):
                    # Prepare the file data
                    f_bytes = u_file.getvalue() if u_file else None
                    f_type = u_file.type if u_file else None
                    
                    # Combine the prompt and run
                    final_p = f"{p_prefix} {u_input}"
                    result = vivann_ai_engine(final_p, f_bytes, f_type)
                    
                    st.success("Analysis Complete:")
                    st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please upload a file or type a question.")
else:
    st.info("👈 Please enter your API Key in the sidebar to start.")
