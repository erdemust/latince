import datetime
import pandas as pd
import streamlit as st

# ==========================================
# SAYFA YAPILANDIRMASI
# ==========================================
st.set_page_config(
    page_title="Quiz & Liderlik Tablosu", page_icon="🏆", layout="centered"
)

# ==========================================
# SESSION STATE BAŞLANGICI
# ==========================================
if "quiz_stage" not in st.session_state:
  st.session_state.quiz_stage = "register"
if "name" not in st.session_state:
  st.session_state.name = ""
if "score" not in st.session_state:
  st.session_state.score = 0
if "recorded" not in st.session_state:
  st.session_state.recorded = False

# Varsayılan örnek liderlik tablosu (İlk açılışta boş görünmesin diye)
if "leaderboard" not in st.session_state:
  st.session_state.leaderboard = [
      {"İsim": "Zeynep K.", "Puan": 3, "Zaman": "10:12"},
      {"İsim": "Ahmet Y.", "Puan": 2, "Zaman": "10:15"},
      {"İsim": "Can M.", "Puan": 3, "Zaman": "10:20"},
  ]

# ==========================================
# 1. ADIM: KULLANICI KAYDI
# ==========================================
if st.session_state.quiz_stage == "register":
  st.title("📝 Python & Teknoloji Bilgi Yarışması")
  st.markdown(
      "Testi çözerek **Liderlik Tablosu'na (Top Scorers)** adını yazdır!"
  )

  with st.form("register_form"):
    name_input = st.text_input(
        "Adınız Soyadınız:", placeholder="Örn: Alan Turing"
    )
    start_button = st.form_submit_button("Quiz'e Başla 🚀")

    if start_button:
      if name_input.strip() == "":
        st.warning("Lütfen geçerli bir ad girin!")
      else:
        st.session_state.name = name_input
        st.session_state.recorded = (
            False  # Yeni kullanıcı için kayıt bayrağını sıfırla
        )
        st.session_state.quiz_stage = "quiz"
        st.rerun()

# ==========================================
# 2. ADIM: QUIZ SORULARI
# ==========================================
elif st.session_state.quiz_stage == "quiz":
  st.title(f"🧠 Başarılar, {st.session_state.name}!")
  st.write("Soruları dikkatlice yanıtlayın.")

  with st.form("quiz_form"):
    q1 = st.radio(
        "1. Streamlit hangi programlama dili ile web uygulaması"
        " geliştirmenizi sağlar?",
        ["JavaScript", "Python", "C++", "HTML"],
    )

    q2 = st.radio(
        "2. ESP32-S3 mikrodenetleyicisi hangi kablosuz bağlantı"
        " özelliklerine sahiptir?",
        [
            "Sadece Bluetooth",
            "Sadece Kablolu Ethernet",
            "Wi-Fi ve Bluetooth",
            "Hiçbiri",
        ],
    )

    q3 = st.radio(
        "3. Streamlit'te kullanıcı etkileşimleriyle anlık verileri"
        " hatırlamak için hangi yapı kullanılır?",
        ["st.session_state", "st.cache_data", "st.sidebar", "st.stop"],
    )

    submit_quiz = st.form_submit_button("Testi Tamamla ve Skoru Gör 🎯")

    if submit_quiz:
      score = 0
      if q1 == "Python":
        score += 1
      if q2 == "Wi-Fi ve Bluetooth":
        score += 1
      if q3 == "st.session_state":
        score += 1

      st.session_state.score = score
      st.session_state.quiz_stage = "result"
      st.rerun()

# ==========================================
# 3. ADIM: SONUÇ VE LİDERLİK TABLOSU (TOP SCORERS)
# ==========================================
elif st.session_state.quiz_stage == "result":
  st.title("🏆 Quiz Sonucu & En İyi Skorlar")

  score = st.session_state.score
  total = 3

  st.metric(label="Senin Puanın", value=f"{score} / {total}")

  # Kullanıcının skoru liderlik tablosuna sadece 1 kez eklensin
  if not st.session_state.recorded:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.leaderboard.append({
        "İsim": st.session_state.name,
        "Puan": score,
        "Zaman": current_time,
    })
    st.session_state.recorded = True

  if score == 3:
    st.success("Mükemmel! Tüm soruları doğru bildin! 🎉")
  else:
    st.info("Testi tamamladın! Skorun listeye eklendi. 👍")

  st.divider()
  st.subheader("🌟 En İyi Skorlar Listesi (Leaderboard)")

  # Tabloyu puana göre büyükten küçüğe sırala
  df_leaderboard = pd.DataFrame(st.session_state.leaderboard)
  df_leaderboard = df_leaderboard.sort_values(
      by=["Puan", "Zaman"], ascending=[False, True]
  ).reset_index(drop=True)

  # Şık bir tablo formatında göster
  st.dataframe(df_leaderboard, use_container_width=True)

  st.divider()
  if st.button("Yeniden Başla / Yeni Oyuncu 🔄"):
    st.session_state.quiz_stage = "register"
    st.rerun()
