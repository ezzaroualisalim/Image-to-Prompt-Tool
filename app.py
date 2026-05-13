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
# إعدادات الصفحة وتنسيق السيو البصري (RTL & Vibrant CSS)
# ==========================================
st.set_page_config(page_title="مُحول الصورة إلى برومبت الذكي", layout="centered")

# تنسيق CSS متطور لجعل الخطوط عريضة، ملونة، وواضحة جداً
visual_seo_css = """
<style>
    /* الإعدادات العامة للخط والاتجاه */
    .stApp { 
        direction: rtl; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 18px; /* تكبير الخط العام */
        color: #2c3e50;
    }
    
    /* تنسيق العناوين الرئيسية في المقالة */
    .article-title {
        color: #003791 !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        text-align: center !important;
        margin-bottom: 30px !important;
        border-bottom: 4px solid #003791;
        padding-bottom: 10px;
    }

    /* تنسيق العناوين الفرعية */
    .article-h2 {
        color: #e67e22 !important; /* لون برتقالي زاهي مختلف تماماً */
        font-size: 26px !important;
        font-weight: 800 !important;
        margin-top: 35px !important;
        border-right: 8px solid #e67e22;
        padding-right: 15px;
    }

    /* تنسيق النصوص العادية */
    .article-p {
        font-size: 20px !important;
        line-height: 1.8 !important;
        color: #444444 !important;
        text-align: justify !important;
        font-weight: 500 !important;
    }

    /* تنسيق القوائم النقطية */
    .article-li {
        font-size: 19px !important;
        color: #2c3e50 !important;
        margin-bottom: 10px !important;
        font-weight: 600 !important;
    }

    /* إصلاح أيقونات التنبيهات */
    div[data-testid="stAlert"] { display: flex; flex-direction: row-reverse; text-align: right; }
    
    /* حماية صندوق البرومبت الإنجليزي ليبقى واضحاً */
    textarea { 
        direction: ltr !important; 
        text-align: left !important; 
        font-size: 16px !important;
        font-weight: bold !important;
        color: #1e8449 !important; /* لون أخضر للبرومبت */
    }

    /* تجميل التبويبات */
    button[data-baseweb="tab"] {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #34495e !important;
    }
</style>
"""
st.markdown(visual_seo_css, unsafe_allow_html=True)

# ==========================================
# إنشاء علامات التبويب (Tabs)
# ==========================================
tab_tool, tab_article = st.tabs(["🛠️ أداة الهندسة العكسية", "📖 دليلك الشامل (المقالة)"])

# ------------------------------------------
# التبويبة الأولى: الأداة
# ------------------------------------------
with tab_tool:
    st.markdown("<h1 style='text-align: center;'>🖼️ أداة الهندسة العكسية</h1>", unsafe_allow_html=True)
    st.write("ارفع أي صورة، اختر النمط الفني، وسنحولها إلى برومبت احترافي.")
    
    uploaded_file = st.file_uploader("اختر صورة للتحليل...", type=["jpg", "jpeg", "png", "webp"])
    
    styles_list = [
        "واقعي ومشرق (Photorealistic & Vibrant)", "إضاءة سينمائية (Cinematic & Dramatic)",
        "تصميم ثلاثي الأبعاد (3D Digital Art)", "أحادي اللون (Monochrome)",
        "رسم زيتي (Oil Painting)", "ستيم بانك (Steampunk)", "كارتون كلاسيكي (Old Cartoon)"
    ]
    selected_style = st.selectbox("🎨 اختر النمط الفني:", styles_list)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        
        if st.button("✨ توليد البرومبت الآن"):
            with st.spinner('جاري التحليل...'):
                try:
                    img_bytes = io.BytesIO()
                    if image.mode in ("RGBA", "P"): image = image.convert("RGB")
                    image.save(img_bytes, format='JPEG')
                    img_parts = [{"mime_type": "image/jpeg", "data": img_bytes.getvalue()}]
                    
                    system_instruction = f"Generate a detailed image prompt for: {selected_style}"
                    response = model.generate_content([system_instruction, img_parts[0]])
                    
                    st.success("تم التوليد بنجاح!")
                    st.text_area("البرومبت الناتج:", value=response.text.strip(), height=150)
                except Exception as e:
                    st.error(f"خطأ: {e}")

# ------------------------------------------
# التبويبة الثانية: المقالة (بتنسيق السيو البصري)
# ------------------------------------------
with tab_article:
    # استخدام HTML مباشرة لضمان تطبيق الألوان والخطوط العريضة
    st.markdown('<h1 class="article-title">أداة تحويل الصورة إلى برومبت (Image to Prompt): دليلك الشامل</h1>', unsafe_allow_html=True)
    
    st.markdown('<p class="article-p">في عصر تطور الذكاء الاصطناعي التوليدي، أصبحت أدوات توليد الصور جزءاً لا يتجزأ من ترسانة المبدعين. ولكن العقبة هي: <b>كيف تكتب الوصف الدقيق؟</b></p>', unsafe_allow_html=True)

    st.markdown('<h2 class="article-h2">🔍 ما هي تقنية الهندسة العكسية للصور؟</h2>', unsafe_allow_html=True)
    st.markdown('<p class="article-p">هي عملية تقنية تعتمد على تحليل صورة موجودة بالفعل وتفكيك عناصرها المرئية لإعادة صياغتها كـ نص (Prompt). الأداة تقرأ:</p>', unsafe_allow_html=True)
    
    st.markdown('<li class="article-li">🎯 الموضوع الأساسي (Subject)</li>', unsafe_allow_html=True)
    st.markdown('<li class="article-li">💡 البيئة والإضاءة (Lighting)</li>', unsafe_allow_html=True)
    st.markdown('<li class="article-li">🎨 الأسلوب الفني (Art Style)</li>', unsafe_allow_html=True)

    st.markdown('<h2 class="article-h2">🚀 كيف تستخدم البرومبت بأفضل طريقة؟</h2>', unsafe_allow_html=True)
    st.markdown('<p class="article-p">بمجرد نسخ البرومبت، ننصحك بالتعديل اليدوي الطفيف، تحديد الأبعاد (Aspect Ratio)، واستخدام النماذج الحديثة لضمان أفضل النتائج.</p>', unsafe_allow_html=True)

    st.info("💡 نصيحة: استخدم خيار 'إضاءة سينمائية' للحصول على نتائج مبهرة في مدونتك التقنية.")
