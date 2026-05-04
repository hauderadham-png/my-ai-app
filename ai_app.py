import streamlit as st
import requests
import io
import anthropic
from PIL import Image

st.set_page_config(page_title="AI Image Generator", page_icon="🤖", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }

h1 { color: #f8c945 !important; text-align: center; font-size: 2.5rem !important; }
h3 { color: #e0e0e0 !important; }

.stButton > button {
    background: linear-gradient(90deg, #f8c945, #f3722c);
    color: #1a1a2e;
    font-weight: 800;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 2rem;
    font-size: 1.1rem;
    width: 100%;
    cursor: pointer;
    transition: transform 0.2s;
}
.stButton > button:hover { transform: scale(1.03); }

.prompt-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(248,201,69,0.3);
    border-radius: 16px;
    padding: 1rem 1.5rem;
    margin: 0.5rem 0;
    color: #f0f0f0;
}
.enhanced-label {
    color: #f8c945;
    font-weight: 700;
    font-size: 0.85rem;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🤖 AI Image Generator 🇹🇳")
st.markdown("---")

# ── Step 1: User Input ────────────────────────────────────────────────────────
st.subheader("1️⃣  Describe the image you want to create:")
user_prompt = st.text_area(
    "Write in any language — English, Arabic or  French",
    placeholder="Example: A cat playing football in an old Tunisian street",
    height=100,
)

st.markdown("---")

# ── Step 2: AI Enhancement ────────────────────────────────────────────────────
st.subheader("2️⃣  Enhance Your Prompt with Claude AI")

def enhance_prompt(raw_prompt: str) -> str:
    """Translate & enhance the user's prompt using Claude."""
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are an expert AI image prompt engineer. "
                    "The user has written the following description in any language "
                    "(Tunisian Arabic, Arabic, French, or English):\n\n"
                    f'"{raw_prompt}"\n\n'
                    "Your task:\n"
                    "1. Understand what the user wants to visualize.\n"
                    "2. Translate it to English if needed.\n"
                    "3. Rewrite it as a vivid, detailed, and optimized English prompt "
                    "for a text-to-image AI model (Flux). "
                    "Add style keywords, lighting, composition, and mood details.\n"
                    "Return ONLY the enhanced English prompt, nothing else."
                ),
            }
        ],
    )
    return message.content[0].text.strip()


if st.button("✨ Enhance Prompt with Claude"):
    if user_prompt.strip():
        with st.spinner("Claude is thinking... 🧠"):
            try:
                enhanced = enhance_prompt(user_prompt)
                st.session_state["enhanced_prompt"] = enhanced
            except Exception as e:
                st.error(f"Claude API error: {e}")
    else:
        st.warning("Please write a description first!")

# Display enhanced prompt if available
if "enhanced_prompt" in st.session_state:
    st.markdown('<div class="enhanced-label">📝 Enhanced Prompt (English):</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="prompt-box">{st.session_state["enhanced_prompt"]}</div>',
        unsafe_allow_html=True,
    )
    edited = st.text_area(
        "You can edit the prompt before generating:",
        value=st.session_state["enhanced_prompt"],
        height=80,
        key="edited_prompt",
    )
    st.session_state["final_prompt"] = edited

st.markdown("---")

# ── Step 3: Image Generation ──────────────────────────────────────────────────
st.subheader("3️⃣  Generate Your Image 🎨")

if st.button("🚀 Generate Image"):
    final = st.session_state.get("final_prompt", user_prompt).strip()
    if not final:
        st.warning("Please write a description and enhance the prompt first!")
    else:
        with st.spinner("Working on your image... please wait 🎨"):
            image_url = (
                f"https://image.pollinations.ai/prompt/"
                f"{requests.utils.quote(final)}"
                f"?width=1024&height=1024&model=flux&nologo=true"
            )
            try:
                response = requests.get(image_url, timeout=60)
                response.raise_for_status()
                image = Image.open(io.BytesIO(response.content))

                st.image(image, caption="✅ Your generated image", use_container_width=True)
                st.success("Done! Your image is ready 🎉")

                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button(
                    "Download Image 📥",
                    buf.getvalue(),
                    "ai_image.png",
                    "image/png",
                )
            except Exception as e:
                st.error("Connection error, please try again! ⚠️")

st.markdown("---")
st.caption("Built by: Hayder Adham & Arij Benltaif 🚀")
