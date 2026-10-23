import time
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Latince Botanik Renkleri Quiz",
    page_icon="🌿",
    layout="centered",
)

# ==========================================
# SORU HAVUZU
# Doğru cevaplar farklı şıklara dağıtılır.
# ==========================================
QUESTIONS = [
    {
        "latin": "Albus",
        "question": "'Albus' hangi rengi ifade eder?",
        "options": ["Siyah", "Beyaz", "Kırmızı", "Sarı"],
        "answer": "Beyaz",
        "plant": "Nymphaea alba",
        "plant_name": "Beyaz nilüfer",
        "explanation": "'Alba', beyaz anlamına gelir.",
    },
    {
        "latin": "Niger",
        "question": "'Niger' hangi rengi ifade eder?",
        "options": ["Yeşil", "Mavi", "Siyah", "Pembe"],
        "answer": "Siyah",
        "plant": "Sambucus nigra",
        "plant_name": "Kara mürver",
        "explanation": "'Nigra', siyah anlamına gelir.",
    },
    {
        "latin": "Ruber",
        "question": "'Ruber' hangi rengi ifade eder?",
        "options": ["Kırmızı", "Mor", "Gri", "Beyaz"],
        "answer": "Kırmızı",
        "plant": "Trifolium rubens",
        "plant_name": "Kızıl çayır üçgülü",
        "explanation": "'Rubens', kızıl veya kırmızımsı anlamıyla ilişkilidir.",
    },
    {
        "latin": "Roseus",
        "question": "'Roseus' hangi rengi ifade eder?",
        "options": ["Turuncu", "Kahverengi", "Sarı", "Pembe"],
        "answer": "Pembe",
        "plant": "Dianthus",
        "plant_name": "Karanfil cinsi",
        "explanation": "'Roseus', gül pembesi veya pembe anlamına gelir.",
    },
    {
        "latin": "Purpureus",
        "question": "'Purpureus' hangi rengi ifade eder?",
        "options": ["Mavi", "Mor", "Yeşil", "Gümüş"],
        "answer": "Mor",
        "plant": "Echinacea purpurea",
        "plant_name": "Mor ekinezya",
        "explanation": "'Purpurea', mor veya erguvan tonlarını ifade eder.",
    },
    {
        "latin": "Violaceus",
        "question": "'Violaceus' hangi rengi ifade eder?",
        "options": ["Kahverengi", "Sarı", "Menekşe moru", "Beyaz"],
        "answer": "Menekşe moru",
        "plant": "Viola odorata",
        "plant_name": "Kokulu menekşe",
        "explanation": "'Violaceus', menekşe moru anlamına gelir.",
    },
    {
        "latin": "Caeruleus",
        "question": "'Caeruleus' hangi rengi ifade eder?",
        "options": ["Gri", "Mavi", "Siyah", "Kırmızı"],
        "answer": "Mavi",
        "plant": "Plumbago auriculata",
        "plant_name": "Mavi yasemin",
        "explanation": "'Caeruleus', mavi veya gök mavisi anlamına gelir.",
    },
    {
        "latin": "Flavus",
        "question": "'Flavus' hangi rengi ifade eder?",
        "options": ["Yeşil", "Mor", "Pembe", "Sarı"],
        "answer": "Sarı",
        "plant": "Rosa foetida",
        "plant_name": "Sarı gül",
        "explanation": "'Flavus', sarı anlamına gelir.",
    },
    {
        "latin": "Luteus",
        "question": "'Luteus' hangi rengi ifade eder?",
        "options": ["Sarı", "Mavi", "Siyah", "Gri"],
        "answer": "Sarı",
        "plant": "Iris pseudacorus",
        "plant_name": "Sarı süsen",
        "explanation": "'Luteus', sarı anlamına gelir.",
    },
    {
        "latin": "Aureus",
        "question": "'Aureus' hangi rengi ifade eder?",
        "options": ["Gümüş", "Kahverengi", "Altın rengi", "Mor"],
        "answer": "Altın rengi",
        "plant": "Forsythia",
        "plant_name": "Altın çanı olarak bilinen çalı cinsi",
        "explanation": "'Aureus', altın veya altın rengi anlamına gelir.",
    },
    {
        "latin": "Viridis",
        "question": "'Viridis' hangi rengi ifade eder?",
        "options": ["Kırmızı", "Yeşil", "Pembe", "Turuncu"],
        "answer": "Yeşil",
        "plant": "Helleborus viridis",
        "plant_name": "Yeşil çöpleme",
        "explanation": "'Viridis', yeşil anlamına gelir.",
    },
    {
        "latin": "Glaucus",
        "question": "'Glaucus' bitki rengini tanımlarken ne anlama gelir?",
        "options": ["Parlak sarı", "Koyu kırmızı", "Saf beyaz", "Mavimsi yeşil veya grimsi mavi"],
        "answer": "Mavimsi yeşil veya grimsi mavi",
        "plant": "Eucalyptus cinerea",
        "plant_name": "Gümüş dolar okaliptüsü",
        "explanation": "'Glaucus', mavimsi yeşil veya grimsi mavi tonlarını ifade eder.",
    },
    {
        "latin": "Cinereus",
        "question": "'Cinereus' hangi renk tonunu ifade eder?",
        "options": ["Kül grisi", "Altın sarısı", "Pembe", "Mor"],
        "answer": "Kül grisi",
        "plant": "Eucalyptus cinerea",
        "plant_name": "Gümüş dolar okaliptüsü",
        "explanation": "'Cinereus', kül grisi anlamına gelir.",
    },
    {
        "latin": "Brunneus",
        "question": "'Brunneus' hangi rengi ifade eder?",
        "options": ["Beyaz", "Mavi", "Kahverengi", "Pembe"],
        "answer": "Kahverengi",
        "plant": "Brunfelsia",
        "plant_name": "Brunfelsia bitki cinsi",
        "explanation": "'Brunneus', kahverengi anlamına gelir.",
    },
    {
        "latin": "Fuscus",
        "question": "'Fuscus' hangi renk tonunu ifade eder?",
        "options": ["Açık mavi", "Koyu kahverengi veya esmer", "Kar beyazı", "Parlak pembe"],
        "answer": "Koyu kahverengi veya esmer",
        "plant": "Renk sıfatı örneği",
        "plant_name": "Botanikte koyu renkleri anlatan sıfat",
        "explanation": "'Fuscus', koyu kahverengi veya esmer tonları ifade eder.",
    },
    {
        "latin": "Fulvus",
        "question": "'Fulvus' hangi renk tonunu ifade eder?",
        "options": ["Mavi", "Siyah", "Mor", "Sarımsı kahverengi"],
        "answer": "Sarımsı kahverengi",
        "plant": "Renk sıfatı örneği",
        "plant_name": "Botanikte sarımsı kahverengi tonunu anlatan sıfat",
        "explanation": "'Fulvus', sarımsı kahverengi veya boz tonları ifade eder.",
    },
    {
        "latin": "Rufus",
        "question": "'Rufus' hangi rengi ifade eder?",
        "options": ["Kızıl veya kızıl kahverengi", "Yeşil", "Beyaz", "Gök mavisi"],
        "answer": "Kızıl veya kızıl kahverengi",
        "plant": "Renk sıfatı örneği",
        "plant_name": "Botanikte kızıl tonlarını anlatan sıfat",
        "explanation": "'Rufus', kızıl veya kızıl kahverengi anlamına gelir.",
    },
    {
        "latin": "Atropurpureus",
        "question": "'Atropurpureus' hangi renk tonunu ifade eder?",
        "options": ["Açık sarı", "Çok koyu mor", "Beyaz", "Gümüş"],
        "answer": "Çok koyu mor",
        "plant": "Ocimum tenuiflorum",
        "plant_name": "Fesleğen türlerinden kutsal fesleğen",
        "explanation": "'Atropurpureus', siyaha yaklaşan çok koyu mor tonunu ifade eder.",
    },
    {
        "latin": "Pallidus",
        "question": "'Pallidus' ne anlama gelir?",
        "options": ["Çok parlak", "Koyu siyah", "Soluk veya açık renkli", "Altın rengi"],
        "answer": "Soluk veya açık renkli",
        "plant": "Renk sıfatı örneği",
        "plant_name": "Soluk renkli bitki kısımlarını anlatan sıfat",
        "explanation": "'Pallidus', soluk veya açık renkli anlamına gelir.",
    },
    {
        "latin": "Argenteus",
        "question": "'Argenteus' hangi rengi ifade eder?",
        "options": ["Turuncu", "Kahverengi", "Kırmızı", "Gümüş rengi"],
        "answer": "Gümüş rengi",
        "plant": "Salix alba",
        "plant_name": "Ak söğüt",
        "explanation": "'Argenteus', gümüş rengi veya gümüşi anlamına gelir.",
    },
    {
        "latin": "Cupreus",
        "question": "'Cupreus' hangi rengi ifade eder?",
        "options": ["Bakır rengi", "Mavi", "Beyaz", "Pembe"],
        "answer": "Bakır rengi",
        "plant": "Renk sıfatı örneği",
        "plant_name": "Bakırımsı renkleri anlatan sıfat",
        "explanation": "'Cupreus', bakır rengi anlamına gelir.",
    },
    {
        "latin": "Lilacinus",
        "question": "'Lilacinus' hangi rengi ifade eder?",
        "options": ["Yeşil", "Leylak rengi", "Siyah", "Sarı"],
        "answer": "Leylak rengi",
        "plant": "Syringa vulgaris",
        "plant_name": "Adi leylak",
        "explanation": "'Lilacinus', leylak rengi veya açık mor tonları ifade eder.",
    },
    {
        "latin": "Lacteus",
        "question": "'Lacteus' hangi rengi ifade eder?",
        "options": ["Koyu kahverengi", "Mor", "Süt beyazı", "Turuncu"],
        "answer": "Süt beyazı",
        "plant": "Euphorbia lactea",
        "plant_name": "Süt ağacı olarak bilinen sütleğen türü",
        "explanation": "'Lacteus', süt beyazı anlamına gelir.",
    },
    {
        "latin": "Niveus",
        "question": "'Niveus' hangi rengi ifade eder?",
        "options": ["Kızıl", "Yeşil", "Mavi", "Kar beyazı"],
        "answer": "Kar beyazı",
        "plant": "Galanthus nivalis",
        "plant_name": "Kardelen",
        "explanation": "'Niveus', kar beyazı anlamına gelir.",
    },
    {
        "latin": "Bicolor",
        "question": "'Bicolor' ne anlama gelir?",
        "options": ["İki renkli", "Tek renkli", "Renksiz", "Kül grisi"],
        "answer": "İki renkli",
        "plant": "Viola tricolor",
        "plant_name": "Hercai menekşe",
        "explanation": "'Bicolor', iki renkli anlamına gelir.",
    },
    {
        "latin": "Tricolor",
        "question": "'Tricolor' ne anlama gelir?",
        "options": ["Siyah", "Üç renkli", "Altın sarısı", "Gri"],
        "answer": "Üç renkli",
        "plant": "Viola tricolor",
        "plant_name": "Hercai menekşe",
        "explanation": "'Tricolor', üç renkli anlamına gelir.",
    },
    {
        "latin": "Versicolor",
        "question": "'Versicolor' ne anlama gelir?",
        "options": ["Beyaz", "Kırmızı", "Çok renkli veya renk değiştiren", "Koyu yeşil"],
        "answer": "Çok renkli veya renk değiştiren",
        "plant": "Lantana camara",
        "plant_name": "Mine çalısı",
        "explanation": "'Versicolor', çok renkli veya renk değiştiren anlamına gelir.",
    },
    {
        "latin": "Coccineus",
        "question": "'Coccineus' hangi rengi ifade eder?",
        "options": ["Gri", "Parlak kırmızı", "Mavimsi yeşil", "Kahverengi"],
        "answer": "Parlak kırmızı",
        "plant": "Salvia coccinea",
        "plant_name": "Kırmızı çiçekli adaçayı",
        "explanation": "'Coccineus', parlak kırmızı veya al rengini ifade eder.",
    },
    {
        "latin": "Sanguineus",
        "question": "'Sanguineus' hangi rengi ifade eder?",
        "options": ["Kan kırmızısı", "Soluk sarı", "Gümüş", "Yeşil"],
        "answer": "Kan kırmızısı",
        "plant": "Renk sıfatı örneği",
        "plant_name": "Derin kırmızı tonlarını anlatan sıfat",
        "explanation": "'Sanguineus', kan kırmızısı anlamına gelir.",
    },
    {
        "latin": "Pallens",
        "question": "'Pallens' hangi özelliği ifade eder?",
        "options": ["Çok koyu", "Altın rengi", "Soluk veya solgun", "Bakır rengi"],
        "answer": "Soluk veya solgun",
        "plant": "Renk sıfatı örneği",
        "plant_name": "Solgun renkli bitki kısımlarını anlatan sıfat",
        "explanation": "'Pallens', soluk veya solgun anlamına gelir.",
    },
    {
        "latin": "Rubescens",
        "question": "'Rubescens' ne anlama gelir?",
        "options": ["Yeşile dönen", "Kırmızılaşan", "Beyazlaşan", "Maviye dönen"],
        "answer": "Kırmızılaşan",
        "plant": "Trifolium rubens",
        "plant_name": "Kızıl çayır üçgülü",
        "explanation": "'Rubescens', kızaran veya kırmızılaşan anlamına gelir.",
    },
    {
        "latin": "Albicans",
        "question": "'Albicans' hangi anlamı taşır?",
        "options": ["Siyahımsı", "Sarımsı", "Beyazımsı", "Kızılımsı"],
        "answer": "Beyazımsı",
        "plant": "Renk sıfatı örneği",
        "plant_name": "Beyaza çalan rengi anlatan sıfat",
        "explanation": "'Albicans', beyazımsı anlamına gelir.",
    },
    {
        "latin": "Flavescens",
        "question": "'Flavescens' ne anlama gelir?",
        "options": ["Mavileşen", "Kararan", "Morlaşan", "Sarılaşan"],
        "answer": "Sarılaşan",
        "plant": "Renk sıfatı örneği",
        "plant_name": "Sarıya dönen bitki kısımlarını anlatan sıfat",
        "explanation": "'Flavescens', sarılaşan veya sarımsı anlamına gelir.",
    },
    {
        "latin": "Viridescens",
        "question": "'Viridescens' ne anlama gelir?",
        "options": ["Yeşile dönen", "Kırmızılaşan", "Beyazlaşan", "Kararan"],
        "answer": "Yeşile dönen",
        "plant": "Renk sıfatı örneği",
        "plant_name": "Yeşile çalan rengi anlatan sıfat",
        "explanation": "'Viridescens', yeşilimsi veya yeşile dönen anlamına gelir.",
    },
    {
        "latin": "Obscurus",
        "question": "'Obscurus' renk tanımında ne anlama gelir?",
        "options": ["Açık", "Parlak", "Koyu veya karanlık", "Süt beyazı"],
        "answer": "Koyu veya karanlık",
        "plant": "Renk sıfatı örneği",
        "plant_name": "Koyu renk tonlarını anlatan sıfat",
        "explanation": "'Obscurus', koyu veya karanlık anlamına gelir.",
    },
    {
        "latin": "Nitidus",
        "question": "'Nitidus' hangi özelliği anlatır?",
        "options": ["Mat", "Parlak", "Soluk", "Kül grisi"],
        "answer": "Parlak",
        "plant": "Renk sıfatı örneği",
        "plant_name": "Parlak yüzey görünümünü anlatan sıfat",
        "explanation": "'Nitidus', parlak veya cilalı görünümlü anlamına gelir.",
    },
    {
        "latin": "Maculatus",
        "question": "'Maculatus' ne anlama gelir?",
        "options": ["Çizgili", "Düz renkli", "Benekli", "Şeffaf"],
        "answer": "Benekli",
        "plant": "Pulmonaria officinalis",
        "plant_name": "Akciğer otu",
        "explanation": "'Maculatus', benekli anlamına gelir; doğrudan bir renk değil, desen belirtir.",
    },
    {
        "latin": "Striatus",
        "question": "'Striatus' ne anlama gelir?",
        "options": ["Çizgili", "Beyaz", "Kızıl", "Altın rengi"],
        "answer": "Çizgili",
        "plant": "Renk ve desen sıfatı örneği",
        "plant_name": "Çizgili görünümü anlatan sıfat",
        "explanation": "'Striatus', çizgili anlamına gelir.",
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
    "quiz_questions": [],
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
        st.session_state[key] = (
            value.copy() if isinstance(value, (list, dict)) else value
        )

# ==========================================
# KAYIT EKRANI
# ==========================================
if st.session_state.stage == "register":
    st.title("🌿 Latince Botanik Renkleri Quiz'i")

    st.markdown(
        """
        Botanikte kullanılan Latince renk terimlerini öğren!

        - Her soruda bir Latince terim gösterilir.
        - Dört seçenekten doğru rengi seç.
        - Cevabından sonra bilimsel bitki örneğini öğren.
        - Soruların sırası ve seçeneklerin sırası her oyunda karıştırılır.
        - Sonuçların liderlik tablosuna eklenir.
        """
    )

    with st.form("register_form"):
        name_input = st.text_input(
            "Adınız:",
            placeholder="Örn. Karl Linnaeus",
        )
        total_questions = st.selectbox(
            "Kaç soru çözmek istersin?",
            [10, 15, 20, 30, len(QUESTIONS)],
            index=2,
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

                # Soruları karıştır.
                shuffled = QUESTIONS.copy()
                random.shuffle(shuffled)

                # İstenen soru sayısını belirle.
                count = min(total_questions, len(shuffled))
                selected_questions = shuffled[:count]

                # Her sorunun şıklarını ayrı ayrı karıştır.
                for q in selected_questions:
                    q["options"] = q["options"].copy()
                    random.shuffle(q["options"])

                st.session_state.quiz_questions = selected_questions
                st.session_state.stage = "quiz"
                st.rerun()

# ==========================================
# SORU EKRANI
# ==========================================
elif st.session_state.stage == "quiz":
    questions = st.session_state.quiz_questions
    index = st.session_state.current_question
    q = questions[index]

    st.title("🌿 Latince Botanik Renkleri")
    st.progress((index + 1) / len(questions))
    st.caption(f"Soru {index + 1} / {len(questions)}")

    st.info(q["question"])

    with st.form(f"question_form_{index}"):
        selected = st.radio(
            "Cevabını seç:",
            q["options"],
            index=None,
        )

        submitted = st.form_submit_button("Cevabı Kontrol Et 🌱")

        if submitted:
            if selected is None:
                st.warning("Lütfen bir seçenek seç.")
            else:
                correct = selected == q["answer"]

                if correct:
                    st.session_state.score += 1

                st.session_state.answers.append({
                    "latin": q["latin"],
                    "selected": selected,
                    "correct": q["answer"],
                    "is_correct": correct,
                })

                st.session_state.stage = "feedback"
                st.rerun()

# ==========================================
# CEVAP VE BİTKİ ÖRNEĞİ
# ==========================================
elif st.session_state.stage == "feedback":
    questions = st.session_state.quiz_questions
    index = st.session_state.current_question
    q = questions[index]
    answer = st.session_state.answers[-1]

    st.title("🌸 Cevap ve Botanik Örneği")

    if answer["is_correct"]:
        st.success("Doğru cevap! 🎉")
    else:
        st.error("Yanlış cevap. Doğru cevap aşağıda.")

    st.markdown(f"## 🎨 Doğru renk: {q['answer']}")
    st.caption(f"Latince terim: {q['latin']}")

    st.divider()
    st.subheader("🌱 Bitki örneği")
    st.markdown(f"### *{q['plant']}*")
    st.write(q["plant_name"])
    st.info(q["explanation"])

    st.metric(
        "Mevcut puanın",
        f"{st.session_state.score} / {len(st.session_state.answers)}",
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
# SONUÇ EKRANI
# ==========================================
elif st.session_state.stage == "result":
    questions = st.session_state.quiz_questions

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
    elif st.session_state.score >= len(questions) / 2:
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
        "en kısa süreye göre yapılır."
    )

    if st.button("Yeniden Oyna 🔄", use_container_width=True):
        st.session_state.stage = "register"
        st.session_state.name = ""
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.quiz_questions = []
        st.session_state.elapsed_time = 0.0
        st.rerun()
