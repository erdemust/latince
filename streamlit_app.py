import random
import time
import html
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
#
# Her soru:
# latin, question, answer, options, plant, plant_name,
# explanation alanlarını içerir.
#
# Doğru cevaplar oyuna başlarken A/B/C/D konumlarına
# mümkün olduğunca dengeli dağıtılır.
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

    # Ek renkler ve tonlar
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
        ["Altın sarısı", "Kurşuni veya mavimsi gri", "Pembe", "Ye
