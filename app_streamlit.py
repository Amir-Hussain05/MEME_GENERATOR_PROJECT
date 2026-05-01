import streamlit as st
import os
from caption_generator import generate_caption
from image_generator import generate_ai_image
from meme_engine import create_meme
from template_selector import get_template
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Meme Generator",
    page_icon="😂",
    layout="centered"
)

# ─── Header ─────────────────────────────────────────────────────────────────
st.title("😂 AI Meme Generator")
st.markdown("Generate hilarious memes using AI captions and images!")

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    st.markdown("### How to use")
    st.markdown("""
    1. Enter a funny scenario
    2. Choose your image source
    3. Click **Generate Meme**
    4. Download your meme!
    """)
    st.markdown("---")
    st.caption("Powered by OpenAI 🤖")

# ─── Main UI ────────────────────────────────────────────────────────────────
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

# ─── Generate Button ────────────────────────────────────────────────────────
if st.button("🚀 Generate Meme", use_container_width=True, type="primary"):

    if not scenario.strip():
        st.warning("⚠️ Please enter a scenario first!")
    else:
        with st.spinner("🎨 Generating your meme..."):
            try:
                # ✅ Generate caption
                top, bottom, category = generate_caption(scenario)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"**Category:** {category}")
                with col2:
                    st.info(f"**Top:** {top}")
                with col3:
                    st.info(f"**Bottom:** {bottom}")

                # ✅ Select / prepare image
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
                    with st.spinner("🤖 Generating AI image (this may take a moment)..."):
                        image_path = generate_ai_image(scenario)

                # ✅ Create meme
                output = create_meme(image_path, top, bottom)

                # ✅ Display meme
                st.success("✅ Meme generated!")
                st.image(output, caption="Your AI Meme", use_container_width=True)

                # ✅ Download button
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
                st.exception(e)
