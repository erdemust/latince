import random
import time
import pandas as pd
import streamlit as st

# ==========================================
# SAYFA YAPILANDIRMASI VE ÖZEL CSS TASARIMI
# ==========================================
st.set_page_config(
    page_title="Latince Botanik Renkleri Quiz",
    page_icon="🌿",
    layout="centered",
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        border-color: #2e7d32;
        color: #2e7d32;
    }
    .card-box {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        color: #1e293b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# DOĞRULANMIŞ VE ZENGİNLEŞTİRİLMİŞ SORU HAVUZU
# ==========================================
QUESTIONS = [
    {
        "latin": "Albus",
        "question": "'Albus' hangi rengi ifade eder?",
        "options": ["Siyah", "Beyaz", "Kırmızı", "Sarı"],
        "answer": "Beyaz",
        "plant": "Nymphaea alba",
        "plant_name": "Beyaz Nilüfer",
        "explanation": "'Alba', saf beyaz çiçekleri ve yapıları tanımlamak için kullanılır.",
    },
    {
        "latin": "Niger",
        "question": "'Niger' hangi rengi ifade eder?",
        "options": ["Yeşil", "Mavi", "Siyah", "Pembe"],
        "answer": "Siyah",
        "plant": "Sambucus nigra",
        "plant_name": "Kara Mürver",
        "explanation": "'Nigra', siyah veya çok koyu renkli meyve ve gövdeleri belirtir.",
    },
    {
        "latin": "Ruber",
        "question": "'Ruber' hangi rengi ifade eder?",
        "options": ["Kırmızı", "Mor", "Gri", "Beyaz"],
        "answer": "Kırmızı",
        "plant": "Acer rubrum",
        "plant_name": "Kırmızı Akçaağaç",
        "explanation": "'Rubrum', sonbaharda kızaran yaprakları ve kırmızı çiçekleri niteler.",
    },
    {
        "latin": "Roseus",
        "question": "'Roseus' hangi rengi ifade eder?",
        "options": ["Turuncu", "Kahverengi", "Sarı", "Pembe"],
        "answer": "Pembe",
        "plant": "Catharanthus roseus",
        "plant_name": "Pembe Cezayir Menekşesi",
        "explanation": "'Roseus', gül pembesi tonlarındaki çiçekleri tanımlar.",
    },
    {
        "latin": "Purpureus",
        "question": "'Purpureus' hangi rengi ifade eder?",
        "options": ["Mavi", "Mor", "Yeşil", "Gümüş"],
        "answer": "Mor",
        "plant": "Echinacea purpurea",
        "plant_name": "Mor Ekinezya",
        "explanation": "'Purpurea', erguvan ve mor tonlarındaki çiçek yapısını ifade eder.",
    },
    {
        "latin": "Violaceus",
        "question": "'Violaceus' hangi rengi ifade eder?",
        "options": ["Kahverengi", "Sarı", "Menekşe moru", "Beyaz"],
        "answer": "Menekşe moru",
        "plant": "Viola odorata",
        "plant_name": "Kokulu Menekşe",
        "explanation": "'Violaceus', menekşe moru tonlarını ve renk geçişlerini belirtir.",
    },
    {
        "latin": "Caeruleus",
        "question": "'Caeruleus' hangi rengi ifade eder?",
        "options": ["Gri", "Mavi", "Siyah", "Kırmızı"],
        "answer": "Mavi",
        "plant": "Ceratostigma plumbaginoides",
        "plant_name": "Mavi Kurşun Otu",
        "explanation": "'Caeruleus', gök mavisi ve canlı mavi tonları simgeler.",
    },
    {
        "latin": "Flavus",
        "question": "'Flavus' hangi rengi ifade eder?",
        "options": ["Yeşil", "Mor", "Pembe", "Sarı"],
        "answer": "Sarı",
        "plant": "Rosa foetida",
        "plant_name": "Yabani Sarı Gül",
        "explanation": "'Flavus', bitkilerde saf sarı renk tonlarını ifade eder.",
    },
    {
        "latin": "Luteus",
        "question": "'Luteus' hangi rengi ifade eder?",
        "options": ["Sarı", "Mavi", "Siyah", "Gri"],
        "answer": "Sarı",
        "plant": "Iris pseudacorus",
        "plant_name": "Sarı Süsen",
        "explanation": "'Luteus', altın sarısı ve sarı tonlardaki çiçekleri tanımlar.",
    },
    {
        "latin": "Aureus",
        "question": "'Aureus' hangi rengi ifade eder?",
        "options": ["Gümüş", "Kahverengi", "Altın rengi", "Mor"],
        "answer": "Altın rengi",
        "plant": "Cytisus scoparius",
        "plant_name": "Altın Sarısı Katırtırnağı",
        "explanation": "'Aureus', parlak altın sarısı görünümü vurgular.",
    },
    {
        "latin": "Viridis",
        "question": "'Viridis' hangi rengi ifade eder?",
        "options": ["Kırmızı", "Yeşil", "Pembe", "Turuncu"],
        "answer": "Yeşil",
        "plant": "Helleborus viridis",
        "plant_name": "Yeşil Çöpleme",
        "explanation": "'Viridis', yaprak ve gövdelerdeki yeşil rengi temsil eder.",
    },
    {
        "latin": "Glaucus",
        "question": "'Glaucus' bitki rengini tanımlarken ne anlama gelir?",
        "options": ["Parlak sarı", "Koyu kırmızı", "Saf beyaz", "Mavimsi yeşil veya grimsi mavi"],
        "answer": "Mavimsi yeşil veya grimsi mavi",
        "plant": "Glaucium flavum",
        "plant_name": "Boynuzlu Gelincik",
        "explanation": "'Glaucus', mumsu veya puslu görünen mavimsi yeşil yaprakları tanımlar.",
    },
    {
        "latin": "Cinereus",
        "question": "'Cinereus' hangi renk tonunu ifade eder?",
        "options": ["Kül grisi", "Altın sarısı", "Pembe", "Mor"],
        "answer": "Kül grisi",
        "plant": "Eucalyptus cinerea",
        "plant_name": "Gümüş Dolar Okaliptüsü",
        "explanation": "'Cinereus', kül grisi tonlardaki yaprak yüzeylerini belirtir.",
    },
    {
        "latin": "Brunneus",
        "question": "'Brunneus' hangi rengi ifade eder?",
        "options": ["Beyaz", "Mavi", "Kahverengi", "Pembe"],
        "answer": "Kahverengi",
        "plant": "Castanea sativa",
        "plant_name": "Anadolu Kestanesi",
        "explanation": "'Brunneus', kahverengi gövde ve kabuk dokularını tanımlar.",
    },
    {
        "latin": "Fuscus",
        "question": "'Fuscus' hangi renk tonunu ifade eder?",
        "options": ["Açık mavi", "Koyu kahverengi veya esmer", "Kar beyazı", "Parlak pembe"],
        "answer": "Koyu kahverengi veya esmer",
        "plant": "Carex fusca",
        "plant_name": "Esmer Saz",
        "explanation": "'Fuscus', koyu kahverengi ve esmer tonları ifade eden bir sıfattır.",
    },
    {
        "latin": "Fulvus",
        "question": "'Fulvus' hangi renk tonunu ifade eder?",
        "options": ["Mavi", "Siyah", "Mor", "Sarımsı kahverengi"],
        "answer": "Sarımsı kahverengi",
        "plant": "Hemerocallis fulva",
        "plant_name": "Sarımsı Kahverengi Zambak",
        "explanation": "'Fulvus', toprak tonlarını andıran sarımsı kahverengi renkleri tanımlar.",
    },
    {
        "latin": "Rufus",
        "question": "'Rufus' hangi rengi ifade eder?",
        "options": ["Kızıl veya kızıl kahverengi", "Yeşil", "Beyaz", "Gök mavisi"],
        "answer": "Kızıl veya kızıl kahverengi",
        "plant": "Lactarius rufus",
        "plant_name": "Kızıl Mantar",
        "explanation": "'Rufus', kızıl ile kızıl kahverengi arasındaki tonları belirtir.",
    },
    {
        "latin": "Atropurpureus",
        "question": "'Atropurpureus' hangi renk tonunu ifade eder?",
        "options": ["Açık sarı", "Çok koyu mor", "Beyaz", "Gümüş"],
        "answer": "Çok koyu mor",
        "plant": "Acer palmatum 'Atropurpureum'",
        "plant_name": "Mor Yapraklı Japon Akçaağacı",
        "explanation": "'Atropurpureus', siyaha yakın çok koyu mor yapraklı formları niteler.",
    },
    {
        "latin": "Pallidus",
        "question": "'Pallidus' ne anlama gelir?",
        "options": ["Çok parlak", "Koyu siyah", "Soluk veya açık renkli", "Altın rengi"],
        "answer": "Soluk veya açık renkli",
        "plant": "Iris pallida",
        "plant_name": "Soluk Süsen",
        "explanation": "'Pallidus', soluk renkli çiçek ve yaprak kısımlarını açıklar.",
    },
    {
        "latin": "Argenteus",
        "question": "'Argenteus' hangi rengi ifade eder?",
        "options": ["Turuncu", "Kahverengi", "Kırmızı", "Gümüş rengi"],
        "answer": "Gümüş rengi",
        "plant": "Convolvulus cneorum",
        "plant_name": "Gümüşi Çalı",
        "explanation": "'Argenteus', parıltılı gümüşi yaprak tüylerini ifade eder.",
    },
    {
        "latin": "Cupreus",
        "question": "'Cupreus' hangi rengi ifade eder?",
        "options": ["Bakır rengi", "Mavi", "Beyaz", "Pembe"],
        "answer": "Bakır rengi",
        "plant": "Carex buchananii",
        "plant_name": "Bakırımsı Saz",
        "explanation": "'Cupreus', bakırımsı kahverengi tonları simgeler.",
    },
    {
        "latin": "Lilacinus",
        "question": "'Lilacinus' hangi rengi ifade eder?",
        "options": ["Yeşil", "Leylak rengi", "Siyah", "Sarı"],
        "answer": "Leylak rengi",
        "plant": "Syringa vulgaris",
        "plant_name": "Adi Leylak",
        "explanation": "'Lilacinus', leylak rengi ve açık mor çiçek kümelerini tanımlar.",
    },
    {
        "latin": "Lacteus",
        "question": "'Lacteus' hangi rengi ifade eder?",
        "options": ["Koyu kahverengi", "Mor", "Süt beyazı", "Turuncu"],
        "answer": "Süt beyazı",
        "plant": "Euphorbia lactea",
        "plant_name": "Süt Ağacı",
        "explanation": "'Lacteus', süt gibi saf ve yumuşak beyaz renk tonlarını ifade eder.",
    },
    {
        "latin": "Niveus",
        "question": "'Niveus' hangi rengi ifade eder?",
        "options": ["Kızıl", "Yeşil", "Mavi", "Kar beyazı"],
        "answer": "Kar beyazı",
        "plant": "Galanthus nivalis",
        "plant_name": "Kardelen",
        "explanation": "'Niveus', kar gibi parlak ve saf beyaz renk tonlarını tanımlar.",
    },
    {
        "latin": "Bicolor",
        "question": "'Bicolor' ne anlama gelir?",
        "options": ["İki renkli", "Tek renkli", "Renksiz", "Kül grisi"],
        "answer": "İki renkli",
        "plant": "Viola tricolor",
        "plant_name": "Hercai Menekşe",
        "explanation": "'Bicolor', aynı yapıda iki farklı rengi barındıran türleri belirtir.",
    },
    {
        "latin": "Tricolor",
        "question": "'Tricolor' ne anlama gelir?",
        "options": ["Siyah", "Üç renkli", "Altın sarısı", "Gri"],
        "answer": "Üç renkli",
        "plant": "Viola tricolor",
        "plant_name": "Hercai Menekşe",
        "explanation": "'Tricolor', çiçeklerinde üç ayrı rengi aynı anda taşıyan türleri ifade eder.",
    },
    {
        "latin": "Versicolor",
        "question": "'Versicolor' ne anlama gelir?",
        "options": ["Beyaz", "Kırmızı", "Çok renkli veya renk değiştiren", "Koyu yeşil"],
        "answer": "Çok renkli veya renk değiştiren",
        "plant": "Iris versicolor",
        "plant_name": "Çok Renkli Süsen",
        "explanation": "'Versicolor', zamanla renk değiştiren veya çok renkli yapıları belirtir.",
    },
    {
        "latin": "Coccineus",
        "question": "'Coccineus' hangi rengi ifade eder?",
        "options": ["Gri", "Parlak kırmızı", "Mavimsi yeşil", "Kahverengi"],
        "answer": "Parlak kırmızı",
        "plant": "Salvia coccinea",
        "plant_name": "Kırmızı Çiçekli Adaçayı",
        "explanation": "'Coccineus', göz alıcı canlı ve parlak kırmızı renk tonlarını ifade eder.",
    },
    {
        "latin": "Sanguineus",
        "question": "'Sanguineus' hangi rengi ifade eder?",
        "options": ["Kan kırmızısı", "Soluk sarı", "Gümüş", "Yeşil"],
        "answer": "Kan kırmızısı",
        "plant": "Cornus sanguinea",
        "plant_name": "Kızılcık",
        "explanation": "'Sanguineus', derin kan kırmızısı renk tonlarını ve kabukları tanımlar.",
    },
    {
        "latin": "Pallens",
        "question": "'Pallens' hangi özelliği ifade eder?",
        "options": ["Çok koyu", "Altın rengi", "Soluk veya solgun", "Bakır rengi"],
        "answer": "Soluk veya solgun",
        "plant": "Carex pallens",
        "plant_name": "Soluk Saz",
        "explanation": "'Pallens', rengi solmuş veya soluk görünümdeki bitki kısımlarını belirtir.",
    },
    {
        "latin": "Rubescens",
        "question": "'Rubescens' ne anlama gelir?",
        "options": ["Yeşile dönen", "Kırmızılaşan", "Beyazlaşan", "Maviye dönen"],
        "answer": "Kırmızılaşan",
        "plant": "Geranium rubescens",
        "plant_name": "Kızaran Turnagagası",
        "explanation": "'Rubescens', zamanla kızaran veya kırmızıya dönen kısımları ifade eder.",
    },
    {
        "latin": "Albicans",
        "question": "'Albicans' hangi anlamı taşır?",
        "options": ["Siyahımsı", "Sarımsı", "Beyazımsı", "Kızılımsı"],
        "answer": "Beyazımsı",
        "plant": "Quercus albicans",
        "plant_name": "Beyazımsı Meşe",
        "explanation": "'Albicans', beyaza çalan renk tonlarını ve tüylü yapıları niteler.",
    },
    {
        "latin": "Flavescens",
        "question": "'Flavescens' ne anlama gelir?",
        "options": ["Mavileşen", "Kararan", "Morlaşan", "Sarılaşan"],
        "answer": "Sarılaşan",
        "plant": "Picea abies f. flavescens",
        "plant_name": "Sarılaşan Ladin",
        "explanation": "'Flavescens', sarıya dönen veya sarılaşmakta olan kısımları açıklar.",
    },
    {
        "latin": "Viridescens",
        "question": "'Viridescens' ne anlama gelir?",
        "options": ["Yeşile dönen", "Kırmızılaşan", "Beyazlaşan", "Kararan"],
        "answer": "Yeşile dönen",
        "plant": "Helleborus viridescens",
        "plant_name": "Yeşile Çalan Çöpleme",
        "explanation": "'Viridescens', yeşile çalan veya yeşilimsi tonlara bürünen yapıları belirtir.",
    },
    {
        "latin": "Obscurus",
        "question": "'Obscurus' renk tanımında ne anlama gelir?",
        "options": ["Açık", "Parlak", "Koyu veya karanlık", "Süt beyazı"],
        "answer": "Koyu veya karanlık",
        "plant": "Pinus obscura",
        "plant_name": "Koyu Karaçam",
        "explanation": "'Obscurus', koyu ve karanlık renk tonlarını ifade eder.",
    },
    {
        "latin": "Nitidus",
        "question": "'Nitidus' hangi özelliği anlatır?",
        "options": ["Mat", "Parlak", "Soluk", "Kül grisi"],
        "answer": "Parlak",
        "plant": "Ilex nitida",
        "plant_name": "Parlak Çobanpüskülü",
        "explanation": "'Nitidus', parlak ve cilalı görünüme sahip yaprak yüzeylerini niteler.",
    },
    {
        "latin": "Maculatus",
        "question": "'Maculatus' ne anlama gelir?",
        "options": ["Çizgili", "Düz renkli", "Benekli", "Şeffaf"],
        "answer": "Benekli",
        "plant": "Arum maculatum",
        "plant_name": "Benekli Yılan Yastığı",
        "explanation": "'Maculatus', yaprak veya çiçeklerde benekli desenleri tanımlar.",
    },
    {
        "latin": "Striatus",
        "question": "'Striatus' ne anlama gelir?",
        "options": ["Çizgili", "Beyaz", "Kızıl", "Altın rengi"],
        "answer": "Çizgili",
        "plant": "Crocus striatus",
        "plant_name": "Çizgili Çiğdem",
        "explanation": "'Striatus', çiçek taç yapraklarındaki çizgili desenleri belirtir.",
    },
]

# ==========================================
# OTURUM DURUMU (SESSION STATE)
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
# 1. KAYIT EKRANI
# ==========================================
if st.session_state.stage == "register":
    st.title("🌿 Latince Botanik Renkleri Quiz'i")
    st.markdown(
        "Botanikte sıkça kullanılan Latince renk terimlerini, köklerini ve örnek bitkileri keşfetmek için teste başla!"
    )

    with st.container():
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        with st.form("register_form"):
            name_input = st.text_input(
                "Adınız Soyadınız:", placeholder="Örn: Karl Linnaeus"
            )
            total_questions = st.selectbox(
                "Kaç soru çözmek istersin?",
                [5, 10, 15, 20, len(QUESTIONS)],
                index=1,
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

                    # Soruları ve şıkları karıştır
                    shuffled = QUESTIONS.copy()
                    random.shuffle(shuffled)
                    count = min(total_questions, len(shuffled))
                    selected_questions = shuffled[:count]

                    for q in selected_questions:
                        q["options"] = q["options"].copy()
                        random.shuffle(q["options"])

                    st.session_state.quiz_questions = selected_questions
                    st.session_state.stage = "quiz"
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 2. SORU EKRANI
# ==========================================
elif st.session_state.stage == "quiz":
    questions = st.session_state.quiz_questions
    index = st.session_state.current_question
    q = questions[index]

    st.title("🌿 Latince Botanik Renkleri Testi")
    st.progress((index + 1) / len(questions))
    st.caption(f"Soru {index + 1} / {len(questions)}")

    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.markdown(f"### ❓ {q['question']}")

    with st.form(f"question_form_{index}"):
        selected = st.radio(
            "Seçeneklerden birini işaretle:",
            q["options"],
            index=None,
        )
        submitted = st.form_submit_button("Cevabı Kontrol Et 🌱")

        if submitted:
            if selected is None:
                st.warning("Lütfen bir seçenek seçin.")
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
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 3. GERİBİLDİRİM VE BİTKİ ÖRNEĞİ EKRANI
# ==========================================
elif st.session_state.stage == "feedback":
    questions = st.session_state.quiz_questions
    index = st.session_state.current_question
    q = questions[index]
    answer = st.session_state.answers[-1]

    st.title("🌸 Cevap ve Botanik Örneği")

    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    if answer["is_correct"]:
        st.success("🎉 Doğru cevap!")
    else:
        st.error(
            f"❌ Yanlış cevap. Doğru cevap: **{q['answer']}** olmalıydı."
        )

    st.markdown(f"### 🏷️ Latince Terim: `{q['latin']}`")
    st.divider()
    st.markdown("#### 🌿 Örnek Bitki ve Açıklaması")
    st.markdown(f"**Bilimsel Adı:** *{q['plant']}* ({q['plant_name']})")
    st.info(q["explanation"])

    st.metric(
        "Mevcut Puanın",
        f"{st.session_state.score} / {len(st.session_state.answers)}",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if index + 1 < len(questions):
        if st.button("Sonraki Soru ➡️", use_container_width=True):
            st.session_state.current_question += 1
            st.session_state.stage = "quiz"
            st.rerun()
    else:
        if st.button("Sonuçları Gör 🏆", use_container_width=True):
            st.session_state.elapsed_time = round(
                time.time() - st.session_state.start_time, 2
            )
            st.session_state.leaderboard.append({
                "İsim": st.session_state.name,
                "Doğru Sayısı": st.session_state.score,
                "Süre (sn)": st.session_state.elapsed_time,
            })
            st.session_state.stage = "result"
            st.rerun()

# ==========================================
# 4. SONUÇ VE LİDERLİK TABLOSU EKRANI
# ==========================================
elif st.session_state.stage == "result":
    questions = st.session_state.quiz_questions

    st.title("🏆 Quiz Tamamlandı!")

    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Toplam Doğru",
            f"{st.session_state.score} / {len(questions)}",
        )
    with col2:
        st.metric(
            "Tamamlama Süresi",
            f"{st.session_state.elapsed_time} saniye",
        )

    if st.session_state.score == len(questions):
        st.balloons()
        st.success("Mükemmel! Bütün soruları kusursuz yanıtladın! 🌿🌟")
    elif st.session_state.score >= len(questions) / 2:
        st.success("Harika iş! Botanik renk bilgini oldukça geliştirdin.")
    else:
        st.info("Tekrar deneyerek latince terimlerdeki ustalığını artırabilirsin.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("📋 Cevap Özeti")
    with st.expander("Detaylı soru incelemesi için tıkla"):
        for i, answer in enumerate(st.session_state.answers):
            symbol = "✅" if answer["is_correct"] else "❌"
            st.write(
                f"{symbol} **{i + 1}. {answer['latin']}** — "
                f"Senin cevabın: *{answer['selected']}* | "
                f"Doğru cevap: *{answer['correct']}*"
            )

    st.divider()
    st.subheader("🌟 En İyi Botanistler (Liderlik Tablosu)")

    df = pd.DataFrame(st.session_state.leaderboard)
    df = df.sort_values(
        by=["Doğru Sayısı", "Süre (sn)"],
        ascending=[False, True],
    ).reset_index(drop=True)
    df.index = df.index + 1

    st.dataframe(df, use_container_width=True)
    st.caption(
        "📌 Sıralama kuralı: Önce en yüksek doğru sayısı, eşitlik durumunda en kısa süre baz alınır."
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
