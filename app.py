import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import numpy as np

st.set_page_config(page_title="AI Futbol Cover Maker", layout="wide")
st.title("🎨 Profesyonel Futbol Cover & CC Maker")

# Bilgileri Alalım
col1, col2 = st.columns(2)
with col1:
    player_name = st.text_input("Oyuncu İsmi:", "MALO GUSTA")
    match_name = st.text_input("Maç:", "VS WOLVERHAMPTON")
    comp_time = st.text_input("Süre:", "7 MINUTES")
with col2:
    cc_power = st.slider("CC (Keskinlik) Gücü:", 1.0, 3.0, 1.8)
    uploaded_files = st.file_uploader("4 Adet Fotoğraf Seç", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)

def apply_cc(image, factor):
    # Keskinlik ve Kontrast (AE Mantığına En Yakın)
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(factor)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)
    return image

if st.button("Cover Oluştur 🚀"):
    if len(uploaded_files) == 4:
        imgs = [apply_cc(Image.open(f).convert("RGB"), cc_power) for f in uploaded_files]
        
        # 4'lü Kolaj Oluşturma (1080x1350 Portrait Boyutu)
        w, h = 540, 675
        canvas = Image.new('RGB', (1080, 1350))
        
        canvas.paste(imgs[0].resize((w, h)), (0, 0))
        canvas.paste(imgs[1].resize((w, h)), (w, 0))
        canvas.paste(imgs[2].resize((w, h)), (0, h))
        canvas.paste(imgs[3].resize((w, h)), (w, h))

        # Yazıları Yazma
        draw = ImageDraw.Draw(canvas)
        # Not: Font dosyası sistemde yoksa standart kullanır, sen GitHub'a .ttf fontu atabilirsin
        try:
            font_main = ImageFont.truetype("arial.ttf", 80)
            font_sub = ImageFont.truetype("arial.ttf", 40)
        except:
            font_main = ImageFont.load_default()
            font_sub = ImageFont.load_default()

        # Üst Yazı
        draw.text((540, 650), "2025/26 UPSCALED COMP", fill="white", anchor="mm")
        # Oyuncu Adı
        draw.text((540, 750), f"{player_name.upper()} {match_name.upper()}", fill="white", anchor="mm")
        # Süre
        draw.text((750, 850), f"{comp_time}\nCOMP", fill="white", anchor="mm")

        st.image(canvas, caption="Senin Yeni Cover'ın!", use_container_width=True)
        
        # İndirme Butonu
        canvas.save("cover.jpg")
        with open("cover.jpg", "rb") as file:
            st.download_button("📥 Cover'ı İndir", file, "ai_cover.jpg", "image/jpeg")
    else:
        st.error("Lütfen tam olarak 4 adet fotoğraf yükle!")
