import time
import pandas as pd
import streamlit as st

# ==========================================
# SAYFA YAPILANDIRMASI
# ==========================================
st.set_page_config(
    page_title="Botanikte Renkler Quiz & Liderlik Tablosu",
    page_icon="🌿",
    layout="centered",
)

# ==========================================
# SESSION STATE (OTURUM) BAŞLANGICI
# ==========================================
if "stage" not in st.session_state:
  st.session_state.stage = "register"
if "name" not in st.session_state:
  st.session_state.name = ""
if "score" not in st.session_state:
  st.session_state.score = 0
if "start_time" not in st.session_state:
  st.session_state.start_time = 0.0
if "elapsed_time" not in st.session_state:
  st.session_state.elapsed_time = 0.0

# Başlangıç için örnek liderlik tablosu
if "leaderboard" not in st.session_state:
  st.session_state.leaderboard = [
      {"İsim": "Linnaeus", "Doğru Sayısı": 5, "Süre (sn)": 14.2},
      {"İsim": "Darwin", "Doğru Sayısı": 4, "Süre (sn)": 11.0},
      {"İsim": "Mendel", "Doğru Sayısı": 3, "Süre (sn)": 9.5},
  ]

# ==========================================
# 1. ADIM: KAYIT VE SÜRE BAŞLANGICI
# ==========================================
if st.session_state.stage == "register":
  st.title("🌿 Latince Botanik Renkleri Quiz'i")
  st.markdown(
      "Botanik adlandırmalarındaki renk terimlerini ne kadar iyi biliyorsun?"
      " Sorular **teker teker** sorulacak ve bitirdiğin an **süren"
      " hesaplanarak** liderlik tablosuna işlenecektir!"
  )

  with st.form("reg_form"):
    name_input = st.text_input(
        "Adınız Soyadınız:", placeholder="Örn: Karl Linnaeus"
    )
    submitted = st.form_submit_button("Quiz'i Başlat 🚀")

    if submitted:
      if not name_input.strip():
        st.warning("Lütfen adınızı girin!")
      else:
        st.session_state.name = name_input.strip()
        st.session_state.score = 0
        st.session_state.start_time = (
            time.time()
        )  # Kronometreyi buradan başlatıyoruz!
        st.session_state.stage = "q1"
        st.rerun()

# ==========================================
# 2. ADIM: SORULAR (TEKER TEKER)
# ==========================================

# Soru 1
elif st.session_state.stage == "q1":
  st.header("Soru 1 / 5")
  st.info(
      "Latince botanik terimlerinde **'Albus'** kelimesi hangi rengi ifade"
      " eder?"
  )

  with st.form("q1_form"):
    ans = st.radio(
        "Seçiniz:",
        ["Siyah (Niger)", "Beyaz (Albus)", "Kırmızı (Ruber)", "Sarı (Luteus)"],
    )
    btn = st.form_submit_button("Sonraki Soru ➡️")
    if btn:
      if "Beyaz" in ans:
        st.session_state.score += 1
      st.session_state.stage = "q2"
      st.rerun()

# Soru 2
elif st.session_state.stage == "q2":
  st.header("Soru 2 / 5")
  st.info(
      "Latince botanik adlandırmalarında **'Viridis'** terimi ne anlama gelir?"
  )

  with st.form("q2_form"):
    ans = st.radio(
        "Seçiniz:",
        [
            "Mavi (Caeruleus)",
            "Yeşil (Viridis)",
            "Kahverengi (Fuscus)",
            "Altın sarısı (Aureus)",
        ],
    )
    btn = st.form_submit_button("Sonraki Soru ➡️")
    if btn:
      if "Yeşil" in ans:
        st.session_state.score += 1
      st.session_state.stage = "q3"
      st.rerun()

# Soru 3
elif st.session_state.stage == "q3":
  st.header("Soru 3 / 5")
  st.info(
      "Bir bitki tanımında **'Ruber'** sıfatı geçiyorsa, bu bitkinin hangi rengi"
      " barındırdığı anlaşılır?"
  )

  with st.form("q3_form"):
    ans = st.radio(
        "Seçiniz:",
        ["Mor (Purpureus)", "Kırmızı (Ruber)", "Pembe (Roseus)", "Gri (Canus)"],
    )
    btn = st.form_submit_button("Sonraki Soru ➡️")
    if btn:
      if "Kırmızı" in ans:
        st.session_state.score += 1
      st.session_state.stage = "q4"
      st.rerun()

# Soru 4
elif st.session_state.stage == "q4":
  st.header("Soru 4 / 5")
  st.info("Botanik latincesinde **'Luteus'** terimi hangi rengin karşılığıdır?")

  with st.form("q4_form"):
    ans = st.radio(
        "Seçiniz:",
        ["Sarı (Luteus)", "Turuncu (Aurantiacus)", "Mavi", "Beyaz"],
    )
    btn = st.form_submit_button("Sonraki Soru ➡️")
    if btn:
      if "Sarı" in ans:
        st.session_state.score += 1
      st.session_state.stage = "q5"
      st.rerun()

# Soru 5
elif st.session_state.stage == "q5":
  st.header("Soru 5 / 5")
  st.info("Latince botanik renk terimlerinden **'Niger'** neyi ifade eder?")

  with st.form("q5_form"):
    ans = st.radio(
        "Seçiniz:", ["Siyah (Niger)", "Koyu Yeşil", "Gümüşi", "Parlak Sarı"]
    )
    btn = st.form_submit_button("Testi Bitir ve Skoru Gör 🎯")
    if btn:
      if "Siyah" in ans:
        st.session_state.score += 1

      # Süreyi hesapla (Başlangıç anı ile şimdi arasındaki fark)
      end_time = time.time()
      st.session_state.elapsed_time = round(
          end_time - st.session_state.start_time, 2
      )

      # Sonucu liderlik tablosuna ekle
      st.session_state.leaderboard.append({
          "İsim": st.session_state.name,
          "Doğru Sayısı": st.session_state.score,
          "Süre (sn)": st.session_state.elapsed_time,
      })

      st.session_state.stage = "result"
      st.rerun()

# ==========================================
# 3. ADIM: SONUÇ VE AKILLI LİDERLİK TABLOSU
# ==========================================
elif st.session_state.stage == "result":
  st.title("🏆 Quiz Sonucu & Liderlik Tablosu")

  col1, col2 = st.columns(2)
  with col1:
    st.metric(label="Doğru Sayın", value=f"{st.session_state.score} / 5")
  with col2:
    st.metric(
        label="Tamamlama Süren",
        value=f"{st.session_state.elapsed_time} saniye",
    )

  if st.session_state.score == 5:
    st.success(
        "Mükemmel! Tüm botanik renk terimlerini kusursuz bildin! 🌿🌟"
    )
  else:
    st.info("Tebrikler! Liderlik tablosundaki yerini aldın. 👍")

  st.divider()
  st.subheader("🌟 En İyi Botanistler (Liderlik Tablosu)")
  st.markdown(
      "📌 *Sıralama Mantığı:* Önce **en yüksek doğru sayısı**, puanlar eşitse"
      " **en kısa süre (saniye)** dikkate alınır."
  )

  # DataFrame oluştur ve akıllı sıralama yap: Doğru Sayısı (azalan), Süre (artan)
  df_lb = pd.DataFrame(st.session_state.leaderboard)
  df_lb = df_lb.sort_values(
      by=["Doğru Sayısı", "Süre (sn)"], ascending=[False, True]
  ).reset_index(drop=True)

  # Liderlik tablosunu ekrana yazdır
  st.dataframe(df_lb, use_container_width=True)

  st.divider()
  if st.button("Yeniden Oyna 🔄"):
    st.session_state.stage = "register"
    st.rerun()
