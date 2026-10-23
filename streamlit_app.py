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
    page_title="Botanica | Latince Renkler",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. TASARIM SİSTEMİ
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        border-radius: 20px;
        border: 1px solid var(--default-border-color);
        background: var(--secondary-background-color);
    }

    .eyebrow {
        color: var(--primary-color);
        font-size: .8rem;
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
    }

    .hero h1 {
        font-size: clamp(1.9rem, 5vw, 2.8rem);
        font-weight: 850;
        letter-spacing: -.04em;
        line-height: 1.15;
    }

    .hero p {
        line-height: 1.7;
        opacity: .85;
    }

    .card {
        padding: 1.4rem;
        margin: 1rem 0;
        border-radius: 18px;
        border: 1px solid var(--default-border-color);
        background: var(--secondary-background-color);
    }

    .latin {
        font-size: clamp(2.2rem, 7vw, 3.5rem);
        font-weight: 850;
        font-style: italic;
        letter-spacing: -.04em;
        overflow-wrap: anywhere;
    }

    .muted {
        opacity: .75;
        line-height: 1.7;
    }

    .plant-name {
        font-size: 1.2rem;
        font-weight: 800;
    }

    .score {
        color: var(--primary-color);
        font-size: clamp(2.5rem, 8vw, 4rem);
        font-weight: 900;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        width: 100%;
        min-height: 46px;
        border-radius: 12px;
        font-weight: 700;
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1rem .8rem 2rem;
        }

        .hero {
            padding: 1.2rem;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            transition: none !important;
            animation: none !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. SORU HAVUZU (50+ Genişletilmiş Botanik Renk ve Terimler)
# ============================================================

RAW_QUESTIONS = [
    # --- Temel Renkler ---
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
        "Aureus",
        "Altın rengi",
        ["Gümüş", "Kahverengi", "Altın rengi", "Mor"],
        "Forsythia",
        "Altın çanı çalısı",
        "'Aureus' altın veya altın rengi anlamına gelir.",
    ),
    (
        "Viridis",
        "Yeşil",
        ["Kırmızı", "Yeşil", "Pembe", "Turuncu"],
        "Helleborus viridis",
        "Yeşil çöpleme",
        "'Viridis' yeşil anlamına gelir.",
    ),

    # --- Ara ve Özel Tonlar ---
    (
        "Glaucus",
        "Mavimsi yeşil veya grimsi mavi",
        [
            "Parlak sarı",
            "Koyu kırmızı",
            "Saf beyaz",
            "Mavimsi yeşil veya grimsi mavi",
        ],
        "Eucalyptus cinerea",
        "Gümüş dolar okaliptüsü",
        "'Glaucus' mavimsi yeşil veya grimsi mavi tonlarını anlatır.",
    ),
    (
        "Cinereus",
        "Kül grisi",
        ["Kül grisi", "Altın sarısı", "Pembe", "Mor"],
        "Eucalyptus cinerea",
        "Gümüş dolar okaliptüsü",
        "'Cinereus' kül grisi anlamına gelir.",
    ),
    (
        "Brunneus",
        "Kahverengi",
        ["Beyaz", "Mavi", "Kahverengi", "Pembe"],
        "Botanik renk sıfatı",
        "Kahverengi tonları",
        "'Brunneus' kahverengi anlamına gelir.",
    ),
    (
        "Fuscus",
        "Koyu kahverengi veya esmer",
        [
            "Açık mavi",
            "Koyu kahverengi veya esmer",
            "Kar beyazı",
            "Parlak pembe",
        ],
        "Botanik renk sıfatı",
        "Koyu renkler",
        "'Fuscus' koyu kahverengi veya esmer anlamına gelebilir.",
    ),
    (
        "Fulvus",
        "Sarımsı kahverengi",
        ["Mavi", "Siyah", "Mor", "Sarımsı kahverengi"],
        "Botanik renk sıfatı",
        "Toprak tonları",
        "'Fulvus' sarımsı kahverengi veya boz tonları anlatır.",
    ),
    (
        "Rufus",
        "Kızıl veya kızıl kahverengi",
        [
            "Kızıl veya kızıl kahverengi",
            "Yeşil",
            "Beyaz",
            "Gök mavisi",
        ],
        "Botanik renk sıfatı",
        "Kızıl tonlar",
        "'Rufus' kızıl veya kızıl kahverengi anlamına gelir.",
    ),
    (
        "Pallidus",
        "Soluk veya açık renkli",
        [
            "Çok parlak",
            "Koyu siyah",
            "Soluk veya açık renkli",
            "Altın rengi",
        ],
        "Botanik renk sıfatı",
        "Soluk tonlar",
        "'Pallidus' soluk veya açık renkli anlamına gelir.",
    ),
    (
        "Argenteus",
        "Gümüş rengi",
        ["Turuncu", "Kahverengi", "Kırmızı", "Gümüş rengi"],
        "Salix alba",
        "Ak söğüt",
        "'Argenteus' gümüş rengi veya gümüşi anlamına gelir.",
    ),
    (
        "Lilacinus",
        "Leylak rengi",
        ["Yeşil", "Leylak rengi", "Siyah", "Sarı"],
        "Syringa vulgaris",
        "Adi leylak",
        "'Lilacinus' leylak rengi veya açık mor tonlarını anlatır.",
    ),

    # --- Genişletilmiş Ek Sorular (50+ Tamamlama) ---
    (
        "Atropurpureus",
        "Çok koyu mor",
        ["Açık sarı", "Çok koyu mor", "Beyaz", "Gümüş"],
        "Ocimum tenuiflorum",
        "Kutsal fesleğen",
        "'Atropurpureus' siyaha yaklaşan çok koyu mor tonunu anlatır.",
    ),
    (
        "Cupreus",
        "Bakır rengi",
        ["Bakır rengi", "Mavi", "Beyaz", "Pembe"],
        "Botanik renk sıfatı",
        "Bakırımsı tonlar",
        "'Cupreus' bakır rengi anlamına gelir.",
    ),
    (
        "Lacteus",
        "Süt beyazı",
        ["Koyu kahverengi", "Mor", "Süt beyazı", "Turuncu"],
        "Euphorbia lactea",
        "Sütleğen türü",
        "'Lacteus' süt beyazı anlamına gelir.",
    ),
    (
        "Niveus",
        "Kar beyazı",
        ["Kızıl", "Yeşil", "Mavi", "Kar beyazı"],
        "Galanthus nivalis",
        "Kardelen",
        "'Niveus' kar beyazı anlamına gelir.",
    ),
    (
        "Bicolor",
        "İki renkli",
        ["İki renkli", "Tek renkli", "Renksiz", "Kül grisi"],
        "Viola tricolor",
        "Hercai menekşe",
        "'Bicolor' iki renkli anlamına gelir.",
    ),
    (
        "Tricolor",
        "Üç renkli",
        ["Siyah", "Üç renkli", "Altın sarısı", "Gri"],
        "Viola tricolor",
        "Hercai menekşe",
        "'Tricolor' üç renkli anlamına gelir.",
    ),
    (
        "Versicolor",
        "Çok renkli veya renk değiştiren",
        ["Beyaz", "Kırmızı", "Çok renkli veya renk değiştiren", "Koyu yeşil"],
        "Lantana camara",
        "Mine çalısı",
        "'Versicolor' çok renkli veya farklı renkler gösterebilen anlamına gelir.",
    ),
    (
        "Coccineus",
        "Parlak kırmızı",
        ["Gri", "Parlak kırmızı", "Mavimsi yeşil", "Kahverengi"],
        "Salvia coccinea",
        "Kırmızı çiçekli adaçayı",
        "'Coccineus' parlak kırmızı veya al rengini ifade eder.",
    ),
    (
        "Sanguineus",
        "Kan kırmızısı",
        ["Kan kırmızısı", "Soluk sarı", "Gümüş", "Yeşil"],
        "Botanik renk sıfatı",
        "Derin kırmızı tonlar",
        "'Sanguineus' kan kırmızısı anlamına gelir.",
    ),
    (
        "Pallens",
        "Soluk veya solgun",
        ["Çok koyu", "Altın rengi", "Soluk veya solgun", "Bakır rengi"],
        "Botanik renk sıfatı",
        "Solgun renkler",
        "'Pallens' soluk veya solgun anlamına gelir.",
    ),
    (
        "Rubescens",
        "Kırmızılaşan",
        ["Yeşile dönen", "Kırmızılaşan", "Beyazlaşan", "Maviye dönen"],
        "Trifolium rubens",
        "Kızıl çayır üçgülü",
        "'Rubescens' kızaran veya kırmızılaşan anlamına gelir.",
    ),
    (
        "Albicans",
        "Beyazımsı",
        ["Siyahımsı", "Sarımsı", "Beyazımsı", "Kızılımsı"],
        "Botanik renk sıfatı",
        "Beyaza çalan tonlar",
        "'Albicans' beyazımsı anlamına gelir.",
    ),
    (
        "Flavescens",
        "Sarılaşan",
        ["Mavileşen", "Kararan", "Morlaşan", "Sarılaşan"],
        "Botanik renk sıfatı",
        "Sarıya dönen tonlar",
        "'Flavescens' sarılaşan veya sarımsı anlamına gelir.",
    ),
    (
        "Viridescens",
        "Yeşile dönen",
        ["Yeşile dönen", "Kırmızılaşan", "Beyazlaşan", "Kararan"],
        "Botanik renk sıfatı",
        "Yeşile dönen tonlar",
        "'Viridescens' yeşilimsi veya yeşile dönen anlamına gelir.",
    ),
    (
        "Obscurus",
        "Koyu veya karanlık",
        ["Açık", "Parlak", "Koyu veya karanlık", "Süt beyazı"],
        "Botanik renk sıfatı",
        "Koyu tonlar",
        "'Obscurus' koyu veya karanlık anlamına gelir.",
    ),
    (
        "Nitidus",
        "Parlak",
        ["Mat", "Parlak", "Soluk", "Kül grisi"],
        "Botanik görünüm sıfatı",
        "Parlak yüzeyler",
        "'Nitidus' parlak veya cilalı görünümlü anlamına gelir.",
    ),
    (
        "Maculatus",
        "Benekli",
        ["Çizgili", "Düz renkli", "Benekli", "Şeffaf"],
        "Pulmonaria officinalis",
        "Akciğer otu",
        "'Maculatus' benekli anlamına gelir; desen belirtir.",
    ),
    (
        "Striatus",
        "Çizgili",
        ["Çizgili", "Beyaz", "Kızıl", "Altın rengi"],
        "Botanik desen sıfatı",
        "Çizgili görünüm",
        "'Striatus' çizgili anlamına gelir.",
    ),
    (
        "Azureus",
        "Azur veya gök mavisi",
        ["Koyu kahverengi", "Azur veya gök mavisi", "Siyah", "Pembe"],
        "Botanik renk sıfatı",
        "Mavi tonları",
        "'Azureus' azur veya gök mavisi anlamına gelir.",
    ),
    (
        "Canus",
        "Beyazımsı gri",
        ["Turuncu", "Mor", "Beyazımsı gri", "Parlak kırmızı"],
        "Botanik renk sıfatı",
        "Gri-beyaz tonlar",
        "'Canus' beyazımsı gri veya kırçıllı görünümü anlatabilir.",
    ),
    (
        "Lividus",
        "Kurşuni veya mavimsi gri",
        ["Altın sarısı", "Kurşuni veya mavimsi gri", "Pembe", "Yeşil"],
        "Botanik renk sıfatı",
        "Soğuk gri tonlar",
        "'Lividus' kurşuni veya mavimsi gri tonlarını ifade edebilir.",
    ),
    (
        "Coloratus",
        "Renkli",
        ["Renksiz", "Renkli", "Yalnızca beyaz", "Çizgili"],
        "Botanik tanımlama sıfatı",
        "Renkli görünüm",
        "'Coloratus' renkli veya belirgin renge sahip anlamına gelir.",
    ),
    (
        "Piceus",
        "Zift siyahı",
        ["Kar beyazı", "Zift siyahı", "Leylak", "Gümüş"],
        "Botanik renk sıfatı",
        "Çok koyu siyah",
        "'Piceus' zift gibi koyu veya siyah anlamına gelir.",
    ),
    (
        "Dilutus",
        "Açılmış veya seyrelmiş",
        ["Çok koyu", "Açılmış veya seyrelmiş", "Parlak siyah", "Altın rengi"],
        "Botanik renk sıfatı",
        "Seyreltik tonlar",
        "'Dilutus' seyrelmiş veya daha açık hale gelmiş anlamına gelir.",
    ),
    (
        "Clarus",
        "Açık veya parlak",
        ["Açık veya parlak", "Siyah", "Koyu kahverengi", "Kırmızı"],
        "Botanik renk sıfatı",
        "Parlak görünüm",
        "'Clarus' açık, parlak veya belirgin anlamına gelebilir.",
    ),
    (
        "Saturatus",
        "Doygun veya yoğun",
        ["Soluk", "Doygun veya yoğun", "Renksiz", "Şeffaf"],
        "Botanik renk sıfatı",
        "Yoğun renkler",
        "'Saturatus' doygun veya yoğun anlamına gelir.",
    ),
    (
        "Opacus",
        "Mat veya donuk",
        ["Parlak", "Mat veya donuk", "Gümüş", "Kızıl"],
        "Botanik görünüm sıfatı",
        "Mat yüzeyler",
        "'Opacus' mat, donuk veya ışığı geçirmeyen anlamına gelebilir.",
    ),
    (
        "Micans",
        "Parıldayan",
        ["Kül grisi", "Parıldayan", "Soluk", "Siyah"],
        "Botanik görünüm sıfatı",
        "Işıltılı yüzeyler",
        "'Micans' parıldayan veya ışıldayan anlamına gelir.",
    ),
    (
        "Subalbus",
        "Beyazımsı",
        ["Kırmızı", "Beyazımsı", "Siyah", "Mavi"],
        "Botanik renk sıfatı",
        "Beyaza çalan tonlar",
        "'Sub-' öneki 'biraz' veya '-ımsı' anlamı katar.",
    ),
    (
        "Subflavus",
        "Sarımsı",
        ["Gümüş", "Mor", "Sarımsı", "Koyu siyah"],
        "Botanik renk sıfatı",
        "Sarıya çalan tonlar",
        "'Subflavus' sarımsı anlamına gelir.",
    ),
    (
        "Subrubens",
        "Kırmızımsı",
        ["Kırmızımsı", "Mavimsi", "Yeşilimsi", "Beyazımsı"],
        "Botanik renk sıfatı",
        "Kırmızıya çalan tonlar",
        "'Subrubens' kırmızımsı anlamında yorumlanabilir.",
    ),
    (
        "Subviridis",
        "Yeşilimsi",
        ["Kızıl", "Gümüş", "Yeşilimsi", "Siyah"],
        "Botanik renk sıfatı",
        "Yeşile çalan tonlar",
        "'Subviridis' yeşilimsi anlamına gelir.",
    ),
]


def build_question_pool():
    """Soru verilerini kontrol eder ve standart biçime dönüştürür."""
    result = []
    for item in RAW_QUESTIONS:
        latin, answer, options, plant, plant_name, explanation = item

        options = list(
            dict.fromkeys(
                str(option).strip()
                for option in options
                if option is not None and str(option).strip()
            )
        )

        if answer not in options:
            options.append(answer)

        if len(options) < 4:
            continue

        result.append(
            {
                "latin": latin,
                "question": f"'{latin}' hangi rengi ifade eder?",
                "answer": answer,
                "options": options,
                "plant": plant,
                "plant_name": plant_name,
                "explanation": explanation,
            }
        )
    return result


QUESTIONS = build_question_pool()


# ============================================================
# 4. OTURUM DURUMU
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
    "leaderboard": [
        {
            "İsim": "Linnaeus",
            "Doğru Sayısı": 5,
            "Toplam Soru": 5,
            "Süre (sn)": 14.2,
        },
        {
            "İsim": "Darwin",
            "Doğru Sayısı": 4,
            "Toplam Soru": 5,
            "Süre (sn)": 11.0,
        },
        {
            "İsim": "Mendel",
            "Doğru Sayısı": 3,
            "Toplam Soru": 5,
            "Süre (sn)": 9.5,
        },
    ],
    "run_id": None,
    "submitted_run_id": None,
    "quiz_length": 10,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = (
            value.copy() if isinstance(value, (dict, list)) else value
        )


# ============================================================
# 5. YARDIMCI FONKSİYONLAR
# ============================================================

def safe_text(value):
    """HTML gösteriminde kullanıcı ve soru metinlerini güvenli kılar."""
    return html.escape(str(value))


def format_seconds(seconds):
    """Saniyeyi dakika ve saniye biçimine dönüştürür."""
    seconds = max(0, int(seconds))
    minutes, remaining = divmod(seconds, 60)
    if minutes:
        return f"{minutes} dk {remaining} sn"
    return f"{remaining} sn"


def make_balanced_questions(count):
    """Geçerli soruları seçer ve doğru cevapların konumlarını dengeler."""
    if not QUESTIONS:
        raise ValueError("Soru havuzu boş.")

    count = max(1, min(int(count), len(QUESTIONS)))

    source = QUESTIONS.copy()
    random.shuffle(source)
    selected = source[:count]

    positions = [0, 1, 2, 3] * ((len(selected) + 3) // 4)
    positions = positions[:len(selected)]
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

        if len(options) != 4 or len(set(options)) != 4:
            continue

        item = question.copy()
        item["options"] = options
        prepared.append(item)

    if not prepared:
        raise ValueError("Geçerli sorular hazırlanamadı.")

    return prepared


def start_quiz(name, count):
    """Yeni test başlatır."""
    name = str(name).strip()
    if not name:
        raise ValueError("Lütfen bir ad girin.")

    questions = make_balanced_questions(count)

    st.session_state.update({
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
    })


def save_result():
    """Sonucu liderlik tablosuna yalnızca bir kez ekler."""
    run_id = st.session_state.get("run_id")
    if not run_id:
        return

    if st.session_state.submitted_run_id == run_id:
        return

    questions = st.session_state.quiz_questions
    if not questions:
        return

    if st.session_state.start_time is not None:
        elapsed = round(
            time.time() - st.session_state.start_time,
            2,
        )
    else:
        elapsed = 0.0

    st.session_state.elapsed_time = elapsed

    st.session_state.leaderboard.append({
        "İsim": st.session_state.name,
        "Doğru Sayısı": st.session_state.score,
        "Toplam Soru": len(questions),
        "Süre (sn)": elapsed,
    })

    st.session_state.submitted_run_id = run_id


def reset_quiz(clear_name=False):
    """Yeni bir test için gerekli durumu sıfırlar."""
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
    })

    if clear_name:
        st.session_state.name = ""


def render_leaderboard():
    """Liderlik tablosunu puana ve süreye göre sıralar."""
    if not st.session_state.leaderboard:
        st.info("Henüz sonuç bulunmuyor.")
        return

    df = pd.DataFrame(st.session_state.leaderboard)
    df = df.sort_values(
        by=["Doğru Sayısı", "Süre (sn)"],
        ascending=[False, True],
    ).reset_index(drop=True)
    df.index = df.index + 1

    st.dataframe(
        df[["İsim", "Doğru Sayısı", "Toplam Soru", "Süre (sn)"]],
        use_container_width=True,
    )


# ============================================================
# 6. UYGULAMA EKRANLARI
# ============================================================

def render_header():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">🌿 Botanica Akademi</div>
            <h1>Latince Botanik Renkleri Macerası</h1>
            <p>
                Bitki bilimi ve taksonomide kullanılan Latince renk
                terimlerini öğren. Soruları yanıtla, botanik bilgini
                geliştir ve liderlik tablosunda yerini al!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# 6.1. KAYIT EKRANI
# ------------------------------------------------------------

def render_register():
    render_header()

    st.subheader("🌱 Teste Hazırlan")

    with st.form("register_form"):
        name = st.text_input(
            "Adınız veya takma adınız",
            value=st.session_state.name,
            placeholder="Örn. Botanica",
            max_chars=50,
        )

        # 50 soruluk seçenek eklendi
        count_options = [5, 10, 15, 20, 50]
        selected_count = st.selectbox(
            "Soru sayısı",
            count_options,
            index=1,
            format_func=lambda x: f"{x} soru",
        )

        submitted = st.form_submit_button(
            "Testi Başlat 🚀",
            use_container_width=True,
        )

    if submitted:
        if not name.strip():
            st.warning("Lütfen adınızı veya takma adınızı girin.")
        else:
            try:
                start_quiz(name, selected_count)
                st.rerun()
            except (ValueError, TypeError, KeyError) as exc:
                st.error(f"Test başlatılamadı: {exc}")

    st.divider()
    st.subheader("🏆 En İyi Skorlar")
    render_leaderboard()


# ------------------------------------------------------------
# 6.2. SORU EKRANI
# ------------------------------------------------------------

def render_quiz():
    questions = st.session_state.quiz_questions
    index = st.session_state.current_question

    if not questions:
        st.error("Soru bulunamadı. Lütfen yeni bir test başlatın.")
        if st.button("Ana Sayfaya Dön"):
            reset_quiz()
            st.rerun()
        return

    if index < 0 or index >= len(questions):
        st.session_state.stage = "result"
        st.rerun()
        return

    q = questions[index]

    st.progress((index + 1) / len(questions))

    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"Soru {index + 1} / {len(questions)}")
    with col2:
        st.caption(f"Puan: {st.session_state.score}")

    st.markdown(
        f"""
        <div class="card">
            <div class="eyebrow">Botanik Terim</div>
            <div class="latin">{safe_text(q['latin'])}</div>
            <p>{safe_text(q['question'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    options = list(dict.fromkeys(q["options"]))
    if len(options) != 4:
        st.error("Bu sorunun seçenekleri geçersiz.")
        return

    form_key = f"quiz_form_{st.session_state.run_id}_{index}"

    with st.form(form_key):
        selected = st.radio(
            "Cevabınızı seçin:",
            options,
            index=None,
            key=f"answer_{st.session_state.run_id}_{index}",
        )

        submitted = st.form_submit_button(
            "Cevabı Kontrol Et ✨",
            use_container_width=True,
        )

    if submitted:
        if selected is None:
            st.warning("Lütfen bir cevap seçin.")
            return

        is_correct = selected == q["answer"]
        if is_correct:
            st.session_state.score += 1

        st.session_state.answers.append({
            "latin": q["latin"],
            "question": q["question"],
            "selected": selected,
            "correct": q["answer"],
            "is_correct": is_correct,
            "plant": q["plant"],
            "plant_name": q["plant_name"],
            "explanation": q["explanation"],
        })

        st.session_state.stage = "feedback"
        st.rerun()


# ------------------------------------------------------------
# 6.3. GERİ BİLDİRİM EKRANI
# ------------------------------------------------------------

def render_feedback():
    answers = st.session_state.answers
    if not answers:
        st.session_state.stage = "quiz"
        st.rerun()
        return

    answer = answers[-1]

    if answer["is_correct"]:
        st.success("🎉 Harika! Doğru cevap.")
    else:
        st.error("Yanlış cevap.")
        st.markdown(
            f"**Doğru cevap:** {safe_text(answer['correct'])}",
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="card">
            <div class="eyebrow">Botanik Bilgisi</div>
            <div class="plant-name">
                🌿 {safe_text(answer['plant'])}
            </div>
            <p class="muted">
                {safe_text(answer['plant_name'])}
            </p>
            <p>{safe_text(answer['explanation'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    current = st.session_state.current_question
    total = len(st.session_state.quiz_questions)

    if current + 1 >= total:
        label = "Sonuçları Gör 🏆"
    else:
        label = "Sonraki Soru ➡️"

    if st.button(label, use_container_width=True):
        if current + 1 >= total:
            save_result()
            st.session_state.stage = "result"
        else:
            st.session_state.current_question += 1
            st.session_state.stage = "quiz"

        st.rerun()


# ------------------------------------------------------------
# 6.4. SONUÇ EKRANI
# ------------------------------------------------------------

def render_result():
    questions = st.session_state.quiz_questions
    total = len(questions)
    score = st.session_state.score

    if total == 0:
        st.warning("Gösterilecek test sonucu bulunamadı.")
        if st.button("Ana Sayfaya Dön"):
            reset_quiz()
            st.rerun()
        return

    percentage = score / total * 100

    if score == total:
        st.balloons()

    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">Quiz Tamamlandı 🌿</div>
            <div class="score">{score} / {total}</div>
            <h2>Başarı oranı: %{percentage:.0f}</h2>
            <p>
                Tamamlanma süresi:
                <strong>{safe_text(format_seconds(st.session_state.elapsed_time))}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if percentage >= 80:
        st.success("Mükemmel! Botanik renk bilgine hâkim görünüyorsun.")
    elif percentage >= 50:
        st.info("Güzel iş! Birkaç tekrar ile daha da ilerleyebilirsin.")
    else:
        st.warning("Yeni bir turla bilgilerini geliştirebilirsin.")

    st.subheader("🏆 Liderlik Tablosu")
    render_leaderboard()

    st.divider()

    with st.expander("📝 Cevaplarını İncele"):
        for i, answer in enumerate(st.session_state.answers, start=1):
            if answer["is_correct"]:
                st.markdown(f"**{i}. {answer['latin']} — ✅ Doğru**")
            else:
                st.markdown(f"**{i}. {answer['latin']} — ❌ Yanlış**")

            st.write(f"Verdiğin cevap: {answer['selected']}")
            st.write(f"Doğru cevap: {answer['correct']}")
            st.caption(
                f"{answer['plant']} — {answer['plant_name']}"
            )
            st.write(answer["explanation"])
            st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Tekrar Oyna 🔄", use_container_width=True):
            reset_quiz()
            st.rerun()

    with col2:
        if st.button("Ana Sayfaya Dön 🏠", use_container_width=True):
            reset_quiz(clear_name=True)
            st.rerun()


# ============================================================
# 7. ANA YÖNLENDİRME
# ============================================================

if not QUESTIONS:
    st.error(
        "Soru havuzu yüklenemedi. RAW_QUESTIONS listesini kontrol edin."
    )
elif st.session_state.stage == "register":
    render_register()
elif st.session_state.stage == "quiz":
    render_quiz()
elif st.session_state.stage == "feedback":
    render_feedback()
elif st.session_state.stage == "result":
    render_result()
else:
    st.session_state.stage = "register"
    st.rerun()
