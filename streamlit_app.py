import time
import pandas as pd
import streamlit as st

# ==========================================
# SAYFA YAPILANDIRMASI
# ==========================================
st.set_page_config(
    page_title="Botanikte Latince Renkler Quiz",
    page_icon="🌿",
    layout="centered",
)

# ==========================================
# SORULAR VE BİTKİ ÖRNEKLERİ
# ==========================================
questions = [
    {
        "latin": "Albus",
        "question": "Latince botanik terimlerinden 'Albus' hangi rengi ifade eder?",
        "options": ["Siyah", "Beyaz", "Kırmızı", "Sarı"],
        "answer": "Beyaz",
        "plant": "Nymphaea alba",
        "plant_name": "Beyaz nilüfer",
        "explanation": "'Alba', beyaz anlamına gelir ve bitkinin adında beyaz rengi belirtir.",
    },
    {
        "latin": "Viridis",
        "question": "'Viridis' Latince hangi rengi ifade eder?",
        "options": ["Mavi", "Yeşil", "Kahverengi", "Altın sarısı"],
        "answer": "Yeşil",
        "plant": "Malva viridis",
        "plant_name": "Yeşil ebegümeci adıyla kullanılan ifade",
        "explanation": "'Viridis', yeşil anlamına gelir. Bu sıfat bitkilerde yeşil rengi ifade etmek için kullanılır.",
    },
    {
        "latin": "Ruber",
        "question": "'Ruber' Latince hangi rengi ifade eder?",
        "options": ["Mor", "Kırmızı", "Pembe", "Gri"],
        "answer": "Kırmızı",
        "plant": "Trifolium rubens",
        "plant_name": "Kızıl çayır üçgülü",
        "explanation": "'Rubens', kızıl veya kırmızımsı anlamıyla ilişkilidir. Trifolium rubens, kırmızımsı çiçekleriyle bilinen bir üçgül türüdür.",
    },
    {
        "latin": "Luteus",
        "question": "'Luteus' Latince hangi rengi ifade eder?",
        "options": ["Sarı", "Turuncu", "Mavi", "Beyaz"],
        "answer": "Sarı",
        "plant": "Iris lutea",
        "plant_name": "Sarı süsen adıyla kullanılan ifade",
        "explanation": "'Luteus', sarı anlamına gelir. Botanikte sarı renkli bitki kısımlarını tanımlayan sıfatlar arasında yer alır.",
    },
    {
        "latin": "Niger",
        "question": "'Niger' Latince hangi rengi ifade eder?",
        "options": ["Siyah", "Koyu yeşil", "Gümüşi", "Parlak sarı"],
        "answer": "Siyah",
        "plant": "Sambucus nigra",
        "plant_name": "Kara mürver",
        "explanation": "'Nigra', siyah veya çok koyu anlamına gelir. Sambucus nigra, kara mürverin bilimsel adıdır.",
    },
]

# ==========================================
# OTURUM DURUMU
# ==========================================
defaults = {
    "stage": "register",
    "name": "",
    "score": 0,
    "start_time": 0.0,
    "elapsed_time": 0.0,
    "current_question": 0,
    "answers": [],
    "leaderboard": [
        {"İsim": "Linnaeus", "Doğru Sayısı": 5, "Süre (sn)": 14.2},
        {"İsim": "Darwin", "Doğru Sayısı": 4, "Süre (sn)": 11.0},
        {"İsim": "Mendel", "Doğru Sayısı": 3, "Süre (sn)": 9.5},
    ],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, list) else value

# ==========================================
# 1. KAYIT EKRANI
# ==========================================
if st.session_state.stage == "register":
    st.title("🌿 Latince Botanik Renkleri Quiz'i")

    st.markdown(
        """
        Botanikte kullanılan Latince renk terimlerini ne kadar biliyorsun?

        - 🌱 Her soruda bir Latince renk terimi göreceksin.
        - 🎨 Dört seçenek arasından doğru rengi seçeceksin.
        - 🌸 Cevabından sonra ilgili bilimsel bitki adını ve açıklamasını göreceksin.
        - ⏱️ Süren ölçülecek ve sonuçların liderlik tablosuna eklenecek.
        """
    )

    with st.form("register_form"):
        name_input = st.text_input(
            "Adınız:",
            placeholder="Örn. Karl Linnaeus",
        )
        submitted = st.form_submit_button("Quiz'i Başlat 🚀")

        if submitted:
            if not name_input.strip():
                st.warning("Lütfen adınızı girin.")
            else:
                st.session_state.name = name_input.strip()
                st.session_state.score = 0
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.session_state.start_time = time.time()
                st.session_state.elapsed_time = 0.0
                st.session_state.stage = "quiz"
                st.rerun()

# ==========================================
# 2. SORU EKRANI
# ==========================================
elif st.session_state.stage == "quiz":
    index = st.session_state.current_question
    q = questions[index]

    st.title("🌿 Latince Botanik Renkleri")
    st.progress((index + 1) / len(questions))
    st.caption(f"Soru {index + 1} / {len(questions)}")

    st.info(q["question"])

    with st.form(f"question_form_{index}"):
        selected = st.radio(
            "Doğru renk hangisi?",
            q["options"],
        )

        submitted = st.form_submit_button(
            "Cevabı Kontrol Et 🌱"
        )

        if submitted:
            is_correct = selected == q["answer"]

            if is_correct:
                st.session_state.score += 1

            st.session_state.answers.append({
                "latin": q["latin"],
                "selected": selected,
                "correct": q["answer"],
                "is_correct": is_correct,
            })

            st.session_state.stage = "feedback"
            st.rerun()

# ==========================================
# 3. CEVAP VE BİTKİ ÖRNEĞİ
# ==========================================
elif st.session_state.stage == "feedback":
    index = st.session_state.current_question
    q = questions[index]
    last_answer = st.session_state.answers[-1]

    st.title("🌸 Cevap ve Botanik Örneği")

    if last_answer["is_correct"]:
        st.success("Doğru cevap! 🎉")
    else:
        st.error("Bu kez doğru cevabı bulamadın.")

    st.markdown(f"### 🎨 Doğru renk: {q['answer']}")

    st.divider()

    st.markdown("### 🌱 Bilimsel bitki örneği")
    st.markdown(f"**{q['plant']}**")
    st.write(q["plant_name"])
    st.caption(q["explanation"])

    st.info(
        f"Şu anki puanın: "
        f"{st.session_state.score} / "
        f"{len(st.session_state.answers)}"
    )

    if index + 1 < len(questions):
        if st.button("Sonraki Soru ➡️", use_container_width=True):
            st.session_state.current_question += 1
            st.session_state.stage = "quiz"
            st.rerun()
    else:
        if st.button("Sonuçları Gör 🏆", use_container_width=True):
            st.session_state.elapsed_time = round(
                time.time() - st.session_state.start_time,
                2,
            )

            st.session_state.leaderboard.append({
                "İsim": st.session_state.name,
                "Doğru Sayısı": st.session_state.score,
                "Süre (sn)": st.session_state.elapsed_time,
            })

            st.session_state.stage = "result"
            st.rerun()

# ==========================================
# 4. SONUÇ VE LİDERLİK TABLOSU
# ==========================================
elif st.session_state.stage == "result":
    st.title("🏆 Quiz Sonucu")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Doğru Sayısı",
            f"{st.session_state.score} / {len(questions)}",
        )

    with col2:
        st.metric(
            "Tamamlama Süresi",
            f"{st.session_state.elapsed_time} saniye",
        )

    if st.session_state.score == len(questions):
        st.balloons()
        st.success("Mükemmel! Bütün soruları doğru cevapladın! 🌿")
    elif st.session_state.score >= 3:
        st.success("Güzel iş! Botanik renkleri konusunda iyi ilerliyorsun.")
    else:
        st.info("Yeni bir turla renk bilgini geliştirebilirsin.")

    st.divider()

    st.subheader("📋 Cevaplarını Gözden Geçir")

    for i, answer in enumerate(st.session_state.answers):
        symbol = "✅" if answer["is_correct"] else "❌"

        st.write(
            f"{symbol} **{i + 1}. {answer['latin']}** — "
            f"Senin cevabın: {answer['selected']} | "
            f"Doğru cevap: {answer['correct']}"
        )

    st.divider()

    st.subheader("🌟 Liderlik Tablosu")

    df = pd.DataFrame(st.session_state.leaderboard)

    df = df.sort_values(
        by=["Doğru Sayısı", "Süre (sn)"],
        ascending=[False, True],
    ).reset_index(drop=True)

    df.index = df.index + 1

    st.dataframe(
        df,
        use_container_width=True,
    )

    st.caption(
        "Sıralamada önce doğru sayısı yüksek olan, "
        "eşitlik durumunda ise daha kısa sürede bitiren yarışmacı üstte yer alır."
    )

    if st.button("Yeniden Oyna 🔄", use_container_width=True):
        st.session_state.stage = "register"
        st.session_state.name = ""
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.elapsed_time = 0.0
        st.rerun()
