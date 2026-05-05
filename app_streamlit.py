import streamlit as st
import os
from meme_engine import create_meme
from template_selector import get_template

st.set_page_config(
    page_title="MemeGPT",
    page_icon="😂",
    layout="centered"
)

with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)

    st.markdown("### 🔑 OpenAI API Key")
    api_key = st.text_input(
        "Paste your API key here",
        type="password",
        placeholder="sk-proj-...",
        help="Your key is never saved."
    )

    if api_key:
        st.success("✅ API Key entered!")
    else:
        st.warning("⚠️ Enter your API key to generate memes")

    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("""
    1. 🔑 Paste your OpenAI API key above
    2. 📝 Enter a funny scenario
    3. 🖼️ Choose image source
    4. 🚀 Click Generate Meme
    5. ⬇️ Download your meme!
    """)
    st.markdown("---")
    st.caption("Developed by Amir and Tarique 🤖")

st.title("😂 MemeGPT")
st.markdown("Generate hilarious memes using AI captions and images!")

scenario = st.text_area(
    "📝 Enter your scenario",
    placeholder="e.g. When you study all night but the exam is tomorrow...",
    height=100
)

option = st.radio(
    "🖼️ Choose image source",
    ["Template", "Upload", "AI Generate"],
    horizontal=True
)

uploaded_file = None
if option == "Upload":
    uploaded_file = st.file_uploader(
        "Upload your image",
        type=["png", "jpg", "jpeg", "webp"]
    )

st.markdown("---")

if st.button("🚀 Generate Meme", use_container_width=True, type="primary"):

    if not api_key.strip():
        st.error("❌ Please enter your OpenAI API key in the sidebar first!")

    elif not scenario.strip():
        st.warning("⚠️ Please enter a scenario first!")

    else:
        with st.spinner("🎨 Generating your meme..."):
            try:
                from caption_generator import generate_caption
                from image_generator import generate_ai_image

                top, bottom, category = generate_caption(scenario, api_key)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"**Category:** {category}")
                with col2:
                    st.info(f"**Top:** {top}")
                with col3:
                    st.info(f"**Bottom:** {bottom}")

                if option == "Template":
                    image_path = get_template(category)

                elif option == "Upload":
                    if uploaded_file:
                        os.makedirs("uploads", exist_ok=True)
                        image_path = os.path.join("uploads", uploaded_file.name)
                        with open(image_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                    else:
                        st.error("❌ Please upload an image first!")
                        st.stop()

                elif option == "AI Generate":
                    with st.spinner("🤖 Generating AI image (this may take 30 seconds)..."):
                        image_path = generate_ai_image(scenario, api_key)

                output = create_meme(image_path, top, bottom)

                st.success("✅ Meme generated!")
                st.image(output, caption="Your AI Meme", use_container_width=True)

                with open(output, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Meme",
                        data=f,
                        file_name=os.path.basename(output),
                        mime="image/png",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"❌ Error: {e}")
