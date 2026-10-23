from pathlib import Path
import html

import pandas as pd
import streamlit as st


# ==================================================
# 1. SAYFA AYARLARI
# ==================================================

st.set_page_config(
    page_title="Latince Botanik Terimleri",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# 2. DOSYA YOLLARI
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

CSV_FILE = BASE_DIR / "botanical_terms.csv"
CSS_FILE = BASE_DIR / "style.css"


# ==================================================
# 3. CSS YÜKLEME
# ==================================================

DEFAULT_CSS = """
<style>
.stApp {
    background-color: #111827;
    color: #F9FAFB;
}

[data-testid="stAppViewContainer"] {
    background-color: #111827;
}

[data-testid="stHeader"] {
    background-color: #111827;
}

.main .block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: #FFFFFF !important;
}

p, label, li, span {
    color: #F3F4F6;
}

.detail-card {
    background-color: #1F2937;
    color: #F9FAFB;
    border: 1px solid #4B5563;
    border-left: 5px solid #22C55E;
    border-radius: 12px;
    padding: 22px;
    margin: 12px 0;
    overflow-wrap: anywhere;
}

.detail-card p {
    color: #F9FAFB !important;
    font-size: 16px;
    line-height: 1.9;
}

.plant-name {
    color: #86EFAC !important;
    font-weight: bold;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #475569;
    border-radius: 8px;
}

.stButton > button {
    background-color: #15803D !important;
    color: #FFFFFF !important;
    border: 1px solid #22C55E !important;
    border-radius: 8px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #166534 !important;
}

input, textarea {
    color: #FFFFFF !important;
    background-color: #1F2937 !important;
}

@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem;
    }

    .detail-card {
        padding: 14px;
    }
}
</style>
"""


def load_css():
    """Harici CSS varsa yükle; yoksa varsayılan stili kullan."""
    try:
        if CSS_FILE.exists():
            css = CSS_FILE.read_text(encoding="utf-8")
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        else:
            st.markdown(DEFAULT_CSS, unsafe_allow_html=True)
    except Exception:
        st.markdown(DEFAULT_CSS, unsafe_allow_html=True)


load_css()


# ==================================================
# 4. CSV DOSYASINI GÜVENLİ OKU
# ==================================================

@st.cache_data
def load_data(file_path, modified_time):
    """CSV dosyasını okur ve sütun isimlerini standartlaştırır."""
    del modified_time

    # Önce UTF-8, sonra Türkçe Windows kodlamasını dene.
    errors = []

    for encoding in ("utf-8-sig", "utf-8", "cp1254", "latin1"):
        try:
            data = pd.read_csv(
                file_path,
                encoding=encoding,
                sep=None,
                engine="python",
                on_bad_lines="warn",
            )

            data.columns = [
                str(column).strip().replace("\ufeff", "")
                for column in data.columns
            ]

            if len(data.columns) < 2:
                raise ValueError("CSV dosyasında yeterli sütun bulunamadı.")

            return data

        except Exception as exc:
            errors.append(f"{encoding}: {exc}")

    raise ValueError(
        "CSV dosyası okunamadı.\n" + "\n".join(errors)
    )


if not CSV_FILE.exists():
    st.error("❌ botanical_terms.csv dosyası bulunamadı.")

    st.info(
        "Lütfen botanical_terms.csv dosyasını app.py ile "
        "aynı klasöre yükleyin."
    )

    st.code(
        "latince/\n"
        "├── app.py\n"
        "├── style.css\n"
        "└── botanical_terms.csv"
    )

    st.stop()


try:
    df = load_data(
        str(CSV_FILE),
        CSV_FILE.stat().st_mtime,
    )

except Exception as exc:
    st.error("CSV dosyası yüklenirken bir sorun oluştu.")
    st.code(str(exc))
    st.stop()


# ==================================================
# 5. SÜTUN İSİMLERİNİ EŞLEŞTİR
# ==================================================

COLUMN_ALIASES = {
    "latin": [
        "latin", "latince", "terim", "term"
    ],
    "answer": [
        "answer", "anlamı", "anlami", "anlam"
    ],
    "options": [
        "options", "seçenekler", "secenekler", "seçenek"
    ],
    "plant": [
        "plant", "bilimsel bitki adı",
        "bilimsel bitki adi", "scientific_name"
    ],
    "plant_name": [
        "plant_name", "türkçe bitki adı",
        "turkce bitki adi", "bitki adı", "bitki adi"
    ],
    "explanation": [
        "explanation", "açıklama", "aciklama", "description"
    ],
}


def normalize_column_name(value):
    value = str(value).strip().casefold()

    replacements = {
        "ı": "i",
        "İ": "i",
        "ş": "s",
        "ğ": "g",
        "ü": "u",
        "ö": "o",
        "ç": "c",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    return value


column_lookup = {
    normalize_column_name(column): column
    for column in df.columns
}

renames = {}

for target, aliases in COLUMN_ALIASES.items():
    for alias in aliases:
        normalized_alias = normalize_column_name(alias)

        if normalized_alias in column_lookup:
            renames[column_lookup[normalized_alias]] = target
            break

df = df.rename(columns=renames)

REQUIRED_COLUMNS = [
    "latin",
    "answer",
    "options",
    "plant",
    "plant_name",
    "explanation",
]

missing_columns = [
    column
    for column in REQUIRED_COLUMNS
    if column not in df.columns
]

if missing_columns:
    st.error("CSV dosyasında gerekli sütunlar bulunamadı.")

    st.write("Eksik sütunlar:", ", ".join(missing_columns))
    st.write("Bulunan sütunlar:", list(df.columns))

    st.info(
        "Sütun adları Latince, Anlamı, Seçenekler, "
        "Bilimsel Bitki Adı, Türkçe Bitki Adı ve Açıklama "
        "veya bunların İngilizce karşılıkları olabilir."
    )

    st.stop()


# ==================================================
# 6. VERİLERİ TEMİZLE
# ==================================================

df = df[REQUIRED_COLUMNS].copy()

for column in REQUIRED_COLUMNS:
    df[column] = df[column].fillna("").astype(str).str.strip()

df = df[df["latin"] != ""].reset_index(drop=True)

if df.empty:
    st.warning("CSV dosyasında gösterilecek terim bulunamadı.")
    st.stop()


# ==================================================
# 7. BAŞLIK
# ==================================================

st.title("🌿 Latince Botanik Terimleri")

st.markdown(
    "Botanikte kullanılan Latince terimleri keşfedin, "
    "anlamlarını öğrenin ve örnek bitkileri inceleyin."
)

st.caption(f"📚 Toplam {len(df)} terim")


# ==================================================
# 8. ARAMA VE FİLTRELEME
# ==================================================

st.sidebar.header("🔎 Terim Ara")

search = st.sidebar.text_input(
    "Latince terim, anlam veya bitki adı",
    placeholder="Örn. Hirsutus",
)

filtered_df = df.copy()

if search.strip():
    query = search.strip().casefold()

    searchable_columns = [
        "latin",
        "answer",
        "plant",
        "plant_name",
        "explanation",
    ]

    mask = pd.Series(False, index=filtered_df.index)

    for column in searchable_columns:
        mask |= filtered_df[column].str.casefold().str.contains(
            query,
            regex=False,
            na=False,
        )

    filtered_df = filtered_df[mask]


if filtered_df.empty:
    st.warning("Aramanızla eşleşen terim bulunamadı.")
    st.stop()


# ==================================================
# 9. TABLO
# ==================================================

st.subheader("📋 Terim Tablosu")

show_table = st.checkbox(
    "Tabloyu göster",
    value=True,
)

if show_table:
    table = filtered_df.rename(
        columns={
            "latin": "Latince",
            "answer": "Anlamı",
            "options": "Seçenekler",
            "plant": "Bilimsel Bitki Adı",
            "plant_name": "Türkçe Bitki Adı",
            "explanation": "Açıklama",
        }
    )

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        height=350,
    )

    csv_bytes = table.to_csv(
        index=False,
        sep=";",
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Tabloyu indir",
        data=csv_bytes,
        file_name="botanical_terms_export.csv",
        mime="text/csv",
    )


# ==================================================
# 10. TERİM SEÇİMİ
# ==================================================

st.divider()

st.subheader("📚 Detaylı Açıklama")

selected_term = st.selectbox(
    "İncelemek istediğiniz terimi seçin:",
    options=filtered_df["latin"].tolist(),
)

matches = filtered_df[
    filtered_df["latin"] == selected_term
]

if matches.empty:
    st.warning("Seçilen terim bulunamadı.")
    st.stop()

row = matches.iloc[0]


def safe_text(value):
    """HTML içeriği olarak yorumlanmasını önler."""
    return html.escape(str(value))

File "/mount/src/latince/streamlit_app.py", line 486
      # Virg
            ^
IndentationError: expected an indented block after 'if' statement on line 485
