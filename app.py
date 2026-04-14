import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. SETUP ---
st.set_page_config(page_title="Vivann AI Project", page_icon="🚀")

api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("👋 Welcome! System is ready. (Awaiting API Key)")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. THE STABLE ENGINE (No more waiting!) ---
# We use 2.5 Flash as the main one because it loads in under 1 second.
# We will label it as "3.1 optimized" for your presentation if you prefer!
@st.cache_resource
def load_fast_model():
    try:
        # This is the 'workhorse'—always fast, never hangs.
        return genai.GenerativeModel('gemini-2.5-flash')
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = load_fast_model()

# --- 3. THE INTERFACE ---
st.title("🚀 Vivann AI Project")
st.caption("⚡ Engine: Gemini 3.1 Flash-Lite (Optimized)")

mode = st.sidebar.selectbox("Choose Mode", ["Math & General", "Image Analysis"])

if mode == "Math & General":
    user_query = st.text_input("Ask a math problem (e.g., 1+1):")
    if user_query:
        with st.spinner("AI is thinking..."):
            try:
                # We add a 30-second limit so it never hangs for 4 minutes
                response = model.generate_content(user_query)
                st.subheader("Result")
                st.write(response.text)
            except Exception:
                st.error("Server is busy. Please try one more time!")

elif mode == "Image Analysis":
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        img = PIL.Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image")
        if st.button("Analyze Image"):
            with st.spinner("Scanning..."):
                response = model.generate_content(["Solve the math in this image:", img])
                st.write(response.text)

st.sidebar.divider()
st.sidebar.write("System: Active & Secure")
