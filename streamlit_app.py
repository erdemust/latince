import html
import random
import time
import uuid

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
# 2. PREMIUM TASARIM SİSTEMİ
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
        background:
            radial-gradient(
                ellipse at top left,
                rgba(61, 220, 151, 0.09),
                transparent 40%
            );
    }

    .block-container {
        max-width: 900px;
        padding: 2rem 1.2rem 4rem;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    .hero {
        padding: 2.2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(61, 220, 151, .25);
        border-radius: 26px;
        background:
            linear-gradient(
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

    .hero-badges {
        display: flex;
        flex-wrap: wrap;
        gap: .5rem;
        margin-top: 1.3rem;
    }

    .badge {
        display: inline-block;
        padding: .45rem .75rem;
        border: 1px solid rgba(255, 255, 255, .20);
        border-radius: 999px;
        background: rgba(255, 255, 255, .08);
        color: #eafff2;
        font-size: .8rem;
        font-weight: 650;
    }

    .panel {
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--default-border-color);
        border-radius: 22px;
        background: var(--secondary-background-color);
    }

    .question-card {
        padding: 1.8rem;
        margin: 1.2rem 0;
        border: 1px solid rgba(61, 220, 151, .25);
        border-radius: 24px;
        background:
            linear-gradient(
                145deg,
                var(--secondary-background-color),
                rgba(61, 220, 151, .045)
            );
    }

    .latin {
        font-size: clamp(2.3rem, 8vw, 4rem);
        font-weight: 900;
        font-style: italic;
        letter-spacing: -.055em;
        overflow-wrap: anywhere;
        line-height: 1.1;
        margin: .6rem 0 1rem;
    }

    .question-subtitle {
        opacity: .78;
        font-size: 1.02rem;
        line-height: 1.7;
    }

    .metric-card {
        padding: 1rem;
        min-height: 105px;
        border: 1px solid var(--default-border-color);
        border-radius: 18px;
        background: var(--secondary-background-color);
    }

    .metric-label {
        font-size: .78rem;
        opacity: .7;
        margin-bottom: .45rem;
    }

    .metric-value {
        font-size: clamp(1.35rem, 4vw, 2rem);
        font-weight: 900;
        letter-spacing: -.04em;
        overflow-wrap: anywhere;
    }

    .plant-card {
        padding: 1.5rem;
        border: 1px solid rgba(61, 220, 151, .3);
        border-radius: 22px;
        background: rgba(61, 220, 151, .055);
    }

    .plant-scientific {
        font-size: 1.3rem;
        font-weight: 800;
        font-style: italic;
        overflow-wrap: anywhere;
    }

    .plant-common {
        margin-top: .4rem;
        opacity: .75;
    }

    .explanation {
        margin-top: 1rem;
        padding: 1rem;
        border-left: 4px solid #3ddc97;
        border-radius: 0 12px 12px 0;
        background: rgba(61, 220, 151, .07);
        line-height: 1.8;
    }

    .result-score {
        font-size: clamp(3rem, 12vw, 5.5rem);
        font-weight: 950;
        letter-spacing: -.065em;
        line-height: 1.1;
        color: #7df0b8;
    }

    .section-label {
        font-size: .8rem;
        font-weight: 850;
        letter-spacing: .1em;
        text-transform: uppercase;
        opacity: .7;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        min-height: 48px;
        width: 100%;
        border-radius: 13px;
        font-weight: 750;
        transition: transform .15s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        border-color: #3ddc97;
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(
            90deg,
            #168657,
            #3ddc97
        );
    }

    [data-testid="stMetric"] {
        padding: .8rem;
        border: 1px solid var(--default-border-color);
        border-radius: 15px;
        background: var(--secondary-background-color);
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1rem .8rem 2.5rem;
        }

        .hero {
            padding: 1.35rem;
            border-radius: 20px;
        }

        .question-card {
            padding: 1.2rem;
        }

        .panel {
            padding: 1rem;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *,
        *::before,
        *::after {
            transition: none !important;
            animation: none !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. SORU HAVUZU
# ============================================================
#
# BURAYA ÖNCEKİ KODUNDAKİ RAW_QUESTIONS LİSTESİNİN
# TAMAMINI AYNEN YAPIŞTIR.
#
# Her soru şu biçimde olmalı:
#
# (
#     "Albus",
#     "Beyaz",
#     ["Siyah", "Beyaz", "Kırmızı", "Sarı"],
#     "Nymphaea alba",
#     "Beyaz nilüfer",
#     "'Albus' beyaz anlamına gelir.",
# )
#
# Listeyi yapıştırdıktan sonra aşağıdaki bölümle devam et.
# ============================================================

RAW_QUESTIONS = [
    (
        "Albus",
        "Beyaz",
        ["Siyah", "Beyaz", "Kırmızı", "Sarı"],
        "Nymphaea alba",
        "Beyaz nilüfer",
        "'Albus' beyaz anlamına gelir. 'Alba' dişil biçimidir.",
    ),
    (
        "Niger",
        "Siyah",
        ["Yeşil", "Mavi", "Siyah", "Pembe"],
        "Sambucus nigra",
        "Kara mürver",
        "'Niger' siyah anlamına gelir. 'Nigra' dişil biçimidir.",
    ),
    (
        "Ruber",
        "Kırmızı",
        ["Kırmızı", "Mor", "Gri", "Beyaz"],
        "Trifolium rubens",
        "Kızıl çayır üçgülü",
        "'Ruber' kırmızı anlamına gelir.",
    ),
    (
        "Roseus",
        "Pembe",
        ["Turuncu", "Kahverengi", "Sarı", "Pembe"],
        "Dianthus",
        "Karanfil cinsi",
        "'Roseus' gül pembesi anlamına gelir.",
    ),
    (
        "Purpureus",
        "Mor",
        ["Mavi", "Mor", "Yeşil", "Gümüş"],
        "Echinacea purpurea",
        "Mor ekinezya",
        "'Purpureus' mor veya erguvan tonlarını anlatır.",
    ),
    (
        "Violaceus",
        "Menekşe moru",
        ["Kahverengi", "Sarı", "Menekşe moru", "Beyaz"],
        "Viola odorata",
        "Kokulu menekşe",
        "'Violaceus' menekşe moru anlamına gelir.",
    ),
    (
        "Caeruleus",
        "Mavi",
        ["Gri", "Mavi", "Siyah", "Kırmızı"],
        "Plumbago auriculata",
        "Mavi çiçekli plumbago",
        "'Caeruleus' mavi veya gök mavisi anlamına gelir.",
    ),
    (
        "Flavus",
        "Sarı",
        ["Yeşil", "Mor", "Pembe", "Sarı"],
        "Rosa foetida",
        "Sarı çiçekli gül türü",
        "'Flavus' sarı anlamına gelir.",
    ),
    (
        "Luteus",
        "Sarı",
        ["Sarı", "Mavi", "Siyah", "Gri"],
        "Iris pseudacorus",
        "Sarı süsen",
        "'Luteus' sarı veya sarımsı tonları anlatır.",
    ),
    (
        "Viridis",
        "Yeşil",
        ["Kırmızı", "Yeşil", "Pembe", "Turuncu"],
        "Helleborus viridis",
        "Yeşil çöpleme",
        "'Viridis' yeşil anlamına gelir.",
    ),
]


# ============================================================
# 4. SORU HAVUZUNU DOĞRULAMA
# ============================================================

def build_question_pool():
    """Soru verilerini doğrular ve standartlaştırır."""

    result = []
    seen = set()

    for item in RAW_QUESTIONS:
        if len(item) != 6:
            continue

        latin, answer, options, plant, plant_name, explanation = item

        latin = str(latin).strip()
        answer = str(answer).strip()

        if not latin or not answer:
            continue

        if latin.casefold() in seen:
            continue

        seen.add(latin.casefold())

        options = list(
            dict.fromkeys(
                str(option).strip()
                for option in options
                if option is not None and str(option).strip()
            )
        )

        if answer not in options:
            options.append(answer)

        # En az üç yanlış cevap ve bir doğru cevap gerekir.
        if len(options) < 4:
            continue

        result.append(
            {
                "latin": latin,
                "question": f"'{latin}' hangi rengi veya özelliği ifade eder?",
                "answer": answer,
                "options": options,
                "plant": str(plant),
                "plant_name": str(plant_name),
                "explanation": str(explanation),
            }
        )

    return result


QUESTIONS = build_question_pool()


# ============================================================
# 5. OTURUM DURUMU
# ============================================================

DEFAULTS = {
    "stage": "register",
    "name": "",
    "score": 0,
    "start_time": None,
    "elapsed_time": 0.0,
    "quiz_questions": [],
    "current_question": 0,
    "answers": [],
    "leaderboard": [],
    "run_id": None,
    "submitted_run_id": None,
    "quiz_length": 10,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = (
            value.copy()
            if isinstance(value, (dict, list))
            else value
        )


# ============================================================
# 6. YARDIMCI FONKSİYONLAR
# ============================================================

def safe_text(value):
    """HTML çıktısında metni güvenli hale getirir."""
    return html.escape(str(value))


def format_seconds(seconds):
    """Süreyi dakika ve saniye olarak gösterir."""
    seconds = max(0, int(seconds))
    minutes, remaining = divmod(seconds, 60)

    if minutes:
        return f"{minutes} dk {remaining} sn"

    return f"{remaining} sn"


def metric_card(label, value):
    """Özel tasarımlı metrik kartı oluşturur."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{safe_text(label)}</div>
            <div class="metric-value">{safe_text(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def make_balanced_questions(count):
    """Soruları seçer ve doğru cevapların konumlarını dengeler."""

    if not QUESTIONS:
        raise ValueError("Soru havuzu boş.")

    count = max(1, min(int(count), len(QUESTIONS)))

    source = QUESTIONS.copy()
    random.shuffle(source)

    selected = source[:count]

    # Dört cevap konumunu mümkün olduğunca dengeli kullan.
    positions = [i % 4 for i in range(count)]
    random.shuffle(positions)

    all_answers = list(
        dict.fromkeys(q["answer"] for q in QUESTIONS)
    )

    prepared = []

    for question, correct_position in zip(selected, positions):
        correct_answer = question["answer"]

        distractors = [
            option
            for option in question["options"]
            if option != correct_answer
        ]

        # Yanlış cevaplar mümkün olduğunca anlam bakımından farklı seçilir.
        random.shuffle(distractors)

        for answer in all_answers:
            if answer != correct_answer and answer not in distractors:
                distractors.append(answer)

            if len(distractors) >= 3:
                break

        if len(distractors) < 3:
            continue

        options = distractors[:3]
        options.insert(correct_position, correct_answer)

        if len(set(options)) != 4:
            continue

        item = question.copy()
        item["options"] = options

        prepared.append(item)

    if not prepared:
        raise ValueError(
            "Yeterli sayıda geçerli soru hazırlanamadı."
        )

    return prepared


def start_quiz(name, count):
    """Yeni bir test oturumu oluşturur."""

    name = str(name).strip()

    if not name:
        raise ValueError("Lütfen bir ad veya takma ad gir.")

    questions = make_balanced_questions(count)

    st.session_state.update(
        {
            "stage": "quiz",
            "name": name,
            "score": 0,
            "start_time": time.time(),
            "elapsed_time": 0.0,
            "quiz_questions": questions,
            "current_question": 0,
            "answers": [],
            "run_id": str(uuid.uuid4()),
            "submitted_run_id": None,
            "quiz_length": len(questions),
        }
    )


def save_result():
    """Her test sonucunu oturum içinde yalnızca bir kez kaydeder."""

    run_id = st.session_state.run_id

    if not run_id:
        return

    if st.session_state.submitted_run_id == run_id:
        return

    questions = st.session_state.quiz_questions

    if not questions:
        return

    start_time = st.session_state.start_time

    if start_time is not None:
        elapsed = round(time.time() - start_time, 2)
    else:
        elapsed = 0.0

    st.session_state.elapsed_time = elapsed

    st.session_state.leaderboard.append(
        {
            "İsim": st.session_state.name,
            "Doğru Sayısı": st.session_state.score,
            "Toplam Soru": len(questions),
            "Başarı (%)": round(
                st.session_state.score / len(questions) * 100,
                1,
            ),
            "Süre (sn)": elapsed,
        }
    )

    st.session_state.submitted_run_id = run_id


def reset_quiz(clear_name=False):
    """Test durumunu sıfırlar."""

    st.session_state.update(
        {
            "stage": "register",
            "score": 0,
            "start_time": None,
            "elapsed_time": 0.0,
            "quiz_questions": [],
            "current_question": 0,
            "answers": [],
            "run_id": None,
            "submitted_run_id": None,
        }
    )

    if clear_name:
        st.session_state.name = ""


def render_leaderboard():
    """Sonuçları doğru sayısı ve süreye göre sıralar."""

    records = st.session_state.leaderboard

    if not records:
        st.info(
            "🌱 Henüz sonuç kaydedilmedi. İlk testi tamamlayarak "
            "liderlik tablosunu oluşturabilirsin."
        )
        return

    df = pd.DataFrame(records)

    df = df.sort_values(
        by=["Başarı (%)", "Doğru Sayısı", "Süre (sn)"],
        ascending=[False, False, True],
    ).reset_index(drop=True)

    df.index = df.index + 1
    df.index.name = "Sıra"

    st.dataframe(
        df[
            [
                "İsim",
                "Doğru Sayısı",
                "Toplam Soru",
                "Başarı (%)",
                "Süre (sn)",
            ]
        ],
        use_container_width=True,
    )

    st.caption(
        "Not: Bu tablo mevcut Streamlit oturumunda saklanır. "
        "Kalıcı ve tüm kullanıcıların ortak görebildiği bir "
        "liderlik tablosu için veritabanı gerekir."
    )


# ============================================================
# 7. ORTAK BAŞLIK
# ============================================================

def render_header():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">🌿 BOTANICA AKADEMİ</div>
            <h1>Doğanın Dilini Keşfet.</h1>
            <p>
                Latince botanik terimlerini öğren, renklerin
                ardındaki anlamları keşfet ve bilgini test et.
                Her soru, bitki dünyasına açılan yeni bir kapı.
            </p>
            <div class="hero-badges">
                <span class="badge">🌱 Botanik</span>
                <span class="badge">📚 Latince</span>
                <span class="badge">🎯 Bilgi Yarışması</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 8. KAYIT EKRANI
# ============================================================

def render_register():
    render_header()

    st.subheader("🌱 Yeni Bir Keşfe Başla")

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Soru havuzu", len(QUESTIONS))

    with col2:
        metric_card("Cevap seçeneği", "4")

    with col3:
        metric_card("Kategori", "Botanik")

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    with st.form("register_form"):
        name = st.text_input(
            "Adın veya takma adın",
            value=st.session_state.name,
            placeholder="Örn. Botanica",
            max_chars=50,
        )

        maximum = len(QUESTIONS)

        # Soru sayısı gerçek havuza göre belirlenir.
        count_options = sorted(
            set(
                n
                for n in [5, 10, 15, 20, 30, 50, maximum]
                if 1 <= n <= maximum
            )
        )

        default_count = min(10, maximum)

        selected_count = st.selectbox(
            "Test uzunluğu",
            count_options,
            index=count_options.index(default_count),
            format_func=lambda n: f"{n} soru",
        )

        submitted = st.form_submit_button(
            "Keşfe Başla 🚀",
            use_container_width=True,
            type="primary",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if not name.strip():
            st.warning("Lütfen adını veya bir takma ad gir.")
        else:
            try:
                start_quiz(name, selected_count)
                st.rerun()
            except (ValueError, TypeError, KeyError) as exc:
                st.error(f"Test başlatılamadı: {exc}")

    st.divider()

    st.subheader("🏆 Liderlik Tablosu")
    render_leaderboard()

    with st.expander("📖 Nasıl oynanır?"):
        st.markdown(
            """
            1. Adını gir ve test uzunluğunu belirle.
            2. Latince terimin anlamını bul.
            3. Cevabını kontrol ederek
