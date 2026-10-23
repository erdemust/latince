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
# Streamlit'in yerleşik tema değişkenlerini kullanır.
# Açık ve koyu temalarda arka plan ve metin renkleri uyumludur.
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --botanica-radius: 18px;
        --botanica-radius-small: 12px;
        --botanica-transition: 180ms ease;
    }

    .stApp {
        background: var(--background-color);
        color: var(--text-color);
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label {
        color: var(--text-color);
    }

    h1 {
        font-weight: 800 !important;
        letter-spacing: -0.04em;
    }

    h2, h3 {
        letter-spacing: -0.025em;
    }

    /* Ana başlık */

    .hero-card {
        padding: 1.7rem;
        margin-bottom: 1.4rem;
        border-radius: var(--botanica-radius);
        border: 1px solid var(--border-color, rgba(128,128,128,.22));
        background:
            linear-gradient(
                135deg,
                var(--secondary-background-color),
                var(--background-color)
            );
        box-shadow: 0 8px 30px rgba(80, 100, 80, 0.07);
    }

    .hero-eyebrow {
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .13em;
        text-transform: uppercase;
        color: var(--primary-color);
        margin-bottom: .6rem;
    }

    .hero-title {
        font-size: clamp(1.8rem, 5vw, 2.8rem);
        line-height: 1.15;
        font-weight: 850;
        letter-spacing: -.045em;
        margin: 0 0 .7rem 0;
        color: var(--text-color);
    }

    .hero-description {
        color: var(--text-color);
        opacity: .78;
        font-size: 1rem;
        line-height: 1.7;
        margin: 0;
    }

    /* Bilgi kartları */

    .info-card {
        height: 100%;
        padding: 1rem 1.1rem;
        border-radius: var(--botanica-radius-small);
        border: 1px solid var(--border-color, rgba(128,128,128,.22));
        background: var(--secondary-background-color);
        transition:
            transform var(--botanica-transition),
            box-shadow var(--botanica-transition);
    }

    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 20px rgba(80, 100, 80, 0.08);
    }

    .info-label {
        font-size: .78rem;
        opacity: .72;
        margin-bottom: .45rem;
    }

    .info-value {
        font-size: 1.4rem;
        line-height: 1.35;
        font-weight: 800;
        overflow-wrap: anywhere;
        color: var(--text-color);
    }

    /* Soru kartı */

    .question-card {
        padding: clamp(1.1rem, 4vw, 2rem);
        margin: 1rem 0;
        border-radius: var(--botanica-radius);
        border: 1px solid var(--border-color, rgba(128,128,128,.22));
        background: var(--secondary-background-color);
        box-shadow: 0 10px 30px rgba(80, 100, 80, 0.06);
    }

    .question-label {
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
        color: var(--primary-color);
        margin-bottom: .6rem;
    }

    .latin-term {
        font-size: clamp(2rem, 7vw, 3.3rem);
        line-height: 1.15;
        font-weight: 850;
        font-style: italic;
        letter-spacing: -.04em;
        overflow-wrap: anywhere;
        margin: .2rem 0 .8rem;
        color: var(--text-color);
    }

    .question-text {
        font-size: 1.05rem;
        line-height: 1.65;
        color: var(--text-color);
        opacity: .9;
    }

    /* Cevap seçenekleri */

    .stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 12px;
        font-weight: 650;
        transition:
            transform var(--botanica-transition),
            box-shadow var(--botanica-transition);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 5px 15px rgba(80, 100, 80, 0.10);
    }

    .answer-card {
        padding: .85rem 1rem;
        margin: .45rem 0;
        border: 1px solid var(--border-color, rgba(128,128,128,.22));
        border-radius: var(--botanica-radius-small);
        background: var(--secondary-background-color);
        color: var(--text-color);
        overflow-wrap: anywhere;
    }

    .answer-correct {
        background: rgba(34, 197, 94, .13);
        border: 1px solid rgba(34, 197, 94, .7);
    }

    .answer-wrong {
        background: rgba(239, 68, 68, .12);
        border: 1px solid rgba(239, 68, 68, .7);
    }

    .answer-neutral {
        background: var(--secondary-background-color);
    }

    .answer-icon {
        display: inline-block;
        width: 1.7rem;
        font-weight: 800;
    }

    /* Botanik bilgi kartı */

    .plant-card {
        padding: 1.15rem;
        border-radius: var(--botanica-radius-small);
        border: 1px solid var(--border-color, rgba(128,128,128,.22));
        background: var(--secondary-background-color);
        margin: .8rem 0;
    }

    .plant-name {
        font-size: 1.2rem;
        font-weight: 800;
        margin: .25rem 0;
        color: var(--text-color);
    }

    .plant-description {
        line-height: 1.65;
        opacity: .82;
        color: var(--text-color);
    }

    /* Sonuç kartı */

    .result-banner {
        padding: 1.4rem;
        border-radius: var(--botanica-radius);
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color, rgba(128,128,128,.22));
        margin: 1rem 0;
    }

    .result-score {
        font-size: clamp(2.5rem, 8vw, 4rem);
        font-weight: 900;
        letter-spacing: -.05em;
        line-height: 1.1;
        color: var(--primary-color);
    }

    /* Genel yardımcı sınıflar */

    .muted-text {
        opacity: .7;
        font-size: .88rem;
        line-height: 1.6;
    }

    .section-heading {
        margin-top: 1.6rem;
        margin-bottom: .7rem;
        font-weight: 800;
    }

    div[data-testid="stProgress"] > div > div {
        background-color: var(--primary-color);
        border-radius: 999px;
    }

    div[data-testid="stProgress"] {
        margin: .7rem 0 1rem;
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1rem .8rem 2rem;
        }

        .hero-card {
            padding: 1.2rem;
        }

        .question-card {
            padding: 1rem;
        }

        .info-value {
            font-size: 1.15rem;
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

RAW_QUESTIONS = [
    (
        "Albus",
        "'Albus' hangi rengi ifade eder?",
        "Beyaz",
        ["Siyah", "Beyaz", "Kırmızı", "Sarı"],
        "Nymphaea alba",
        "Beyaz nilüfer",
        "'Albus' beyaz anlamına gelir. 'Alba', bu sıfatın dişil biçimidir.",
    ),
    (
        "Niger",
        "'Niger' hangi rengi ifade eder?",
        "Siyah",
        ["Yeşil", "Mavi", "Siyah", "Pembe"],
        "Sambucus nigra",
        "Kara mürver",
        "'Niger' siyah, 'nigra' ise bu sıfatın dişil biçimidir.",
    ),
    (
        "Ruber",
        "'Ruber' hangi rengi ifade eder?",
        "Kırmızı",
        ["Kırmızı", "Mor", "Gri", "Beyaz"],
        "Trifolium rubens",
        "Kızıl çayır üçgülü",
        "'Ruber' kırmızı anlamına gelir. 'Rubens' kızaran veya kırmızımsı olmayı anlatabilir.",
    ),
    (
        "Roseus",
        "'Roseus' hangi rengi ifade eder?",
        "Pembe",
        ["Turuncu", "Kahverengi", "Sarı", "Pembe"],
        "Dianthus",
        "Karanfil cinsi",
        "'Roseus' gül pembesi veya pembe anlamına gelir.",
    ),
    (
        "Purpureus",
        "'Purpureus' hangi rengi ifade eder?",
        "Mor",
        ["Mavi", "Mor", "Yeşil", "Gümüş"],
        "Echinacea purpurea",
        "Mor ekinezya",
        "'Purpureus' mor ve erguvan tonlarını ifade eder.",
    ),
    (
        "Violaceus",
        "'Violaceus' hangi rengi ifade eder?",
        "Menekşe moru",
        ["Kahverengi", "Sarı", "Menekşe moru", "Beyaz"],
        "Viola odorata",
        "Kokulu menekşe",
        "'Violaceus' menekşe moru anlamına gelir.",
    ),
    (
        "Caeruleus",
        "'Caeruleus' hangi rengi ifade eder?",
        "Mavi",
        ["Gri", "Mavi", "Siyah", "Kırmızı"],
        "Plumbago auriculata",
        "Mavi çiçekli plumbago",
        "'Caeruleus' mavi veya gök mavisi anlamına gelir.",
    ),
    (
        "Flavus",
        "'Flavus' hangi rengi ifade eder?",
        "Sarı",
        ["Yeşil", "Mor", "Pembe", "Sarı"],
        "Rosa foetida",
        "Sarı çiçekli gül türü",
        "'Flavus' sarı anlamına gelir.",
    ),
    (
        "Luteus",
        "'Luteus' hangi rengi ifade eder?",
        "Sarı",
        ["Sarı", "Mavi", "Siyah", "Gri"],
        "Iris pseudacorus",
        "Sarı süsen",
        "'Luteus' sarı veya sarımsı tonları anlatır.",
    ),
    (
        "Aureus",
        "'Aureus' hangi rengi ifade eder?",
        "Altın rengi",
        ["Gümüş", "Kahverengi", "Altın rengi", "Mor"],
        "Forsythia",
        "Altın çanı olarak bilinen çalı cinsi",
        "'Aureus' altın veya altın rengi anlamına gelir.",
    ),
    (
        "Viridis",
        "'Viridis' hangi rengi ifade eder?",
        "Yeşil",
        ["Kırmızı", "Yeşil", "Pembe", "Turuncu"],
        "Helleborus viridis",
        "Yeşil çöpleme",
        "'Viridis' yeşil anlamına gelir.",
    ),
    (
        "Glaucus",
        "'Glaucus' bitki rengini tanımlarken ne anlama gelir?",
        "Mavimsi yeşil veya grimsi mavi",
        ["Parlak sarı", "Koyu kırmızı", "Saf beyaz", "Mavimsi yeşil veya grimsi mavi"],
        "Eucalyptus cinerea",
        "Gümüş dolar okaliptüsü",
        "'Glaucus' çoğunlukla mumsu veya puslu görünümlü mavimsi yeşil ve grimsi mavi tonlarını anlatır.",
    ),
    (
        "Cinereus",
        "'Cinereus' hangi renk tonunu ifade eder?",
        "Kül grisi",
        ["Kül grisi", "Altın sarısı", "Pembe", "Mor"],
        "Eucalyptus cinerea",
        "Gümüş dolar okaliptüsü",
        "'Cinereus' kül grisi anlamına gelir.",
    ),
    (
        "Brunneus",
        "'Brunneus' hangi rengi ifade eder?",
        "Kahverengi",
        ["Beyaz", "Mavi", "Kahverengi", "Pembe"],
        "Brunfelsia",
        "Brunfelsia bitki cinsi",
        "'Brunneus' kahverengi anlamına gelir.",
    ),
    (
        "Fuscus",
        "'Fuscus' hangi renk tonunu ifade eder?",
        "Koyu kahverengi veya esmer",
        ["Açık mavi", "Koyu kahverengi veya esmer", "Kar beyazı", "Parlak pembe"],
        "Botanik renk sıfatı",
        "Koyu renkleri anlatan sıfat",
        "'Fuscus' koyu kahverengi, esmer veya koyu renkli anlamına gelebilir.",
    ),
    (
        "Fulvus",
        "'Fulvus' hangi renk tonunu ifade eder?",
        "Sarımsı kahverengi",
        ["Mavi", "Siyah", "Mor", "Sarımsı kahverengi"],
        "Botanik renk sıfatı",
        "Toprak tonlarını anlatan sıfat",
        "'Fulvus' sarımsı kahverengi veya boz tonları anlatır.",
    ),
    (
        "Rufus",
        "'Rufus' hangi rengi ifade eder?",
        "Kızıl veya kızıl kahverengi",
        ["Kızıl veya kızıl kahverengi", "Yeşil", "Beyaz", "Gök mavisi"],
        "Botanik renk sıfatı",
        "Kızıl tonları anlatan sıfat",
        "'Rufus' kızıl veya kızıl kahverengi anlamına gelir.",
    ),
    (
        "Atropurpureus",
        "'Atropurpureus' hangi renk tonunu ifade eder?",
        "Çok koyu mor",
        ["Açık sarı", "Çok koyu mor", "Beyaz", "Gümüş"],
        "Ocimum tenuiflorum",
        "Kutsal fesleğen",
        "'Atropurpureus' siyaha yaklaşan çok koyu mor tonunu anlatır.",
    ),
    (
        "Pallidus",
        "'Pallidus' ne anlama gelir?",
        "Soluk veya açık renkli",
        ["Çok parlak", "Koyu siyah", "Soluk veya açık renkli", "Altın rengi"],
        "Botanik renk sıfatı",
        "Soluk renkleri anlatan sıfat",
        "'Pallidus' soluk veya açık renkli anlamına gelir.",
    ),
    (
        "Argenteus",
        "'Argenteus' hangi rengi ifade eder?",
        "Gümüş rengi",
        ["Turuncu", "Kahverengi", "Kırmızı", "Gümüş rengi"],
        "Salix alba",
        "Ak söğüt",
        "'Argenteus' gümüş rengi veya gümüşi anlamına gelir.",
    ),
    (
        "Cupreus",
        "'Cupreus' hangi rengi ifade eder?",
        "Bakır rengi",
        ["Bakır rengi", "Mavi", "Beyaz", "Pembe"],
        "Botanik renk sıfatı",
        "Bakırımsı tonları anlatan sıfat",
        "'Cupreus' bakır rengi anlamına gelir.",
    ),
    (
        "Lilacinus",
        "'Lilacinus' hangi rengi ifade eder?",
        "Leylak rengi",
        ["Yeşil", "Leylak rengi", "Siyah", "Sarı"],
        "Syringa vulgaris",
        "Adi leylak",
        "'Lilacinus' leylak rengi veya açık mor tonları anlatır.",
    ),
    (
        "Lacteus",
        "'Lacteus' hangi rengi ifade eder?",
        "Süt beyazı",
        ["Koyu kahverengi", "Mor", "Süt beyazı", "Turuncu"],
        "Euphorbia lactea",
        "Sütleğen türü",
        "'Lacteus' süt beyazı anlamına gelir.",
    ),
    (
        "Niveus",
        "'Niveus' hangi rengi ifade eder?",
        "Kar beyazı",
        ["Kızıl", "Yeşil", "Mavi", "Kar beyazı"],
        "Galanthus nivalis",
        "Kardelen",
        "'Niveus' kar beyazı anlamına gelir.",
    ),
    (
        "Bicolor",
        "'Bicolor' ne anlama gelir?",
        "İki renkli",
        ["İki renkli", "Tek renkli", "Renksiz", "Kül grisi"],
        "Viola tricolor",
        "Hercai menekşe",
        "'Bicolor' iki renkli anlamına gelir.",
    ),
    (
        "Tricolor",
        "'Tricolor' ne anlama gelir?",
        "Üç renkli",
        ["Siyah", "Üç renkli", "Altın sarısı", "Gri"],
        "Viola tricolor",
        "Hercai menekşe",
        "'Tricolor' üç renkli anlamına gelir.",
    ),
    (
        "Versicolor",
        "'Versicolor' ne anlama gelir?",
        "Çok renkli veya renk değiştiren",
        ["Beyaz", "Kırmızı", "Çok renkli veya renk değiştiren", "Koyu yeşil"],
        "Lantana camara",
        "Mine çalısı",
        "'Versicolor' çok renkli veya farklı renkler gösterebilen anlamına gelir.",
    ),
    (
        "Coccineus",
        "'Coccineus' hangi rengi ifade eder?",
        "Parlak kırmızı",
        ["Gri", "Parlak kırmızı", "Mavimsi yeşil", "Kahverengi"],
        "Salvia coccinea",
        "Kırmızı çiçekli adaçayı",
        "'Coccineus' parlak kırmızı veya al rengini ifade eder.",
    ),
    (
        "Sanguineus",
        "'Sanguineus' hangi rengi ifade eder?",
        "Kan kırmızısı",
        ["Kan kırmızısı", "Soluk sarı", "Gümüş", "Yeşil"],
        "Botanik renk sıfatı",
        "Derin kırmızı tonlarını anlatan sıfat",
        "'Sanguineus' kan kırmızısı anlamına gelir.",
    ),
    (
        "Pallens",
        "'Pallens' hangi özelliği ifade eder?",
        "Soluk veya solgun",
        ["Çok koyu", "Altın rengi", "Soluk veya solgun", "Bakır rengi"],
        "Botanik renk sıfatı",
        "Solgun renkleri anlatan sıfat",
        "'Pallens' soluk veya solgun anlamına gelir.",
    ),
    (
        "Rubescens",
        "'Rubescens' ne anlama gelir?",
        "Kırmızılaşan",
        ["Yeşile dönen", "Kırmızılaşan", "Beyazlaşan", "Maviye dönen"],
        "Trifolium rubens",
        "Kızıl çayır üçgülü",
        "'Rubescens' kızaran veya kırmızılaşan anlamına gelir.",
    ),
    (
        "Albicans",
        "'Albicans' hangi anlamı taşır?",
        "Beyazımsı",
        ["Siyahımsı", "Sarımsı", "Beyazımsı", "Kızılımsı"],
        "Botanik renk sıfatı",
        "Beyaza çalan tonları anlatan sıfat",
        "'Albicans' beyazımsı anlamına gelir.",
    ),
    (
        "Flavescens",
        "'Flavescens' ne anlama gelir?",
        "Sarılaşan",
        ["Mavileşen", "Kararan", "Morlaşan", "Sarılaşan"],
        "Botanik renk sıfatı",
        "Sarıya dönen tonları anlatan sıfat",
        "'Flavescens' sarılaşan veya sarımsı anlamına gelir.",
    ),
    (
        "Viridescens",
        "'Viridescens' ne anlama gelir?",
        "Yeşile dönen",
        ["Yeşile dönen", "Kırmızılaşan", "Beyazlaşan", "Kararan"],
        "Botanik renk sıfatı",
        "Yeşile dönen tonları anlatan sıfat",
        "'Viridescens' yeşilimsi veya yeşile dönen anlamına gelir.",
    ),
    (
        "Obscurus",
        "'Obscurus' renk tanımında ne anlama gelir?",
        "Koyu veya karanlık",
        ["Açık", "Parlak", "Koyu veya karanlık", "Süt beyazı"],
        "Botanik renk sıfatı",
        "Koyu tonları anlatan sıfat",
        "'Obscurus' koyu veya karanlık anlamına gelir.",
    ),
    (
        "Nitidus",
        "'Nitidus' hangi özelliği anlatır?",
        "Parlak",
        ["Mat", "Parlak", "Soluk", "Kül grisi"],
        "Botanik görünüm sıfatı",
        "Parlak yüzeyleri anlatan sıfat",
        "'Nitidus' parlak veya cilalı görünümlü anlamına gelir.",
    ),
    (
        "Maculatus",
        "'Maculatus' ne anlama gelir?",
        "Benekli",
        ["Çizgili", "Düz renkli", "Benekli", "Şeffaf"],
        "Pulmonaria officinalis",
        "Akciğer otu",
        "'Maculatus' benekli anlamına gelir; doğrudan bir renk değil, desen belirtir.",
    ),
    (
        "Striatus",
        "'Striatus' ne anlama gelir?",
        "Çizgili",
        ["Çizgili", "Beyaz", "Kızıl", "Altın rengi"],
        "Botanik desen sıfatı",
        "Çizgili görünümü anlatan sıfat",
        "'Striatus' çizgili anlamına gelir.",
    ),
    (
        "Azureus",
        "'Azureus' hangi rengi ifade eder?",
        "Azur veya gök mavisi",
        ["Koyu kahverengi", "Azur veya gök mavisi", "Siyah", "Pembe"],
        "Botanik renk sıfatı",
        "Mavi tonlarını anlatan sıfat",
        "'Azureus' azur veya gök mavisi anlamına gelir.",
    ),
    (
        "Canus",
        "'Canus' hangi renk tonunu ifade eder?",
        "Beyazımsı gri",
        ["Turuncu", "Mor", "Beyazımsı gri", "Parlak kırmızı"],
        "Botanik renk sıfatı",
        "Gri-beyaz tonlarını anlatan sıfat",
        "'Canus' beyazımsı gri veya kırçıllı görünümü anlatabilir.",
    ),
    (
        "Lividus",
        "'Lividus' hangi renk tonunu ifade eder?",
        "Kurşuni veya mavimsi gri",
        ["Altın sarısı", "Kurşuni veya mavimsi gri", "Pembe", "Yeşil"],
        "Botanik renk sıfatı",
        "Soğuk gri tonlarını anlatan sıfat",
        "'Lividus' kurşuni veya mavimsi gri tonlarını ifade edebilir.",
    ),
    (
        "Coloratus",
        "'Coloratus' ne anlama gelir?",
        "Renkli",
        ["Renksiz", "Renkli", "Yalnızca beyaz", "Çizgili"],
        "Botanik tanımlama sıfatı",
        "Renkli görünümü anlatan sıfat",
        "'Coloratus' renkli veya belirgin renge sahip anlamına gelir.",
    ),
    (
        "Argentea",
        "'Argentea' hangi rengi ifade eder?",
        "Gümüş rengi",
        ["Gümüş rengi", "Bakır", "Kızıl", "Sarı"],
        "Salix alba",
        "Ak söğüt",
        "'Argentea', gümüşi anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Aureolus",
        "'Aureolus' hangi renk tonunu ifade eder?",
        "Altınsı",
        ["Mavimsi", "Kül grisi", "Altınsı", "Siyah"],
        "Botanik renk sıfatı",
        "Yumuşak altın tonlarını anlatan sıfat",
        "'Aureolus' altın renkli veya altınsı anlamına gelir.",
    ),
    (
        "Piceus",
        "'Piceus' hangi rengi ifade eder?",
        "Zift siyahı",
        ["Kar beyazı", "Zift siyahı", "Leylak", "Gümüş"],
        "Botanik renk sıfatı",
        "Çok koyu siyahı anlatan sıfat",
        "'Piceus' zift gibi koyu veya siyah anlamına gelir.",
    ),
    (
        "Nivea",
        "'Nivea' hangi rengi ifade eder?",
        "Kar beyazı",
        ["Kızıl", "Yeşil", "Kar beyazı", "Bakır"],
        "Galanthus nivalis",
        "Kardelen",
        "'Nivea', kar beyazı anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Fulva",
        "'Fulva' hangi renk tonunu ifade eder?",
        "Sarımsı kahverengi",
        ["Sarımsı kahverengi", "Mavi", "Siyah", "Gümüş"],
        "Botanik renk sıfatı",
        "Sıcak toprak tonlarını anlatan sıfat",
        "'Fulva', sarımsı kahverengi anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Cinerea",
        "'Cinerea' hangi rengi ifade eder?",
        "Kül grisi",
        ["Pembe", "Kül grisi", "Altın sarısı", "Mor"],
        "Eucalyptus cinerea",
        "Gümüş dolar okaliptüsü",
        "'Cinerea', kül grisi anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Rosea",
        "'Rosea' hangi rengi ifade eder?",
        "Pembe",
        ["Kahverengi", "Siyah", "Pembe", "Mavi"],
        "Rosa",
        "Gül cinsi",
        "'Rosea', pembe anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Rubra",
        "'Rubra' hangi rengi ifade eder?",
        "Kırmızı",
        ["Gri", "Kırmızı", "Yeşil", "Sarı"],
        "Rosa rubra",
        "Kırmızı renk sıfatı içeren botanik ad",
        "'Rubra', kırmızı anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Flava",
        "'Flava' hangi rengi ifade eder?",
        "Sarı",
        ["Mavi", "Siyah", "Sarı", "Pembe"],
        "Iris pseudacorus",
        "Sarı süsen",
        "'Flava', sarı anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Glauca",
        "'Glauca' hangi renk tonunu ifade eder?",
        "Mavimsi yeşil veya grimsi mavi",
        ["Parlak turuncu", "Mavimsi yeşil veya grimsi mavi", "Siyah", "Pembe"],
        "Eucalyptus cinerea",
        "Gümüş dolar okaliptüsü",
        "'Glauca', mavimsi yeşil veya grimsi mavi anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Sanguinea",
        "'Sanguinea' hangi rengi ifade eder?",
        "Kan kırmızısı",
        ["Kan kırmızısı", "Soluk mavi", "Gümüş", "Yeşil"],
        "Botanik renk sıfatı",
        "Derin kırmızı tonlarını anlatan sıfat",
        "'Sanguinea', kan kırmızısı anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Coccinea",
        "'Coccinea' hangi rengi ifade eder?",
        "Parlak kırmızı",
        ["Kül grisi", "Mavimsi yeşil", "Parlak kırmızı", "Kahverengi"],
        "Salvia coccinea",
        "Kırmızı çiçekli adaçayı",
        "'Coccinea', parlak kırmızı anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Purpurea",
        "'Purpurea' hangi rengi ifade eder?",
        "Mor veya erguvan",
        ["Mavi", "Mor veya erguvan", "Yeşil", "Gümüş"],
        "Echinacea purpurea",
        "Mor ekinezya",
        "'Purpurea', mor anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Violacea",
        "'Violacea' hangi rengi ifade eder?",
        "Menekşe moru",
        ["Kahverengi", "Sarı", "Menekşe moru", "Beyaz"],
        "Viola odorata",
        "Kokulu menekşe",
        "'Violacea', menekşe moru anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Lutea",
        "'Lutea' hangi rengi ifade eder?",
        "Sarı",
        ["Sarı", "Mavi", "Siyah", "Gri"],
        "Iris pseudacorus",
        "Sarı süsen",
        "'Lutea', sarı anlamındaki sıfatın dişil biçimidir.",
    ),
    (
        "Viridescens",
        "'Viridescens' hangi renk değişimini ifade eder?",
        "Yeşile dönen",
        ["Kızaran", "Yeşile dönen", "Beyazlaşan", "Kararan"],
        "Botanik renk sıfatı",
        "Yeşile dönen tonları anlatan sıfat",
        "'Viridescens' yeşilimsi veya yeşile dönen anlamına gelir.",
    ),
    (
        "Dilutus",
        "'Dilutus' renk tanımında ne anlama gelir?",
        "Açılmış veya seyrelmiş",
        ["Çok koyu", "Açılmış veya seyrelmiş", "Parlak siyah", "Altın rengi"],
        "Botanik renk sıfatı",
        "Rengin açılmış olduğunu anlatan sıfat",
        "'Dilutus' seyrelmiş veya daha açık hale gelmiş anlamına gelir.",
    ),
    (
        "Clarus",
        "'Clarus' renk tanımında hangi anlamı taşır?",
        "Açık veya parlak",
        ["Açık veya parlak", "Siyah", "Koyu kahverengi", "Kırmızı"],
        "Botanik renk sıfatı",
        "Açık ve parlak görünümü anlatan sıfat",
        "'Clarus' açık, parlak veya belirgin anlamına gelebilir.",
    ),
    (
        "Saturatus",
        "'Saturatus' renk tanımında ne anlama gelir?",
        "Doygun veya yoğun",
        ["Soluk", "Doygun veya yoğun", "Renksiz", "Şeffaf"],
        "Botanik renk sıfatı",
        "Yoğun renkleri anlatan sıfat",
        "'Saturatus' doygun veya yoğun anlamına gelir.",
    ),
    (
        "Opacus",
        "'Opacus' görünüm bakımından ne anlama gelir?",
        "Mat veya donuk",
        ["Parlak", "Mat veya donuk", "Gümüş", "Kızıl"],
        "Botanik görünüm sıfatı",
        "Mat yüzeyleri anlatan sıfat",
        "'Opacus' mat, donuk veya ışığı geçirmeyen anlamına gelebilir.",
    ),
    (
        "Micans",
        "'Micans' hangi görünümü anlatır?",
        "Parıldayan",
        ["Kül grisi", "Parıldayan", "Soluk", "Siyah"],
        "Botanik görünüm sıfatı",
        "Işıltılı yüzeyleri anlatan sıfat",
        "'Micans' parıldayan veya ışıldayan anlamına gelir.",
    ),
    (
        "Subalbus",
        "'Subalbus' hangi anlamı taşır?",
        "Beyazımsı",
        ["Kırmızı", "Beyazımsı", "Siyah", "Mavi"],
        "Botanik renk sıfatı",
        "Beyaza çalan tonları anlatan sıfat",
        "'Sub-' öneki yaklaşık olarak 'biraz' veya '-ımsı' anlamı katabilir.",
    ),
    (
        "Subflavus",
        "'Subflavus' hangi anlamı taşır?",
        "Sarımsı",
        ["Gümüş", "Mor", "Sarımsı", "Koyu siyah"],
        "Botanik renk sıfatı",
        "Sarıya çalan tonları anlatan sıfat",
        "'Subflavus' sarımsı anlamına gelir.",
    ),
    (
        "Subrubens",
        "'Subrubens' hangi anlamı taşır?",
        "Kırmızımsı",
        ["Kırmızımsı", "Mavimsi", "Yeşilimsi", "Beyazımsı"],
        "Botanik renk sıfatı",
        "Kırmızıya çalan tonları anlatan sıfat",
        "'Subrubens' kırmızımsı anlamında yorumlanabilir.",
    ),
    (
        "Subviridis",
        "'Subviridis' hangi anlamı taşır?",
        "Yeşilimsi",
        ["Kızıl", "Gümüş", "Yeşilimsi", "Siyah"],
        "Botanik renk sıfatı",
        "Yeşile çalan tonları anlatan sıfat",
        "'Subviridis' yeşilimsi anlamına gelir.",
    ),
]


def build_question_pool():
    """Ham soru verilerini uygulamanın kullandığı sözlüklere dönüştürür."""
    result = []

    for item in RAW_QUESTIONS:
        latin, question, answer, options, plant, plant_name, explanation = item

        unique_options = list(dict.fromkeys(options))

        if answer not in unique_options:
            unique_options.append(answer)

        if len(unique_options) < 4:
            continue

        result.append(
            {
                "latin": latin,
                "question": question,
                "answer": answer,
                "options": unique_options,
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
    "selected_answer": None,
    "leaderboard": [
        {
            "id": "seed-linnaeus",
            "İsim": "Linnaeus",
            "Doğru Sayısı": 5,
            "Toplam Soru": 5,
            "Süre (sn)": 14.2,
        },
        {
            "id": "seed-darwin",
            "İsim": "Darwin",
            "Doğru Sayısı": 4,
            "Toplam Soru": 5,
            "Süre (sn)": 11.0,
        },
        {
            "id": "seed-mendel",
            "İsim": "Mendel",
            "Doğru Sayısı": 3,
            "Toplam Soru": 5,
            "Süre (sn)": 9.5,
        },
    ],
    "run_id": None,
    "submitted_run_id": None,
    "last_answer_time": None,
    "quiz_length": 20,
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
    """HTML içinde gösterilen metinleri güvenli biçimde kaçışlar."""
    return html.escape(str(value))


def format_seconds(seconds):
    """Saniyeyi okunabilir dakika/saniye biçimine dönüştürür."""
    seconds = max(0, int(seconds))
    minutes, remaining = divmod(seconds, 60)

    if minutes:
        return f"{minutes} dk {remaining} sn"

    return f"{remaining} sn"


def make_balanced_questions(count):
    """Soruları karıştırır ve doğru cevapların konumlarını dengeler."""
    source = QUESTIONS.copy()
    random.shuffle(source)

    selected = source[: min(count, len(source))]

    positions = [0, 1, 2, 3] * ((len(selected) + 3) // 4)
    positions = positions[: len(selected)]
    random.shuffle(positions)

    prepared = []

    for question, correct_position in zip(selected, positions):
        correct_answer = question["answer"]

        distractors = [
            option for option in question["options"] if option != correct_answer
        ]

        random.shuffle(distractors)
        distractors = distractors[:3]

        if len(distractors) < 3:
            other_answers = list(
                dict.fromkeys(
                    q["answer"]
                    for q in QUESTIONS
                    if q["answer"] != correct_answer
                    and q["answer"] not in distractors
                )
            )

            random.shuffle(other_answers)

            for option in other_answers:
                if option not in distractors:
                    distractors.append(option)

                if len(distractors) == 3:
                    break

        if len(distractors) < 3:
            continue

        distractors = distractors[:3]
        options = distractors.copy()
        options.insert(correct_position, correct_answer)

        prepared_question = question.copy()
        prepared_question["options"] = options

        prepared.append(prepared_question)

    return prepared


def start_quiz(name, count):
    """Yeni bir oyun başlatır ve durumu ayarlar."""
    selected_questions = make_balanced_questions(count)

    st.session_state.name = name.strip()
    st.session_state.score = 0
    st.session_state.current_question = 0
    st.session_state.answers = []
    st.session_state.quiz_questions = selected_questions
    st.session_state.start_time = time.time()
    st.session_state.elapsed_time = 0.0
    st.session_state.selected_answer = None
    st.session_state.run_id = str(uuid.uuid4())
    st.session_state.submitted_run_id = None
    st.session_state.last_answer_time = None
    st.session_state.stage = "quiz"


# ============================================================
# 6. SAYFA AKIŞLARI
# ============================================================

# ------------------------------------------------------------
# 6.1. KAYIT EKRANI
# ------------------------------------------------------------
if st.session_state.stage == "register":
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-eyebrow">🌿 Botanica Akademi</div>
            <h1 class="hero-title">Latince Botanik Renkleri Macerası</h1>
            <p class="hero-description">
                Bitki bilimi ve taksonomide kullanılan Latince renk terimlerini,
                kökenlerini ve örnek bitki adlarını interaktif biçimde keşfedin.
                Süreniz tutulur ve liderlik tablosuna kaydedilir!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("register_form"):
        name_input = st.text_input(
            "Adınız veya Takma Adınız:",
            value=st.session_state.name,
            placeholder="Örn: Karl Linnaeus",
        )

        question_counts = [5, 10, 15, 20, len(QUESTIONS)]
        selected_count = st.selectbox(
            "Soru Sayısı:",
            question_counts,
            index=1,
            format_func=lambda x: f"{x} Soru",
        )

        submitted = st.form_submit_button("Testi Başlat 🚀", use_container_width=True)

        if submitted:
            if not name_input.strip():
                st.warning("Lütfen başlamak için adınızı girin.")
            else:
                start_quiz(name_input, selected_count)
                st.rerun()

    # Liderlik Tablosu Önizleme
    if st.session_state.leaderboard:
        st.markdown(
            '<div class="section-heading"><h3>🏆 En İyi Skorlar</h3></div>',
            unsafe_allow_html=True,
        )
        df_preview = pd.DataFrame(st.session_state.leaderboard)
        df_preview = df_preview.sort_values(
            by=["Doğru Sayısı", "Süre (sn)"], ascending=[False, True]
        ).reset_index(drop=True)
        df_preview.index = df_preview.index + 1
        st.dataframe(
            df_preview[["İsim", "Doğru Sayısı", "Toplam Soru", "Süre (sn)"]],
            use_container_width=True,
        )


# ------------------------------------------------------------
# 6.2. SORU EKRANI
# ------------------------------------------------------------
elif st.session_state.stage == "quiz":
    questions = st.session_state.quiz_questions
    index = st.session_state.current_question

    if not questions or index >= len(questions):
        st.session_state.stage = "register"
        st.rerun()

    q = questions[index]

    progress = (index + 1) / len(questions)
    st.progress(progress)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption(f"Soru {index + 1} / {len(questions)}")
    with col2:
        st.caption(f"Puan: {st.session_state.score}")

    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-label">Botanik Terim</div>
            <div class="latin-term">{safe_text(q['latin'])}</div>
            <div class="question-text">{safe_text(q['question'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Şık seçimi için form
    with st.form(f"quiz_form_{index}"):
        selected_option = st.radio(
            "Seçeneğinizi belirleyin:",
            q["options"],
            index=None,
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button("Cevabı Kontrol Et ✨", use_container_width=True)

        if submitted:
            if selected_option is None:
                st.warning("Lütfen bir seçenek seçin.")
            else:
                is_correct = selected_option == q["answer"]
                if is_correct:
                    st.session_state.score += 1

                st.session_state.answers.append(
                    {
                        "latin": q["latin"],
                        "question": q["question"],
                        "selected": selected_option,
                        "correct": q["answer"],
                        "is_correct": is_correct,
                        "plant": q["plant"],
                        "plant_name": q["plant_name"],
                        "explanation": q["explanation"],
                    }
                )

                st.session_state.last_answer_time = time.time()
                st.session_state.stage = "feedback"
                st.rerun()


# ------------------------------------------------------------
# 6.3. GERİBİLDİRİM VE AÇIKLAMA EKRANI
# ------------------------------------------------------------
elif st.session_state.stage == "feedback":
    questions = st.session_state.quiz_questions
    index = st.session_state.current_question
    last_answer = st.session_state.answers[-1]
    q = questions[index]

    if last_answer["is_correct"]:
        st.success("🎉 Harika! Doğru cevap.")
    else:
        st.error(
            f"❌ Yanlış cevap. Doğru seçenek: **{safe_text(last_answer['correct'])}**"
        )

    st.markdown(
        f"""
        <div class="plant-card">
            <div class="muted-text">Botanik Açıklama ve Örnek</div>
            <div class="plant-name">🌿 {safe_text(q['plant'])} — <em>{safe_text(q['plant_name'])}</em></div>
            <p class="plant-description">{safe_text(q['explanation'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    is_last = index + 1 >= len(questions)
    button_label = "Sonuçları Gör 🏆" if is_last else "Sonraki Soru ➡️"

    if st.button(button_label, use_container_width=True):
        if is_last:
            if st.session_state.start_time:
                st.session_state.elapsed_time = round(
                    time.time() - st.session_state.start_time, 2
                )
            else:
                st.session_state.elapsed_time = 0.0

            current_run_id = st.session_state.get("run_id")
            if (
                current_run_id
                and st.session_state.get("submitted_run_id") != current_run_id
            ):
                st.session_state.leaderboard.append(
                    {
                        "id": current_run_id,
                        "İsim": st.session_state.name,
                        "Doğru Sayısı": st.session_state.score,
                        "Toplam Soru": len(questions),
                        "Süre (sn)": st.session_state.elapsed_time,
                    }
                )
                st.session_state.submitted_run_id = current_run_id

            st.session_state.stage = "result"
            st.rerun()
        else:
            st.session_state.current_question += 1
            st.session_state.stage = "quiz"
            st.rerun()


# ------------------------------------------------------------
# 6.4. SONUÇ VE LİDERLİK TABLOSU EKRANI
# ------------------------------------------------------------
elif st.session_state.stage == "result":
    questions = st.session_state.quiz_questions
    total_q = len(questions) if questions else 1
    score = st.session_state.score
    percentage = (score / total_q) * 100

    if score == total_q:
        st.balloons()

    st.markdown(
        f"""
        <div class="result-banner">
            <div class="hero-eyebrow">Quiz Tamamlandı</div>
            <div class="result-score">{score} / {total_q} Doğru (%{percentage:.0f})</div>
            <p class="muted-text" style="margin-top: .5rem;">
                Süre: <strong>{format_seconds(st.session_state.elapsed_time)}</strong> ({st.session_state.elapsed_time} sn)
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-heading"><h3>🌟 Liderlik Tablosu</h3></div>',
        unsafe_allow_html=True,
    )

    df_lb = pd.DataFrame(st.session_state.leaderboard)
    if not df_lb.empty:
        # Doğru sayısına göre azalan, süreye göre artan sıralama
        df_lb = df_lb.sort_values(
            by=["Doğru Sayısı", "Süre (sn)"], ascending=[False, True]
        ).reset_index(drop=True)
        df_lb.index = df_lb.index + 1

        # Kullanıcının kendi skorunu vurgulama veya şık gösterim
        st.dataframe(
            df_lb[["İsim", "Doğru Sayısı", "Toplam Soru", "Süre (sn)"]],
            use_container_width=True,
        )

    with st.expander("📝 Detaylı Soru İncelemesi"):
        for i, ans in enumerate(st.session_state.answers, 1):
            icon = "✅" if ans["is_correct"] else "❌"
            st.markdown(
                f"""
                <div class="answer-card {'answer-correct' if ans['is_correct'] else 'answer-wrong'}">
                    <strong>{i}. {safe_text(ans['latin'])}</strong> — {safe_text(ans['question'])}<br>
                    <span class="muted-text">Senin cevabın:</span> <strong>{safe_text(ans['selected'])}</strong> | 
                    <span class="muted-text">Doğru cevap:</span> <strong>{safe_text(ans['correct'])}</strong><br>
                    <em>🌱 {safe_text(ans['plant'])} ({safe_text(ans['plant_name'])})</em>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Tekrar Oyna 🔄", use_container_width=True):
            st.session_state.stage = "register"
            st.session_state.run_id = None
            st.session_state.submitted_run_id = None
            st.rerun()
    with col2:
        if st.button("Ana Sayfaya Dön 🏠", use_container_width=True):
            st.session_state.stage = "register"
            st.session_state.name = ""
            st.session_state.run_id = None
            st.session_state.submitted_run_id = None
            st.rerun()
