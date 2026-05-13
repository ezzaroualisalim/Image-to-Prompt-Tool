import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# جلب المفتاح السري بأمان من إعدادات المنصة
GOOGLE_API_KEY = st.secrets["AIzaSyBKD_D97KZiRjEHH_8wXAFI81PylKLBelE"]
genai.configure(api_key=GOOGLE_API_KEY)

# استخدام النموذج السريع والمجاني للزوار
model = genai.GenerativeModel('gemini-2.5-flash')

# ... (باقي الكود القديم يبقى كما هو دون تغيير) ...
# ==========================================
# 2. تصميم واجهة المستخدم (UI Design)
# ==========================================
st.set_page_config(page_title="مُحول الصورة إلى برومبت", layout="centered")

st.title("🖼️ أداة الهندسة العكسية للصور المشرقة")
st.subheader("قم برفع صورتك المفضلة، واحصل فوراً على البرومبت المقترح لتوليد صور مشابهة ولكن بأسلوب مشرق وفاتح.")
st.markdown("---")

# تم التعديل هنا: إضافة دعم لصيغة webp التي استخدمتها
uploaded_file = st.file_uploader("اختر صورة للتحليل...", type=["jpg", "jpeg", "png", "webp"])

# ==========================================
# 3. المنطق الخلفي للأداة (Backend Logic)
# ==========================================
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # تم التعديل هنا: استخدام الخاصية الجديدة لتجنب رسالة التحذير
    st.image(image, caption='الصورة المرفوعة', use_container_width=True)
    
    st.markdown("---")
    
    if st.button("تحويل الصورة إلى برومبت"):
        with st.spinner('جاري تحليل الصورة وصياغة البرومبت... يرجى الانتظار.'):
            try:
                # معالجة احترافية للصورة لتتوافق دائماً مع جوجل مهما كانت صيغتها
                img_bytes = io.BytesIO()
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                
                image.save(img_bytes, format='JPEG')
                img_parts = [
                    {
                        "mime_type": "image/jpeg",
                        "data": img_bytes.getvalue()
                    }
                ]

                # الأمر الخفي: يضمن لك دائماً صوراً فاتحة الألوان ومشرقة وخالية من الظلال الداكنة
                system_instruction = (
                    "Analyze the provided image in detail. Your task is to generate a detailed prompt in English "
                    "that could be used by an AI image generator to create a SIMILAR image. "
                    "HOWEVER, you must apply a specific style transform: make the output image EXTREMELY BRIGHT, "
                    "AIRY, AND HIGH-KEY. "
                    "\n\nInstructions for the prompt composition:\n"
                    "1. Subject: Clearly describe the main subject and composition of the original image.\n"
                    "2. Lighting: Mandatorily specify over-the-top, brilliant, bright studio or natural lighting. "
                    "There must be ZERO dark shadows or strong contrasts.\n"
                    "3. Color Palette: Focus on soft, pastel, light, or vibrant washed-out colors. Eliminate "
                    "dark colors (blacks, deep browns, dark blues).\n"
                    "4. Atmosphere: Describe a cheerful, positive, clear, and dreamy atmosphere.\n"
                    "5. Specific Quality Keywords: Include terms like '8k, ultra-detailed, photorealistic, high-key lighting, "
                    "soft shadows, brilliant exposure, clean background'.\n"
                    "\nProvide only the final English prompt ready for copying."
                )

                response = model.generate_content([system_instruction, img_parts[0]])
                generated_prompt = response.text

                st.success("تم إنشاء البرومبت بنجاح!")
                st.markdown("### 📝 البرومبت المقترح (بالإنجليزية):")
                st.text_area("انسخ هذا النص واستخدمه في مولدات الصور:", value=generated_prompt, height=200)
                st.info("ملاحظة: هذا البرومبت مصمم لإنشاء صورة مشابهة لمحتوى صورتك ولكن بأسلوب ساطع ومشرق للغاية.")

            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء تحليل الصورة. تفاصيل الخطأ: {e}")

st.markdown("---")
st.caption("تم تطوير هذه الأداة باستخدام Gemini و Streamlit.")