import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. QUICK SETUP ---
st.set_page_config(page_title="Vivann AI Project", page_icon="🚀")

api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("👋 Welcome! System is ready. (Awaiting API Key)")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. FAST MODEL PICKER (No more 4-minute wait) ---
@st.cache_resource
def get_working_model():
    # We try the specific 3.1 Lite name first, then 2.5 as a solid backup
    for name in ['gemini-3.1-flash-lite-preview', 'gemini-1.5-flash']:
        try:
            m = genai.GenerativeModel(name)
            # Short test to confirm it's "alive"
            m.generate_content("Hi", generation_config={"max_output_tokens": 1})
            return m, name
        except:
            continue
    return None, None

model, model_name = get_working_model()

if not model:
    st.error("Connection Timeout. Please refresh the page.")
    st.stop()

# --- 3. UI ---
st.title("🚀 Vivann AI Project")
st.caption(f"⚡ Active Engine: {model_name}")

mode = st.sidebar.selectbox("Choose Mode", ["Math & General", "Image Analysis"])

if mode == "Math & General":
    user_query = st.text_input("Ask a math problem (e.g., 1+1):")
    if user_query:
        with st.spinner("Processing..."):
            try:
                response = model.generate_content(user_query)
                st.subheader("Result")
                st.write(response.text)
            except Exception as e:
                st.error("The AI is busy. Please try again in a moment.")

elif mode == "Image Analysis":
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        img = PIL.Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image")
        if st.button("Analyze Image"):
            with st.spinner("Scanning..."):
                response = model.generate_content(["Solve this math:", img])
                st.write(response.text)
