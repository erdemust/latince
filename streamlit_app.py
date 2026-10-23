import streamlit as st
import pandas as pd
import random
import io

# --------------------------------------------------
# SAYFA AYARLARI
# --------------------------------------------------

st.set_page_config(
    page_title="Botanik Latince Öğrenme",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 Botanik Latince Öğrenme")
st.write("Latince bitki terimlerini öğren, bilgini test et!")

st.divider()


# --------------------------------------------------
# CSV OKUMA FONKSİYONU
# --------------------------------------------------

REQUIRED_COLUMNS = [
    "latin",
    "answer",
    "options",
    "plant",
    "plant_name",
    "explanation"
]


def load_csv(uploaded_file):
    """CSV dosyasını okur ve gerekli sütunları kontrol eder."""

    raw_data = uploaded_file.getvalue()

    df = None

    for encoding in ["utf-8-sig", "utf-8", "cp1254", "latin1"]:
        try:
            df = pd.read_csv(
                io.BytesIO(raw_data),
                encoding=encoding,
                dtype=str
            )
            break
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue

    if df is None:
        raise ValueError("CSV dosyası okunamadı.")

    # Sütun adlarının başındaki ve sonundaki boşlukları temizle.
    df.columns = df.columns.str.strip()

    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            "CSV dosyasında eksik sütunlar var: "
            + ", ".join(missing)
        )

    # Boş değerleri temizle.
    for col in REQUIRED_COLUMNS:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # Latince kelimesi veya cevabı olmayan satırları çıkar.
    df = df[
        (df["latin"] != "") &
        (df["answer"] != "")
    ].reset_index(drop=True)

    if df.empty:
        raise ValueError("CSV dosyasında geçerli soru bulunamadı.")

    return df


# --------------------------------------------------
# OTURUM DURUMU
# --------------------------------------------------

def initialize_quiz(df, shuffle=True):
    """Yeni bir quiz oturumu başlatır."""

    order = list(range(len(df)))

    if shuffle:
        random.shuffle(order)

    st.session_state.question_order = order
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_answer = None
    st.session_state.finished = False
    st.session_state.correct_count = 0
    st.session_state.wrong_count = 0


# --------------------------------------------------
# CSV DOSYASI YÜKLEME
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📂 CSV dosyanızı yükleyin",
    type=["csv"]
)

if uploaded_file is None:
    st.info(
        "Başlamak için latin, answer, options, plant, "
        "plant_name ve explanation sütunlarını içeren "
        "CSV dosyanızı yükleyin."
    )

    st.code(
        "latin,answer,options,plant,plant_name,explanation\n"
        'Glaber,Tüysüz veya pürüzsüz,'
        '"Tüylü;Tüysüz veya pürüzsüz;Dikenli;Benekli",'
        'Acer glabrum,Pürüzsüz akçaağaç,'
        '"Glaber Latince tüysüz veya pürüzsüz anlamına gelir."',
        language="csv"
    )

    st.stop()


# --------------------------------------------------
# DOSYAYI OKU
# --------------------------------------------------

try:
    df = load_csv(uploaded_file)
except (ValueError, pd.errors.ParserError) as e:
    st.error(str(e))
    st.stop()


# Dosya değiştiğinde quiz'i sıfırla.
file_signature = (
    uploaded_file.name,
    uploaded_file.size,
    hash(uploaded_file.getvalue())
)

if st.session_state.get("file_signature") != file_signature:
    st.session_state.file_signature = file_signature
    initialize_quiz(df)


# --------------------------------------------------
# YAN PANEL
# --------------------------------------------------

with st.sidebar:
    st.header("⚙️ Quiz Ayarları")

    shuffle_questions = st.checkbox(
        "Soruları karıştır",
        value=True
    )

    shuffle_options = st.checkbox(
        "Cevap seçeneklerini karıştır",
        value=True
    )

    st.divider()

    st.metric("📚 Toplam terim", len(df))

    st.caption(
        "Her soruda Latince terimin Türkçe karşılığını "
        "bulmaya çalışın."
    )

    if st.button("🔄 Quiz'i yeniden başlat", use_container_width=True):
        initialize_quiz(df, shuffle=shuffle_questions)
        st.rerun()


# --------------------------------------------------
# QUIZ SONUÇ EKRANI
# --------------------------------------------------

if st.session_state.finished:

    st.success("🎉 Quiz tamamlandı!")

    total = len(st.session_state.question_order)
    correct = st.session_state.correct_count
    wrong = st.session_state.wrong_count

    percentage = (correct / total * 100) if total else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Toplam soru", total)
    col2.metric("Doğru cevap", correct)
    col3.metric("Başarı oranı", f"%{percentage:.1f}")

    st.progress(percentage / 100)

    if percentage >= 90:
        st.balloons()
        st.success("Mükemmel! Botanik Latince bilginiz çok iyi.")
    elif percentage >= 70:
        st.success("Çok iyi! Biraz daha pratikle daha da gelişebilirsiniz.")
    elif percentage >= 50:
        st.info("İyi bir başlangıç! Açıklamaları tekrar inceleyin.")
    else:
        st.info("Kelimeleri tekrar ederek bilginizi geliştirebilirsiniz.")

    if st.button("🔁 Yeniden çöz", use_container_width=True):
        initialize_quiz(df, shuffle=shuffle_questions)
        st.rerun()

    st.stop()


# --------------------------------------------------
# SORU BİLGİLERİ
# --------------------------------------------------

question_number = st.session_state.question_index
total_questions = len(st.session_state.question_order)

if question_number >= total_questions:
    st.session_state.finished = True
    st.rerun()

row_index = st.session_state.question_order[question_number]
row = df.iloc[row_index]


# --------------------------------------------------
# İLERLEME DURUMU
# --------------------------------------------------

st.progress(question_number / total_questions)

st.caption(
    f"📖 Soru {question_number + 1} / {total_questions}"
)

st.metric("🏆 Puanınız", st.session_state.score)

st.divider()


# --------------------------------------------------
# LATİNCE KELİME SORUSU
# --------------------------------------------------

st.subheader("❓ Bu Latince kelimenin Türkçe karşılığı nedir?")

st.markdown(
    f"""
    <div style="
        background-color: #e8f5e9;
        padding: 28px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #a5d6a7;
    ">
        <h1 style="color: #1b5e20; margin: 0;">
            {row['latin']}
        </h1>
        <p style="color: #2e7d32; margin-bottom: 0;">
            Latince botanik terimi
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# --------------------------------------------------
# CEVAP SEÇENEKLERİ
# --------------------------------------------------

# CSV'de seçenekler virgül veya noktalı virgülle ayrılmış olabilir.
raw_options = str(row["options"])

if ";" in raw_options:
    options = [
        option.strip()
        for option in raw_options.split(";")
        if option.strip()
    ]
else:
    options = [
        option.strip()
        for option in raw_options.split(",")
        if option.strip()
    ]

# Doğru cevap seçeneklerde yoksa ekle.
if row["answer"] not in options:
    options.append(row["answer"])

# Aynı seçeneğin birden fazla görünmesini önle.
options = list(dict.fromkeys(options))

# Seçenekleri her soruda yeniden karıştır.
if (
    shuffle_options
    and st.session_state.get("last_option_question") != question_number
):
    random.shuffle(options)
    st.session_state.last_option_question = question_number
    st.session_state.current_options = options
elif shuffle_options:
    options = st.session_state.get("current_options", options)

if not shuffle_options:
    options = options


# --------------------------------------------------
# CEVAP FORMU
# --------------------------------------------------

if not st.session_state.answered:

    with st.form(key=f"question_form_{question_number}"):

        selected = st.radio(
            "Doğru cevabı seçin:",
            options,
            index=None,
            key=f"answer_{question_number}"
        )

        submitted = st.form_submit_button(
            "✅ Cevabımı kontrol et",
            use_container_width=True
        )

        if submitted:

            if selected is None:
                st.warning("Lütfen bir cevap seçin.")
            else:
                st.session_state.selected_answer = selected
                st.session_state.answered = True

                if selected == row["answer"]:
                    st.session_state.score += 10
                    st.session_state.correct_count += 1
                else:
                    st.session_state.wrong_count += 1

                st.rerun()


# --------------------------------------------------
# CEVAP SONRASI AÇIKLAMA
# --------------------------------------------------

if st.session_state.answered:

    selected = st.session_state.selected_answer
    correct_answer = row["answer"]

    if selected == correct_answer:
        st.success("🎉 Doğru cevap! +10 puan")
    else:
        st.error("❌ Yanlış cevap!")

        st.markdown(
            f"**Doğru cevap:** {correct_answer}"
        )

    st.divider()

    # Bitki bilgileri
    st.subheader("🌱 Bitki örneği")

    st.markdown(
        f"""
        **Bilimsel adı:** *{row['plant']}*

        **Türkçe adı:** {row['plant_name']}
        """
    )

    # Açıklama
    st.subheader("📘 Açıklama")

    st.info(row["explanation"])

    st.caption(
        "Not: CSV'deki bitki adları ve botanik açıklamalar "
        "bilimsel kaynaklardan ayrıca doğrulanabilir."
    )

    st.divider()

    # Sonraki soru
    if question_number + 1 < total_questions:

        if st.button(
            "➡️ Sonraki soru",
            type="primary",
            use_container_width=True
        ):
            st.session_state.question_index += 1
            st.session_state.answered = False
            st.session_state.selected_answer = None
            st.rerun()

    else:

        if st.button(
            "🏁 Sonuçları gör",
            type="primary",
            use_container_width=True
        ):
            st.session_state.finished = True
            st.rerun()
