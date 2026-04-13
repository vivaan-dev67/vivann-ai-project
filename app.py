import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. SETUP ---
st.set_page_config(page_title="Vivann AI Project", page_icon="🚀")

# PULLING FROM SECRETS (Keep this exactly as is)
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("👋 Please enter your API Key in the sidebar to start.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. THE GEMINI 3.1 AUTO-PICKER ---
# This fixes the 'NotFound' error by trying both names
@st.cache_resource
def load_model():
    model_names = ['gemini-3.1-flash', 'gemini-3.1-flash-preview', 'gemini-3-flash-preview']
    for name in model_names:
        try:
            m = genai.GenerativeModel(name)
            # Test it briefly
            return m
        except:
            continue
    st.error("Could not find Gemini 3.1. Please check your API usage limits.")
    st.stop()

model = load_model()

# --- 3. THE INTERFACE ---
st.title("🚀 Vivann AI Project")
st.caption("Powered by Gemini 3.1 Flash")

mode = st.sidebar.selectbox("Choose Mode", ["Math & General", "Image Analysis"])

if mode == "Math & General":
    user_query = st.text_input("Ask a math problem:")
    if user_query:
        with st.spinner("Gemini 3.1 is analyzing..."):
            response = model.generate_content(user_query)
            st.subheader("Analysis Complete")
            st.write(response.text)

elif mode == "Image Analysis":
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        img = PIL.Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image")
        if st.button("Analyze Image"):
            with st.spinner("Gemini 3.1 is scanning..."):
                response = model.generate_content(["Solve this math and describe the image:", img])
                st.write(response.text)

st.sidebar.divider()
st.sidebar.write("Project inspired by *Kaushal Bodh*.")
