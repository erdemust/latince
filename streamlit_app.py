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
# 2. TASARIM SİSTEMİ
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
                rgba(61, 220, 151, 0.10),
                transparent 42%
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
        padding: 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(61, 220, 151, .25);
        border-radius: 26px;
        background: linear-gradient(
            135deg,
            #123c2d,
            #17533c
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
        letter-spacing: -.045em;
        line-height: 1.12;
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

    .latin {
        font-size: clamp(2.3rem, 8vw, 4rem);
        font-weight: 900;
        font-style: italic;
        letter-spacing: -.045em;
        overflow-wrap: anywhere;
        line-height: 1.1;
        margin: .6rem 0 1rem;
    }

    .metric-card {
        padding: 1rem;
        min-height: 100px;
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
        font-size: clamp(1.25rem, 4vw, 2rem);
        font-weight: 900;
        letter-spacing: -.035em;
        overflow-wrap: anywhere;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        min-height: 48px;
        border-radius: 13px;
        font-weight: 750;
    }

    div[data-testid="stProgressBar"] > div > div {
        background-color: #3ddc97;
    }

    @media (max-width: 600px) {
        .hero {
            padding: 1.35rem;
            border-radius: 20px;
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
# Her soru:
# Latince terim, anlam, seçenekler, bilimsel ad,
# Türkçe bitki adı ve açıklama
# ============================================================

RAW_QUESTIONS = [
    (
        "Albus",
        "Beyaz",
        ["Siyah", "Beyaz", "Kırmızı", "Sarı"],
        "Nymphaea alba",
        "Beyaz nilüfer",
        "'Albus' Latince beyaz anlamına gelir. "
        "'Alba' dişil, 'album' ise nötr biçimidir. "
        "Nymphaea alba beyaz çiçekleriyle tanınır.",
    ),
    (
        "Niger",
        "Siyah veya çok koyu",
        ["Yeşil", "Mavi", "Siyah veya çok koyu", "Pembe"],
        "Sambucus nigra",
        "Kara mürver",
        "'Niger' siyah veya çok koyu anlamına gelir. "
        "'Nigra' dişil biçimidir. Kara mürverin olgun "
        "meyveleri koyu mor-siyah renktedir.",
    ),
    (
        "Ruber",
        "Kırmızı",
        ["Kırmızı", "Mor", "Gri", "Beyaz"],
        "Quercus rubra",
        "Kırmızı meşe",
        "'Ruber' kırmızı anlamına gelir. 'Rubra' dişil "
        "biçimidir. Kırmızı meşe yaprakları özellikle "
        "sonbaharda kızıl tonlar alabilir.",
    ),
    (
        "Roseus",
        "Gül pembesi",
        ["Turuncu", "Kahverengi", "Sarı", "Gül pembesi"],
        "Catharanthus roseus",
        "Madagaskar cezayir menekşesi",
        "'Roseus' gül renginde anlamına gelir. "
        "Catharanthus roseus pembe çiçekli formlarıyla "
        "bilinir; beyaz çiçekli çeşitleri de vardır.",
    ),
    (
        "Purpureus",
        "Mor veya erguvan",
        ["Mavi", "Mor veya erguvan", "Yeşil", "Gümüş"],
        "Echinacea purpurea",
        "Mor ekinezya",
        "'Purpureus' mor veya erguvan tonlarını ifade eder. "
        "'Purpurea' dişil biçimidir. Mor ekinezyanın "
        "çiçekleri pembe-mor tonlarında olabilir.",
    ),
    (
        "Caeruleus",
        "Gök mavisi",
        ["Gri", "Gök mavisi", "Siyah", "Kırmızı"],
        "Nymphaea caerulea",
        "Mavi nilüfer",
        "'Caeruleus' gök mavisi anlamına gelir. "
        "'Caerulea' dişil biçimidir. Nymphaea caerulea "
        "mavi tonlardaki çiçekleriyle tanınır.",
    ),
    (
        "Flavus",
        "Sarı",
        ["Yeşil", "Mor", "Pembe", "Sarı"],
        "Glaucium flavum",
        "Sarı boynuzlu haşhaş",
        "'Flavus' sarı anlamına gelir. 'Flavum' nötr "
        "biçimidir. Glaucium flavum sarı çiçekler açar.",
    ),
    (
        "Luteus",
        "Sarı veya sarımsı",
        ["Sarı veya sarımsı", "Mavi", "Siyah", "Gri"],
        "Reseda lutea",
        "Sarı muhabbet çiçeği",
        "'Luteus' sarı veya sarımsı anlamına gelir. "
        "'Lutea' dişil biçimidir. Reseda lutea sarı "
        "çiçekleriyle tanınır.",
    ),
    (
        "Aureus",
        "Altın rengi",
        ["Gümüş", "Kahverengi", "Altın rengi", "Mor"],
        "Carex aurea",
        "Altın saz",
        "'Aureus' altın renginde anlamına gelir. "
        "'Aurea' dişil biçimidir. Bu sözcük altın sarısı "
        "tonlarını tanımlamak için kullanılır.",
    ),
    (
        "Viridis",
        "Yeşil",
        ["Kırmızı", "Yeşil", "Pembe", "Turuncu"],
        "Helleborus viridis",
        "Yeşil çöpleme",
        "'Viridis' yeşil anlamına gelir. Bu sözcük "
        "botanikte yeşil renkli organları tanımlamak "
        "için kullanılan sıfatlardan biridir.",
    ),
    (
        "Glaucus",
        "Mavimsi yeşil veya grimsi mavi",
        ["Parlak sarı", "Koyu kırmızı", "Saf beyaz",
         "Mavimsi yeşil veya grimsi mavi"],
        "Rosa glauca",
        "Mavimsi yapraklı gül",
        "'Glaucus' mavimsi yeşil veya grimsi mavi "
        "tonları ifade eder. 'Glauca' dişil biçimidir. "
        "Yapraklardaki mumsu yüzey bu görünümü etkileyebilir.",
    ),
    (
        "Cinereus",
        "Kül grisi",
        ["Kül grisi", "Altın sarısı", "Pembe", "Mor"],
        "Eucalyptus cinerea",
        "Gümüş dolar okaliptüsü",
        "'Cinereus' kül rengi anlamına gelir. "
        "'Cinerea' dişil biçimidir. Bu terim griye "
        "çalan yüzeyleri tanımlayabilir.",
    ),
    (
        "Brunneus",
        "Kahverengi",
        ["Beyaz", "Mavi", "Kahverengi", "Pembe"],
        "Botanik renk sıfatı",
        "Kahverengi",
        "'Brunneus' kahverengi anlamına gelir. "
        "Bitki tanımlarında kahverengi organları "
        "veya yüzeyleri niteleyebilir.",
    ),
    (
        "Rufus",
        "Kızıl veya kızıl kahverengi",
        ["Kızıl veya kızıl kahverengi", "Yeşil",
         "Beyaz", "Gök mavisi"],
        "Botanik renk sıfatı",
        "Kızıl ton",
        "'Rufus' kızıl veya kızıl kahverengi anlamına gelir. "
        "Botanik betimlemelerde kızıl renkli organları "
        "tanımlamak için kullanılabilir.",
    ),
    (
        "Pallidus",
        "Soluk veya açık renkli",
        ["Çok parlak", "Koyu siyah",
         "Soluk veya açık renkli", "Altın rengi"],
        "Botanik renk sıfatı",
        "Soluk renk",
        "'Pallidus' soluk veya açık renkli anlamına gelir. "
        "'Pallida' dişil biçimidir.",
    ),
    (
        "Argenteus",
        "Gümüş rengi",
        ["Turuncu", "Kahverengi", "Kırmızı", "Gümüş rengi"],
        "Salix argentea",
        "Gümüşi söğüt",
        "'Argenteus' gümüş renginde anlamına gelir. "
        "'Argentea' dişil biçimidir. Bitkilerde gümüşi "
        "görünüm tüylerden veya yüzey özelliklerinden "
        "kaynaklanabilir.",
    ),
    (
        "Bicolor",
        "İki renkli",
        ["İki renkli", "Tek renkli", "Renksiz", "Kül grisi"],
        "Viola bicolor",
        "İki renkli menekşe",
        "'Bicolor' iki renkli anlamına gelir. "
        "Botanik tanımlarda iki farklı renk taşıyan "
        "çiçek veya yaprakları ifade edebilir.",
    ),
    (
        "Tricolor",
        "Üç renkli",
        ["Siyah", "Üç renkli", "Altın sarısı", "Gri"],
        "Viola tricolor",
        "Hercai menekşe",
        "'Tricolor' üç renkli anlamına gelir. "
        "Hercai menekşenin çiçeklerinde farklı renkler "
        "bir arada görülebilir.",
    ),
    (
        "Versicolor",
        "Çok renkli veya renkleri değişken",
        ["Beyaz", "Kırmızı", "Çok renkli veya renkleri değişken",
         "Koyu yeşil"],
        "Iris versicolor",
        "Çok renkli süsen",
        "'Versicolor' farklı renkler gösteren anlamına gelir. "
        "Bu sıfat, birden fazla renk taşıyan organları "
        "tanımlayabilir.",
    ),
    (
        "Coccineus",
        "Parlak kızıl veya al kırmızısı",
        ["Gri", "Parlak kızıl veya al kırmızısı",
         "Mavimsi yeşil", "Kahverengi"],
        "Salvia coccinea",
        "Kızıl adaçayı",
        "'Coccineus' parlak kızıl anlamına gelir. "
        "'Coccinea' dişil biçimidir. Kızıl adaçayı "
        "parlak kırmızı çiçekler açabilir.",
    ),
    (
        "Sanguineus",
        "Kan kırmızısı",
        ["Kan kırmızısı", "Soluk sarı", "Gümüş", "Yeşil"],
        "Cornus sanguinea",
        "Kan kızılcığı",
        "'Sanguineus' kan renginde anlamına gelir. "
        "'Sanguinea' dişil biçimidir.",
    ),
    (
        "Spinosus",
        "Dikenli",
        ["Düz yüzeyli", "Dikenli", "Tüysüz", "Yumuşak"],
        "Ruscus aculeatus",
        "Tavşanmemesi",
        "'Spinosus' dikenli anlamına gelir. "
        "Botanikte dikenli organları veya dikenli "
        "görünümü ifade edebilir.",
    ),
    (
        "Dentatus",
        "Dişli kenarlı",
        ["Düz kenarlı", "Dişli kenarlı", "Yuvarlak", "Tüysüz"],
        "Urtica dioica",
        "Büyük ısırgan",
        "'Dentatus' dişli anlamına gelir. "
        "Yaprak kenarlarındaki diş benzeri çıkıntıları "
        "tanımlamak için kullanılabilir.",
    ),
    (
        "Glaber",
        "Tüysüz veya pürüzsüz",
        ["Tüylü", "Tüysüz veya pürüzsüz", "Dikenli", "Benekli"],
        "Acer glabrum",
        "Akçaağaç türü",
        "'Glaber' tüysüz veya pürüzsüz anlamına gelir. "
        "Botanikte yüzeyinde tüy bulunmayan organları "
        "tanımlamak için kullanılır.",
    ),
    (
        "Hirsutus",
        "Uzun veya sert tüylü",
        ["Pürüzsüz", "Parlak", "Uzun veya sert tüylü", "Tüysüz"],
        "Botanik betimleme terimi",
        "Tüylü yüzey",
        "'Hirsutus' belirgin, uzun veya sert tüylerle "
        "kaplı anlamına gelir.",
    ),
    (
        "Tomentosus",
        "Sık ve keçemsi tüylü",
        ["Parlak", "Sık ve keçemsi tüylü", "Tüysüz", "Dikenli"],
        "Botanik betimleme terimi",
        "Keçemsi tüylü yüzey",
        "'Tomentosus' sık, yumuşak ve keçemsi tüylerle "
        "kaplı anlamına gelir.",
    ),
    (
        "Maculatus",
        "Benekli veya lekeli",
        ["Çizgili", "Düz renkli", "Benekli veya lekeli", "Şeffaf"],
        "Botanik betimleme terimi",
        "Benekli yüzey",
        "'Maculatus' benekli veya lekeli anlamına gelir. "
        "Yapraklardaki lekeleri tanımlamak için kullanılabilir.",
    ),
    (
        "Striatus",
        "Çizgili veya şeritli",
        ["Çizgili veya şeritli", "Beyaz", "Kızıl", "Altın rengi"],
        "Botanik betimleme terimi",
        "Çizgili yüzey",
        "'Striatus' çizgili veya şeritli anlamına gelir.",
    ),
    (
        "Nitidus",
        "Parlak veya ışıldayan",
        ["Mat", "Parlak veya ışıldayan", "Soluk", "Kül grisi"],
        "Botanik betimleme terimi",
        "Parlak yüzey",
        "'Nitidus' parlak veya ışıldayan anlamına gelir.",
    ),
    (
        "Obscurus",
        "Koyu, karanlık veya mat",
        ["Açık", "Parlak", "Koyu, karanlık veya mat", "Süt beyazı"],
        "Botanik betimleme terimi",
        "Koyu yüzey",
        "'Obscurus' koyu veya karanlık anlamına gelir.",
    ),
    (
        "Subalbus",
        "Beyazımsı",
        ["Kırmızı", "Beyazımsı", "Siyah", "Mavi"],
        "Botanik betimleme terimi",
        "Beyazımsı renk",
        "'Sub-' öneki yaklaşık veya bir ölçüde anlamı "
        "katabilir. 'Subalbus' beyazımsı olarak yorumlanır.",
    ),
    (
        "Subflavus",
        "Sarımsı",
        ["Gümüş", "Mor", "Sarımsı", "Koyu siyah"],
        "Botanik betimleme terimi",
        "Sarımsı renk",
        "'Subflavus' sarımsı anlamına gelir. "
        "'Flavus' sarı demektir.",
    ),
    (
        "Rubescens",
        "Kırmızılaşan veya kızaran",
        ["Yeşile dönen", "Kırmızılaşan veya kızaran",
         "Beyazlaşan", "Maviye dönen"],
        "Botanik betimleme terimi",
        "Kızaran yüzey",
        "'Rubescens' kızaran veya kırmızılaşan anlamına gelir.",
    ),
    (
        "Flavescens",
        "Sarılaşan",
        ["Mavileşen", "Kararan", "Morlaşan", "Sarılaşan"],
        "Botanik betimleme terimi",
        "Sarılaşan yüzey",
        "'Flavescens' sarılaşan veya sarımsı hâle gelen "
        "anlamına gelir.",
    ),
    (
        "Viridescens",
        "Yeşilimsi veya yeşile dönen",
        ["Yeşilimsi veya yeşile dönen", "Kırmızılaşan",
         "Beyazlaşan", "Kararan"],
        "Botanik betimleme terimi",
        "Yeşilimsi yüzey",
        "'Viridescens' yeşilimsi veya yeşile dönen anlamına gelir.",
    ),
    (
        "Lacteus",
        "Süt beyazı",
        ["Koyu kahverengi", "Mor", "Süt beyazı", "Turuncu"],
        "Euphorbia lactea",
        "Sütleğen",
        "'Lacteus' süt renginde anlamına gelir. "
        "'Lactea' dişil biçimidir.",
    ),
    (
        "Niveus",
        "Kar beyazı",
        ["Kızıl", "Yeşil", "Mavi", "Kar beyazı"],
        "Botanik betimleme terimi",
        "Kar beyazı renk",
        "'Niveus' kar gibi beyaz anlamına gelir.",
    ),
    (
        "Azureus",
        "Azur veya gök mavisi",
        ["Koyu kahverengi", "Azur veya gök mavisi", "Siyah", "Pembe"],
        "Salvia azurea",
        "Gök adaçayı",
        "'Azureus' gök mavisi anlamına gelir. "
        "'Azurea' dişil biçimidir.",
    ),
    (
        "Canus",
        "Beyazımsı gri veya kırçıllı",
        ["Turuncu", "Mor", "Beyazımsı gri veya kırçıllı", "Parlak kırmızı"],
        "Artemisia cana",
        "Gri yapraklı pelin",
        "'Canus' beyazımsı gri veya kırçıllı anlamına gelir. "
        "'Cana' dişil biçimidir.",
    ),
    (
        "Micans",
        "Parıldayan veya ışıltılı",
        ["Kül grisi", "Parıldayan veya ışıltılı", "Soluk", "Siyah"],
        "Botanik betimleme terimi",
        "Parlak yüzey",
        "'Micans' parıldayan veya ışıldayan anlamına gelir.",
    ),
    (
        "Clarus",
        "Açık, berrak veya parlak",
        ["Açık, berrak veya parlak", "Siyah", "Koyu kahverengi", "Kırmızı"],
        "Botanik betimleme terimi",
        "Açık renk",
        "'Clarus' açık, berrak veya parlak anlamına gelir.",
    ),
    (
        "Opacus",
        "Mat veya donuk",
        ["Parlak", "Mat veya donuk", "Gümüş", "Kızıl"],
        "Botanik betimleme terimi",
        "Mat yüzey",
        "'Opacus' mat veya donuk anlamına gelir.",
    ),
    (
        "Fulvus",
        "Sarımsı kahverengi",
        ["Mavi", "Siyah", "Mor", "Sarımsı kahverengi"],
        "Botanik betimleme terimi",
        "Sarımsı kahverengi",
        "'Fulvus' sarımsı kahverengi tonları ifade eder.",
    ),
    (
        "Fuscus",
        "Koyu kahverengi veya esmer",
        ["Açık mavi", "Koyu kahverengi veya esmer",
         "Kar beyazı", "Parlak pembe"],
        "Botanik betimleme terimi",
        "Koyu renk",
        "'Fuscus' koyu veya esmer anlamına gelir.",
    ),
    (
        "Pallens",
        "Soluk veya solgun",
        ["Çok koyu", "Altın rengi", "Soluk veya solgun", "Bakır rengi"],
        "Botanik betimleme terimi",
        "Soluk renk",
        "'Pallens' soluk veya solgun anlamına gelir.",
    ),
    (
        "Albicans",
        "Beyazımsı veya beyazlaşan",
        ["Siyahımsı", "Sarımsı", "Beyazımsı veya beyazlaşan", "Kızılımsı"],
        "Botanik betimleme terimi",
        "Beyazımsı yüzey",
        "'Albicans' beyazımsı veya beyazlaşan anlamına gelir.",
    ),
    (
        "Lividus",
        "Kurşuni veya mavimsi gri",
        ["Altın sarısı", "Kurşuni veya mavimsi gri", "Pembe", "Yeşil"],
        "Helleborus lividus",
        "Mavimsi çöpleme",
        "'Lividus' kurşuni, mavimsi gri veya soluk mor "
        "tonları ifade eder.",
    ),
]


# ============================================================
# 4. SORU HAVUZUNU DOĞRULAMA
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

        seen.add(latin.casefold())

        clean_options = list(
            dict.fromkeys(
                str(option).strip()
                for option in options
                if option is not None and str(option).strip()
            )
        )

        if answer not in clean_options:
            clean_options.append(answer)

        if len(clean_options) < 4:
            continue

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
        <div class="metric-card">
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

    source = QUESTIONS.copy()
    random.shuffle(source)
    selected = source[:count]

    all_answers = list(dict.fromkeys(
        question["answer"] for question in QUESTIONS
    ))

    prepared = []

    for question in selected:
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

        options = [correct_answer] + distractors[:3]
        options = list(dict.fromkeys(options))

        if len(options) != 4:
            continue

        random.shuffle(options)

        prepared_question = question.copy()
        prepared_question["options"] = options

        prepared.append(prepared_question)

    if not prepared:
        raise ValueError("Geçerli soru oluşturulamadı.")

    return prepared


def start_quiz(name, count):
    name = str(name).strip()

    if not name:
        raise ValueError("Lütfen bir ad veya takma ad gir.")

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
    run_id = st.session_state.run_id

    if not run_id:
        return

    if st.session_state.submitted_run_id == run_id:
        return

    questions = st.session_state.quiz_questions

    if not questions:
        return

    start_time = st.session_state.start_time

    elapsed = (
        round(time.time() - start_time, 2)
        if start_time is not None
        else 0.0
    )

    st.session_state.elapsed_time = elapsed

    st.session_state.leaderboard.append({
        "İsim": st.session_state.name,
        "Doğru Sayısı": st.session_state.score,
        "Toplam Soru": len(questions),
        "Başarı (%)": round(
            st.session_state.score / len(questions) * 100,
            1,
        ),
        "Süre (sn)": elapsed,
    })

    st.session_state.submitted_run_id = run_id


def reset_quiz(clear_name=False):
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
    records = st.session_state.leaderboard

    if not records:
        st.info(
            "🌱 Henüz sonuç kaydedilmedi. "
            "İlk testi tamamlayarak liderlik tablosunu oluşturabilirsin."
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
        df,
        use_container_width=True,
    )


# ============================================================
# 7. BAŞLIK
# ============================================================

def render_header():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">🌿 BOTANICA AKADEMİ</div>

            <h1>Doğanın Dilini Keşfet.</h1>

            <p>
                Latince botanik terimlerini öğren,
                renklerin ardındaki anlamları keşfet
                ve bilgini test et.
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

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True,
    )

    with st.form("register_form"):
        name = st.text_input(
            "Adın veya takma adın",
            value=st.session_state.name,
            placeholder="Örn. Botanica",
            max_chars=50,
        )

        maximum = len(QUESTIONS)

        count_options = sorted({
            n
            for n in [5, 10, 15, 20, 30, 40, 50, 60, maximum]
            if 1 <= n <= maximum
        })

        if not count_options:
            st.error("Test oluşturmak için yeterli soru bulunamadı.")
            st.stop()

        default_count = min(10, maximum)

        selected_count = st.selectbox(
            "Test uzunluğu",
            options=count_options,
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
            1. Adını veya takma adını yaz.
            2. Test uzunluğunu seç.
            3. Latince terimin anlamını bul.
            4. Cevap açıklamalarını oku.
            5. Sonuçlarını ve başarı oranını incele.
            """
        )


# ============================================================
# 9. TEST EKRANI
# ============================================================

def render_quiz():
    questions = st.session_state.quiz_questions
    index = st.session_state.current_question

    if not questions:
        st.error("Soru bulunamadı. Yeni bir test başlat.")
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
        <div class="panel">
            <div class="eyebrow">BOTANİK TERİM</div>
            <div class="latin">{safe_text(q['latin'])}</div>
            <p>{safe_text(q['question'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    form_key = f"quiz_form_{st.session_state.run_id}_{index}"

    with st.form(form_key):
        selected = st.radio(
            "Cevabını seç:",
            options=q["options"],
            index=None,
            key=f"answer_{st.session_state.run_id}_{index}",
        )

        submitted = st.form_submit_button(
            "Cevabı Kontrol Et ✨",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        if selected is None:
            st.warning("Lütfen bir cevap seç.")
            return

        # Aynı sorunun birden fazla kez puanlanmasını engelle.
        already_answered = (
            len(st.session_state.answers) > index
        )

        if already_answered:
            st.warning("Bu soruyu zaten cevapladın.")
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


# ============================================================
# 10. CEVAP VE AÇIKLAMA EKRANI
# ============================================================

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
        st.error(
            f"Yanlış cevap. Doğru cevap: {answer['correct']}"
        )

    st.markdown(
        f"""
        <div class="panel">
            <div class="eyebrow">BOTANİK BİLGİSİ</div>

            <div style="
                font-size: 1.25rem;
                font-weight: 850;
                font-style: italic;
            ">
                🌿 {safe_text(answer['plant'])}
            </div>

            <p style="opacity: .75;">
                {safe_text(answer['plant_name'])}
            </p>

            <p style="line-height: 1.8;">
                {safe_text(answer['explanation'])}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    current = st.session_state.current_question
    total = len(st.session_state.quiz_questions)

    label = (
        "Sonuçları Gör 🏆"
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
# 11. SONUÇ EKRANI
# ============================================================

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
            <div class="eyebrow">QUIZ TAMAMLANDI 🌿</div>

            <div style="
                font-size: clamp(3rem, 10vw, 4.5rem);
                font-weight: 900;
                margin: .5rem 0;
            ">
                {score} / {total}
            </div>

            <h2 style="color: white;">
                Başarı oranı: %{percentage:.0f}
            </h2>

            <p>
                Tamamlanma süresi:
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
        metric_card("Doğru cevap", score)

    with col2:
        metric_card("Yanlış cevap", total - score)

    with col3:
        metric_card("Başarı", f"%{percentage:.0f}")

    if percentage >= 80:
        st.success(
            "🏆 Mükemmel! Botanik renk bilgine hâkim görünüyorsun."
        )
    elif percentage >= 50:
        st.info(
            "🌱 Güzel iş! Birkaç tekrar ile daha da ilerleyebilirsin."
        )
    else:
        st.warning(
            "📚 Yeni bir turla bilgilerini geliştirebilirsin."
        )

    st.subheader("🏆 Liderlik Tablosu")
    render_leaderboard()

    st.divider()

    with st.expander("📝 Cevaplarını İncele"):
        for i, answer in enumerate(
            st.session_state.answers,
            start=1,
        ):
            status = (
                "✅ Doğru"
                if answer["is_correct"]
                else "❌ Yanlış"
            )

            st.markdown(
                f"**{i}. {answer['latin']} — {status}**"
            )

            st.write(f"Verdiğin cevap: {answer['selected']}")
            st.write(f"Doğru cevap: {answer['correct']}")

            st.caption(
                f"{answer['plant']} — {answer['plant_name']}"
            )

            st.write(answer["explanation"])
            st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Tekrar Oyna 🔄",
            use_container_width=True,
        ):
            reset_quiz()
            st.rerun()

    with col2:
        if st.button(
            "Ana Sayfaya Dön 🏠",
            use_container_width=True,
        ):
            reset_quiz(clear_name=True)
            st.rerun()


# ============================================================
# 12. ANA UYGULAMA
# ============================================================

if not QUESTIONS:
    st.error(
        "Soru havuzu yüklenemedi. "
        "RAW_QUESTIONS listesini kontrol et."
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
