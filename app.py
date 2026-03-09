import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

# FONT YAKALAYICI: Klasördeki fontları otomatik eşleştirir
def get_best_font(font_name, size):
    if os.path.exists(font_name):
        return ImageFont.truetype(font_name, size)
    return ImageFont.load_default()

st.set_page_config(page_title="EAGLE22 AI Studio", layout="wide")
st.title("🎬 EAGLE22 AI Cover & CC Engine")

# Girdi Paneli
with st.sidebar:
    st.header("⚙️ Ayarlar")
    p_name = st.text_input("Oyuncu İsmi:", "RAFA SILVA")
    m_info = st.text_input("Maç Bilgisi:", "VS FENERBAHÇE")
    u_text = st.text_input("Üst Yazı:", "2025/26 UPSCALED COMP")
    duration = st.text_input("Süre:", "7 MINUTES")
    cc_power = st.slider("AI CC (Keskinlik) Gücü:", 1.0, 3.5, 2.5)

st.info("Lütfen 4 adet kaliteli futbolcu fotoğrafı yükleyin.")
files = st.file_uploader("", type=['jpg','jpeg','png'], accept_multiple_files=True)

if st.button("TASARIMI OLUŞTUR 🚀"):
    if len(files) == 4:
        with st.spinner('AI Görüntüleri İşliyor ve CC Basılıyor...'):
            # 1. Tuval Oluşturma (1080x1350 Portrait)
            canvas = Image.new('RGB', (1080, 1350))
            
            # 2. Resim İşleme (CC ve Upscale)
            imgs = []
            for f in files:
                img = Image.open(f).convert("RGB")
                # CC: Keskinlik ve Kontrast Basma
                img = ImageEnhance.Sharpness(img).enhance(cc_power)
                img = ImageEnhance.Contrast(img).enhance(1.2)
                img = img.resize((540, 675), Image.Resampling.LANCZOS)
                imgs.append(img)
            
            # 3. Kolaj Yerleşimi
            canvas.paste(imgs[0], (0, 0))
            canvas.paste(imgs[1], (540, 0))
            canvas.paste(imgs[2], (0, 675))
            canvas.paste(imgs[3], (540, 675))
            
            # 4. Yazı Yazma (Profesyonel Katmanlar)
            draw = ImageDraw.Draw(canvas)
            
            # Fontları Klasörden Çek
            f_top = get_best_font("Arial Narrow Bold.ttf", 55)
            f_main = get_best_font("Arial-bold.ttf", 95)
            f_sub = get_best_font("ArialCEBoldItalic.ttf", 45)
            
            # Yazı Yerleşimleri (Merkezi Hizalama)
            # Üst Bilgi
            draw.text((540, 640), u_text, font=f_top, fill="white", anchor="mm")
            # Ana Başlık (Glow efekti için hafif gölge)
            draw.text((540, 740), f"{p_name.upper()} {m_info.upper()}", font=f_main, fill="white", anchor="mm", stroke_width=2, stroke_fill="black")
            # Alt Detaylar
            draw.text((320, 840), "- 4K UPSCALED -\n- EAGLE22 EXCLUSIVE -", font=f_sub, fill="white", anchor="mm")
            draw.text((760, 840), f"{duration}\nCOMP", font=f_sub, fill="white", anchor="mm")

            # 5. Sonuç Gösterimi
            st.image(canvas, use_container_width=True)
            
            # İndirme Butonu
            canvas.save("eagle_ai_cover.jpg", quality=95)
            with open("eagle_ai_cover.jpg", "rb") as b:
                st.download_button("📥 KUSURSUZ COVER'I İNDİR", b, "eagle22_ai_cover.jpg")
    else:
        st.error("Eksik fotoğraf! Lütfen tam 4 adet seç.")
