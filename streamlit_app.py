import time
import pandas as pd
import streamlit as st

# ==========================================
# SAYFA YAPILANDIRMASI
# ==========================================
st.set_page_config(
    page_title="Botanikte Latince Renkler Quiz & Liderlik Tablosu",
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

# Örnek liderlik tablosu
if "leaderboard" not in st.session_state:
  st.session_state.leaderboard = [
      {"İsim": "Linnaeus", "Doğru Sayısı": 5, "Süre (sn)": 11.2},
      {"İsim": "Darwin", "Doğru Sayısı": 4, "Süre (sn)": 9.5},
      {"İsim": "Mendel", "Doğru Sayısı": 3, "Süre (sn)": 7.1},
  ]

# ==========================================
# 1. ADIM: KAYIT VE KRONOMETRE BAŞLANGICI
# ==========================================
if st.session_state.stage == "register":
  st.title("🌿 Latince Botanik Renkleri Quiz'i")
  st.markdown(
      "Metindeki Latince renk terimlerini ve örnek bitki özelliklerini ne kadar"
      " iyi anladığını test et! Sorular **teker teker** sorulacak, süren"
      " tutulacak ve sonuçlar liderlik tablosuna işlenecektir."
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
        )  # Kronometreyi buradan başlatıyoruz
        st.session_state.stage = "q1"
        st.rerun()

# ==========================================
# 2. ADIM: SORULAR (TEKER TEKER)
# ==========================================

# Soru 1: Albus
elif st.session_state.stage == "q1":
  st.header("Soru 1 / 5")
  st.info(
      "Latince botanik terimlerinde **'Albus'** kelimesi hangi rengi ifade"
      " eder?"
  )

  with st.form("q1_form"):
    ans = st.radio("Seçiniz:", ["Siyah", "Beyaz", "Kırmızı", "Sarı"])
    btn = st.form_submit_button("Sonraki Soru ➡️")
    if btn:
      if ans == "Beyaz":
        st.session_state.score += 1
      st.session_state.stage = "q2"
      st.rerun()

# Soru 2: Viridis
elif st.session_state.stage == "q2":
  st.header("Soru 2 / 5")
  st.info(
      "Botanik adlandırmalarında **'Viridis'** terimi hangi anlama gelir?"
  )

  with st.form("q2_form"):
    ans = st.radio("Seçiniz:", ["Mavi", "Yeşil", "Kahverengi", "Altın rengi"])
    btn = st.form_submit_button("Sonraki Soru ➡️")
    if btn:
      if ans == "Yeşil":
        st.session_state.score += 1
      st.session_state.stage = "q3"
      st.rerun()

# Soru 3: Rubra / Ruber
elif st.session_state.stage == "q3":
  st.header("Soru 3 / 5")
  st.info(
      "Bir bitki tanımında **'Rubra'** veya **'Ruber'** sıfatı geçiyorsa,"
      " bu bitkinin hangi rengi barındırdığı anlaşılır?"
  )

  with st.form("q3_form"):
    ans = st.radio("Seçiniz:", ["Mor", "Kırmızı", "Pembe", "Gri"])
    btn = st.form_submit_button("Sonraki Soru ➡️")
    if btn:
      if ans == "Kırmızı":
        st.session_state.score += 1
      st.session_state.stage = "q4"
      st.rerun()

# Soru 4: Aureus / Aurea
elif st.session_state.stage == "q4":
  st.header("Soru 4 / 5")
  st.info(
      "Botanik latincesinde **'Aureus'** veya **'Aurea'** terimi hangi"
      " rengin karşılığıdır?"
  )

  with st.form("q4_form"):
    ans = st.radio("Seçiniz:", ["Sarı", "Altın rengi", "Gümüş rengi", "Mavi"])
    btn = st.form_submit_button("Sonraki Soru ➡️")
    if btn:
      if ans == "Altın rengi":
        st.session_state.score += 1
      st.session_state.stage = "q5"
      st.rerun()

# Soru 5: Örnek Bitki (Rosa alba)
elif st.session_state.stage == "q5":
  st.header("Soru 5 / 5")
  st.info(
      "Metindeki örneklerden hareketle, **'Rosa alba'** bitki adındaki"
      " *alba* kelimesi bu türe ait hangi özelliği belirtir?"
  )

  with st.form("q5_form"):
    ans = st.radio(
        "Seçiniz:",
        ["Beyaz çiçek", "Kırmızı meyve", "Dikenli gövde", "Mor yaprak"],
    )
    btn = st.form_submit_button("Testi Bitir ve Skoru Gör 🎯")
    if btn:
      if ans == "Beyaz çiçek":
        st.session_state.score += 1

      # Kronometreyi durdur ve süreyi hesapla
      end_time = time.time()
      st.session_state.elapsed_time = round(
          end_time - st.session_state.start_time, 2
      )

      # Liderlik tablosuna kaydet
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
    st.success("Mükemmel! Latince renk terimlerini kusursuz bildin! 🌿🌟")
  else:
    st.info("Tebrikler! Liderlik tablosundaki yerini aldın. 👍")

  st.divider()
  st.subheader("🌟 En İyi Botanistler (Liderlik Tablosu)")
  st.markdown(
      "📌 *Sıralama Kuralı:* Önce **en yüksek doğru sayısı**, puanlar eşitse"
      " **en kısa süre (saniye)** önceliklidir."
  )

  # DataFrame sıralaması: Doğru Sayısı (azalan), Süre (artan)
  df_lb = pd.DataFrame(st.session_state.leaderboard)
  df_lb = df_lb.sort_values(
      by=["Doğru Sayısı", "Süre (sn)"], ascending=[False, True]
  ).reset_index(drop=True)

  st.dataframe(df_lb, use_container_width=True)

  st.divider()
  if st.button("Yeniden Oyna 🔄"):
    st.session_state.stage = "register"
    st.rerun()
