import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

# Font yükleme yardımcısı
def get_f(name, size):
    try:
        # GitHub'a yüklediğin dosya yolunu kontrol eder
        return ImageFont.truetype(name, size)
    except:
        # Dosya bulunamazsa hata vermemesi için varsayılanı yükler
        return ImageFont.load_default()

st.set_page_config(page_title="EAGLE22 Studio", layout="wide")
st.title("🦅 EAGLE22 Pro Cover & CC Studio")

# Kullanıcı Girişleri
col1, col2 = st.columns(2)
with col1:
    p_name = st.text_input("Oyuncu İsmi:", "RAFA SILVA")
    m_info = st.text_input("Maç Bilgisi:", "VS FENERBAHÇE")
    u_text = st.text_input("Üst Yazı:", "2025/26 UPSCALED COMP")
with col2:
    duration = st.text_input("Süre:", "7 MINUTES")
    cc_val = st.slider("CC Keskinlik Gücü:", 1.0, 3.0, 2.0)
    files = st.file_uploader("4 Adet Maç Fotoğrafı Seç", type=['jpg','png','jpeg'], accept_multiple_files=True)

if st.button("Cover'ı Oluştur ve CC Bas 🚀"):
    if len(files) == 4:
        # 1080x1350 (Instagram Portrait Boyutu) için tuval
        canvas = Image.new('RGB', (1080, 1350))
        
        # Fotoğrafları işle ve CC uygula
        processed_imgs = []
        for f in files:
            img = Image.open(f).convert("RGB")
            # Keskinlik artırma (CC)
            img = ImageEnhance.Sharpness(img).enhance(cc_val)
            # Hafif kontrast artırma
            img = ImageEnhance.Contrast(img).enhance(1.1)
            # Her kareyi kolaj boyutuna getir
            img = img.resize((540, 675))
            processed_imgs.append(img)
        
        # Fotoğrafları yerleştir
        canvas.paste(processed_imgs[0], (0, 0))
        canvas.paste(processed_imgs[1], (540, 0))
        canvas.paste(processed_imgs[2], (0, 675))
        canvas.paste(processed_imgs[3], (540, 675))
        
        draw = ImageDraw.Draw(canvas)
        
        # Yüklediğin fontları isimlerine göre çağırıyoruz
        f_top = get_f("Arial Narrow Bold.ttf", 55)   # Üst yazı
        f_main = get_f("Arial-bold.ttf", 95)        # Oyuncu ismi
        f_sub = get_f("ArialCEBoldItalic.ttf", 45)  # Alt detaylar

        # Yazıları tam merkeze (anchor="mm") yerleştirme
        # Üst Yazı
        draw.text((540, 640), u_text, font=f_top, fill="white", anchor="mm")
        # Oyuncu ve Maç
        draw.text((540, 740), f"{p_name.upper()} {m_info.upper()}", font=f_main, fill="white", anchor="mm")
        # Alt Bilgiler
        draw.text((350, 840), "- 4K UPSCALED -\n- EAGLE22 EXCLUSIVE -", font=f_sub, fill="white", anchor="mm")
        draw.text((750, 840), f"{duration}\nCOMP", font=f_sub, fill="white", anchor="mm")

        # Ekranda göster
        st.image(canvas, caption="Tasarımın Hazır!", use_container_width=True)
        
        # İndirme hazırlığı
        canvas.save("eagle22_cover.jpg")
        with open("eagle22_cover.jpg", "rb") as file:
            st.download_button("📥 Tasarımı Full Kalite İndir", file, "eagle22_cover.jpg", "image/jpeg")
    else:
        st.error("Lütfen tam olarak 4 adet fotoğraf seçtiğinden emin ol!") 
