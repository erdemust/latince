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
        "Nymphaea alba'nın beyaz taç yaprakları tür epitetiyle doğrudan "
        "örtüşür. Çiçeklerdeki beyaz görünüm, taç yaprakların ışığı "
        "geniş ölçüde yansıtması ve görünür ışığı soğuran pigmentlerin "
        "az olmasıyla ilişkilidir.",
    ),
    (
        "Niger",
        "Siyah",
        ["Yeşil", "Mavi", "Siyah", "Pembe"],
        "Sambucus nigra",
        "Kara mürver",
        "'Niger' Latince siyah veya çok koyu renkli anlamına gelir; "
        "'nigra', dişil biçimidir. Sambucus nigra'nın olgun meyveleri "
        "antosiyanin pigmentleri nedeniyle koyu mor-siyah görünür. "
        "Tür epiteti bu belirgin meyve rengiyle doğrudan ilişkilidir.",
    ),
    (
        "Ruber",
        "Kırmızı",
        ["Kırmızı", "Mor", "Gri", "Beyaz"],
        "Trifolium rubens",
        "Kızıl çayır üçgülü",
        "'Ruber' Latince kırmızı anlamına gelir. 'Rubens', kızaran veya "
        "kırmızımsı görünen anlamındaki ilişkili bir biçimdir. "
        "Trifolium rubens'in çiçek başları pembe-kırmızı ile koyu "
        "kızıl tonlar arasında değişir; tür epiteti aynı renk kökünü "
        "taşır ve çiçeklerin görünümüyle uyumludur.",
    ),
    (
        "Roseus",
        "Gül pembesi",
        ["Turuncu", "Kahverengi", "Sarı", "Gül pembesi"],
        "Rosa canina",
        "Kuşburnu gülü",
        "'Roseus' gül renginde veya gül pembesi anlamına gelir. "
        "Rosa canina'nın çiçekleri çoğunlukla açık pembe veya beyazımsı "
        "pembe tonlardadır. Bu seçim doğrudan renk kökü eşleşmesi "
        "değildir; açık pembe çiçekleri nedeniyle renk kavramını "
        "gösterebilir, ancak epitet temelli bir örnek olarak "
        "Rosa rosea gibi doğrulanmış bir takson tercih edilmelidir.",
    ),
    (
        "Purpureus",
        "Mor veya erguvan",
        ["Mavi", "Mor veya erguvan", "Yeşil", "Gümüş"],
        "Echinacea purpurea",
        "Mor ekinezya",
        "'Purpureus' mor veya erguvan tonlarını ifade eder. "
        "Echinacea purpurea'nın ışın çiçekleri tipik olarak pembe-mor "
        "ve erguvan tonlarındadır. Tür epiteti doğrudan aynı renk "
        "kökünü taşır; renk özellikle çiçeklerin dilsi taç "
        "yapraklarında belirgindir.",
    ),
    (
        "Violaceus",
        "Menekşe moru",
        ["Kahverengi", "Sarı", "Menekşe moru", "Beyaz"],
        "Viola odorata",
        "Kokulu menekşe",
        "'Violaceus' menekşe moru anlamına gelir. Viola odorata'nın "
        "karakteristik çiçekleri menekşe-mor tonlarındadır. Cins adı "
        "Viola da menekşe bitkisini belirtir; ancak bu örnekte tür "
        "epiteti renk sıfatının kendisi değildir. Renk, çiçeklerdeki "
        "antosiyanin pigmentleriyle ilişkilidir.",
    ),
    (
        "Caeruleus",
        "Gök mavisi",
        ["Gri", "Gök mavisi", "Siyah", "Kırmızı"],
        "Salvia azurea",
        "Gök mavisi adaçayı",
        "'Caeruleus' Latince mavi veya gök mavisi anlamına gelir. "
        "Salvia azurea'nın çiçekleri belirgin gök mavisi tonları taşır. "
        "Tür epiteti aynı renk kavramına yakın anlamlı olan 'azure' "
        "kökünden gelir; mavi görünüm taç yapraklardaki pigmentlerin "
        "ışığı seçici biçimde soğurmasıyla oluşur.",
    ),
    (
        "Flavus",
        "Sarı",
        ["Yeşil", "Mor", "Pembe", "Sarı"],
        "Rosa foetida",
        "Sarı gül",
        "'Flavus' Latince sarı anlamına gelir. Rosa foetida'nın "
        "karakteristik çiçekleri parlak sarıdır. Bu türün sarı taç "
        "yaprakları, sarı pigmentlerin ve özellikle karotenoidlerin "
        "ışığı soğurma özellikleri nedeniyle belirgin bir sarı "
        "görünüm sergiler.",
    ),
    (
        "Luteus",
        "Sarı",
        ["Sarı", "Mavi", "Siyah", "Gri"],
        "Iris pseudacorus",
        "Sarı süsen",
        "'Luteus' Latince sarı anlamına gelir. Iris pseudacorus'un "
        "büyük çiçekleri parlak sarı renktedir. Sarı pigmentler, "
        "çiçek dokusunun görünür ışığın mavi-mor dalga boylarını "
        "soğurup sarı dalga boylarını yansıtmasına katkıda bulunur.",
    ),
    (
        "Aureus",
        "Altın rengi",
        ["Gümüş", "Kahverengi", "Altın rengi", "Mor"],
        "Forsythia suspensa",
        "Sarkan altın çanı",
        "'Aureus' Latince altın renginde anlamına gelir. Forsythia "
        "suspensa, yapraklanmadan önce açabilen yoğun sarı çiçekleriyle "
        "tanınır. Çiçeklerin doygun altın sarısı görünümü, sarı "
        "pigmentlerin ışığı seçici biçimde soğurmasıyla ilişkilidir. "
        "Tür epiteti doğrudan 'aureus' biçiminde olmasa da bitki "
        "rengi açıkça temsil eder.",
    ),
    (
        "Viridis",
        "Yeşil",
        ["Kırmızı", "Yeşil", "Pembe", "Turuncu"],
        "Helleborus viridis",
        "Yeşil çöpleme",
        "'Viridis' Latince yeşil anlamına gelir. Helleborus viridis'in "
        "çiçek örtüsü yaprak benzeri yeşil çanak yapraklardan oluşur. "
        "Bu dokulardaki klorofil, kırmızı ve mavi ışığı soğururken "
        "yeşil ışığın daha büyük bir bölümünün yansımasına veya "
        "geçmesine neden olur. Tür epiteti renk sıfatıyla aynıdır.",
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
        "Eucalyptus cinerea",
        "Gümüş dolar okaliptüsü",
        "'Glaucus', mavimsi yeşil veya grimsi mavi, çoğu zaman puslu "
        "görünümlü tonları ifade eder. Eucalyptus cinerea'nın genç "
        "yaprakları mumsu yüzeyleri nedeniyle gümüşi mavi-gri görünür. "
        "Yüzeydeki mumsu tabaka ışığın yansımasını değiştirerek bu "
        "mat, mavimsi görünümü güçlendirir. Bu, doğrudan epitet "
        "eşleşmesi değil, görünür renk bakımından uygun bir örnektir.",
    ),
    (
        "Cinereus",
        "Kül grisi",
        ["Kül grisi", "Altın sarısı", "Pembe", "Mor"],
        "Jacobaea maritima",
        "Gümüş yapraklı kanarya otu",
        "'Cinereus' kül rengi veya kül grisi anlamına gelir. "
        "Jacobaea maritima'nın yaprakları yoğun beyazımsı tüylerle "
        "kaplıdır. Bu tüyler ışığı dağıtarak yaprakların gümüşi "
        "açık gri görünmesine neden olur. Tür epiteti aynı renk "
        "kökünü taşımasa da yaprak rengi kül grisi kavramına yakındır.",
    ),
    (
        "Brunneus",
        "Kahverengi",
        ["Beyaz", "Mavi", "Kahverengi", "Pembe"],
        "Carex brunnescens",
        "Kahverengileşen saz",
        "'Brunneus' Latince kahverengi anlamına gelir. Carex "
        "brunnescens'in tür epiteti aynı kahverengi renk kökünü "
        "taşır. Başakçıkların ve meyve taşıyan yapıların kahverengimsi "
        "görünümü bu adlandırmayla uyumludur; renk, olgunlaşan "
        "üreme yapılarında belirginleşir.",
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
        "'Fuscus' koyu, esmer veya koyu kahverengiye çalan renkleri "
        "ifade eder. Juncus fuscus tür epiteti aynı renk kökünü "
        "taşır. Bununla birlikte, türün bilimsel adının bulunması "
        "tek başına belirli bir organın koyu kahverengi olduğunu "
        "kanıtlamaz; renk açıklaması kullanılmadan önce güvenilir "
        "bir floristik kaynakla doğrulanmalıdır.",
    ),
    (
        "Fulvus",
        "Sarımsı kahverengi",
        ["Mavi", "Siyah", "Mor", "Sarımsı kahverengi"],
        "Carex fulva",
        "Sarımsı kahverengi saz",
        "'Fulvus' sarımsı kahverengi, boz veya kızılımsı sarı-kahverengi "
        "anlamına gelir. Carex fulva tür epiteti doğrudan aynı renk "
        "kökünü taşır. Ancak bu taksonun geçerli adı ve renk "
        "özelliği, veri havuzuna alınmadan önce güncel taksonomik "
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
        "'Rufus' kızıl veya kızıl kahverengi anlamına gelir. Rumex "
        "rufus adı renk kökünü doğrudan taşır. Bununla birlikte, "
        "türün taksonomik geçerliliği ve kızıl rengin hangi organında "
        "görüldüğü doğrulanmadan bu kaydın bilimsel açıdan kesin "
        "olduğu kabul edilmemelidir.",
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
        "Rosa pallida adının renk epiteti bu anlamı doğrudan taşır. "
        "Ancak bu adın kabul edilmiş bir tür adı olup olmadığı "
        "güvenilir bir taksonomik veri tabanından doğrulanmalıdır; "
        "yalnızca Latince açıdan uygun görünmesi yeterli değildir.",
    ),
    (
        "Argenteus",
        "Gümüş rengi",
        ["Turuncu", "Kahverengi", "Kırmızı", "Gümüş rengi"],
        "Salix alba",
        "Ak söğüt",
        "'Argenteus' gümüş renginde veya gümüşi anlamına gelir. "
        "Salix alba'nın özellikle genç sürgün ve yapraklarının "
        "alt yüzeylerinde bulunan ince tüyler, ışığı dağıtarak "
        "gümüşi bir görünüm oluşturabilir. Bununla birlikte, "
        "'alba' epiteti beyaz anlamına gelir; gümüş rengiyle "
        "aynı kökten gelmez.",
    ),
    (
        "Lilacinus",
        "Leylak rengi",
        ["Yeşil", "Leylak rengi", "Siyah", "Sarı"],
        "Syringa vulgaris",
        "Adi leylak",
        "'Lilacinus' leylak rengi veya açık mor tonlarını ifade eder. "
        "Syringa vulgaris'in bazı çeşitleri leylak-mor çiçekler "
        "açar; beyaz çiçekli çeşitleri de bulunur. Bu nedenle "
        "renk açıklaması özellikle mor çiçekli formlarla "
        "sınırlandırılmalıdır. Tür epiteti renk sıfatıyla aynı "
        "kökten gelmez.",
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
        "Acer palmatum 'Atropurpureum'",
        "Koyu mor yapraklı Japon akçaağacı",
        "'Atropurpureus', çok koyu mor veya siyaha çalan erguvan "
        "tonlarını ifade eder. Acer palmatum'un 'Atropurpureum' "
        "kültivarı koyu bordo-mor yapraklarıyla tanınır. Yaprak "
        "rengi antosiyanin pigmentleriyle ilişkilidir. Buradaki "
        "adlandırma bir kültivar epitetidir; bağımsız bir tür "
        "epiteti olarak değerlendirilmemelidir.",
    ),
    (
        "Cupreus",
        "Bakır rengi",
        ["Bakır rengi", "Mavi", "Beyaz", "Pembe"],
        "Acer griseum",
        "Kâğıt kabuklu akçaağaç",
        "'Cupreus' bakır renginde veya bakırımsı anlamına gelir. "
        "Acer griseum'un gövdeden soyulan tarçın-kızıl kahverengi "
        "kabuğu, bakırımsı tonlarıyla dikkat çeker. Bu renk, "
        "kabuğun dış dokularındaki pigmentler ve yaşlanmayla "
        "oluşan yüzey değişimleriyle ilişkilidir. Ancak tür "
        "epiteti 'griseum' gri anlamındadır; bakır rengiyle "
        "aynı kökten gelmez.",
    ),
    (
        "Lacteus",
        "Süt beyazı",
        ["Koyu kahverengi", "Mor", "Süt beyazı", "Turuncu"],
        "Euphorbia lactea",
        "Sütleğen",
        "'Lacteus' süt renginde anlamına gelir. Euphorbia lactea'nın "
        "tür epiteti süt anlamındaki Latince 'lac' köküyle ilişkilidir. "
        "Euphorbia türlerinin yaralanmış dokularından çıkan lateks "
        "genellikle süt beyazıdır; ancak bu özellik bütün türlerde "
        "aynı yoğunlukta değildir. Renk, öz suyu üzerinden "
        "doğrudan gözlemlenebilir.",
    ),
    (
        "Niveus",
        "Kar beyazı",
        ["Kızıl", "Yeşil", "Mavi", "Kar beyazı"],
        "Leucojum aestivum",
        "Yaz nergisi",
        "'Niveus' kar gibi beyaz anlamına gelir. Leucojum aestivum'un "
        "sarkık çiçekleri beyaz taç yaprakları üzerinde küçük yeşil "
        "işaretler taşır. Beyaz görünüm çiçek örtüsünün geniş "
        "ölçüde ışık yansıtmasıyla ilişkilidir. Bununla birlikte, "
        "tür epiteti 'aestivum' yaz mevsimine gönderme yapar; "
        "kar beyazı anlamını doğrudan taşımaz.",
    ),
    (
        "Bicolor",
        "İki renkli",
        ["İki renkli", "Tek renkli", "Renksiz", "Kül grisi"],
        "Abutilon pictum",
        "Boyalı abutilon",
        "'Bicolor' iki renkli anlamına gelir. Abutilon pictum'un "
        "çiçeklerinde sarı-turuncu zemin üzerinde kırmızı damarlar "
        "veya lekeler görülebilir. Bu renk dağılımı çiçeğin iki "
        "veya daha fazla renkli görünmesini sağlar. Ancak 'pictum' "
        "epiteti boyalı veya desenli anlamındadır; 'bicolor' ile "
        "aynı sözcük değildir.",
    ),
    (
        "Tricolor",
        "Üç renkli",
        ["Siyah", "Üç renkli", "Altın sarısı", "Gri"],
        "Viola tricolor",
        "Hercai menekşe",
        "'Tricolor' Latince üç renkli anlamına gelir. Viola tricolor'un "
        "çiçeklerinde mor, sarı ve beyaz renkler bir arada "
        "görülebilir. Renkler taç yapraklarda farklı bölgelerde "
        "dağılarak üç renkli bir görünüm oluşturur. Tür epiteti "
        "terimle doğrudan aynıdır.",
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
        "'Versicolor' farklı renkler gösteren veya renkleri değişken "
        "olan anlamına gelir. Iris versicolor'un çiçekleri mavi-mor "
        "tonlarda olup taç yapraklarında sarı ve beyaz işaretler "
        "bulunabilir. Bu renklerin bir arada görülmesi epitetin "
        "anlamıyla uyumludur; ancak türün temel rengi çoğunlukla "
        "mavi-mor aralığındadır.",
    ),
    (
        "Coccineus",
        "Parlak kızıl veya al kırmızısı",
        ["Gri", "Parlak kızıl veya al kırmızısı", "Mavimsi yeşil", "Kahverengi"],
        "Salvia coccinea",
        "Kızıl adaçayı",
        "'Coccineus' parlak kızıl veya al kırmızısı anlamına gelir. "
        "Salvia coccinea'nın çiçekleri çoğunlukla canlı kırmızıdır; "
        "pembe ve beyaz formları da görülebilir. Tür epiteti "
        "kırmızı renk kavramını doğrudan taşır ve özellikle "
        "çiçeklerin taç yapraklarında gözlenebilir.",
    ),
    (
        "Sanguineus",
        "Kan kırmızısı",
        ["Kan kırmızısı", "Soluk sarı", "Gümüş", "Yeşil"],
        "Cornus sanguinea",
        "Kan kızılcığı",
        "'Sanguineus' kan renginde veya kan kırmızısı anlamına gelir. "
        "Cornus sanguinea'nın tür epiteti kan anlamındaki Latince "
        "'sanguis' köküyle ilişkilidir. Genç sürgünler ve özellikle "
        "güneş gören dallar sonbahar-kış döneminde kırmızımsı "
        "tonlar gösterebilir; ancak dal rengi çevre koşullarına "
        "göre değişir ve her zaman kan kırmızısı değildir.",
    ),

    # ============================================================
    # 4. AÇIK RENKLER VE RENK DEĞİŞİMLERİ
    # ============================================================
    (
        "Pallens",
        "Soluk veya solgun",
        ["Çok koyu", "Altın rengi", "Soluk veya solgun", "Bakır rengi"],
        "Carex pallescens",
        "Soluk saz",
        "'Pallens' soluk veya solgun anlamına gelir. Carex pallescens "
        "adındaki 'pallescens', soluklaşan veya soluk renkli hale "
        "gelen anlamını taşıyan aynı sözcük ailesindendir. Bu nedenle "
        "renk kökü bakımından uygundur; ancak belirli bir organın "
        "rengiyle ilgili açıklama, türün güvenilir bir floristik "
        "tanımıyla doğrulanmalıdır.",
    ),
    (
        "Rubescens",
        "Kırmızılaşan veya kızaran",
        ["Yeşile dönen", "Kırmızılaşan veya kızaran", "Beyazlaşan", "Maviye dönen"],
        "Acer rubrum",
        "Kırmızı akçaağaç",
        "'Rubescens' kızaran veya kırmızılaşan anlamına gelir. "
        "Acer rubrum'un yaprakları sonbaharda kırmızı veya turuncu "
        "kırmızı tonlara dönebilir. Bu değişim, klorofilin "
        "parçalanması ve antosiyaninlerin birikmesiyle ilişkilidir. "
        "Tür epiteti 'rubrum' kırmızı anlamına gelir ve aynı renk "
        "kökünü taşır.",
    ),
    (
        "Albicans",
        "Beyazımsı veya beyazlaşan",
        ["Siyahımsı", "Sarımsı", "Beyazımsı veya beyazlaşan", "Kızılımsı"],
        "Populus alba",
        "Ak kavak",
        "'Albicans' beyazımsı veya beyazlaşan anlamına gelir. "
        "Populus alba'nın yaprak alt yüzeyleri yoğun beyazımsı "
        "tüylerle kaplıdır ve yapraklar rüzgârda döndüğünde bu "
        "açık yüzey belirginleşir. Ancak 'alba' beyaz anlamına "
        "gelse de 'albicans' ile aynı sözcük biçimi değildir; "
        "bu seçim renk görünümüne dayalıdır.",
    ),
    (
        "Flavescens",
        "Sarılaşan veya sarımsı",
        ["Mavileşen", "Kararan", "Morlaşan", "Sarılaşan veya sarımsı"],
        "Quercus flavescens",
        "Sarılaşan meşe",
        "'Flavescens' sarılaşan veya sarımsı hale gelen anlamına gelir. "
        "Quercus flavescens epiteti aynı sarı renk kökünü taşır. "
        "Ancak bu adın kabul edilmiş bir meşe taksonuna karşılık "
        "geldiği ve sarılaşmanın hangi organında görüldüğü "
        "taksonomik ve floristik kaynaklarla doğrulanmadan "
        "kayıt kesin kabul edilmemelidir.",
    ),
    (
        "Viridescens",
        "Yeşilimsi veya yeşile dönen",
        ["Yeşilimsi veya yeşile dönen", "Kırmızılaşan", "Beyazlaşan", "Kararan"],
        "Carex viridescens",
        "Yeşilimsi saz",
        "'Viridescens' yeşilimsi veya yeşile dönen anlamına gelir. "
        "Carex viridescens epiteti doğrudan aynı renk kökünü taşır. "
        "Ancak türün geçerli adı ve yeşilimsi rengin hangi "
        "organında belirgin olduğu, güvenilir bir taksonomik "
        "kaynakla doğrulanmalıdır.",
    ),
    (
        "Obscurus",
        "Koyu, karanlık veya mat",
        ["Açık", "Parlak", "Koyu, karanlık veya mat", "Süt beyazı"],
        "Carex obscura",
        "Koyu renkli saz",
        "'Obscurus' koyu, karanlık veya belirsiz anlamlarına gelir. "
        "Carex obscura adı epitet bakımından doğrudan eşleşiyor "
        "görünse de türün taksonomik geçerliliği ve belirli "
        "organlarının koyu renkli olduğuna ilişkin kanıt "
        "doğrulanmadan bu eşleştirme bilimsel açıdan kesin "
        "kabul edilmemelidir.",
    ),
    (
        "Nitidus",
        "Parlak veya ışıldayan",
        ["Mat", "Parlak veya ışıldayan", "Soluk", "Kül grisi"],
        "Ilex aquifolium",
        "Adi çobanpüskülü",
        "'Nitidus' parlak veya ışıldayan anlamına gelir. Ilex "
        "aquifolium'un derimsi yapraklarının üst yüzeyi belirgin "
        "parlaklık gösterir. Kutikulanın ışığı yansıtması, "
        "yaprak yüzeyinin cilalı görünmesine katkıda bulunur. "
        "Tür epiteti 'aquifolium' olduğundan, bu örnek renk "
        "kökü eşleşmesine değil, görünür yüzey özelliğine dayanır.",
    ),
    (
        "Maculatus",
        "Benekli veya lekeli",
        ["Çizgili", "Düz renkli", "Benekli veya lekeli", "Şeffaf"],
        "Pulmonaria officinalis",
        "Akciğer otu",
        "'Maculatus' benekli veya lekeli anlamına gelir. Pulmonaria "
        "officinalis'in yeşil yapraklarında açık renkli benekler "
        "görülür. Bu lekeler yaprak dokusundaki pigment dağılımı "
        "ve hücresel yapı farklılıklarıyla ilişkilidir. Bununla "
        "birlikte, tür epiteti 'officinalis' olup 'maculatus' "
        "ile aynı sözcük değildir.",
    ),
    (
        "Striatus",
        "Çizgili veya şeritli",
        ["Çizgili veya şeritli", "Beyaz", "Kızıl", "Altın rengi"],
        "Iris striata",
        "Çizgili süsen",
        "'Striatus' çizgili veya şeritli anlamına gelir. Iris striata "
        "adı doğrudan çizgi anlamındaki Latince kökle ilişkilidir. "
        "Bununla birlikte, tür adının geçerliliği ve çizgilerin "
        "çiçeklerde mi yoksa yapraklarda mı görüldüğü güncel "
        "taksonomik kaynaklarla doğrulanmalıdır; yalnızca ad "
        "benzerliği morfolojik kanıt yerine geçmez.",
    ),
    (
        "Azureus",
        "Azur veya gök mavisi",
        ["Koyu kahverengi", "Azur veya gök mavisi", "Siyah", "Pembe"],
        "Salvia azurea",
        "Gök mavisi adaçayı",
        "'Azureus' azur veya gök mavisi anlamına gelir. Salvia "
        "azurea'nın çiçekleri belirgin gök mavisi tonlarındadır. "
        "Tür epiteti aynı renk kavramını doğrudan taşır. Mavi "
        "görünüm, taç yapraklardaki pigmentlerin ışıkla etkileşimi "
        "ve hücresel ortamın optik özellikleriyle oluşur.",
    ),
    (
        "Canus",
        "Beyazımsı gri veya kırçıllı",
        ["Turuncu", "Mor", "Beyazımsı gri veya kırçıllı", "Parlak kırmızı"],
        "Artemisia cana",
        "Gri yapraklı pelin",
        "'Canus' beyazımsı gri veya kırçıllı anlamına gelir. Artemisia "
        "cana'nın yaprak ve sürgünleri gri-beyazımsı tüylerle "
        "kaplı olabilir; bu örtü ışığı dağıtarak açık gri bir "
        "görünüm oluşturur. Tür epiteti aynı renk kökünü taşır, "
        "ancak belirli bir bitkideki renk yoğunluğu çevresel "
        "koşullara göre değişebilir.",
    ),
    (
        "Lividus",
        "Kurşuni, mavimsi gri veya soluk mor",
        ["Altın sarısı", "Kurşuni, mavimsi gri veya soluk mor", "Pembe", "Yeşil"],
        "Helleborus lividus",
        "Mavimsi çöpleme",
        "'Lividus' kurşuni, mavimsi gri veya soluk mor tonlarını "
        "ifade eder. Helleborus lividus'un yaprakları mavimsi-yeşil "
        "ve griye çalan tonlar gösterebilir. Bu görünüm yaprak "
        "yüzeyinin optik özellikleri ve pigment bileşimiyle "
        "ilişkilidir. Tür epiteti aynı renk sıfatını taşır.",
    ),
    (
        "Coloratus",
        "Renkli veya belirgin renk taşıyan",
        ["Renksiz", "Renkli veya belirgin renk taşıyan", "Yalnızca beyaz", "Çizgili"],
        "Rhododendron coloratum",
        "Belirgin renkli orman gülü",
        "'Coloratus' renkli veya belirgin biçimde renklendirilmiş "
        "anlamına gelir. Rhododendron coloratum epiteti renk "
        "kökünü doğrudan taşır. Bununla birlikte, bu bilimsel "
        "adın kabul edilmiş bir taksona karşılık gelip gelmediği "
        "güncel taksonomik kaynaklardan doğrulanmalıdır. Yalnızca "
        "Latince açıdan uygun görünen bir ad bilimsel doğruluk "
        "için yeterli değildir.",
    ),
    (
        "Piceus",
        "Zift siyahı veya katran rengi",
        ["Kar beyazı", "Zift siyahı veya katran rengi", "Leylak", "Gümüş"],
        "Pinus nigra",
        "Karaçam",
        "'Piceus' zift veya katran gibi koyu renkleri ifade eder. "
        "Pinus nigra'nın tür epiteti 'nigra', siyah veya çok koyu "
        "anlamına gelir; 'piceus' ile aynı sözcük değildir. Karaçamın "
        "koyu kabuğu ve koyu yeşil iğne yaprakları bu renk grubuyla "
        "kısmen ilişkilendirilebilir, ancak zift siyahı anlamı için "
        "doğrudan epitet eşleşmesi sayılmaz.",
    ),
    (
        "Dilutus",
        "Seyreltik veya soluk renkli",
        ["Çok koyu", "Seyreltik veya soluk renkli", "Parlak siyah", "Altın rengi"],
        "Gentiana diluta",
        "Soluk renkli kantaron",
        "'Dilutus' seyreltilmiş, açılmış veya yoğunluğu azaltılmış "
        "anlamına gelir. Gentiana diluta adı renk yoğunluğunun "
        "azalmasını çağrıştıran epiteti doğrudan taşır. Ancak "
        "bu adın geçerli bir tür adına karşılık gelip gelmediği "
        "ve çiçek renginin gerçekten soluk olduğu doğrulanmadan "
        "kesin botanik eşleştirme olarak kullanılmamalıdır.",
    ),
    (
        "Clarus",
        "Açık, berrak veya parlak",
        ["Açık, berrak veya parlak", "Siyah", "Koyu kahverengi", "Kırmızı"],
        "Narcissus poeticus",
        "Şair nergisi",
        "'Clarus' açık, berrak veya parlak anlamına gelir. Narcissus "
        "poeticus'un beyaz taç yaprakları ve kırmızı kenarlı sarı "
        "taç borusu belirgin renk karşıtlığı oluşturur. Bununla "
        "birlikte, tür epiteti 'poeticus' olduğundan 'clarus' ile "
        "aynı renk kökünü taşımaz; bu eşleştirme yalnızca görünür "
        "renk niteliğine dayalıdır.",
    ),
    (
        "Saturatus",
        "Doygun veya yoğun renkli",
        ["Soluk", "Doygun veya yoğun renkli", "Renksiz", "Şeffaf"],
        "Tulipa gesneriana",
        "Bahçe lalesi",
        "'Saturatus' doygun veya yoğun renkli anlamına gelir. "
        "Tulipa gesneriana'nın kültivarlarında kırmızı, mor, sarı "
        "ve turuncu gibi doygun çiçek renkleri yaygındır. Ancak "
        "tür ve kültivarlar arasında geniş renk çeşitliliği vardır; "
        "bu nedenle açıklama tek bir renge değil, doygun renkli "
        "kültivarların çiçek pigmentlerine dayanır.",
    ),
    (
        "Opacus",
        "Mat, donuk veya ışık geçirmeyen",
        ["Parlak", "Mat, donuk veya ışık geçirmeyen", "Gümüş", "Kızıl"],
        "Stachys byzantina",
        "Kuzu kulağı",
        "'Opacus' mat, donuk veya ışık geçirmeyen anlamına gelir. "
        "Stachys byzantina'nın yoğun beyazımsı tüylerle kaplı "
        "yaprakları ışığı dağınık biçimde yansıtır ve kadifemsi, "
        "mat bir görünüm oluşturur. Tür epiteti 'byzantina' "
        "olduğundan bu örnek doğrudan ad kökü eşleşmesi değildir.",
    ),
    (
        "Micans",
        "Parıldayan veya ışıltılı",
        ["Kül grisi", "Parıldayan veya ışıltılı", "Soluk", "Siyah"],
        "Tradescantia zebrina",
        "Telgraf çiçeği",
        "'Micans' parıldayan veya ışıldayan anlamına gelir. "
        "Tradescantia zebrina'nın yapraklarında gümüşi, ışığı "
        "yansıtan şeritler bulunur; bu şeritler yaprak yüzeyinin "
        "optik özellikleri nedeniyle belirgin bir ışıltı oluşturur. "
        "Ancak tür epiteti 'zebrina' olduğundan 'micans' ile "
        "aynı sözcük kökünü taşımaz.",
    ),

    # ============================================================
    # 5. SUB- ÖNEKLİ VE BENZER ANLAMLAR
    # ============================================================
    (
        "Subalbus",
        "Beyazımsı",
        ["Kırmızı", "Beyazımsı", "Siyah", "Mavi"],
        "Melilotus albus",
        "Ak kokulu yonca",
        "'Sub-' öneki yaklaşık olma veya bir niteliği daha düşük "
        "derecede taşıma anlamı katabilir; 'subalbus' bu nedenle "
        "beyazımsı olarak yorumlanır. Melilotus albus'un beyaz "
        "çiçekleri belirgin biçimde beyazdır; ancak tür epiteti "
        "'albus' doğrudan beyaz anlamına gelir ve 'subalbus' ile "
        "aynı sözcük değildir. Bu nedenle renk anlamı yakın olsa "
        "da tam epitet eşleşmesi değildir.",
    ),
    (
        "Subflavus",
        "Sarımsı",
        ["Gümüş", "Mor", "Sarımsı", "Koyu siyah"],
        "Verbascum thapsus",
        "Sığırkuyruğu",
        "'Subflavus', sarıya çalan veya sarımsı anlamında "
        "yorumlanabilir. Verbascum thapsus'un çiçekleri sarıdır, "
        "yaprakları ise yoğun tüylenme nedeniyle grimsi görünür. "
        "Bu nedenle bitki sarımsı anlamını yalnızca çiçekleri "
        "üzerinden kısmen karşılar; tür epiteti 'thapsus' olduğundan "
        "doğrudan renk kökü eşleşmesi değildir.",
    ),
    (
        "Subrubens",
        "Kırmızımsı",
        ["Kırmızımsı", "Mavimsi", "Yeşilimsi", "Beyazımsı"],
        "Silene rubella",
        "Kırmızımsı nakıl",
        "'Subrubens' kırmızımsı veya hafifçe kızaran anlamında "
        "yorumlanabilir. Silene rubella adındaki 'rubella', "
        "kırmızı anlamındaki 'ruber' sözcük ailesiyle ilişkilidir. "
        "Bununla birlikte, bu türün çiçeklerinin renk tonu ve "
        "taksonomik geçerliliği güvenilir kaynaklarla doğrulanmadan "
        "kesin bir renk örneği olarak kullanılmamalıdır.",
    ),
    (
        "Subviridis",
        "Yeşilimsi",
        ["Kızıl", "Gümüş", "Yeşilimsi", "Siyah"],
        "Amaranthus viridis",
        "Yeşil amarant",
        "'Subviridis' yeşilimsi veya tam doygun olmayan yeşil "
        "anlamında yorumlanabilir. Amaranthus viridis'in yaprakları "
        "yeşildir; ancak tür epiteti 'viridis' doğrudan yeşil "
        "anlamına gelir ve 'subviridis' ile aynı sözcük değildir. "
        "Yapraklardaki yeşil görünüm klorofil pigmentlerinden "
        "kaynaklanır; bu örnek yaklaşık yeşil tonunu tek başına "
        "kanıtlamaz.",
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
