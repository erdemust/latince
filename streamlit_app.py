import streamlit as st
import pandas as pd
import random
import csv
from io import StringIO

st.set_page_config(
    page_title="Botanik Latince Öğrenme",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 Botanik Latince Öğrenme")
st.write("Latince bitki terimlerini öğren, bilgini test et!")

st.divider()

# Gerekli sütunlar
REQUIRED_COLUMNS = [
    "latin",
    "answer",
    "options",
    "plant",
    "plant_name",
    "explanation"
]


def read_csv_file(uploaded_file):
    """CSV dosyasını farklı kodlamalar ve ayraçlarla okumayı dener."""

    file_bytes = uploaded_file.getvalue()

    encodings = [
        "utf-8-sig",
        "utf-8",
        "cp1254",
        "iso-8859-9",
        "latin1"
    ]

    errors = []

    for encoding in encodings:
        try:
            text = file_bytes.decode(encoding)

            # Ayraç karakterini belirle
            try:
                dialect = csv.Sniffer().sniff(
                    text[:10000],
                    delimiters=",;\t|"
                )
                separator = dialect.delimiter
            except csv.Error:
                separator = ","

            df = pd.read_csv(
                StringIO(text),
                sep=separator,
                dtype=str,
                keep_default_na=False,
                on_bad_lines="error"
            )

            # Sütun adlarını temizle
            df.columns = [
                str(col).strip().replace("\ufeff", "")
                for col in df.columns
            ]

            # Sütun adlarında olası boşlukları temizle
            df.columns = [
                col.lower() for col in df.columns
            ]

            missing = [
                col for col in REQUIRED_COLUMNS
                if col not in df.columns
            ]

            if missing:
                errors.append(
                    f"{encoding}: Eksik sütunlar: {missing}"
                )
                continue

            # Tamamen boş satırları kaldır
            df = df.dropna(how="all")

            # Boşlukları temizle
            for col in REQUIRED_COLUMNS:
                df[col] = df[col].astype(str).str.strip()

            # Latince kelimesi veya cevabı boş olan satırları kaldır
            df = df[
                (df["latin"] != "") &
                (df["answer"] != "")
            ].reset_index(drop=True)

            if df.empty:
                errors.append(
                    f"{encoding}: Kullanılabilir veri bulunamadı."
                )
                continue

            return df, None

        except Exception as e:
            errors.append(f"{encoding}: {str(e)}")

    return None, "\n".join(errors)


# CSV yükleme
uploaded_file = st.file_uploader(
    "📂 CSV dosyanızı yükleyin",
    type=["csv"]
)

if uploaded_file is not None:

    df, error = read_csv_file(uploaded_file)

    if error:
        st.error("CSV dosyası okunamadı.")
        with st.expander("Hata ayrıntılarını göster"):
            st.code(error)

        st.info(
            "Dosyanın ilk satırında latin, answer, options, "
            "plant, plant_name ve explanation sütunları "
            "bulunmalıdır."
        )

        st.stop()

    st.success(
        f"✅ CSV başarıyla yüklendi! "
        f"{len(df)} terim bulundu."
    )

    # Oturum değişkenlerini başlat
    if (
        "quiz_data" not in st.session_state
        or st.session_state.get("file_name") != uploaded_file.name
    ):
        st.session_state.quiz_data = df.to_dict("records")
        st.session_state.file_name = uploaded_file.name
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.used_questions = []
        st.session_state.selected_option = None

    quiz_data = st.session_state.quiz_data

    if not quiz_data:
        st.warning("CSV dosyasında soru bulunamadı.")
        st.stop()

    total_questions = len(quiz_data)

    # İlerleme
    progress = min(
        st.session_state.question_index / total_questions,
        1.0
    )

    st.progress(progress)

    st.write(
        f"**Soru:** "
        f"{min(st.session_state.question_index + 1, total_questions)}"
        f" / {total_questions}"
    )

    st.write(f"🏆 **Doğru cevap:** {st.session_state.score}")

    # Tüm sorular tamamlandı mı?
    if st.session_state.question_index >= total_questions:

        st.balloons()
        st.success("🎉 Test tamamlandı!")

        st.subheader("Sonuçlar")

        st.metric(
            "Doğru cevap sayısı",
            st.session_state.score
        )

        st.metric(
            "Başarı oranı",
            f"%{st.session_state.score / total_questions * 100:.1f}"
        )

        if st.button("🔄 Testi yeniden başlat"):
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.used_questions = []
            st.session_state.selected_option = None

            random.shuffle(st.session_state.quiz_data)
            st.rerun()

        st.stop()

    # Soruyu seç
    current = quiz_data[st.session_state.question_index]

    st.divider()

    st.subheader("🌱 Bu Latince kelimenin Türkçe karşılığı nedir?")

    st.markdown(
        f"<h2 style='text-align:center; color:#228B22;'>"
        f"{current['latin']}</h2>",
        unsafe_allow_html=True
    )

    # Şıkları CSV içindeki options sütunundan al
    options = [
        option.strip()
        for option in current["options"].split(",")
        if option.strip()
    ]

    # Doğru cevap seçenekler arasında yoksa ekle
    if current["answer"] not in options:
        options.append(current["answer"])

    # Seçeneklerin sırasını karıştır
    if "options_question" not in st.session_state:
        st.session_state.options_question = -1

    if (
        st.session_state.options_question
        != st.session_state.question_index
    ):
        random.shuffle(options)
        st.session_state.current_options = options
        st.session_state.options_question = (
            st.session_state.question_index
        )

    selected = st.radio(
        "Doğru cevabı seç:",
        st.session_state.current_options,
        index=None,
        key=f"answer_{st.session_state.question_index}",
        disabled=st.session_state.answered
    )

    # Cevabı kontrol et
    if not st.session_state.answered:

        if st.button("✅ Cevabı kontrol et", use_container_width=True):

            if selected is None:
                st.warning("Lütfen bir seçenek işaretleyin.")
            else:
                st.session_state.selected_option = selected
                st.session_state.answered = True

                if selected == current["answer"]:
                    st.session_state.score += 1

                st.rerun()

    # Cevap sonrası bitki bilgilerini göster
    if st.session_state.answered:

        if (
            st.session_state.selected_option
            == current["answer"]
        ):
            st.success("🎉 Doğru cevap!")
        else:
            st.error(
                f"❌ Yanlış cevap. Doğru cevap: "
                f"{current['answer']}"
            )

        st.divider()

        st.subheader("🌿 Örnek bitki")

        st.markdown(
            f"### {current['plant_name']}"
        )

        st.markdown(
            f"**Bilimsel adı:** *{current['plant']}*"
        )

        st.markdown(
            f"**Latince terim:** {current['latin']}"
        )

        st.markdown(
            f"**Türkçe anlamı:** {current['answer']}"
        )

        st.subheader("📖 Açıklama")

        st.write(current["explanation"])

        if st.button(
            "➡️ Sonraki soru",
            use_container_width=True
        ):
            st.session_state.question_index += 1
            st.session_state.answered = False
            st.session_state.selected_option = None
            st.rerun()

else:
    st.info(
        "Başlamak için botanical_terms.csv dosyanızı yükleyin."
    )

    st.markdown(
        """
        ### 📚 Nasıl çalışır?

        1. CSV dosyanızı yüklersiniz.
        2. Ekranda bir Latince botanik terimi belirir.
        3. Dört Türkçe seçenek arasından doğru anlamı seçersiniz.
        4. Cevabınızı kontrol edersiniz.
        5. Doğru cevapla birlikte örnek bitki, bilimsel adı
           ve botanik açıklaması gösterilir.
        6. Test sonunda başarı yüzdenizi görürsünüz.
        """
    )
