import random
import pandas as pd
import streamlit as st


# ============================================================
# 1. SAYFA AYARLARI
# ============================================================

st.set_page_config(
    page_title="Botanica Akademi | Latince Botanik",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. PREMIUM TASARIM SİSTEMİ (CSS)
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --botanica-green: #3ddc97;
        --botanica-deep: #123c2d;
        --botanica-soft: #e5f7ed;
    }

    .stApp {
        background: radial-gradient(
            ellipse at top left,
            rgba(61, 220, 151, 0.09),
            transparent 40%
        );
    }

    .block-container {
        max-width: 900px;
        padding: 2rem 1.2rem 4rem;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    .hero {
        padding: 2.2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(61, 220, 151, .25);
        border-radius: 26px;
        background: linear-gradient(
            135deg,
            rgba(18, 60, 45, .98),
            rgba(23, 83, 60, .94)
        );
        color: #f4fff8;
        box-shadow: 0 18px 45px rgba(0, 0, 0, .10);
    }

    .eyebrow {
        color: #7df0b8;
        font-size: .76rem;
        font-weight: 850;
        letter-spacing: .16em;
        text-transform: uppercase;
        margin-bottom: .7rem;
    }

    .hero h1 {
        color: #ffffff;
        font-size: clamp(2rem, 6vw, 3.3rem);
        font-weight: 900;
        letter-spacing: -.055em;
        line-height: 1.1;
        margin: .2rem 0 1rem;
    }

    .hero p {
        color: #d9f5e5;
        line-height: 1.8;
        font-size: 1rem;
    }

    .latin {
        font-size: clamp(2.3rem, 8vw, 4rem);
        font-weight: 900;
        font-style: italic;
        letter-spacing: -.055em;
        overflow-wrap: anywhere;
        line-height: 1.1;
        margin: .6rem 0 1rem;
        color: var(--botanica-deep);
    }

    .panel {
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(61, 220, 151, 0.2);
        border-radius: 22px;
        background: rgba(255, 255, 255, 0.8);
    }

    .stButton > button,
    .stFormSubmitButton > button {
        min-height: 48px;
        width: 100%;
        border-radius: 13px;
        font-weight: 750;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. VERİ YÜKLEME FONKSİYONU (questions.csv'den Okuma)
# ============================================================

@st.cache_data
def load_questions_from_csv():
    try:
        df = pd.read_csv("botanical_terms.csv")
    except FileNotFoundError:
        st.error("⚠️ 'questions.csv' dosyası bulunamadı! Lütfen ana dizine ekleyin.")
        return []

    result = []
    seen = set()

    for _, row in df.iterrows():
        latin = str(row["latin"]).strip()
        answer = str(row["answer"]).strip()
        
        # Seçenekleri virgülle ayırıp liste yapıyoruz
        options_raw = str(row["options"])
        options = [opt.strip() for opt in options_raw.split(",")]

        plant = str(row["plant"])
        plant_name = str(row["plant_name"])
        explanation = str(row["explanation"])

        if not latin or not answer:
            continue

        if latin.casefold() in seen:
            continue

        seen.add(latin.casefold())

        # Seçeneklerin tekrarsız olmasını sağlama
        options = list(dict.fromkeys(opt for opt in options if opt))

        if answer not in options:
            options.append(answer)

        if len(options) < 4:
            continue

        result.append({
            "latin": latin,
            "question": f"'{latin}' Latince terimi hangi anlama gelir?",
            "answer": answer,
            "options": options,
            "plant": plant,
            "plant_name": plant_name,
            "explanation": explanation,
        })

    return result


QUESTIONS = load_questions_from_csv()


# ============================================================
# 4. SESSION STATE BAŞLANGIÇ DEĞERLERİ
# ============================================================

DEFAULTS = {
    "stage": "register",       # 'register', 'quiz', 'result'
    "name": "",
    "score": 0,
    "quiz_questions": [],
    "current_question": 0,
    "selected_answer": None,
    "show_explanation": False,
    "quiz_length": 10,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# 5. UYGULAMA AKIŞI (PAGES / STAGES)
# ============================================================

# --- AŞAMA 1: GİRİŞ / KAYIT ---
if st.session_state.stage == "register":
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">🌿 Botanica Akademi</div>
            <h1>Latince Botanik Terimleri Sınavı</h1>
            <p>Bitki adlarında geçen Latince sıfatların, renklerin ve morfolojik terimlerin anlamlarını keşfedin, bilginizi test edin!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not QUESTIONS:
        st.warning("Yüklenecek soru bulunamadı. Lütfen `questions.csv` dosyanızı kontrol edin.")
    else:
        with st.form("register_form"):
            st.subheader("Quiz'e Başlamak İçin Bilgilerinizi Girin")
            user_name = st.text_input("Adınız Soyadınız", placeholder="Örn: Doğa Sever")
            
            # Soru sayısı seçimi (Havuzdaki soru sayısını aşmayacak şekilde)
            max_q = min(len(QUESTIONS), 30)
            default_q = min(10, max_q)
            q_count = st.slider("Soru Sayısı", min_value=5, max_value=max_q, value=default_q)

            submitted = st.form_submit_button("Testi Başlat 🚀")

            if submitted:
                if user_name.strip():
                    st.session_state.name = user_name.strip()
                    st.session_state.quiz_length = q_count
                    # Soruları rastgele karıştırıp seçelim
                    st.session_state.quiz_questions = random.sample(QUESTIONS, q_count)
                    st.session_state.score = 0
                    st.session_state.current_question = 0
                    st.session_state.selected_answer = None
                    st.session_state.show_explanation = False
                    st.session_state.stage = "quiz"
                    st.rerun()
                else:
                    st.warning("Lütfen devam etmek için adınızı girin.")


# --- AŞAMA 2: QUIZ EKRANI ---
elif st.session_state.stage == "quiz":
    q_list = st.session_state.quiz_questions
    idx = st.session_state.current_question

    if idx >= len(q_list):
        st.session_state.stage = "result"
        st.rerun()

    q_data = q_list[idx]

    # İlerleme Çubuğu
    progress = (idx + 1) / len(q_list)
    st.progress(progress, text=f"Soru {idx + 1} / {len(q_list)}")

    st.markdown(f"### Soru {idx + 1}")
    st.markdown(f"**'{q_data['latin']}'** teriminin Türkçe karşılığı nedir?")
    
    # Şıkların her soruda karışık gelmesi için geçici karıştırma (Session State ile sabitlenebilir veya anlık shuffle)
    if "current_options" not in st.session_state or st.session_state.get("active_q_idx") != idx:
        opts = q_data["options"].copy()
        random.shuffle(opts)
        st.session_state.current_options = opts
        st.session_state.active_q_idx = idx

    options = st.session_state.current_options

    # Cevap verilmediyse seçim formu/butonları
    if not st.session_state.show_explanation:
        with st.form(f"question_form_{idx}"):
            choice = st.radio("Seçenekler:", options, index=None, key=f"radio_{idx}")
            submit_answer = st.form_submit_button("Cevapla")

            if submit_answer:
                if choice is not None:
                    st.session_state.selected_answer = choice
                    st.session_state.show_explanation = True
                    if choice == q_data["answer"]:
                        st.session_state.score += 1
                    st.rerun()
                else:
                    st.warning("Lütfen bir seçenek işaretleyin.")
    else:
        # Cevap verildi, açıklamaları ve doğru/yanlış durumunu göster
        user_choice = st.session_state.selected_answer
        correct_answer = q_data["answer"]

        if user_choice == correct_answer:
            st.success(f"🎉 Doğru! Tebrikler.")
        else:
            st.error(f"❌ Yanlış. Doğru cevap: **{correct_answer}**")

        # Detaylı Açıklama Paneli
        st.markdown(
            f"""
            <div class="panel">
                <h4>📚 Detaylı Açıklama</h4>
                <p><b>Örnek Bitki:</b> <i>{q_data['plant']}</i> ({q_data['plant_name']})</p>
                <p>{q_data['explanation']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Sonraki Soruye Geç ➡️"):
            st.session_state.current_question += 1
            st.session_state.show_explanation = False
            st.session_state.selected_answer = None
            if st.session_state.current_question >= len(q_list):
                st.session_state.stage = "result"
            st.rerun()


# --- AŞAMA 3: SONUÇ EKRANI ---
elif st.session_state.stage == "result":
    score = st.session_state.score
    total = len(st.session_state.quiz_questions)
    success_rate = (score / total) * 100

    st.markdown(
        f"""
        <div class="hero" style="text-align: center;">
            <div class="eyebrow">Tebrikler, {st.session_state.name}! 🎉</div>
            <h1>Quiz Tamamlandı</h1>
            <p style="font-size: 1.5rem; margin-top: 1rem;">Skorunuz: <b>{score} / {total}</b> (%{success_rate:.0f})</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if success_rate >= 80:
        st.balloons()
        st.success("Mükemmel! Latince botanik terimlerine oldukça hakimsin.")
    elif success_rate >= 50:
        st.info("İyi iş! Birkaç tekrarla çok daha iyi olacağına emin olabilirsin.")
    else:
        st.warning("Botanik terimlerini pekiştirmek için tekrar denemek isteyebilirsin.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yeniden Başla 🔄"):
            st.session_state.stage = "register"
            st.session_state.score = 0
            st.session_state.current_question = 0
            st.session_state.show_explanation = False
            st.rerun()
