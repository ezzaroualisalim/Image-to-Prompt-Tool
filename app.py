import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# جلب المفتاح السري بأمان
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# استخدام النموذج السريع
model = genai.GenerativeModel('gemini-2.5-flash')

# ==========================================
# إعدادات الصفحة و (RTL CSS)
# ==========================================
st.set_page_config(page_title="مُحول الصورة إلى برومبت الذكي", layout="centered")

# كود CSS السحري لجعل الواجهة عربية احترافية بدون تشوه
rtl_css = """
<style>
    /* جعل الاتجاه العام من اليمين لليسار */
    .stApp {
        direction: rtl;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* محاذاة جميع النصوص لليمين */
    p, div, h1, h2, h3, h4, h5, h6, label, span {
        text-align: right !important;
    }

    /* إصلاح أيقونات التنبيهات (النجاح، الخطأ، الملاحظات) لتظهر على اليمين بشكل صحيح */
    div[data-testid="stAlert"] {
        display: flex;
        flex-direction: row-reverse;
        text-align: right;
    }
    
    /* إصلاح زر رفع الملفات */
    div[data-testid="stFileUploader"] {
        direction: rtl;
        text-align: right;
    }

    /* استثناء مربع النص الذي يظهر فيه البرومبت الإنجليزي ليبقى من اليسار لليمين */
    textarea {
        direction: ltr !important;
        text-align: left !important;
        font-family: monospace;
    }
</style>
"""
# تفعيل كود الـ CSS في الواجهة
st.markdown(rtl_css, unsafe_allow_html=True)

# ==========================================
# تصميم واجهة المستخدم (UI Design)
# ==========================================
st.title("🖼️ أداة الهندسة العكسية للصور الفنية")
st.subheader("ارفع أي صورة، اختر النمط الفني، وسنحولها إلى برومبت احترافي جاهز للاستخدام.")
st.markdown("---")

# رفع الصورة
uploaded_file = st.file_uploader("اختر صورة للتحليل...", type=["jpg", "jpeg", "png", "webp"])

# ==========================================
# قائمة الخيارات الفنية (Dropdown Menu)
# ==========================================
st.markdown("### 🎨 اختر النمط الفني للبرومبت:")

styles_list = [
    "واقعي ومشرق (Photorealistic & Vibrant)",
    "إضاءة سينمائية (Cinematic & Dramatic)",
    "تصميم ثلاثي الأبعاد (3D Digital Art)",
    "أحادي اللون (Monochrome)",
    "كتل الألوان (Color Block / Bloc de couleurs)",
    "عرض أزياء (Catwalk)",
    "طباعة ريزوغراف (Risograph)",
    "تكنيكولور (Technicolor)",
    "تمثال قوطي (Gothic Figurine)",
    "ديناميت / طاقة متفجرة (Dynamite)",
    "صالون كلاسيكي (Salon)",
    "رسم يدوي (Drawing / Dessin)",
    "ستيم بانك (Steampunk)",
    "شروق الشمس (Sunrise / Lever du soleil)",
    "مقاتل أسطوري (Mythical Fighter)",
    "سريالي (Surrealist)",
    "غموض (Mystery)",
    "دبوس مطلي بالمينا (Enamel Pin)",
    "سايبورغ / آلي (Cyborg)",
    "بورتريه ناعم (Soft Portrait)",
    "كارتون كلاسيكي (Old Cartoon)",
    "رسم زيتي (Oil Painting)"
]

# عنصر القائمة المنسدلة ليختار منه المستخدم
selected_style = st.selectbox("اضغط هنا لاختيار النمط:", styles_list)

# ==========================================
# المنطق الخلفي للأداة (Backend Logic)
# ==========================================
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='الصورة المرفوعة', use_container_width=True)
    st.markdown("---")
    
    # الزر التفاعلي الذي يوضح النمط المختار
    if st.button(f"✨ توليد برومبت بأسلوب: {selected_style.split('(')[0].strip()}"):
        with st.spinner('جاري تحليل الصورة وصياغة البرومبت... يرجى الانتظار.'):
            try:
                img_bytes = io.BytesIO()
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                
                image.save(img_bytes, format='JPEG')
                img_parts = [{"mime_type": "image/jpeg", "data": img_bytes.getvalue()}]

                # الأمر الخفي الديناميكي
                system_instruction = f"""
                Analyze the provided image in detail. Your task is to generate ONE highly detailed prompt in English 
                that could be used by an AI image generator to create a SIMILAR image, but it MUST strictly adopt the following visual style:
                
                TARGET STYLE: {selected_style}
                
                Instructions for the prompt composition:
                1. Subject & Action: Clearly describe the main subjects, composition, and actions of the original image.
                2. Style Application: Heavily integrate aesthetic keywords, lighting, and textures that match the TARGET STYLE exactly.
                3. Precision: Include high-quality modifiers relevant to the style (e.g., '8k, highly detailed' for photorealism, 'brushstrokes' for oil painting, etc.).
                4. Output constraints: Provide ONLY the final English prompt ready for copying. Do not include introductory text, markdown formatting, or explanations.
                """

                response = model.generate_content([system_instruction, img_parts[0]])
                generated_prompt = response.text.strip()

                st.success("تم إنشاء البرومبت بنجاح!")
                st.markdown("### 📝 البرومبت المقترح (بالإنجليزية):")
                # هذا المربع سيبقى إنجليزياً بفضل كود CSS لحماية النص
                st.text_area("انسخ هذا النص واستخدمه في مولدات الصور:", value=generated_prompt, height=200)

            except Exception as e:
                st.error(f"عذراً، حدث خطأ أثناء التحليل. تفاصيل الخطأ: {e}")

st.markdown("---")
