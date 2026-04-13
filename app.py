import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. SETUP ---
st.set_page_config(page_title="Vivann AI Project", page_icon="🚀")

# Pulls from your Streamlit "Secrets" dashboard
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("👋 Please enter your API Key in the sidebar to start.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. THE SMART MODEL PICKER (Fixes the 404 Error) ---
@st.cache_resource
def get_best_model():
    # We try the newest Gemini 3.1 IDs first
    test_models = [
        'gemini-3.1-flash-lite-preview', 
        'gemini-3.1-flash-preview', 
        'gemini-2.5-flash' # Ultimate fallback
    ]
    for m_name in test_models:
        try:
            m = genai.GenerativeModel(m_name)
            # Try a tiny test call to see if the model name is 'Found'
            m.generate_content("test", generation_config={"max_output_tokens": 1})
            return m, m_name
        except Exception:
            continue
    st.error("Could not connect to any Gemini models. Check your API key.")
    st.stop()

model, model_name = get_best_model()

# --- 3. THE INTERFACE ---
st.title("🚀 Vivann AI Project")
st.caption(f"Currently active: {model_name}")

mode = st.sidebar.selectbox("Choose Mode", ["Math & General", "Image Analysis"])

if mode == "Math & General":
    user_query = st.text_input("Ask a math problem:")
    if user_query:
        with st.spinner("Analyzing..."):
            response = model.generate_content(user_query)
            st.subheader("Analysis Complete")
            st.write(response.text)

elif mode == "Image Analysis":
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        img = PIL.Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image")
        if st.button("Analyze Image"):
            with st.spinner("Scanning image..."):
                response = model.generate_content(["Solve this math and describe the image:", img])
                st.write(response.text)

st.sidebar.divider()
st.sidebar.write("Project inspired by *Kaushal Bodh*.")
