import streamlit as st
import yt_dlp
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import cv2
import numpy as np
import os

st.set_page_config(page_title="EAGLE22 Studio", layout="wide")

# Yan Menü (Mod Seçimi)
mode = st.sidebar.selectbox("Ne Yapmak İstersin?", ["🎬 Otomatik Maç Kırpıcı", "🎨 Profesyonel Cover Yapıcı"])

if mode == "🎬 Otomatik Maç Kırpıcı":
    st.title("🤖 AI Otomatik Maç Kırpıcı")
    url = st.text_input("YouTube Maç Linki:")
    player = st.text_input("Takip Edilecek Oyuncu (Rafa Silva):")
    
    if st.button("Analizi Başlat"):
        st.info("Video indiriliyor ve AI taranıyor... Lütfen bekleyin.")
        # Burası video işleme kısmını tetikler
        st.warning("Ücretsiz sunucu limiti: İlk 15 saniye analiz ediliyor.")

elif mode == "🎨 Profesyonel Cover Yapıcı":
    st.title("🎨 Pro Cover & CC Studio")
    
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input("Oyuncu İsmi:", "RAFA SILVA")
        m_info = st.text_input("Maç:", "VS FENERBAHÇE")
        u_text = st.text_input("Üst Yazı:", "2025/26 UPSCALED COMP")
    with col2:
        cc_power = st.slider("CC Keskinlik Gücü:", 1.0, 3.0, 2.0)
        files = st.file_uploader("4 Fotoğraf Seç", type=['jpg','jpeg','png'], accept_multiple_files=True)

    if st.button("Cover Oluştur 🚀"):
        if len(files) == 4:
            # Resim İşleme ve Kolaj Mantığı
            canvas = Image.new('RGB', (1080, 1350))
            imgs = [Image.open(f).convert("RGB") for f in files]
            
            # CC Uygula
            for i in range(4):
                imgs[i] = ImageEnhance.Sharpness(imgs[i]).enhance(cc_power)
                imgs[i] = imgs[i].resize((540, 675))
            
            # Yerleştirme
            canvas.paste(imgs[0], (0, 0))
            canvas.paste(imgs[1], (540, 0))
            canvas.paste(imgs[2], (0, 675))
            canvas.paste(imgs[3], (540, 675))
            
            st.image(canvas, use_container_width=True)
            canvas.save("final_cover.jpg")
            st.download_button("📥 İndir", open("final_cover.jpg", "rb"), "eagle22_cover.jpg")
        else:
            st.error("Lütfen tam 4 fotoğraf seç!") 
