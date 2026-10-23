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
# 2. PREMIUM TASARIM
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

    #MainMenu, footer {
        visibility: hidden;
    }

    .hero {
        padding: 2rem;
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

    .hero h2 {
        color: #ffffff;
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
        letter-spacing: -.055em;
        overflow-wrap: anywhere;
        line-height: 1.1;
        margin: .6rem 0 1rem;
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
        font-size: clamp(1.1rem, 4vw, 2rem);
        font-weight: 900;
        letter-spacing: -.04em;
        overflow-wrap: anywhere;
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
# 3. RASTGELE BİTKİ İSİMLERİ
# ============================================================

PLANT_NAMES = [
    "Lavanta",
    "Biberiye",
    "Papatya",
    "Orkide",
    "Manolya",
    "Yasemin",
    "Lale",
    "Menekşe",
    "Nilüfer",
    "Fesleğen",
    "Kekik",
    "Adaçayı",
    "Nergis",
    "Sümbül",
    "Kamelya",
    "Begonya",
    "Gardenya",
    "Zambak",
    "Akasya",
    "Mimoza",
    "Defne",
    "Zeytin",
    "Kardelen",
    "Gelincik",
    "Badem",
    "Bambu",
    "Sardunya",
    "Ortanca",
    "Sıklamen",
    "Gül",
    "Menengiç",
    "Melisa",
    "Mine Çiçeği",
    "Fulya",
    "Açelya",
    "Şakayık",
    "Süsen",
    "Karanfil",
    "Çuha Çiçeği",
    "Kasımpatı",
]


# ============================================================
# 4. SORU HAVUZU
# ============================================================

# Soru formatı:
# (
#     Latince terim,
#     Doğru cevap,
#     Cevap seçenekleri,
#     Örnek bitkinin bilimsel adı,
#     Bitkinin Türkçe adı,
#     Açıklama,
# )

RAW_QUESTIONS = [
    (
        "Glaber",
        "Tüysüz veya pürüzsüz",
        ["Tüylü", "Tüysüz veya pürüzsüz", "Dikenli", "Benekli"],
        "Acer glabrum",
        "Pürüzsüz akçaağaç",
        "'Glaber' tüysüz veya pürüzsüz anlamına gelir. "
        "Botanikte bitki yüzeyinde tüy bulunmamasını ifade eder. "
        "Sıfatın biçimi, eşlik ettiği bilimsel ada göre değişebilir.",
    ),
    (
        "Hirsutus",
        "Uzun veya sert tüylü",
        ["Pürüzsüz", "Parlak", "Uzun veya sert tüylü", "Tüysüz"],
        "Rosa hirsuta",
        "Tüylü gül",
        "'Hirsutus' uzun veya sert tüylerle kaplı anlamına gelir. "
        "Yaprak ve gövde yüzeyindeki belirgin tüyleri tanımlamak "
        "için kullanılan botanik terimlerdendir.",
    ),
    (
        "Glabrescens",
        "Zamanla tüysüzleşen",
        [
            "Zamanla tüysüzleşen",
            "Sürekli tüylü",
            "Dikenlenen",
            "Renk değiştiren",
        ],
        "Bitkilerde glabrescent yüzey",
        "Zamanla tüysüzleşen yüzey",
        "'Glabrescens', gelişim sırasında tüylerini kaybederek "
        "tüysüzleşen bitki yüzeyini ifade eder.",
    ),
    (
        "Tomentosus",
        "Sık ve keçemsi tüylü",
        ["Parlak", "Sık ve keçemsi tüylü", "Tüysüz", "Dikenli"],
        "Verbascum",
        "Sığırkuyruğu",
        "'Tomentosus' sık, yumuşak ve keçemsi tüylerle kaplı "
        "anlamına gelir. Bu tüyler bitki yüzeyinin dokusunu "
        "ve görünümünü değiştirebilir.",
    ),
    (
        "Spinosus",
        "Dikenli",
        ["Düz yüzeyli", "Dikenli", "Tüysüz", "Yumuşak"],
        "Ruscus aculeatus",
        "Tavşanmemesi",
        "'Spinosus' dikenli anlamına gelir. Botanikte diken "
        "taşıyan bitkileri veya dikenli görünümü tanımlayabilir.",
    ),
    (
        "Dentatus",
        "Dişli kenarlı",
        ["Düz kenarlı", "Dişli kenarlı", "Yuvarlak", "Tüysüz"],
        "Urtica dioica",
        "Büyük ısırgan",
        "'Dentatus' dişli anlamına gelir. Yaprak kenarlarında "
        "diş benzeri çıkıntılar bulunmasını ifade eder.",
    ),
    (
        "Albus",
        "Beyaz",
        ["Siyah", "Beyaz", "Kırmızı", "Sarı"],
        "Nymphaea alba",
        "Beyaz nilüfer",
        "'Albus' Latince beyaz anlamına gelir. 'Alba' dişil, "
        "'album' ise nötr biçimidir. Sıfatın biçimi, bilimsel "
        "adın dilbilgisel yapısıyla uyum gösterir.",
    ),
    (
        "Niger",
        "Siyah veya çok koyu",
        ["Yeşil", "Mavi", "Siyah veya çok koyu", "Pembe"],
        "Sambucus nigra",
        "Kara mürver",
        "'Niger' siyah veya çok koyu renkli anlamına gelir. "
        "'Nigra', aynı sıfatın dişil biçimidir.",
    ),
    (
        "Ruber",
        "Kırmızı",
        ["Kırmızı", "Mor", "Gri", "Beyaz"],
        "Quercus rubra",
        "Kırmızı meşe",
        "'Ruber' Latince kırmızı anlamına gelir. 'Rubra', "
        "sıfatın dişil biçimidir.",
    ),
    (
        "Roseus",
        "Gül pembesi",
        ["Turuncu", "Kahverengi", "Sarı", "Gül pembesi"],
        "Catharanthus roseus",
        "Madagaskar cezayir menekşesi",
        "'Roseus' gül renginde veya gül pembesi anlamına gelir. "
        "Türün pembe çiçekli formları bu renkle ilişkilendirilir.",
    ),
    (
        "Purpureus",
        "Mor veya erguvan",
        ["Mavi", "Mor veya erguvan", "Yeşil", "Gümüş"],
        "Echinacea purpurea",
        "Mor ekinezya",
        "'Purpureus' mor veya erguvan tonlarını ifade eder. "
        "'Purpurea', sıfatın dişil biçimidir.",
    ),
    (
        "Violaceus",
        "Menekşe moru",
        ["Kahverengi", "Sarı", "Menekşe moru", "Beyaz"],
        "Viola",
        "Menekşe",
        "'Violaceus' menekşe moru anlamına gelir. Bitkilerin "
        "çiçek rengini tanımlamak için kullanılabilir.",
    ),
    (
        "Caeruleus",
        "Gök mavisi",
        ["Gri", "Gök mavisi", "Siyah", "Kırmızı"],
        "Nymphaea caerulea",
        "Mavi nilüfer",
        "'Caeruleus' gök mavisi anlamına gelir. 'Caerulea', "
        "aynı sıfatın dişil biçimidir.",
    ),
    (
        "Flavus",
        "Sarı",
        ["Yeşil", "Mor", "Pembe", "Sarı"],
        "Glaucium flavum",
        "Sarı boynuzlu haşhaş",
        "'Flavus' Latince sarı anlamına gelir. 'Flavum', "
        "sıfatın nötr biçimidir.",
    ),
    (
        "Luteus",
        "Sarı veya sarımsı",
        ["Sarı veya sarımsı", "Mavi", "Siyah", "Gri"],
        "Reseda lutea",
        "Sarı muhabbet çiçeği",
        "'Luteus' sarı veya sarımsı anlamına gelir. 'Lutea', "
        "aynı sıfatın dişil biçimidir.",
    ),
    (
        "Aureus",
        "Altın rengi",
        ["Gümüş", "Kahverengi", "Altın rengi", "Mor"],
        "Carex aurea",
        "Altın saz",
        "'Aureus' altın renginde veya altın sarısı anlamına gelir. "
        "'Aurea', sıfatın dişil biçimidir.",
    ),
    (
        "Viridis",
        "Yeşil",
        ["Kırmızı", "Yeşil", "Pembe", "Turuncu"],
        "Helleborus viridis",
        "Yeşil çöpleme",
        "'Viridis' Latince yeşil anlamına gelir. Bitki organlarının "
        "yeşil rengini tanımlamak için kullanılabilir.",
    ),
    (
        "Glaucus",
        "Mavimsi yeşil veya grimsi mavi",
        [
            "Parlak sarı",
            "Koyu kırmızı",
            "Saf beyaz",
            "Mavimsi yeşil veya grimsi mavi",
        ],
        "Rosa glauca",
        "Mavimsi yapraklı gül",
        "'Glaucus' mavimsi yeşil veya grimsi mavi, çoğunlukla "
        "puslu görünümlü tonları ifade eder.",
    ),
    (
        "Cinereus",
        "Kül grisi",
        ["Kül grisi", "Altın sarısı", "Pembe", "Mor"],
        "Eucalyptus cinerea",
        "Gümüş dolar okaliptüsü",
        "'Cinereus' kül rengi veya kül grisi anlamına gelir.",
    ),
    (
        "Brunneus",
        "Kahverengi",
        ["Beyaz", "Mavi", "Kahverengi", "Pembe"],
        "Bitkilerde kahverengi renk",
        "Kahverengi bitki dokuları",
        "'Brunneus' kahverengi anlamına gelir. Bitki organlarının "
        "rengini tanımlamak için kullanılabilir.",
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
        "Bitkilerde koyu renk",
        "Koyu renkli bitki dokuları",
        "'Fuscus' koyu, esmer veya koyu kahverengiye çalan "
        "anlamına gelir.",
    ),
    (
        "Fulvus",
        "Sarımsı kahverengi",
        ["Mavi", "Siyah", "Mor", "Sarımsı kahverengi"],
        "Bitkilerde sarımsı kahverengi renk",
        "Sarımsı kahverengi bitki dokuları",
        "'Fulvus' sarımsı kahverengi veya boz tonları ifade eder.",
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
        "Bitkilerde kızıl renk",
        "Kızıl bitki dokuları",
        "'Rufus' kızıl veya kızıl kahverengi anlamına gelir.",
    ),
    (
        "Pallidus",
        "Soluk veya açık renkli",
        ["Çok parlak", "Koyu siyah", "Soluk veya açık renkli", "Altın rengi"],
        "Bitkilerde soluk renk",
        "Soluk renkli bitki dokuları",
        "'Pallidus' soluk, solgun veya açık renkli anlamına gelir.",
    ),
    (
        "Argenteus",
        "Gümüş rengi",
        ["Turuncu", "Kahverengi", "Kırmızı", "Gümüş rengi"],
        "Salix",
        "Söğüt",
        "'Argenteus' gümüş renginde veya gümüşi anlamına gelir.",
    ),
    (
        "Lilacinus",
        "Leylak rengi",
        ["Yeşil", "Leylak rengi", "Siyah", "Sarı"],
        "Bitkilerde leylak rengi",
        "Leylak renkli bitki dokuları",
        "'Lilacinus' leylak rengi veya açık mor anlamına gelir.",
    ),
    (
        "Atropurpureus",
        "Çok koyu mor veya siyaha çalan erguvan",
        ["Açık sarı", "Çok koyu mor veya siyaha çalan erguvan", "Beyaz", "Gümüş"],
        "Koyu mor yapraklı bitkiler",
        "Koyu mor yapraklar",
        "'Atropurpureus' çok koyu mor veya siyaha çalan "
        "erguvan tonlarını ifade eder.",
    ),
    (
        "Cupreus",
        "Bakır rengi",
        ["Bakır rengi", "Mavi", "Beyaz", "Pembe"],
        "Bitkilerde bakır rengi",
        "Bakır renkli bitki dokuları",
        "'Cupreus' bakır renginde veya bakırımsı anlamına gelir.",
    ),
    (
        "Lacteus",
        "Süt beyazı",
        ["Koyu kahverengi", "Mor", "Süt beyazı", "Turuncu"],
        "Euphorbia lactea",
        "Sütleğen",
        "'Lacteus' süt renginde veya süt beyazı anlamına gelir.",
    ),
    (
        "Niveus",
        "Kar beyazı",
        ["Kızıl", "Yeşil", "Mavi", "Kar beyazı"],
        "Rubus niveus",
        "Böğürtlen cinsi bir bitki",
        "'Niveus' kar gibi beyaz anlamına gelir.",
    ),
    (
        "Bicolor",
        "İki renkli",
        ["İki renkli", "Tek renkli", "Renksiz", "Kül grisi"],
        "Viola",
        "Menekşe",
        "'Bicolor' iki renkli anlamına gelir. Çiçeklerde veya "
        "yapraklarda iki farklı rengin bulunmasını ifade edebilir.",
    ),
    (
        "Tricolor",
        "Üç renkli",
        ["Siyah", "Üç renkli", "Altın sarısı", "Gri"],
        "Viola tricolor",
        "Hercai menekşe",
        "'Tricolor' üç renkli anlamına gelir. Hercai menekşede "
        "farklı renkler aynı çiçekte görülebilir.",
    ),
    (
        "Versicolor",
        "Çok renkli veya renkleri değişken",
        ["Beyaz", "Kırmızı", "Çok renkli veya renkleri değişken", "Koyu yeşil"],
        "Iris versicolor",
        "Çok renkli süsen",
        "'Versicolor' farklı renkler gösteren veya renkleri "
        "değişken olan anlamına gelir.",
    ),
    (
        "Coccineus",
        "Parlak kızıl veya al kırmızısı",
        ["Gri", "Parlak kızıl veya al kırmızısı", "Mavimsi yeşil", "Kahverengi"],
        "Salvia coccinea",
        "Kızıl adaçayı",
        "'Coccineus' parlak kızıl veya al kırmızısı anlamına gelir.",
    ),
    (
        "Sanguineus",
        "Kan kırmızısı",
        ["Kan kırmızısı", "Soluk sarı", "Gümüş", "Yeşil"],
        "Cornus sanguinea",
        "Kan kızılcığı",
        "'Sanguineus' kan renginde veya kan kırmızısı anlamına gelir.",
    ),
    (
        "Pallens",
        "Soluk veya solgun",
        ["Çok koyu", "Altın rengi", "Soluk veya solgun", "Bakır rengi"],
        "Bitkilerde soluk renk",
        "Soluk bitki dokuları",
        "'Pallens' soluk veya solgun anlamına gelir.",
    ),
    (
        "Rubescens",
        "Kırmızılaşan veya kızaran",
        ["Yeşile dönen", "Kırmızılaşan veya kızaran", "Beyazlaşan", "Maviye dönen"],
        "Bitkilerde kırmızılaşma",
        "Kırmızılaşan bitki dokuları",
        "'Rubescens' kızaran veya kırmızılaşan anlamına gelir.",
    ),
    (
        "Albicans",
        "Beyazımsı veya beyazlaşan",
        ["Siyahımsı", "Sarımsı", "Beyazımsı veya beyazlaşan", "Kızılımsı"],
        "Bitkilerde beyazlaşma",
        "Beyazımsı bitki dokuları",
        "'Albicans' beyazımsı veya beyazlaşan anlamına gelir.",
    ),
    (
        "Flavescens",
        "Sarılaşan veya sarımsı",
        ["Mavileşen", "Kararan", "Morlaşan", "Sarılaşan veya sarımsı"],
        "Bitkilerde sarılaşma",
        "Sarılaşan bitki dokuları",
        "'Flavescens' sarılaşan veya sarımsı hâle gelen anlamına gelir.",
    ),
    (
        "Viridescens",
        "Yeşilimsi veya yeşile dönen",
        ["Yeşilimsi veya yeşile dönen", "Kırmızılaşan", "Beyazlaşan", "Kararan"],
        "Bitkilerde yeşile dönüş",
        "Yeşilimsi bitki dokuları",
        "'Viridescens' yeşilimsi veya yeşile dönen anlamına gelir.",
    ),
    (
        "Obscurus",
        "Koyu, karanlık veya mat",
        ["Açık", "Parlak", "Koyu, karanlık veya mat", "Süt beyazı"],
        "Bitkilerde koyu renk",
        "Koyu renkli bitki dokuları",
        "'Obscurus' koyu, karanlık veya belirsiz anlamlarına gelir.",
    ),
    (
        "Nitidus",
        "Parlak veya ışıldayan",
        ["Mat", "Parlak veya ışıldayan", "Soluk", "Kül grisi"],
        "Bitkilerde parlak yüzey",
        "Parlak bitki yüzeyleri",
        "'Nitidus' parlak veya ışıldayan anlamına gelir.",
    ),
    (
        "Maculatus",
        "Benekli veya lekeli",
        ["Çizgili", "Düz renkli", "Benekli veya lekeli", "Şeffaf"],
        "Benekli bitki yaprakları",
        "Benekli yapraklar",
        "'Maculatus' benekli veya lekeli anlamına gelir.",
    ),
    (
        "Striatus",
        "Çizgili veya şeritli",
        ["Çizgili veya şeritli", "Beyaz", "Kızıl", "Altın rengi"],
        "Çizgili bitki yaprakları",
        "Çizgili yapraklar",
        "'Striatus' çizgili veya şeritli anlamına gelir.",
    ),
    (
        "Azureus",
        "Azur veya gök mavisi",
        ["Koyu kahverengi", "Azur veya gök mavisi", "Siyah", "Pembe"],
        "Salvia azurea",
        "Gök adaçayı",
        "'Azureus' azur veya gök mavisi anlamına gelir.",
    ),
    (
        "Canus",
        "Beyazımsı gri veya kırçıllı",
        ["Turuncu", "Mor", "Beyazımsı gri veya kırçıllı", "Parlak kırmızı"],
        "Artemisia cana",
        "Gri yapraklı pelin",
        "'Canus' beyazımsı gri veya kırçıllı anlamına gelir.",
    ),
    (
        "Lividus",
        "Kurşuni, mavimsi gri veya soluk mor",
        ["Altın sarısı", "Kurşuni, mavimsi gri veya soluk mor", "Pembe", "Yeşil"],
        "Helleborus lividus",
        "Mavimsi çöpleme",
        "'Lividus' kurşuni, mavimsi gri veya soluk mor tonlarını ifade eder.",
    ),
    (
        "Coloratus",
        "Renkli veya belirgin renk taşıyan",
        ["Renksiz", "Renkli veya belirgin renk taşıyan", "Yalnızca beyaz", "Çizgili"],
        "Renkli bitki dokuları",
        "Belirgin renk taşıyan bitki dokuları",
        "'Coloratus' renkli veya belirgin biçimde renklendirilmiş anlamına gelir.",
    ),
    (
        "Piceus",
        "Zift siyahı veya katran rengi",
        ["Kar beyazı", "Zift siyahı veya katran rengi", "Leylak", "Gümüş"],
        "Bitkilerde çok koyu renk",
        "Koyu renkli bitki dokuları",
        "'Piceus' zift siyahı veya katran rengi anlamına gelir.",
    ),
    (
        "Dilutus",
        "Seyreltik veya soluk renkli",
        ["Çok koyu", "Seyreltik veya soluk renkli", "Parlak siyah", "Altın rengi"],
        "Bitkilerde soluk renk",
        "Soluk bitki dokuları",
        "'Dilutus' seyreltilmiş veya yoğunluğu azaltılmış anlamına gelir.",
    ),
    (
        "Clarus",
        "Açık, berrak veya parlak",
        ["Açık, berrak veya parlak", "Siyah", "Koyu kahverengi", "Kırmızı"],
        "Bitkilerde açık renk",
        "Açık renkli bitki dokuları",
        "'Clarus' açık, berrak veya parlak anlamına gelir.",
    ),
    (
        "Saturatus",
        "Doygun veya yoğun renkli",
        ["Soluk", "Doygun veya yoğun renkli", "Renksiz", "Şeffaf"],
        "Bitkilerde yoğun renk",
        "Yoğun renkli bitki dokuları",
        "'Saturatus' doygun veya yoğun renkli anlamına gelir.",
    ),
    (
        "Opacus",
        "Mat, donuk veya ışık geçirmeyen",
        ["Parlak", "Mat, donuk veya ışık geçirmeyen", "Gümüş", "Kızıl"],
        "Bitkilerde mat yüzey",
        "Mat bitki yüzeyleri",
        "'Opacus' mat, donuk veya ışık geçirmeyen anlamına gelir.",
    ),
    (
        "Micans",
        "Parıldayan veya ışıltılı",
        ["Kül grisi", "Parıldayan veya ışıltılı", "Soluk", "Siyah"],
        "Parlak bitki yüzeyleri",
        "Işıltılı bitki yüzeyleri",
        "'Micans' parıldayan veya ışıldayan anlamına gelir.",
    ),
    (
        "Subalbus",
        "Beyazımsı",
        ["Kırmızı", "Beyazımsı", "Siyah", "Mavi"],
        "Beyazımsı bitki dokuları",
        "Beyazımsı renk",
        "'Sub-' öneki, temel anlama yaklaşık veya daha düşük "
        "derecede olma anlamı katabilir. 'Subalbus' beyazımsı demektir.",
    ),
    (
        "Subflavus",
        "Sarımsı",
        ["Gümüş", "Mor", "Sarımsı", "Koyu siyah"],
        "Sarımsı bitki dokuları",
        "Sarımsı renk",
        "'Subflavus', sarıya yakın veya sarımsı anlamına gelir.",
    ),
    (
        "Subrubens",
        "Kırmızımsı",
        ["Kırmızımsı", "Mavimsi", "Yeşilimsi", "Beyazımsı"],
        "Kırmızımsı bitki dokuları",
        "Kırmızımsı renk",
        "'Subrubens' kırmızımsı anlamına gelir.",
    ),
    (
        "Subviridis",
        "Yeşilimsi",
        ["Kızıl", "Gümüş", "Yeşilimsi", "Siyah"],
        "Yeşilimsi bitki dokuları",
        "Yeşilimsi renk",
        "'Subviridis' yeşilimsi anlamına gelir.",
    ),
]


# ============================================================
# 5. SORU HAVUZUNU DOĞRULAMA
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
                "question": (
                    f"'{latin}' hangi rengi veya özelliği ifade eder?"
                ),
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
# 6. OTURUM DURUMU
# ============================================================

DEFAULTS = {
    "stage": "register",
    "name": "",
    "student_number": "",
    "plant_name": None,
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
            value.copy() if isinstance(value, (dict, list)) else value
        )


# ============================================================
# 7. YARDIMCI FONKSİYONLAR
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

    # Doğru cevapların seçeneklerdeki yerlerini dengeli dağıt.
    positions = [i % 4 for i in range(count)]
    random.shuffle(positions)

    all_answers = list(dict.fromkeys(q["answer"] for q in QUESTIONS))

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

        if len(set(options)) != 4:
            continue

        item = question.copy()
        item["options"] = options

        prepared.append(item)

    if not prepared:
        raise ValueError("Geçerli sorular hazırlanamadı.")

    return prepared


def start_quiz(name, count):
    name = str(name).strip()

    if not name:
        raise ValueError("Öğrenci numarası ve bitki adı gereklidir.")

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

    st.session_state.leaderboard.append(
        {
            "Öğrenci": st.session_state.name,
            "Öğrenci Numarası": st.session_state.student_number,
            "Bitki": st.session_state.plant_name or "",
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
            "plant_name": None,
        }
    )

    if clear_name:
        st.session_state.name = ""
        st.session_state.student_number = ""


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

    columns = [
        "Öğrenci",
        "Bitki",
        "Doğru Sayısı",
        "Toplam Soru",
        "Başarı (%)",
        "Süre (sn)",
    ]

    st.dataframe(
        df[columns],
        use_container_width=True,
    )


# ============================================================
# 8. SAYFA BAŞLIĞI
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
# 9. ÖĞRENCİ GİRİŞ EKRANI
# ============================================================

def render_register():
    render_header()

    st.subheader("🌱 Öğrenci Girişi")

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
        student_number = st.text_input(
            "Öğrenci numaranız",
            value=st.session_state.student_number,
            placeholder="Örn. 20261025",
            max_chars=20,
        )

        maximum = len(QUESTIONS)

        count_options = sorted(
            set(
                n
                for n in [5, 10, 15, 20, 30, 40, 50, 60, maximum]
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
        student_number = student_number.strip()

        if not student_number:
            st.warning("Lütfen öğrenci numaranızı girin.")

        elif not student_number.isdigit():
            st.warning(
                "Öğrenci numarası yalnızca rakamlardan oluşmalıdır."
            )

        else:
            try:
                # Her test başlangıcında rastgele bitki adı ata.
                plant_name = random.choice(PLANT_NAMES)

                display_name = f"{student_number} - {plant_name}"

                start_quiz(display_name, selected_count)

                st.session_state.student_number = student_number
                st.session_state.plant_name = plant_name

                st.rerun()

            except (ValueError, TypeError, KeyError) as exc:
                st.error(f"Test başlatılamadı: {exc}")

    st.divider()

    st.subheader("🏆 Liderlik Tablosu")
    render_leaderboard()

    with st.expander("📖 Nasıl oynanır?"):
        st.markdown(
            """
            1. Öğrenci numaranızı girin.
            2. Sistem size rastgele bir bitki adı atar.
            3. Test uzunluğunu seçin.
            4. Latince botanik terimlerinin anlamlarını bulun.
            5. Cevap açıklamalarını okuyarak öğrenin.
            6. Testin sonunda puanınızı ve sıralamanızı görün.
            """
        )


# ============================================================
# 10. SORU EKRANI
# ============================================================

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

    st.caption(
        f"🌿 Öğrenci: {st.session_state.name}"
    )

    st.markdown(
        f"""
        <div class="panel">
            <div class="eyebrow">Botanik Terim</div>
            <div class="latin">{safe_text(q['latin'])}</div>
            <p>{safe_text(q['question'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    options = list(dict.fromkeys(q["options"]))

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
            type="primary",
        )

    if submitted:
        if selected is None:
            st.warning("Lütfen bir cevap seçin.")
            return

        is_correct = selected == q["answer"]

        if is_correct:
            st.session_state.score += 1

        st.session_state.answers.append(
            {
                "latin": q["latin"],
                "question": q["question"],
                "selected": selected,
                "correct": q["answer"],
                "is_correct": is_correct,
                "plant": q["plant"],
                "plant_name": q["plant_name"],
                "explanation": q["explanation"],
            }
        )

        st.session_state.stage = "feedback"
        st.rerun()


# ============================================================
# 11. CEVAP VE AÇIKLAMA EKRANI
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
            <div class="eyebrow">Botanik Bilgisi</div>

            <div style="
                font-size: 1.2rem;
                font-weight: 800;
                font-style: italic;
            ">
                🌿 {safe_text(answer['plant'])}
            </div>

            <p style="opacity: 0.75; margin-top: 0.3rem;">
                {safe_text(answer['plant_name'])}
            </p>

            <p style="margin-top: 0.8rem;">
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
# 12. SONUÇ EKRANI
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
            <div class="eyebrow">Quiz Tamamlandı 🌿</div>

            <div style="
                font-size: 3.5rem;
                font-weight: 900;
                margin: 0.5rem 0;
            ">
                {score} / {total}
            </div>

            <h2>Başarı oranı: %{percentage:.0f}</h2>

            <p>
                Öğrenci: <strong>{safe_text(st.session_state.name)}</strong>
            </p>

            <p>
                Tamamlanma süresi:
                <strong>
                    {safe_text(format_seconds(st.session_state.elapsed_time))}
                </strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if percentage >= 80:
        st.success(
            "Mükemmel! Botanik renk bilgine hâkim görünüyorsun."
        )

    elif percentage >= 50:
        st.info(
            "Güzel iş! Birkaç tekrar ile daha da ilerleyebilirsin."
        )

    else:
        st.warning(
            "Yeni bir turla botanik bilgilerini geliştirebilirsin."
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Doğru", score)

    with col2:
        metric_card("Yanlış", total - score)

    with col3:
        metric_card("Başarı", f"%{percentage:.0f}")

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
# 13. ANA YÖNLENDİRME
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
