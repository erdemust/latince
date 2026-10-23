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
        font-size: clamp(1.35rem, 4vw, 2rem);
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
# 3. SORU HAVUZU (50+ Genişletilmiş Botanik Terimler)
# ============================================================
RAW_QUESTIONS = [
    # ============================================================
    # 1. TEMEL RENKLER
    # ============================================================
    (
        "Albus",
        "Beyaz",
        ["Siyah", "Beyaz", "Kırmızı", "Sarı"],
        "Nymphaea alba",
        "Beyaz nilüfer",
        "'Albus' Latince beyaz anlamına gelir; 'alba', dişil biçimidir. "
        "Nymphaea alba'nın 'alba' epiteti aynı renk kökünü taşır. "
        "Beyaz taç yapraklar, görünür ışığın geniş bir bölümünü "
        "yansıtarak karakteristik beyaz görünümü oluşturur.",
    ),
    (
        "Niger",
        "Siyah",
        ["Yeşil", "Mavi", "Siyah", "Pembe"],
        "Sambucus nigra",
        "Kara mürver",
        "'Niger' Latince siyah veya çok koyu renkli anlamına gelir; "
        "'nigra', dişil biçimidir. Sambucus nigra'nın 'nigra' epiteti "
        "aynı renk kökünü taşır. Olgun meyveleri antosiyanin "
        "pigmentleri nedeniyle koyu mor-siyah görünür.",
    ),
    (
        "Ruber",
        "Kırmızı",
        ["Kırmızı", "Mor", "Gri", "Beyaz"],
        "Quercus rubra",
        "Kırmızı meşe",
        "'Ruber' Latince kırmızı anlamına gelir. Quercus rubra'nın "
        "'rubra' epiteti aynı renk kökünün dişil biçimidir. "
        "Yapraklar özellikle sonbaharda kırmızı ve kızıl tonlar "
        "alabilir; bu renklenmede antosiyanin pigmentleri rol oynar.",
    ),
    (
        "Roseus",
        "Gül pembesi",
        ["Turuncu", "Kahverengi", "Sarı", "Gül pembesi"],
        "Catharanthus roseus",
        "Madagaskar cezayir menekşesi",
        "'Roseus' gül renginde veya gül pembesi anlamına gelir. "
        "Catharanthus roseus'un 'roseus' epiteti terimle birebir "
        "aynı biçimdedir. Türün yaygın pembe çiçekli formlarında "
        "taç yapraklar gül pembesi görünür; beyaz çiçekli "
        "kültivarları da bulunur.",
    ),
    (
        "Purpureus",
        "Mor veya erguvan",
        ["Mavi", "Mor veya erguvan", "Yeşil", "Gümüş"],
        "Echinacea purpurea",
        "Mor ekinezya",
        "'Purpureus' mor veya erguvan tonlarını ifade eder. "
        "Echinacea purpurea'nın 'purpurea' epiteti aynı renk "
        "kökünün dişil biçimidir. Dilsi çiçekler genellikle "
        "pembe-mor ve erguvan tonlarındadır.",
    ),
    (
        "Violaceus",
        "Menekşe moru",
        ["Kahverengi", "Sarı", "Menekşe moru", "Beyaz"],
        "Viola violacea",
        "Menekşe moru çiçekli menekşe",
        "'Violaceus' menekşe moru anlamına gelir. Viola violacea "
        "adındaki 'violacea' epiteti aynı renk kökünün dişil "
        "biçimidir. Bu bilimsel adın güncel taksonomik statüsü "
        "ve çiçek rengi güvenilir bir taksonomik kaynakla "
        "doğrulanmalıdır.",
    ),
    (
        "Caeruleus",
        "Gök mavisi",
        ["Gri", "Gök mavisi", "Siyah", "Kırmızı"],
        "Nymphaea caerulea",
        "Mavi nilüfer",
        "'Caeruleus' Latince gök mavisi anlamına gelir. "
        "Nymphaea caerulea'nın 'caerulea' epiteti aynı renk "
        "kökünün dişil biçimidir. Çiçekleri mavi ve gök mavisi "
        "tonlarında olabilir.",
    ),
    (
        "Flavus",
        "Sarı",
        ["Yeşil", "Mor", "Pembe", "Sarı"],
        "Glaucium flavum",
        "Sarı boynuzlu haşhaş",
        "'Flavus' Latince sarı anlamına gelir. Glaucium flavum'un "
        "'flavum' epiteti aynı renk kökünün nötr biçimidir. "
        "Bitkinin çiçekleri parlak sarıdır.",
    ),
    (
        "Luteus",
        "Sarı",
        ["Sarı", "Mavi", "Siyah", "Gri"],
        "Reseda lutea",
        "Sarı muhabbet çiçeği",
        "'Luteus' Latince sarı veya sarımsı anlamına gelir. "
        "Reseda lutea'nın 'lutea' epiteti aynı renk kökünün "
        "dişil biçimidir. Bitkinin küçük sarı çiçekleri "
        "dallanmış çiçek durumlarında toplanır.",
    ),
    (
        "Aureus",
        "Altın rengi",
        ["Gümüş", "Kahverengi", "Altın rengi", "Mor"],
        "Carex aurea",
        "Altın saz",
        "'Aureus' altın renginde veya altın sarısı anlamına gelir. "
        "Carex aurea'nın 'aurea' epiteti aynı renk kökünün "
        "dişil biçimidir. Olgunlaşan başakçıklar ve meyve taşıyan "
        "yapılar altın sarısı ile sarımsı kahverengi tonlar alabilir.",
    ),
    (
        "Viridis",
        "Yeşil",
        ["Kırmızı", "Yeşil", "Pembe", "Turuncu"],
        "Helleborus viridis",
        "Yeşil çöpleme",
        "'Viridis' Latince yeşil anlamına gelir. Helleborus viridis'in "
        "'viridis' epiteti terimle birebir aynıdır. Yeşil çanak "
        "yapraklarında bulunan klorofil, yeşil görünümün oluşmasına "
        "katkıda bulunur.",
    ),

    # ============================================================
    # 2. ARA VE ÖZEL RENK TONLARI
    # ============================================================
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
        "'Glaucus' mavimsi yeşil veya grimsi mavi, çoğunlukla puslu "
        "görünümlü tonları ifade eder. Rosa glauca'nın 'glauca' "
        "epiteti aynı renk kökünün dişil biçimidir. Yapraklardaki "
        "mavimsi-yeşil görünüm, yüzeyin optik özellikleri ve "
        "mumsu tabakayla ilişkilidir.",
    ),
    (
        "Cinereus",
        "Kül grisi",
        ["Kül grisi", "Altın sarısı", "Pembe", "Mor"],
        "Eucalyptus cinerea",
        "Gümüş dolar okaliptüsü",
        "'Cinereus' kül rengi veya kül grisi anlamına gelir. "
        "Eucalyptus cinerea adındaki 'cinerea' epiteti aynı "
        "renk kökünün dişil biçimidir. Yapraklardaki kül grisi "
        "görünüm, yüzeyin mumsu dokusu ve ışığı dağıtmasıyla ilişkilidir.",
    ),
    (
        "Brunneus",
        "Kahverengi",
        ["Beyaz", "Mavi", "Kahverengi", "Pembe"],
        "Carex brunnea",
        "Kahverengi saz",
        "'Brunneus' kahverengi anlamına gelir. Carex brunnea "
        "adındaki 'brunnea' epiteti aynı renk kökünün dişil "
        "biçimidir. Türün taksonomik statüsü ve kahverengi "
        "özelliğinin hangi organlarda görüldüğü güncel "
        "floristik kaynaklardan doğrulanmalıdır.",
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
        "Juncus fuscus",
        "Koyu renkli hasırotu",
        "'Fuscus' koyu, esmer veya koyu kahverengiye çalan "
        "anlamına gelir. Juncus fuscus adındaki 'fuscus' "
        "epiteti terimle birebir aynıdır. Bu adın güncel "
        "taksonomik geçerliliği ve renk özelliği güvenilir "
        "botanik kaynaklardan doğrulanmalıdır.",
    ),
    (
        "Fulvus",
        "Sarımsı kahverengi",
        ["Mavi", "Siyah", "Mor", "Sarımsı kahverengi"],
        "Carex fulva",
        "Sarımsı kahverengi saz",
        "'Fulvus' sarımsı kahverengi veya boz tonları ifade eder. "
        "Carex fulva'nın 'fulva' epiteti aynı renk kökünün "
        "dişil biçimidir. Taksonun güncel geçerliliği ve "
        "rengin hangi organlarda görüldüğü floristik "
        "kaynaklardan doğrulanmalıdır.",
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
        "Rumex rufus",
        "Kızıl labada",
        "'Rufus' kızıl veya kızıl kahverengi anlamına gelir. "
        "Rumex rufus adındaki 'rufus' epiteti terimle birebir "
        "aynıdır. Bu adın güncel taksonomik statüsü ve kızıl "
        "rengin hangi bitki organında görüldüğü doğrulanmalıdır.",
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
        "Rosa pallida",
        "Soluk renkli gül",
        "'Pallidus' soluk, solgun veya açık renkli anlamına gelir. "
        "Rosa pallida adındaki 'pallida' aynı renk kökünün "
        "dişil biçimidir. Bilimsel adın geçerli taksonomik "
        "statüsü ve renk özelliği doğrulanmalıdır.",
    ),
    (
        "Argenteus",
        "Gümüş rengi",
        ["Turuncu", "Kahverengi", "Kırmızı", "Gümüş rengi"],
        "Salix argentea",
        "Gümüşi söğüt",
        "'Argenteus' gümüş renginde veya gümüşi anlamına gelir. "
        "Salix argentea adındaki 'argentea' aynı renk kökünün "
        "dişil biçimidir. Bu adın güncel taksonomik statüsü "
        "ve yapraklardaki gümüşi görünüm güvenilir kaynaklardan "
        "doğrulanmalıdır.",
    ),
    (
        "Lilacinus",
        "Leylak rengi",
        ["Yeşil", "Leylak rengi", "Siyah", "Sarı"],
        "Syringa lilacina",
        "Leylak renkli leylak",
        "'Lilacinus' leylak rengi veya açık mor anlamına gelir. "
        "Syringa lilacina adındaki 'lilacina' aynı renk kökünün "
        "dişil biçimidir. Bu bilimsel adın güncel taksonomik "
        "geçerliliği doğrulanmalıdır.",
    ),

    # ============================================================
    # 3. KOYU RENKLER VE METALİK TONLAR
    # ============================================================
    (
        "Atropurpureus",
        "Çok koyu mor veya siyaha çalan erguvan",
        [
            "Açık sarı",
            "Çok koyu mor veya siyaha çalan erguvan",
            "Beyaz",
            "Gümüş",
        ],
        "Acer atropurpureum",
        "Koyu mor yapraklı akçaağaç",
        "'Atropurpureus' çok koyu mor veya siyaha çalan erguvan "
        "tonlarını ifade eder. Acer atropurpureum adındaki "
        "'atropurpureum' aynı renk kökünün nötr biçimidir. "
        "Bu bilimsel adın taksonomik statüsü ve koyu mor "
        "renk özelliği doğrulanmalıdır.",
    ),
    (
        "Cupreus",
        "Bakır rengi",
        ["Bakır rengi", "Mavi", "Beyaz", "Pembe"],
        "Carex cuprea",
        "Bakır renkli saz",
        "'Cupreus' bakır renginde veya bakırımsı anlamına gelir. "
        "Carex cuprea adındaki 'cuprea' aynı renk kökünün "
        "dişil biçimidir. Bilimsel adın taksonomik statüsü ve "
        "bakırımsı renk özelliği güncel floristik kaynaklardan "
        "doğrulanmalıdır.",
    ),
    (
        "Lacteus",
        "Süt beyazı",
        ["Koyu kahverengi", "Mor", "Süt beyazı", "Turuncu"],
        "Euphorbia lactea",
        "Sütleğen",
        "'Lacteus' süt renginde veya süt beyazı anlamına gelir. "
        "Euphorbia lactea adındaki 'lactea' aynı renk kökünün "
        "dişil biçimidir. Bitkinin yaralanan dokularından çıkan "
        "lateks süt beyazıdır.",
    ),
    (
        "Niveus",
        "Kar beyazı",
        ["Kızıl", "Yeşil", "Mavi", "Kar beyazı"],
        "Rubus niveus",
        "Kar ahududusu",
        "'Niveus' kar gibi beyaz anlamına gelir. Rubus niveus "
        "adındaki 'niveus' epiteti terimle birebir aynıdır. "
        "Bu eşleşme epitet uyumunu sağlar; ancak bitkinin "
        "bütün organlarının kar beyazı olduğu anlamına gelmez.",
    ),
    (
        "Bicolor",
        "İki renkli",
        ["İki renkli", "Tek renkli", "Renksiz", "Kül grisi"],
        "Viola bicolor",
        "İki renkli menekşe",
        "'Bicolor' iki renkli anlamına gelir. Viola bicolor "
        "adındaki 'bicolor' epiteti terimle birebir aynıdır. "
        "Bilimsel adın güncel taksonomik statüsü ve iki renkli "
        "görünümün hangi organlarda bulunduğu doğrulanmalıdır.",
    ),
    (
        "Tricolor",
        "Üç renkli",
        ["Siyah", "Üç renkli", "Altın sarısı", "Gri"],
        "Viola tricolor",
        "Hercai menekşe",
        "'Tricolor' üç renkli anlamına gelir. Viola tricolor "
        "adındaki 'tricolor' epiteti terimle birebir aynıdır. "
        "Çiçeklerde mor, sarı ve beyaz tonlar aynı anda "
        "görülebilir.",
    ),
    (
        "Versicolor",
        "Çok renkli veya renkleri değişken",
        [
            "Beyaz",
            "Kırmızı",
            "Çok renkli veya renkleri değişken",
            "Koyu yeşil",
        ],
        "Iris versicolor",
        "Çok renkli süsen",
        "'Versicolor' farklı renkler gösteren veya renkleri "
        "değişken olan anlamına gelir. Iris versicolor adındaki "
        "'versicolor' epiteti terimle birebir aynıdır. Çiçeklerde "
        "mavi-mor zemin üzerinde sarı ve beyaz işaretler bulunabilir.",
    ),
    (
        "Coccineus",
        "Parlak kızıl veya al kırmızısı",
        ["Gri", "Parlak kızıl veya al kırmızısı", "Mavimsi yeşil", "Kahverengi"],
        "Salvia coccinea",
        "Kızıl adaçayı",
        "'Coccineus' parlak kızıl veya al kırmızısı anlamına gelir. "
        "Salvia coccinea adındaki 'coccinea' aynı renk kökünün "
        "dişil biçimidir. Çiçekleri çoğunlukla parlak kırmızıdır.",
    ),
    (
        "Sanguineus",
        "Kan kırmızısı",
        ["Kan kırmızısı", "Soluk sarı", "Gümüş", "Yeşil"],
        "Cornus sanguinea",
        "Kan kızılcığı",
        "'Sanguineus' kan renginde veya kan kırmızısı anlamına gelir. "
        "Cornus sanguinea adındaki 'sanguinea' aynı renk kökünün "
        "dişil biçimidir. Genç sürgünler ve dallar kırmızımsı "
        "tonlar gösterebilir.",
    ),

    # ============================================================
    # 4. AÇIK RENKLER VE RENK DEĞİŞİMLERİ
    # ============================================================
    (
        "Pallens",
        "Soluk veya solgun",
        ["Çok koyu", "Altın rengi", "Soluk veya solgun", "Bakır rengi"],
        "Carex pallens",
        "Soluk saz",
        "'Pallens' soluk veya solgun anlamına gelir. Carex pallens "
        "adındaki 'pallens' epiteti terimle birebir aynıdır. "
        "Taksonun geçerliliği ve soluk rengin hangi organlarda "
        "görüldüğü floristik kaynaklardan doğrulanmalıdır.",
    ),
    (
        "Rubescens",
        "Kırmızılaşan veya kızaran",
        ["Yeşile dönen", "Kırmızılaşan veya kızaran", "Beyazlaşan", "Maviye dönen"],
        "Acer rubescens",
        "Kızaran akçaağaç",
        "'Rubescens' kızaran veya kırmızılaşan anlamına gelir. "
        "Acer rubescens adındaki 'rubescens' epiteti terimle "
        "birebir aynıdır. Adın güncel taksonomik statüsü ve "
        "renk değişiminin hangi organlarda görüldüğü doğrulanmalıdır.",
    ),
    (
        "Albicans",
        "Beyazımsı veya beyazlaşan",
        ["Siyahımsı", "Sarımsı", "Beyazımsı veya beyazlaşan", "Kızılımsı"],
        "Eucalyptus albicans",
        "Beyazımsı okaliptüs",
        "'Albicans' beyazımsı veya beyazlaşan anlamına gelir. "
        "Eucalyptus albicans adındaki 'albicans' epiteti terimle "
        "birebir aynıdır. Bilimsel adın güncel geçerliliği ve "
        "beyazımsı rengin görüldüğü organlar doğrulanmalıdır.",
    ),
    (
        "Flavescens",
        "Sarılaşan veya sarımsı",
        ["Mavileşen", "Kararan", "Morlaşan", "Sarılaşan veya sarımsı"],
        "Carex flavescens",
        "Sarılaşan saz",
        "'Flavescens' sarılaşan veya sarımsı hale gelen anlamına gelir. "
        "Carex flavescens adındaki 'flavescens' epiteti terimle "
        "birebir aynıdır. Taksonun geçerliliği ve sarılaşmanın "
        "gözlendiği organlar doğrulanmalıdır.",
    ),
    (
        "Viridescens",
        "Yeşilimsi veya yeşile dönen",
        ["Yeşilimsi veya yeşile dönen", "Kırmızılaşan", "Beyazlaşan", "Kararan"],
        "Carex viridescens",
        "Yeşilimsi saz",
        "'Viridescens' yeşilimsi veya yeşile dönen anlamına gelir. "
        "Carex viridescens adındaki 'viridescens' epiteti terimle "
        "birebir aynıdır. Taksonun geçerliliği ve yeşilimsi rengin "
        "görüldüğü organlar doğrulanmalıdır.",
    ),
    (
        "Obscurus",
        "Koyu, karanlık veya mat",
        ["Açık", "Parlak", "Koyu, karanlık veya mat", "Süt beyazı"],
        "Carex obscura",
        "Koyu renkli saz",
        "'Obscurus' koyu, karanlık veya belirsiz anlamlarına gelir. "
        "Carex obscura adındaki 'obscura' aynı sözcük kökünün "
        "dişil biçimidir. Taksonun geçerliliği ve koyu rengin "
        "görüldüğü organlar doğrulanmalıdır.",
    ),
    (
        "Nitidus",
        "Parlak veya ışıldayan",
        ["Mat", "Parlak veya ışıldayan", "Soluk", "Kül grisi"],
        "Carex nitida",
        "Parlak saz",
        "'Nitidus' parlak veya ışıldayan anlamına gelir. Carex "
        "nitida adındaki 'nitida' aynı kökün dişil biçimidir. "
        "Taksonun güncel geçerliliği ve parlaklık özelliğinin "
        "hangi organlarda bulunduğu doğrulanmalıdır.",
    ),
    (
        "Maculatus",
        "Benekli veya lekeli",
        ["Çizgili", "Düz renkli", "Benekli veya lekeli", "Şeffaf"],
        "Pulmonaria maculata",
        "Benekli akciğer otu",
        "'Maculatus' benekli veya lekeli anlamına gelir. "
        "Pulmonaria maculata adındaki 'maculata' aynı kökün "
        "dişil biçimidir. Taksonun geçerliliği ve benekli "
        "yaprak özelliği güvenilir botanik kaynaklardan doğrulanmalıdır.",
    ),
    (
        "Striatus",
        "Çizgili veya şeritli",
        ["Çizgili veya şeritli", "Beyaz", "Kızıl", "Altın rengi"],
        "Iris striata",
        "Çizgili süsen",
        "'Striatus' çizgili veya şeritli anlamına gelir. Iris "
        "striata adındaki 'striata' aynı kökün dişil biçimidir. "
        "Taksonun güncel taksonomik statüsü ve çizgilerin "
        "görüldüğü organlar doğrulanmalıdır.",
    ),
    (
        "Azureus",
        "Azur veya gök mavisi",
        ["Koyu kahverengi", "Azur veya gök mavisi", "Siyah", "Pembe"],
        "Salvia azurea",
        "Gök adaçayı",
        "'Azureus' azur veya gök mavisi anlamına gelir. Salvia "
        "azurea adındaki 'azurea' aynı renk kökünün dişil "
        "biçimidir. Çiçekleri gök mavisi tonlarında olabilir.",
    ),
    (
        "Canus",
        "Beyazımsı gri veya kırçıllı",
        ["Turuncu", "Mor", "Beyazımsı gri veya kırçıllı", "Parlak kırmızı"],
        "Artemisia cana",
        "Gri yapraklı pelin",
        "'Canus' beyazımsı gri veya kırçıllı anlamına gelir. "
        "Artemisia cana adındaki 'cana' aynı renk kökünün "
        "dişil biçimidir. Yaprak ve sürgünlerdeki beyazımsı "
        "tüyler gri görünümü güçlendirebilir.",
    ),
    (
        "Lividus",
        "Kurşuni, mavimsi gri veya soluk mor",
        ["Altın sarısı", "Kurşuni, mavimsi gri veya soluk mor", "Pembe", "Yeşil"],
        "Helleborus lividus",
        "Mavimsi çöpleme",
        "'Lividus' kurşuni, mavimsi gri veya soluk mor tonlarını "
        "ifade eder. Helleborus lividus adındaki 'lividus' "
        "epiteti terimle birebir aynıdır. Yapraklar mavimsi-yeşil "
        "ve griye çalan tonlar gösterebilir.",
    ),
    (
        "Coloratus",
        "Renkli veya belirgin renk taşıyan",
        ["Renksiz", "Renkli veya belirgin renk taşıyan", "Yalnızca beyaz", "Çizgili"],
        "Rhododendron coloratum",
        "Renkli orman gülü",
        "'Coloratus' renkli veya belirgin biçimde renklendirilmiş "
        "anlamına gelir. Rhododendron coloratum adındaki "
        "'coloratum' aynı kökün nötr biçimidir. Bilimsel adın "
        "taksonomik geçerliliği ve renk özelliği doğrulanmalıdır.",
    ),
    (
        "Piceus",
        "Zift siyahı veya katran rengi",
        ["Kar beyazı", "Zift siyahı veya katran rengi", "Leylak", "Gümüş"],
        "Carex picea",
        "Koyu renkli saz",
        "'Piceus' zift siyahı veya katran rengi anlamına gelir. "
        "Carex picea adındaki 'picea' aynı sözcük kökünün "
        "dişil biçimidir. Bilimsel adın geçerliliği ve koyu "
        "rengin görüldüğü organlar doğrulanmalıdır.",
    ),
    (
        "Dilutus",
        "Seyreltik veya soluk renkli",
        ["Çok koyu", "Seyreltik veya soluk renkli", "Parlak siyah", "Altın rengi"],
        "Gentiana diluta",
        "Soluk renkli kantaron",
        "'Dilutus' seyreltilmiş veya yoğunluğu azaltılmış anlamına "
        "gelir. Gentiana diluta adındaki 'diluta' aynı kökün "
        "dişil biçimidir. Bilimsel adın geçerliliği ve soluk "
        "renk özelliği doğrulanmalıdır.",
    ),
    (
        "Clarus",
        "Açık, berrak veya parlak",
        ["Açık, berrak veya parlak", "Siyah", "Koyu kahverengi", "Kırmızı"],
        "Carex clara",
        "Açık renkli saz",
        "'Clarus' açık, berrak veya parlak anlamına gelir. Carex "
        "clara adındaki 'clara' aynı kökün dişil biçimidir. "
        "Bilimsel adın geçerliliği ve renk özelliği doğrulanmalıdır.",
    ),
    (
        "Saturatus",
        "Doygun veya yoğun renkli",
        ["Soluk", "Doygun veya yoğun renkli", "Renksiz", "Şeffaf"],
        "Rosa saturata",
        "Yoğun renkli gül",
        "'Saturatus' doygun veya yoğun renkli anlamına gelir. "
        "Rosa saturata adındaki 'saturata' aynı kökün dişil "
        "biçimidir. Bilimsel adın taksonomik geçerliliği ve "
        "çiçek renginin yoğunluğu doğrulanmalıdır.",
    ),
    (
        "Opacus",
        "Mat, donuk veya ışık geçirmeyen",
        ["Parlak", "Mat, donuk veya ışık geçirmeyen", "Gümüş", "Kızıl"],
        "Carex opaca",
        "Mat renkli saz",
        "'Opacus' mat, donuk veya ışık geçirmeyen anlamına gelir. "
        "Carex opaca adındaki 'opaca' aynı kökün dişil biçimidir. "
        "Bilimsel adın geçerliliği ve mat yüzey özelliği "
        "güvenilir botanik kaynaklardan doğrulanmalıdır.",
    ),
    (
        "Micans",
        "Parıldayan veya ışıltılı",
        ["Kül grisi", "Parıldayan veya ışıltılı", "Soluk", "Siyah"],
        "Tibouchina micans",
        "Parıldayan tibuçina",
        "'Micans' parıldayan veya ışıldayan anlamına gelir. "
        "Tibouchina micans adındaki 'micans' epiteti terimle "
        "birebir aynıdır. Parlaklık özelliğinin hangi organlarda "
        "görüldüğü güvenilir botanik kaynaklarla doğrulanmalıdır.",
    ),

    # ============================================================
    # 5. SUB- ÖNEKLİ VE BENZER ANLAMLAR
    # ============================================================
    (
        "Subalbus",
        "Beyazımsı",
        ["Kırmızı", "Beyazımsı", "Siyah", "Mavi"],
        "Carex subalba",
        "Beyazımsı saz",
        "'Subalbus', beyaz anlamındaki 'albus' sıfatına yaklaşık "
        "veya daha düşük derecede olma anlamı katan 'sub-' "
        "önekinden oluşur. Carex subalba adındaki 'subalba' "
        "aynı sözcük yapısının dişil biçimidir. Taksonun "
        "geçerliliği ve beyazımsı renk özelliği doğrulanmalıdır.",
    ),
    (
        "Subflavus",
        "Sarımsı",
        ["Gümüş", "Mor", "Sarımsı", "Koyu siyah"],
        "Carex subflava",
        "Sarımsı saz",
        "'Subflavus', sarı anlamındaki 'flavus' sıfatına yaklaşık "
        "veya daha düşük derecede olma anlamı katan 'sub-' "
        "önekinden oluşur. Carex subflava adındaki 'subflava' "
        "aynı sözcük yapısının dişil biçimidir. Taksonun "
        "geçerliliği ve sarımsı renk özelliği doğrulanmalıdır.",
    ),
    (
        "Subrubens",
        "Kırmızımsı",
        ["Kırmızımsı", "Mavimsi", "Yeşilimsi", "Beyazımsı"],
        "Silene subrubens",
        "Kırmızımsı nakıl",
        "'Subrubens', kırmızı anlamındaki 'ruber' sözcük ailesine "
        "yaklaşık veya daha düşük derecede olma anlamı katan "
        "'sub-' önekini ekler. Silene subrubens adındaki "
        "'subrubens' terimle birebir aynıdır. Taksonun geçerliliği "
        "ve kırmızımsı renk özelliği doğrulanmalıdır.",
    ),
    (
        "Subviridis",
        "Yeşilimsi",
        ["Kızıl", "Gümüş", "Yeşilimsi", "Siyah"],
        "Carex subviridis",
        "Yeşilimsi saz",
        "'Subviridis', yeşil anlamındaki 'viridis' sıfatına "
        "yaklaşık veya daha düşük derecede olma anlamı katan "
        "'sub-' önekinden oluşur. Carex subviridis adındaki "
        "'subviridis' terimle birebir aynıdır. Taksonun "
        "geçerliliği ve yeşilimsi renk özelliği doğrulanmalıdır.",
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

    positions = [i % 4 for i in range(count)]
    random.shuffle(positions)

    all_answers = list(dict.fromkeys(q["answer"] for q in QUESTIONS))
    prepared = []

    for question, correct_position in zip(selected, positions):
        correct_answer = question["answer"]
        distractors = [
            option for option in question["options"] if option != correct_answer
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
        raise ValueError("Yeterli sayıda geçerli soru hazırlanamadı.")

    return prepared


def start_quiz(name, count):
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
    run_id = st.session_state.run_id
    if not run_id or st.session_state.submitted_run_id == run_id:
        return

    questions = st.session_state.quiz_questions
    if not questions:
        return

    start_time = st.session_state.start_time
    elapsed = round(time.time() - start_time, 2) if start_time is not None else 0.0

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
    records = st.session_state.leaderboard
    if not records:
        st.info("🌱 Henüz sonuç kaydedilmedi. İlk testi tamamlayarak liderlik tablosunu oluşturabilirsin.")
        return

    df = pd.DataFrame(records)
    df = df.sort_values(
        by=["Başarı (%)", "Doğru Sayısı", "Süre (sn)"],
        ascending=[False, False, True],
    ).reset_index(drop=True)
    df.index = df.index + 1
    df.index.name = "Sıra"

    st.dataframe(
        df[["İsim", "Doğru Sayısı", "Toplam Soru", "Başarı (%)", "Süre (sn)"]],
        use_container_width=True,
    )


# ============================================================
# 7. EKRAN BİLEŞENLERİ
# ============================================================

def render_header():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">🌿 BOTANICA AKADEMİ</div>
            <h1>Doğanın Dilini Keşfet.</h1>
            <p>
                Latince botanik terimlerini öğren, renklerin ardındaki anlamları keşfet ve bilgini test et.
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
        count_options = sorted(
            set(n for n in [5, 10, 15, 20, 30, 50, maximum] if 1 <= n <= maximum)
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

    # Hatalı/girintisiz kalan expander düzeltildi:
    with st.expander("📖 Nasıl oynanır?"):
        st.markdown(
            """
            <div style="padding: 0.5rem; line-height: 1.7;">
                <p>1. Adını yaz ve test uzunluğunu seç.</p>
                <p>2. Karşına çıkan Latince terimin hangi renk veya özelliği ifade ettiğini bul.</p>
                <p>3. Soruların ardından botanik açıklamalarını oku ve süreni yarışmaya dahil et!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


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
        st.error(f"Yanlış cevap. Doğru cevap: **{safe_text(answer['correct'])}**")

    st.markdown(
        f"""
        <div class="panel">
            <div class="eyebrow">Botanik Bilgisi</div>
            <div style="font-size: 1.2rem; font-weight: 800; font-style: italic;">
                🌿 {safe_text(answer['plant'])}
            </div>
            <p style="opacity: 0.75; margin-top: 0.3rem;">{safe_text(answer['plant_name'])}</p>
            <p style="margin-top: 0.8rem;">{safe_text(answer['explanation'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    current = st.session_state.current_question
    total = len(st.session_state.quiz_questions)
    label = "Sonuçları Gör 🏆" if current + 1 >= total else "Sonraki Soru ➡️"

    if st.button(label, use_container_width=True, type="primary"):
        if current + 1 >= total:
            save_result()
            st.session_state.stage = "result"
        else:
            st.session_state.current_question += 1
            st.session_state.stage = "quiz"
        st.rerun()


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
            <div style="font-size: 3.5rem; font-weight: 900; margin: 0.5rem 0;">{score} / {total}</div>
            <h2>Başarı oranı: %{percentage:.0f}</h2>
            <p style="margin-top: 0.5rem;">
                Tamamlanma süresi: <strong>{safe_text(format_seconds(st.session_state.elapsed_time))}</strong>
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
            status = "✅ Doğru" if answer["is_correct"] else "❌ Yanlış"
            st.markdown(f"**{i}. {answer['latin']} — {status}**")
            st.write(f"Verdiğin cevap: {answer['selected']}")
            st.write(f"Doğru cevap: {answer['correct']}")
            st.caption(f"{answer['plant']} — {answer['plant_name']}")
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
# 8. ANA YÖNLENDİRME
# ============================================================

if not QUESTIONS:
    st.error("Soru havuzu yüklenemedi. RAW_QUESTIONS listesini kontrol edin.")
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
