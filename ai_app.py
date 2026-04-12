import streamlit as st
import requests
import io
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="Tunisian AI Generator", page_icon="🤖")

st.title("🤖 🇹🇳")
st.markdown("---")

# خانة إدخال الكلام
st.subheader("أوصفلي التصويرة اللي تحب تصنعها:")
prompt = st.text_input("أكتب بالإنجليزية ", "")

# زر الصناعة
if st.button("أصنع السحر ✨"):
    if prompt:
        with st.spinner('قاعد نخدم على تصويرتك...'):
            # الرابط السريع (Pollinations AI) - ما يسخنش وما يطلبش وقت
            image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&model=flux"
            
            try:
                response = requests.get(image_url)
                image = Image.open(io.BytesIO(response.content))
                
                # إظهار النتيجة
                st.image(image, caption=f"النتيجة لـ: {prompt}", use_container_width=True)
                st.success("مبروك! هاذي تصويرتك حضرت.")
                
                # زر التحميل
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button("تحميل الصورة 📥", buf.getvalue(), "ai_image.png", "image/png")
                
            except Exception as e:
                st.error("فمة مشكلة في الكونكسيون، عاود جرب!")
    else:
        st.warning("لازم تكتب حاجة باش الماكينة تخدم!")

st.markdown("---")
st.caption("برمجة وتطوير: [إسمك هنا] 🚀")
