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

rtl_css = """
<style>
    /* الإعدادات العامة للاتجاه */
    .stApp { direction: rtl; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    p, div, h1, h2, h3, h4, h5, h6, label, span, li { text-align: right !important; }
    div[data-testid="stAlert"] { display: flex; flex-direction: row-reverse; text-align: right; }
    div[data-testid="stFileUploader"] { direction: rtl; text-align: right; }
    textarea { direction: ltr !important; text-align: left !important; font-family: monospace; }
    
    /* ==================================================== */
    /* السحر هنا: تكبير وتلوين خط التبويبات (Tabs) بشكل بارز */
    /* ==================================================== */
    button[data-baseweb="tab"] { 
        font-size: 22px !important;       /* تكبير الخط بشكل ملحوظ */
        font-weight: 900 !important;      /* جعل الخط عريض جداً */
        color: #003791 !important;        /* لون أزرق داكن احترافي */
        padding: 15px 25px !important;    /* زيادة المساحة حول النص */
    }
    
    /* لون التبويبة عندما تكون مفتوحة (نشطة) */
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #e67e22 !important;        /* لون برتقالي زاهي */
        border-bottom: 4px solid #e67e22 !important; /* خط تحتي سميك */
    }
</style>
"""
st.markdown(rtl_css, unsafe_allow_html=True)

# ==========================================
# إنشاء علامات التبويب (Tabs)
# ==========================================
tab_tool, tab_article = st.tabs(["🛠️ أداة الهندسة العكسية", "📖 دليلك الشامل (المقالة)"])

# ------------------------------------------
# التبويبة الأولى: الأداة
# ------------------------------------------
with tab_tool:
    st.title("🖼️ أداة الهندسة العكسية للصور الفنية")
    st.subheader("ارفع أي صورة، اختر النمط الفني، وسنحولها إلى برومبت احترافي جاهز للاستخدام.")
    st.markdown("---")

    uploaded_file = st.file_uploader("اختر صورة للتحليل...", type=["jpg", "jpeg", "png", "webp"])

    st.markdown("### 🎨 اختر النمط الفني للبرومبت:")
    styles_list = [
        "واقعي ومشرق (Photorealistic & Vibrant)", "إضاءة سينمائية (Cinematic & Dramatic)",
        "تصميم ثلاثي الأبعاد (3D Digital Art)", "أحادي اللون (Monochrome)",
        "كتل الألوان (Color Block / Bloc de couleurs)", "عرض أزياء (Catwalk)",
        "طباعة ريزوغراف (Risograph)", "تكنيكولور (Technicolor)", "تمثال قوطي (Gothic Figurine)",
        "ديناميت / طاقة متفجرة (Dynamite)", "صالون كلاسيكي (Salon)", "رسم يدوي (Drawing / Dessin)",
        "ستيم بانك (Steampunk)", "شروق الشمس (Sunrise / Lever du soleil)",
        "مقاتل أسطوري (Mythical Fighter)", "سريالي (Surrealist)", "غموض (Mystery)",
        "دبوس مطلي بالمينا (Enamel Pin)", "سايبورغ / آلي (Cyborg)", "بورتريه ناعم (Soft Portrait)",
        "كارتون كلاسيكي (Old Cartoon)", "رسم زيتي (Oil Painting)"
    ]
    selected_style = st.selectbox("اضغط هنا لاختيار النمط:", styles_list)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='الصورة المرفوعة', use_container_width=True)
        st.markdown("---")
        
        if st.button(f"✨ توليد برومبت بأسلوب: {selected_style.split('(')[0].strip()}"):
            with st.spinner('جاري تحليل الصورة وصياغة البرومبت... يرجى الانتظار.'):
                try:
                    img_bytes = io.BytesIO()
                    if image.mode in ("RGBA", "P"): image = image.convert("RGB")
                    image.save(img_bytes, format='JPEG')
                    img_parts = [{"mime_type": "image/jpeg", "data": img_bytes.getvalue()}]

                    system_instruction = f"""
                    Analyze the provided image in detail. Your task is to generate ONE highly detailed prompt in English 
                    that could be used by an AI image generator to create a SIMILAR image, but it MUST strictly adopt the following visual style:
                    TARGET STYLE: {selected_style}
                    Instructions for the prompt composition:
                    1. Subject & Action: Clearly describe the main subjects, composition, and actions of the original image.
                    2. Style Application: Heavily integrate aesthetic keywords, lighting, and textures that match the TARGET STYLE exactly.
                    3. Precision: Include high-quality modifiers relevant to the style.
                    4. Output constraints: Provide ONLY the final English prompt ready for copying.
                    """

                    response = model.generate_content([system_instruction, img_parts[0]])
                    generated_prompt = response.text.strip()

                    st.success("تم إنشاء البرومبت بنجاح!")
                    st.markdown("### 📝 البرومبت المقترح (بالإنجليزية):")
                    st.text_area("انسخ هذا النص واستخدمه في مولدات الصور:", value=generated_prompt, height=200)

                except Exception as e:
                    st.error(f"عذراً، حدث خطأ أثناء التحليل. تفاصيل الخطأ: {e}")

# ------------------------------------------
# التبويبة الثانية: المقالة (تم استرجاع النص الأصلي الجميل)
# ------------------------------------------
with tab_article:
    st.markdown("""
    # أداة تحويل الصورة إلى برومبت (Image to Prompt): دليلك الشامل للهندسة العكسية للصور

    في عصر تطور الذكاء الاصطناعي التوليدي، أصبحت أدوات توليد الصور مثل Midjourney، و DALL-E 3، و Gemini، جزءاً لا يتجزأ من ترسانة أي صانع محتوى، مصمم، أو مسوق رقمي. ولكن، يواجه الكثيرون عقبة رئيسية: **كيف أكتب الوصف (البرومبت) الدقيق الذي يعطيني النتيجة التي أتخيلها؟**

    هنا تبرز الحاجة الماسة إلى تقنية "الهندسة العكسية للصور" (Reverse Prompt Engineering). ولحل هذه المشكلة المعقدة، يسعدنا أن نقدم لكم أداة تحويل الصورة إلى برومبت (Image to Prompt) المجانية والاحترافية.

    ---
    ### 🔍 ما هي تقنية الهندسة العكسية للصور (Reverse Prompting)؟
    الهندسة العكسية للصور هي عملية تقنية تعتمد على استخدام نماذج الرؤية الحاسوبية (Computer Vision) والذكاء الاصطناعي المتقدم لتحليل صورة موجودة بالفعل، وتفكيك عناصرها المرئية، ثم إعادة صياغتها في شكل نص مكتوب (Prompt).

    بدلاً من المحاولة والخطأ، تقوم الأداة بقراءة:
    * **الموضوع الأساسي (Subject):** الأشخاص، الحيوانات، المباني، أو الأشياء.
    * **البيئة والإضاءة (Environment & Lighting):** إضاءة سينمائية، شمس ساطعة، ظلال عميقة، أو إضاءة استوديو.
    * **الأسلوب الفني (Art Style):** رسم زيتي، تصميم ثلاثي الأبعاد، أو صورة فوتوغرافية واقعية.
    * **التفاصيل الدقيقة (Modifiers):** دقة 8K، عدسة ماكرو، أو تأثير البوكيه (Bokeh).

    ---
    ### 💡 لماذا تحتاج إلى استخدام هذه الأداة؟
    * **التغلب على حاجز الكتابة (Writer’s Block):** تمنحك الأداة نقطة انطلاق مثالية.
    * **توفير الوقت والجهد:** تمنحك وصفاً دقيقاً ومُجرباً يضمن لك نسبة نجاح أعلى.
    * **تعلم هندسة الأوامر (Prompt Engineering):** ستتعلم تدريجياً المصطلحات الفنية والكلمات المفتاحية السرية.
    * **تجنب حقوق الملكية:** استخراج البرومبت وتوليد صورة مشابهة في الروح ولكنها أصلية 100%.

    ---
     🎨 الأنماط الفنية المتاحة في الأداة (Art Styles):
    * **الواقعية المشرقة (Photorealistic):** لصور تبدو وكأنها التقطت بكاميرا احترافية حقيقية.
    * **الإضاءة السينمائية (Cinematic):** لصور درامية ذات تباين عالي تناسب البوسترات والأغلفة.
    * **التصميم ثلاثي الأبعاد (3D Digital Art):** لأسلوب مشابه لألعاب الفيديو وتصاميم "Unreal Engine".
    * **الرسم الزيتي (Oil Painting):** لتحويل صورتك إلى لوحة كلاسيكية بفرشاة فنية.
    * **أسلوب الستيم بانك (Steampunk):** لدمج التكنولوجيا البخارية القديمة مع الخيال العلمي.

    ---
    🚀 كيف تستخدم البرومبت المستخرج بأفضل طريقة؟
    1. **التعديل اليدوي الطفيف:** اقرأ البرومبت المستخرج. يمكنك حذف أي كلمة لا تناسب رؤيتك، أو إضافة تفاصيل خاصة بك.
    2. **تحديد الأبعاد (Aspect Ratio):** أدوات التوليد تحتاج إلى معرفة أبعاد الصورة. أضف في نهاية البرومبت عوامل مثل `--ar 16:9` للصور العرضية أو `--ar 9:16` للصور الطولية.
    3. **استخدام النماذج المناسبة:** هذا البرومبت تم تحسينه ليعمل بكفاءة مذهلة مع محركات مثل Midjourney v6، DALL-E 3، ونماذج الجيل الجديد.

    ---
    **الخلاصة:**
    باستخدام أداة تحويل الصورة إلى برومبت، أصبح بإمكانك ترجمة أي إلهام بصري تقع عليه عيناك إلى أوامر دقيقة يفهمها الذكاء الاصطناعي. عد للتبويبة الأولى، جرب الأداة الآن، وأطلق العنان لإبداعك المرئي!
    """)
