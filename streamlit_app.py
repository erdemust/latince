import time
import pandas as pd
import streamlit as st

# ==========================================
# SAYFA AYARLARI
# ==========================================
st.set_page_config(
    page_title="Latince Botanik Renkleri Quiz",
    page_icon="🌿",
    layout="centered",
)

# ==========================================
# SORULAR
# Önce renk sorulur, cevap sonrası bitki örneği gösterilir.
# ==========================================
QUESTIONS = [
    {
        "latin": "Albus",
        "question": "'Albus' Latince hangi rengi ifade eder?",
        "options": ["Siyah", "Beyaz", "Kırmızı", "Sarı"],
        "answer": "Beyaz",
        "plant": "Nymphaea alba",
        "plant_name": "Beyaz nilüfer",
        "explanation": "'Alba', beyaz anlamına gelir. Bu bitkinin bilimsel adında da kullanılır.",
    },
    {
        "latin": "Viridis",
        "question": "'Viridis' Latince hangi rengi ifade eder?",
        "options": ["Mavi", "Yeşil", "Kahverengi", "Altın sarısı"],
        "answer": "Yeşil",
        "plant": "Helleborus viridis",
        "plant_name": "Yeşil çöpleme",
        "explanation": "'Viridis', yeşil anlamına gelir ve bitkinin bilimsel adında yer alır.",
    },
    {
        "latin": "Rubens",
        "question": "'Rubens' Latince hangi renk özelliğini ifade eder?",
        "options": ["Beyazımsı", "Kızıl veya kırmızımsı", "Mavimsi", "Sarımsı"],
        "answer": "Kızıl veya kırmızımsı",
        "plant": "Trifolium rubens",
        "plant_name": "Kızıl çayır üçgülü",
        "explanation": "'Rubens', kızıl veya kırmızımsı anlamıyla ilişkilidir.",
    },
    {
        "latin": "Luteus",
        "question": "'Luteus' Latince hangi rengi ifade eder?",
        "options": ["Sarı", "Turuncu", "Mavi", "Beyaz"],
        "answer": "Sarı",
        "plant": "Iris pseudacorus",
        "plant_name": "Sarı süsen",
        "explanation": "'Luteus', sarı anlamına gelir. Sarı renkli çiçekleriyle bilinen bitkiler bu renkle ilişkilendirilir.",
    },
    {
        "latin": "Niger",
        "question": "'Niger' Latince hangi rengi ifade eder?",
        "options": ["Siyah", "Koyu yeşil", "Gümüşi", "Parlak sarı"],
        "answer": "Siyah",
        "plant": "Sambucus nigra",
        "plant_name": "Kara mürver",
        "explanation": "'Nigra', siyah anlamına gelir. Sambucus nigra, kara mürverin bilimsel adıdır.",
    },
    {
        "latin": "Roseus",
        "question": "'Roseus' Latince hangi rengi ifade eder?",
        "options": ["Pembe", "Gri", "Yeşil", "Kahverengi"],
        "answer": "Pembe",
        "plant": "Dianthus deltoides",
        "plant_name": "Karanfilgillerden bir bitki türü",
        "explanation": "'Roseus', gül pembesi veya pembe anlamına gelir.",
    },
    {
        "latin": "Purpureus",
        "question": "'Purpureus' Latince hangi rengi ifade eder?",
        "options": ["Sarı", "Beyaz", "Mor", "Turuncu"],
        "answer": "Mor",
        "plant": "Echinacea purpurea",
        "plant_name": "Mor ekinezya",
        "explanation": "'Purpurea', mor veya erguvan tonlarını ifade eder.",
    },
    {
        "latin": "Caeruleus",
        "question": "'Caeruleus' Latince hangi rengi ifade eder?",
        "options": ["Mavi", "Siyah", "Kırmızı", "Kahverengi"],
        "answer": "Mavi",
        "plant": "Plumbago auriculata",
        "plant_name": "Mavi yasemin",
        "explanation": "'Caeruleus', mavi veya gök mavisi anlamına gelir.",
    },
    {
        "latin": "Aureus",
        "question": "'Aureus' Latince hangi rengi ifade eder?",
        "options": ["Gümüş", "Altın rengi", "Siyah", "Yeşil"],
        "answer": "Altın rengi",
        "plant": "Aurea",
        "plant_name": "Altın rengi belirten Latince sıfat",
        "explanation": "'Aureus', altın veya altın rengi anlamına gelir.",
    },
    {
        "latin": "Glaucus",
        "question": "'Glaucus' bitki rengini tanımlarken ne anlama gelir?",
        "options": [
            "Parlak kırmızı",
            "Mavimsi yeşil veya grimsi mavi",
            "Saf beyaz",
            "Koyu kahverengi",
        ],
        "answer": "Mavimsi yeşil veya grimsi mavi",
        "plant": "Eucalyptus cinerea",
        "plant_name": "Gümüş dolar okaliptüsü",
        "explanation": "'Glaucus', mavimsi yeşil veya grimsi mavi tonlarını anlatır.",
    },
]

# ==========================================
# SESSION STATE
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

        - 🎨 Her soruda bir Latince renk terimi göreceksin.
        - 🌱 Dört seçenek arasından doğru rengi seçeceksin.
        - 🌸 Cevabından sonra bilimsel bitki örneğini göreceksin.
        - ⏱️ Süren ölçülecek.
        - 🏆 Sonuçların liderlik tablosuna eklenecek.
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
    q = QUESTIONS[index]

    st.title("🌿 Latince Botanik Renkleri")
    st.progress((index + 1) / len(QUESTIONS))
    st.caption(f"Soru {index + 1} / {len(QUESTIONS)}")

    st.info(q["question"])

    with st.form(f"question_form_{index}"):

        selected = st.radio(
            "Doğru rengi seç:",
            q["options"],
        )

        submitted = st.form_submit_button("Cevabımı Kontrol Et 🌱")

        if submitted:

            is_correct = selected == q["answer"]

            if is_correct:
                st.session_state.score += 1

            st.session_state.answers.append(
                {
                    "latin": q["latin"],
                    "selected": selected,
                    "correct": q["answer"],
                    "is_correct": is_correct,
                }
            )

            st.session_state.stage = "feedback"
            st.rerun()

# ==========================================
# 3. CEVAP VE BİTKİ ÖRNEĞİ
# ==========================================
elif st.session_state.stage == "feedback":

    index = st.session_state.current_question
    q = QUESTIONS[index]
    answer = st.session_state.answers[-1]

    st.title("🌸 Cevap ve Botanik Örneği")

    if answer["is_correct"]:
        st.success("Doğru cevap! 🎉")
    else:
        st.error("Yanlış cevap. Doğru cevabı aşağıda görebilirsin.")

    st.markdown(f"## 🎨 Doğru renk: {q['answer']}")
    st.caption(f"Latince terim: {q['latin']}")

    st.divider()

    st.subheader("🌱 Örnek bitki")
    st.markdown(f"### *{q['plant']}*")
    st.write(q["plant_name"])
    st.info(q["explanation"])

    st.metric(
        "Mevcut puanın",
        f"{st.session_state.score} / {len(st.session_state.answers)}",
    )

    if index + 1 < len(QUESTIONS):

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

            st.session_state.leaderboard.append(
                {
                    "İsim": st.session_state.name,
                    "Doğru Sayısı": st.session_state.score,
                    "Süre (sn)": st.session_state.elapsed_time,
                }
            )

            st.session_state.stage = "result"
            st.rerun()

# ==========================================
# 4. SONUÇ EKRANI
# ==========================================
elif st.session_state.stage == "result":

    st.title("🏆 Quiz Sonucu")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Doğru Sayısı",
            f"{st.session_state.score} / {len(QUESTIONS)}",
        )

    with col2:
        st.metric(
            "Tamamlama Süresi",
            f"{st.session_state.elapsed_time} saniye",
        )

    if st.session_state.score == len(QUESTIONS):
        st.balloons()
        st.success("Mükemmel! Bütün soruları doğru cevapladın! 🌿")
    elif st.session_state.score >= len(QUESTIONS) / 2:
        st.success("Güzel iş! Botanik renkleri bilgin gelişiyor.")
    else:
        st.info("Tekrar deneyerek renk bilgini geliştirebilirsin.")

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

    st.dataframe(df, use_container_width=True)

    st.caption(
        "Sıralama önce doğru cevap sayısına, eşitlik durumunda "
        "en kısa tamamlama süresine göre yapılır."
    )

    if st.button("Yeniden Oyna 🔄", use_container_width=True):

        st.session_state.stage = "register"
        st.session_state.name = ""
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.elapsed_time = 0.0

        st.rerun()
