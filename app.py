import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. SETUP & SECRETS ---
st.set_page_config(page_title="Vivann AI Project", page_icon="🚀")

# Automatically pulls from your Streamlit Secrets dashboard
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("👋 Please enter your API Key in the sidebar to start.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. THE GEMINI 3.1 MODEL SETUP ---
# For Gemini 3.1, we use the specific model ID. 
# If 'gemini-3.1-flash' gives an error, it will try the preview version.
try:
    model = genai.GenerativeModel('gemini-3.1-flash')
except:
    try:
        model = genai.GenerativeModel('gemini-3.1-flash-preview')
    except Exception as e:
        st.error(f"Could not connect to Gemini 3.1: {e}")
        st.stop()

# --- 3. THE UI ---
st.title("🚀 Vivann AI Project")
st.caption("Powered by Gemini 3.1 Flash")

mode = st.sidebar.selectbox("Choose Mode", ["Math & General", "Image Analysis"])

# --- 4. THE LOGIC ---
if mode == "Math & General":
    user_query = st.text_input("Ask a math problem:")
    if user_query:
        with st.spinner("Gemini 3.1 is thinking..."):
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
st.sidebar.write("System: Gemini 3.1 Flash")
st.sidebar.write("Project inspired by *Kaushal Bodh*.")
