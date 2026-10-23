import html
import random
import sqlite3
import time
import uuid
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# 1. UYGULAMA AYARLARI
# ============================================================

st.set_page_config(
    page_title="Botanica Akademi | Öğrenci Sınavı",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "botanica_sinav.db"


# ============================================================
# 2. TASARIM
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --green: #3ddc97;
        --deep: #123c2d;
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at top left,
                rgba(61,220,151,.10),
                transparent 45%
            );
    }

    .block-container {
        max-width: 900px;
        padding: 2rem 1rem 4rem;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    .hero {
        padding: 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(61,220,151,.25);
        border-radius: 24px;
        background: linear-gradient(135deg,#123c2d,#17533c);
        color: #fff;
    }

    .hero h1 {
        color: #fff;
        font-size: clamp(2rem,6vw,3.2rem);
        font-weight: 900;
        line-height: 1.15;
    }

    .hero p {
        color: #d9f5e5;
        line-height: 1.8;
    }

    .latin {
        font-size: clamp(2rem,7vw,3.7rem);
        font-weight: 900;
        font-style: italic;
        overflow-wrap: anywhere;
        line-height: 1.2;
    }

    .panel {
        padding: 1.4rem;
        margin: 1rem 0;
        border: 1px solid var(--default-border-color);
        border-radius: 20px;
        background: var(--secondary-background-color);
    }

    .metric {
        padding: 1rem;
        border: 1px solid var(--default-border-color);
        border-radius: 16px;
        background: var(--secondary-background-color);
    }

    .metric-label {
        opacity: .7;
        font-size: .8rem;
    }

    .metric-value {
        font-size: 1.6rem;
        font-weight: 850;
        overflow-wrap: anywhere;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        min-height: 46px;
        border-radius: 12px;
        font-weight: 750;
    }

    @media(max-width:600px) {
        .hero {
            padding: 1.3rem;
        }

        .panel {
            padding: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. SORU HAVUZU
# ============================================================

RAW_QUESTIONS = [
    (
        "Albus",
        "Beyaz",
        ["Siyah", "Beyaz", "Kırmızı", "Sarı"],
        "Nymphaea alba",
        "Beyaz nilüfer",
        "'Albus' Latince beyaz anlamına gelir. "
        "'Alba' dişil biçimidir. Nymphaea alba beyaz "
        "çiçekleriyle tanınır."
    ),
    (
        "Niger",
        "Siyah veya çok koyu",
        ["Yeşil", "Mavi", "Siyah veya çok koyu", "Pembe"],
        "Sambucus nigra",
        "Kara mürver",
        "'Niger' siyah veya çok koyu anlamına gelir. "
        "'Nigra' dişil biçimidir."
    ),
    (
        "Ruber",
        "Kırmızı",
        ["Kırmızı", "Mor", "Gri", "Beyaz"],
        "Quercus rubra",
        "Kırmızı meşe",
        "'Ruber' kırmızı anlamına gelir. 'Rubra' dişil "
        "biçimidir."
    ),
    (
        "Roseus",
        "Gül pembesi",
        ["Turuncu", "Kahverengi", "Sarı", "Gül pembesi"],
        "Catharanthus roseus",
        "Madagaskar cezayir menekşesi",
        "'Roseus' gül renginde anlamına gelir."
    ),
    (
        "Purpureus",
        "Mor veya erguvan",
        ["Mavi", "Mor veya erguvan", "Yeşil", "Gümüş"],
        "Echinacea purpurea",
        "Mor ekinezya",
        "'Purpureus' mor veya erguvan tonlarını ifade eder."
    ),
    (
        "Caeruleus",
        "Gök mavisi",
        ["Gri", "Gök mavisi", "Siyah", "Kırmızı"],
        "Nymphaea caerulea",
        "Mavi nilüfer",
        "'Caeruleus' gök mavisi anlamına gelir. "
        "'Caerulea' dişil biçimidir. Nymphaea caerulea "
        "mavi tonlardaki çiçekleriyle tanınır."
    ),
    (
        "Flavus",
        "Sarı",
        ["Yeşil", "Mor", "Pembe", "Sarı"],
        "Glaucium flavum",
        "Sarı boynuzlu haşhaş",
        "'Flavus' sarı anlamına gelir."
    ),
    (
        "Luteus",
        "Sarı veya sarımsı",
        ["Sarı veya sarımsı", "Mavi", "Siyah", "Gri"],
        "Reseda lutea",
        "Reseda",
        "'Luteus' sarı veya sarımsı anlamına gelir."
    ),
    (
        "Aureus",
        "Altın rengi",
        ["Gümüş", "Kahverengi", "Altın rengi", "Mor"],
        "Botanik renk sıfatı",
        "Altın rengi",
        "'Aureus' altın renginde anlamına gelir."
    ),
    (
        "Viridis",
        "Yeşil",
        ["Kırmızı", "Yeşil", "Pembe", "Turuncu"],
        "Helleborus viridis",
        "Yeşil çöpleme",
        "'Viridis' yeşil anlamına gelir."
    ),
    (
        "Glaucus",
        "Mavimsi yeşil veya grimsi mavi",
        [
            "Parlak sarı",
            "Koyu kırmızı",
            "Saf beyaz",
            "Mavimsi yeşil veya grimsi mavi"
        ],
        "Rosa glauca",
        "Mavimsi yapraklı gül",
        "'Glaucus' mavimsi yeşil veya grimsi mavi "
        "tonları ifade eder."
    ),
    (
        "Cinereus",
        "Kül grisi",
        ["Kül grisi", "Altın sarısı", "Pembe", "Mor"],
        "Eucalyptus cinerea",
        "Gümüş dolar okaliptüsü",
        "'Cinereus' kül rengi anlamına gelir."
    ),
    (
        "Brunneus",
        "Kahverengi",
        ["Beyaz", "Mavi", "Kahverengi", "Pembe"],
        "Botanik renk sıfatı",
        "Kahverengi",
        "'Brunneus' kahverengi anlamına gelir."
    ),
    (
        "Rufus",
        "Kızıl veya kızıl kahverengi",
        [
            "Kızıl veya kızıl kahverengi",
            "Yeşil",
            "Beyaz",
            "Gök mavisi"
        ],
        "Botanik renk sıfatı",
        "Kızıl ton",
        "'Rufus' kızıl veya kızıl kahverengi anlamına gelir."
    ),
    (
        "Pallidus",
        "Soluk veya açık renkli",
        [
            "Çok parlak",
            "Koyu siyah",
            "Soluk veya açık renkli",
            "Altın rengi"
        ],
        "Botanik renk sıfatı",
        "Soluk renk",
        "'Pallidus' soluk veya açık renkli anlamına gelir."
    ),
    (
        "Argenteus",
        "Gümüş rengi",
        ["Turuncu", "Kahverengi", "Kırmızı", "Gümüş rengi"],
        "Botanik renk sıfatı",
        "Gümüş rengi",
        "'Argenteus' gümüş renginde anlamına gelir."
    ),
    (
        "Bicolor",
        "İki renkli",
        ["İki renkli", "Tek renkli", "Renksiz", "Kül grisi"],
        "Viola bicolor",
        "İki renkli menekşe",
        "'Bicolor' iki renkli anlamına gelir."
    ),
    (
        "Tricolor",
        "Üç renkli",
        ["Siyah", "Üç renkli", "Altın sarısı", "Gri"],
        "Viola tricolor",
        "Hercai menekşe",
        "'Tricolor' üç renkli anlamına gelir."
    ),
    (
        "Versicolor",
        "Çok renkli veya renkleri değişken",
        [
            "Beyaz",
            "Kırmızı",
            "Çok renkli veya renkleri değişken",
            "Koyu yeşil"
        ],
        "Iris versicolor",
        "Çok renkli süsen",
        "'Versicolor' farklı renkler gösteren anlamına gelir."
    ),
    (
        "Coccineus",
        "Parlak kızıl veya al kırmızısı",
        [
            "Gri",
            "Parlak kızıl veya al kırmızısı",
            "Mavimsi yeşil",
            "Kahverengi"
        ],
        "Salvia coccinea",
        "Kızıl adaçayı",
        "'Coccineus' parlak kızıl anlamına gelir."
    ),
    (
        "Sanguineus",
        "Kan kırmızısı",
        ["Kan kırmızısı", "Soluk sarı", "Gümüş", "Yeşil"],
        "Cornus sanguinea",
        "Kan kızılcığı",
        "'Sanguineus' kan renginde anlamına gelir."
    ),
    (
        "Spinosus",
        "Dikenli",
        ["Düz yüzeyli", "Dikenli", "Tüysüz", "Yumuşak"],
        "Ruscus aculeatus",
        "Tavşanmemesi",
        "'Spinosus' dikenli anlamına gelir."
    ),
    (
        "Dentatus",
        "Dişli kenarlı",
        ["Düz kenarlı", "Dişli kenarlı", "Yuvarlak", "Tüysüz"],
        "Urtica dioica",
        "Büyük ısırgan",
        "'Dentatus' dişli anlamına gelir."
    ),
    (
        "Glaber",
        "Tüysüz veya pürüzsüz",
        ["Tüylü", "Tüysüz veya pürüzsüz", "Dikenli", "Benekli"],
        "Acer glabrum",
        "Akçaağaç",
        "'Glaber' tüysüz veya pürüzsüz anlamına gelir."
    ),
    (
        "Hirsutus",
        "Uzun veya sert tüylü",
        ["Pürüzsüz", "Parlak", "Uzun veya sert tüylü", "Tüysüz"],
        "Botanik betimleme terimi",
        "Tüylü yüzey",
        "'Hirsutus' belirgin veya sert tüylerle kaplı anlamına gelir."
    ),
    (
        "Tomentosus",
        "Sık ve keçemsi tüylü",
        ["Parlak", "Sık ve keçemsi tüylü", "Tüysüz", "Dikenli"],
        "Botanik betimleme terimi",
        "Keçemsi tüylü yüzey",
        "'Tomentosus' sık ve keçemsi tüylerle kaplı anlamına gelir."
    ),
    (
        "Maculatus",
        "Benekli veya lekeli",
        ["Çizgili", "Düz renkli", "Benekli veya lekeli", "Şeffaf"],
        "Botanik betimleme terimi",
        "Benekli yüzey",
        "'Maculatus' benekli veya lekeli anlamına gelir."
    ),
    (
        "Striatus",
        "Çizgili veya şeritli",
        ["Çizgili veya şeritli", "Beyaz", "Kızıl", "Altın rengi"],
        "Botanik betimleme terimi",
        "Çizgili yüzey",
        "'Striatus' çizgili veya şeritli anlamına gelir."
    ),
    (
        "Nitidus",
        "Parlak veya ışıldayan",
        ["Mat", "Parlak veya ışıldayan", "Soluk", "Kül grisi"],
        "Botanik betimleme terimi",
        "Parlak yüzey",
        "'Nitidus' parlak veya ışıldayan anlamına gelir."
    ),
    (
        "Obscurus",
        "Koyu, karanlık veya mat",
        ["Açık", "Parlak", "Koyu, karanlık veya mat", "Süt beyazı"],
        "Botanik betimleme terimi",
        "Koyu yüzey",
        "'Obscurus' koyu veya karanlık anlamına gelir."
    ),
    (
        "Subalbus",
        "Beyazımsı",
        ["Kırmızı", "Beyazımsı", "Siyah", "Mavi"],
        "Botanik betimleme terimi",
        "Beyazımsı renk",
        "'Subalbus' beyazımsı anlamına gelir."
    ),
    (
        "Subflavus",
        "Sarımsı",
        ["Gümüş", "Mor", "Sarımsı", "Koyu siyah"],
        "Botanik betimleme terimi",
        "Sarımsı renk",
        "'Subflavus' sarımsı anlamına gelir."
    ),
    (
        "Rubescens",
        "Kırmızılaşan veya kızaran",
        [
            "Yeşile dönen",
            "Kırmızılaşan veya kızaran",
            "Beyazlaşan",
            "Maviye dönen"
        ],
        "Botanik betimleme terimi",
        "Kızaran yüzey",
        "'Rubescens' kızaran veya kırmızılaşan anlamına gelir."
    ),
    (
        "Flavescens",
        "Sarılaşan",
        ["Mavileşen", "Kararan", "Morlaşan", "Sarılaşan"],
        "Botanik betimleme terimi",
        "Sarılaşan yüzey",
        "'Flavescens' sarılaşan anlamına gelir."
    ),
    (
        "Viridescens",
        "Yeşilimsi veya yeşile dönen",
        [
            "Yeşilimsi veya yeşile dönen",
            "Kırmızılaşan",
            "Beyazlaşan",
            "Kararan"
        ],
        "Botanik betimleme terimi",
        "Yeşilimsi yüzey",
        "'Viridescens' yeşilimsi veya yeşile dönen anlamına gelir."
    ),
    (
        "Lacteus",
        "Süt beyazı",
        ["Koyu kahverengi", "Mor", "Süt beyazı", "Turuncu"],
        "Euphorbia lactea",
        "Sütleğen",
        "'Lacteus' süt renginde anlamına gelir."
    ),
    (
        "Niveus",
        "Kar beyazı",
        ["Kızıl", "Yeşil", "Mavi", "Kar beyazı"],
        "Botanik betimleme terimi",
        "Kar beyazı renk",
        "'Niveus' kar gibi beyaz anlamına gelir."
    ),
    (
        "Azureus",
        "Azur veya gök mavisi",
        ["Koyu kahverengi", "Azur veya gök mavisi", "Siyah", "Pembe"],
        "Salvia azurea",
        "Gök adaçayı",
        "'Azureus' gök mavisi anlamına gelir."
    ),
    (
        "Canus",
        "Beyazımsı gri veya kırçıllı",
        ["Turuncu", "Mor", "Beyazımsı gri veya kırçıllı", "Parlak kırmızı"],
        "Artemisia cana",
        "Gri yapraklı pelin",
        "'Canus' beyazımsı gri veya kırçıllı anlamına gelir."
    ),
    (
        "Micans",
        "Parıldayan veya ışıltılı",
        ["Kül grisi", "Parıldayan veya ışıltılı", "Soluk", "Siyah"],
        "Botanik betimleme terimi",
        "Parlak yüzey",
        "'Micans' parıldayan veya ışıldayan anlamına gelir."
    ),
    (
        "Clarus",
        "Açık, berrak veya parlak",
        ["Açık, berrak veya parlak", "Siyah", "Koyu kahverengi", "Kırmızı"],
        "Botanik betimleme terimi",
        "Açık renk",
        "'Clarus' açık, berrak veya parlak anlamına gelir."
    ),
    (
        "Opacus",
        "Mat veya donuk",
        ["Parlak", "Mat veya donuk", "Gümüş", "Kızıl"],
        "Botanik betimleme terimi",
        "Mat yüzey",
        "'Opacus' mat veya donuk anlamına gelir."
    ),
    (
        "Fulvus",
        "Sarımsı kahverengi",
        ["Mavi", "Siyah", "Mor", "Sarımsı kahverengi"],
        "Botanik betimleme terimi",
        "Sarımsı kahverengi",
        "'Fulvus' sarımsı kahverengi tonları ifade eder."
    ),
    (
        "Fuscus",
        "Koyu kahverengi veya esmer",
        ["Açık mavi", "Koyu kahverengi veya esmer", "Kar beyazı", "Parlak pembe"],
        "Botanik betimleme terimi",
        "Koyu renk",
        "'Fuscus' koyu veya esmer anlamına gelir."
    ),
    (
        "Pallens",
        "Soluk veya solgun",
        ["Çok koyu", "Altın rengi", "Soluk veya solgun", "Bakır rengi"],
        "Botanik betimleme terimi",
        "Soluk renk",
        "'Pallens' soluk veya solgun anlamına gelir."
    ),
    (
        "Albicans",
        "Beyazımsı veya beyazlaşan",
        ["Siyahımsı", "Sarımsı", "Beyazımsı veya beyazlaşan", "Kızılımsı"],
        "Botanik betimleme terimi",
        "Beyazımsı yüzey",
        "'Albicans' beyazımsı veya beyazlaşan anlamına gelir."
    ),
    (
        "Lividus",
        "Kurşuni veya mavimsi gri",
        ["Altın sarısı", "Kurşuni veya mavimsi gri", "Pembe", "Yeşil"],
        "Helleborus lividus",
        "Mavimsi çöpleme",
        "'Lividus' kurşuni, mavimsi gri veya soluk mor tonları ifade eder."
    ),
]


# ============================================================
# 4. SORU HAVUZUNU GÜVENLİ HAZIRLA
# ============================================================

def build_question_pool():
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

        clean_options = list(dict.fromkeys(
            str(option).strip()
            for option in options
            if option is not None and str(option).strip()
        ))

        if answer not in clean_options:
            clean_options.append(answer)

        if len(clean_options) < 4:
            continue

        seen.add(latin.casefold())

        result.append({
            "latin": latin,
            "question": (
                f"'{latin}' Latince botanik terimi "
                "hangi renk veya özelliği ifade eder?"
            ),
            "answer": answer,
            "options": clean_options,
            "plant": str(plant),
            "plant_name": str(plant_name),
            "explanation": str(explanation),
        })

    return result


QUESTIONS = build_question_pool()


# ============================================================
# 5. SQLITE VERİTABANI
# ============================================================

def get_connection():
    return sqlite3.connect(DB_PATH, timeout=15)


def init_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT UNIQUE NOT NULL,
                student TEXT NOT NULL,
                student_no TEXT NOT NULL,
                correct INTEGER NOT NULL,
                total INTEGER NOT NULL,
                percentage REAL NOT NULL,
                duration REAL NOT NULL,
                completed_at TEXT NOT NULL
            )
        """)

        conn.commit()


def save_result():
    run_id = st.session_state.get("run_id")

    if not run_id:
        return

    if st.session_state.get("submitted_run_id") == run_id:
        return

    questions = st.session_state.get("quiz_questions", [])

    if not questions:
        return

    started = st.session_state.get("start_time")

    elapsed = (
        max(0, round(time.time() - started, 2))
        if started is not None
        else 0.0
    )

    correct = int(st.session_state.get("score", 0))
    total = len(questions)
    percentage = round(correct / total * 100, 2)

    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO results (
                run_id,
                student,
                student_no,
                correct,
                total,
                percentage,
                duration,
                completed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
            """,
            (
                run_id,
                st.session_state.get("name", ""),
                st.session_state.get("student_no", ""),
                correct,
                total,
                percentage,
                elapsed,
            ),
        )
        conn.commit()

    st.session_state.elapsed_time = elapsed
    st.session_state.submitted_run_id = run_id


def load_results():
    with get_connection() as conn:
        return pd.read_sql_query(
            """
            SELECT
                student AS 'Öğrenci',
                student_no AS 'Öğrenci No',
                correct AS 'Doğru',
                total AS 'Toplam Soru',
                percentage AS 'Başarı (%)',
                ROUND(duration, 1) AS 'Süre (sn)',
                completed_at AS 'Tamamlanma'
            FROM results
            ORDER BY percentage DESC, correct DESC, duration ASC
            """,
            conn,
        )


init_database()


# ============================================================
# 6. OTURUM DURUMU
# ============================================================

DEFAULTS = {
    "stage": "register",
    "name": "",
    "student_no": "",
    "score": 0,
    "start_time": None,
    "elapsed_time": 0.0,
    "quiz_questions": [],
    "current_question": 0,
    "answers": [],
    "run_id": None,
    "submitted_run_id": None,
    "feedback_index": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = (
            value.copy()
            if isinstance(value, (dict, list))
            else value
        )


# ============================================================
# 7. YARDIMCILAR
# ============================================================

def safe_text(value):
    return html.escape(str(value))


def format_seconds(seconds):
    seconds = max(0, int(seconds))
    minutes, remaining = divmod(seconds, 60)

    if minutes:
        return f"{minutes} dk {remaining} sn"

    return f"{remaining} sn"


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">{safe_text(label)}</div>
            <div class="metric-value">{safe_text(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def make_balanced_questions(count):
    if not QUESTIONS:
        raise ValueError("Soru havuzu boş.")

    count = max(1, min(int(count), len(QUESTIONS)))
    selected = random.sample(QUESTIONS, count)

    prepared = []

    for q in selected:
        correct = q["answer"]

        distractors = [
            option for option in q["options"]
            if option != correct
        ]

        random.shuffle(distractors)

        if len(distractors) < 3:
            other_answers = list(dict.fromkeys(
                x["answer"]
                for x in QUESTIONS
                if x["answer"] != correct
            ))

            random.shuffle(other_answers)

            for candidate in other_answers:
                if candidate not in distractors:
                    distractors.append(candidate)

                if len(distractors) >= 3:
                    break

        options = list(dict.fromkeys(
            [correct] + distractors[:3]
        ))

        if len(options) < 4:
            continue

        options = options[:4]
        random.shuffle(options)

        item = q.copy()
        item["options"] = options
        prepared.append(item)

    if not prepared:
        raise ValueError("Geçerli soru oluşturulamadı.")

    return prepared


def start_quiz(name, student_no, count):
    questions = make_balanced_questions(count)

    st.session_state.update({
        "stage": "quiz",
        "name": name.strip(),
        "student_no": student_no.strip(),
        "score": 0,
        "start_time": time.time(),
        "elapsed_time": 0.0,
        "quiz_questions": questions,
        "current_question": 0,
        "answers": [],
        "run_id": str(uuid.uuid4()),
        "submitted_run_id": None,
        "feedback_index": None,
    })


def reset_quiz(clear_identity=False):
    st.session_state.update({
        "stage": "register",
        "score": 0,
        "start_time": None,
        "elapsed_time": 0.0,
        "quiz_questions": [],
        "current_question": 0,
        "answers": [],
        "run_id": None,
        "submitted_run_id": None,
        "feedback_index": None,
    })

    if clear_identity:
        st.session_state.name = ""
        st.session_state.student_no = ""


# ============================================================
# 8. BAŞLIK
# ============================================================

def render_header():
    st.markdown(
        """
        <div class="hero">
            <div style="
                color:#7df0b8;
                font-weight:850;
                letter-spacing:.15em;
                font-size:.78rem;
            ">
                🌿 BOTANICA AKADEMİ
            </div>

            <h1>Doğanın Dilini Keşfet.</h1>

            <p>
                Latince botanik terimlerini öğren,
                renklerin ve bitki özelliklerinin anlamlarını
                keşfet, bilgini sınavla ölç.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 9. ÖĞRENCİ GİRİŞİ
# ============================================================

def render_register():
    render_header()

    st.subheader("🌱 Öğrenci Sınav Girişi")

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Soru havuzu", len(QUESTIONS))

    with col2:
        metric_card("Seçenek", "4")

    with col3:
        metric_card("Sınav türü", "Botanik")

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    with st.form("register_form"):
        name = st.text_input(
            "Ad soyad",
            value=st.session_state.name,
            max_chars=70,
            placeholder="Örn. Ayşe Yılmaz",
        )

        student_no = st.text_input(
            "Öğrenci numarası",
            value=st.session_state.student_no,
            max_chars=40,
            placeholder="Örn. 2026001",
        )

        maximum = len(QUESTIONS)

        count_options = [
            n for n in [5, 10, 15, 20, 30, 40, maximum]
            if 1 <= n <= maximum
        ]

        count_options = sorted(set(count_options))

        selected_count = st.selectbox(
            "Soru sayısı",
            options=count_options,
            index=count_options.index(min(10, maximum)),
            format_func=lambda n: f"{n} soru",
        )

        submitted = st.form_submit_button(
            "Sınava Başla 🚀",
            use_container_width=True,
            type="primary",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if not name.strip():
            st.error("Ad soyad alanını doldur.")

        elif not student_no.strip():
            st.error("Öğrenci numarasını doldur.")

        else:
            try:
                start_quiz(name, student_no, selected_count)
                st.rerun()

            except (ValueError, TypeError, KeyError) as exc:
                st.error(f"Sınav başlatılamadı: {exc}")

    with st.expander("📖 Sınav hakkında"):
        st.markdown(
            """
            - Her soruda yalnızca bir seçenek işaretlenir.
            - Cevabını onayladıktan sonra sonraki soruya geçersin.
            - Cevaplar sınav sonunda puanlanır.
            - Sonuçlar uygulamanın SQLite veritabanına kaydedilir.
            """
        )


# ============================================================
# 10. SINAV
# ============================================================

def render_quiz():
    questions = st.session_state.quiz_questions
    index = st.session_state.current_question

    if not questions:
        st.error("Sınav soruları bulunamadı.")

        if st.button("Ana sayfaya dön"):
            reset_quiz()
            st.rerun()

        return

    if index >= len(questions):
        save_result()
        st.session_state.stage = "result"
        st.rerun()
        return

    q = questions[index]

    st.progress((index + 1) / len(questions))

    col1, col2 = st.columns(2)

    with col1:
        st.caption(f"Soru {index + 1} / {len(questions)}")

    with col2:
        st.caption(f"Öğrenci: {st.session_state.name}")

    st.markdown(
        f"""
        <div class="panel">
            <div style="
                opacity:.7;
                font-size:.8rem;
                font-weight:800;
                letter-spacing:.12em;
            ">
                LATİNCE BOTANİK
            </div>

            <div class="latin">{safe_text(q['latin'])}</div>

            <p>{safe_text(q['question'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    form_key = f"form_{st.session_state.run_id}_{index}"

    with st.form(form_key):
        selected = st.radio(
            "Cevabını seç:",
            options=q["options"],
            index=None,
            key=f"choice_{st.session_state.run_id}_{index}",
        )

        submitted = st.form_submit_button(
            "Cevabı Onayla",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        if selected is None:
            st.warning("Devam etmeden önce bir seçenek işaretle.")
            return

        if len(st.session_state.answers) > index:
            st.warning("Bu soru daha önce cevaplanmış.")
            return

        is_correct = selected == q["answer"]

        if is_correct:
            st.session_state.score += 1

        st.session_state.answers.append({
            "latin": q["latin"],
            "selected": selected,
            "correct": q["answer"],
            "is_correct": is_correct,
            "plant": q["plant"],
            "plant_name": q["plant_name"],
            "explanation": q["explanation"],
        })

        st.session_state.feedback_index = index
        st.session_state.stage = "feedback"
        st.rerun()


# ============================================================
# 11. CEVAP SONRASI BİLGİLENDİRME
# ============================================================

def render_feedback():
    answers = st.session_state.answers
    index = st.session_state.feedback_index

    if index is None or index >= len(answers):
        st.session_state.stage = "quiz"
        st.rerun()
        return

    answer = answers[index]

    if answer["is_correct"]:
        st.success("🎉 Doğru cevap!")
    else:
        st.error("Yanlış cevap.")

    # Sınav sırasında doğru yanıtı açıklamıyoruz.
    # Böylece sonraki sorularda cevaplar hakkında ipucu verilmez.
    st.info(
        "Cevap açıklamaları ve doğru yanıtlar sınav bitiminde gösterilecektir."
    )

    current = st.session_state.current_question
    total = len(st.session_state.quiz_questions)

    label = (
        "Sınavı Bitir ve Sonuçları Gör 🏆"
        if current + 1 >= total
        else "Sonraki Soru ➡️"
    )

    if st.button(
        label,
        use_container_width=True,
        type="primary",
    ):
        if current + 1 >= total:
            save_result()
            st.session_state.stage = "result"
        else:
            st.session_state.current_question += 1
            st.session_state.stage = "quiz"

        st.rerun()


# ============================================================
# 12. SONUÇLAR
# ============================================================

def render_result():
    questions = st.session_state.quiz_questions
    total = len(questions)
    score = st.session_state.score

    if total == 0:
        st.warning("Sınav sonucu bulunamadı.")

        if st.button("Ana sayfaya dön"):
            reset_quiz()
            st.rerun()

        return

    save_result()

    percentage = score / total * 100

    if score == total:
        st.balloons()

    st.markdown(
        f"""
        <div class="hero">
            <div style="
                color:#7df0b8;
                font-weight:850;
                letter-spacing:.12em;
            ">
                SINAV TAMAMLANDI
            </div>

            <div style="
                font-size:clamp(3rem,10vw,4.5rem);
                font-weight:900;
                margin:.5rem 0;
            ">
                {score} / {total}
            </div>

            <h2 style="color:white;">
                Başarı oranı: %{percentage:.1f}
            </h2>

            <p>
                Süre:
                <strong>
                    {safe_text(format_seconds(
                        st.session_state.elapsed_time
                    ))}
                </strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Doğru", score)

    with col2:
        metric_card("Yanlış", total - score)

    with col3:
        metric_card("Başarı", f"%{percentage:.1f}")

    st.subheader("📝 Cevaplarını İncele")

    for i, answer in enumerate(st.session_state.answers, start=1):
        with st.expander(
            f"{i}. {answer['latin']} — "
            f"{'✅ Doğru' if answer['is_correct'] else '❌ Yanlış'}"
        ):
            st.write(f"Verdiğin cevap: {answer['selected']}")
            st.write(f"Doğru cevap: {answer['correct']}")

            st.markdown(
                f"**{safe_text(answer['plant'])}**"
                f" — {safe_text(answer['plant_name'])}",
                unsafe_allow_html=True,
            )

            st.write(answer["explanation"])

    st.divider()

    if st.button(
        "Yeni Sınava Başla 🔄",
        use_container_width=True,
        type="primary",
    ):
        reset_quiz()
        st.rerun()

    if st.button(
        "Ana sayfaya dön",
        use_container_width=True,
    ):
        reset_quiz(clear_identity=True)
        st.rerun()


# ============================================================
# 13. ÖĞRETMEN PANELİ
# ============================================================

def render_teacher():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">ÖĞRETMEN PANELİ</div>
            <h1>Sınav Sonuçları</h1>
            <p>
                Tamamlanan sınavları görüntüle ve sonuçları CSV
                dosyası olarak indir.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    password = st.text_input(
        "Öğretmen şifresi",
        type="password",
        key="teacher_password",
    )

    # Üretim ortamında bu değeri ortam değişkeninden al.
    expected_password = __import__("os").environ.get(
        "BOTANICA_TEACHER_PASSWORD",
        "",
    )

    if not expected_password:
        st.warning(
            "Öğretmen paneli etkin değil. "
            "BOTANICA_TEACHER_PASSWORD ortam değişkenini ayarla."
        )
        return

    if password != expected_password:
        st.info("Sonuçları görmek için öğretmen şifresini gir.")
        return

    df = load_results()

    st.metric("Tamamlanan sınav", len(df))

    if df.empty:
        st.info("Henüz tamamlanmış sınav yok.")
        return

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    csv_data = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "Sonuçları CSV olarak indir 📥",
        data=csv_data,
        file_name="botanica_sinav_sonuclari.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ============================================================
# 14. UYGULAMA YÖNLENDİRME
# ============================================================

if not QUESTIONS:
    st.error("Soru havuzu boş veya geçersiz.")

else:
    with st.sidebar:
        st.markdown("### 🌿 Botanica Akademi")

        page = st.radio(
            "Sayfa",
            ["Öğrenci Sınavı", "Öğretmen Paneli"],
        )

    if page == "Öğretmen Paneli":
        render_teacher()

    elif st.session_state.stage == "register":
        render_register()

    elif st.session_state.stage == "quiz":
        render_quiz()

    elif st.session_state.stage == "feedback":
        render_feedback()

    elif st.session_state.stage == "result":
        render_result()

    else:
        reset_quiz()
        st.rerun()
