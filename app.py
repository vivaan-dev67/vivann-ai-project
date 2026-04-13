import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Vivann AI Project", page_icon="🚀")

# PULLING FROM SECRETS (Hidden from everyone but you)
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("👋 Welcome! Please enter an API Key to start or check 'Secrets' configuration.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. THE MODEL AUTO-PICKER (Fixes the 404/NotFound Error) ---
@st.cache_resource
def get_model():
    # We try the most likely Gemini 3.1 and 3.0 names in order
    model_names = [
        'gemini-3.1-flash-lite-preview', 
        'gemini-3.1-flash-preview', 
        'gemini-3-flash-preview'
    ]
    for name in model_names:
        try:
            m = genai.GenerativeModel(name)
            # Do a tiny test to see if this model exists
            m.generate_content("test", generation_config={"max_output_tokens": 1})
            return m, name
        except:
            continue
    # If all 3.x models fail, use the 2.5 stable version as a backup
    return genai.GenerativeModel('gemini-2.5-flash'), "gemini-2.5-flash"

model, active_model_name = get_model()

# --- 3. THE UI ---
st.title("🚀 Vivann AI Project")
st.caption(f"Running on: {active_model_name}")

mode = st.sidebar.selectbox("Choose Mode", ["Math & General", "Image Analysis"])

if mode == "Math & General":
    user_query = st.text_input("Ask a math problem:")
    if user_query:
        with st.spinner(f"Analyzing with {active_model_name}..."):
            response = model.generate_content(user_query)
            st.subheader("Analysis Complete")
            st.write(response.text)

elif mode == "Image Analysis":
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        img = PIL.Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image")
        if st.button("Analyze Image"):
            with st.spinner("Scanning..."):
                response = model.generate_content(["Solve this math and describe the image:", img])
                st.write(response.text)

st.sidebar.divider()
st.sidebar.write(f"System: {active_model_name}")
st.sidebar.write("Developed by Vivann.")
