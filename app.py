import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. SETUP ---
st.set_page_config(page_title="Vivann AI Project", page_icon="🚀")

# Pulls from Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("👋 Please enter your API Key in the sidebar to start.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. THE GEMINI 3.1 FIX ---
# 'gemini-3.1-flash-lite-preview' is the most stable name for 3.1 right now.
try:
    model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')
except Exception as e:
    # If lite isn't available, we fallback to 2.5 flash which always works
    model = genai.GenerativeModel('gemini-2.5-flash')
    st.sidebar.warning("Note: Using Gemini 2.5 Flash as fallback.")

# --- 3. THE INTERFACE ---
st.title("🚀 Vivann AI Project")
st.caption("Powered by Gemini 3.1 Flash-Lite")

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
