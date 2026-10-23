
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

# ==========================================
# SAYFA YAPILANDIRMASI
# ==========================================
st.set_page_config(
    page_title="İnteraktif Quiz & E-Posta Gönderimi",
    page_icon="📝",
    layout="centered",
)

# ==========================================
# SESSION STATE BAŞLANGICI
# ==========================================
if "quiz_stage" not in st.session_state:
  st.session_state.quiz_stage = "register"  # register, quiz, result
  st.session_state.name = ""
  st.session_state.email = ""
  st.session_state.score = 0

# ==========================================
# 1. ADIM: KULLANICI BİLGİLERİ (KAYIT)
# ==========================================
if st.session_state.quiz_stage == "register":
  st.title("📝 Python & Teknoloji Bilgi Yarışması")
  st.markdown(
      "Testi çözmek ve sonucunuzu anında e-posta ile almak için bilgilerinizi"
      " girin."
  )

  with st.form("register_form"):
    name_input = st.text_input("Adınız Soyadınız:")
    email_input = st.text_input(
        "E-Posta Adresiniz (Sonucun gönderileceği adres):"
    )

    start_button = st.form_submit_button("Quiz'e Başla 🚀")

    if start_button:
      if name_input.strip() == "" or "@" not in email_input:
        st.warning("Lütfen geçerli bir ad ve e-posta adresi girin!")
      else:
        st.session_state.name = name_input
        st.session_state.email = email_input
        st.session_state.quiz_stage = "quiz"
        st.rerun()

# ==========================================
# 2. ADIM: QUIZ SORULARI
# ==========================================
elif st.session_state.quiz_stage == "quiz":
  st.title(f"🧠 Başarılar, {st.session_state.name}!")
  st.write("Aşağıdaki soruları yanıtlayın ve gönderin.")

  with st.form("quiz_form"):
    # Soru 1
    q1 = st.radio(
        "1. Streamlit hangi programlama dili ile web uygulaması geliştirmenizi"
        " sağlar?",
        ["JavaScript", "Python", "C++", "HTML"],
    )

    # Soru 2
    q2 = st.radio(
        "2. ESP32-S3 mikrodenetleyicisi hangi kablosuz bağlantı özelliklerine"
        " sahiptir?",
        [
            "Sadece Bluetooth",
            "Sadece Kablolu Ethernet",
            "Wi-Fi ve Bluetooth",
            "Hiçbiri",
        ],
    )

    # Soru 3
    q3 = st.radio(
        "3. Streamlit'te kullanıcı etkileşimleriyle anlık verileri hatırlamak"
        " için hangi yapı kullanılır?",
        ["st.session_state", "st.cache_data", "st.sidebar", "st.stop"],
    )

    submit_quiz = st.form_submit_button("Testi Tamamla ve Sonucu Gör 🎯")

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
# 3. ADIM: SONUÇ VE E-POSTA GÖNDERME
# ==========================================
elif st.session_state.quiz_stage == "result":
  st.title("🏆 Quiz Sonucunuz")

  score = st.session_state.score
  total = 3
  percentage = (score / total) * 100

  st.metric(label="Toplam Puanınız", value=f"{score} / {total}")

  if score == 3:
    st.success("Mükemmel! Tüm soruları doğru bildiniz! 🎉")
  elif score > 0:
    st.info("Tebrikler, fena sayılmaz! 👍")
  else:
    st.warning("Bir dahaki sefere daha iyisini yapabilirsin! 💪")

  st.divider()
  st.subheader("📬 Sonucu E-Posta ile Gönder")
  st.write(
      f"Sonucunuz **{st.session_state.email}** adresine gönderilecek. Lütfen"
      " aşağıdaki SMTP ayarlarını doldurun:"
  )

  # Güvenlik için e-posta gönderen (admin) bilgileri
  with st.form("email_form"):
    sender_email = st.text_input(
        "Gönderici E-Posta (Sizin Gmail Adresiniz):",
        placeholder="ornegin@gmail.com",
    )
    sender_password = st.text_input(
        "Gönderici Uygulama Şifresi (Google App Password):",
        type="password",
        placeholder="16 haneli uygulama şifresi",
    )

    send_button = st.form_submit_button("E-Posta Gönder 📨")

    if send_button:
      if not sender_email or not sender_password:
        st.error("Lütfen gönderici e-posta ve şifre alanlarını doldurun!")
      else:
        # E-posta gönderme işlemi
        try:
          smtp_server = "smtp.gmail.com"
          port = 587

          message = MIMEMultipart("alternative")
          message["Subject"] = (
              f"Quiz Sonucu - {st.session_state.name} ({score}/{total})"
          )
          message["From"] = sender_email
          message["To"] = st.session_state.email

          html_content = f"""
                    <html>
                      <body style="font-family: Arial, sans-serif;">
                        <h2 style="color: #2e6c80;">Tebrikler, {st.session_state.name}!</h2>
                        <p>Streamlit Quiz platformunu başarıyla tamamladınız.</p>
                        <hr>
                        <h3>Sınav Sonucunuz:</h3>
                        <p style="font-size: 18px;">Doğru Sayısı: <b>{score} / {total}</b></p>
                        <p style="font-size: 18px;">Başarı Oranı: <b>%{percentage:.0f}</b></p>
                        <hr>
                        <p style="color: gray; font-size: 12px;">Bu e-posta otomatik olarak Streamlit Quiz Uygulaması tarafından gönderilmiştir.</p>
                      </body>
                    </html>
                    """

          message.attach(MIMEText(html_content, "html"))

          # SMTP bağlantısı ve gönderim
          server = smtplib.SMTP(smtp_server, port)
          server.starttls()
          server.login(sender_email, sender_password)
          server.sendmail(
              sender_email, st.session_state.email, message.as_string()
          )
          server.quit()

          st.success(
              f"✅ Sonucunuz başarıyla {st.session_state.email} adresine"
              " gönderildi!"
          )
          st.balloons()

        except Exception as e:
          st.error(f"❌ E-posta gönderilemedi. Hata: `{e}`")

  if st.button("Yeniden Başla 🔄"):
    st.session_state.clear()
    st.rerun()
