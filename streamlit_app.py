from pathlib import Path
import html

import pandas as pd
import streamlit as st


# ==========================================
# 1. SAYFA AYARLARI
# ==========================================

st.set_page_config(
    page_title="Latince Botanik Terimleri",
    page_icon="🌿",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "botanical_terms.csv"
CSS_FILE = BASE_DIR / "style.css"


# ==========================================
# 2. CSS YÜKLEME
# CSS yoksa uygulama çalışmaya devam eder.
# ==========================================

if CSS_FILE.exists():
    try:
        css = CSS_FILE.read_text(encoding="utf-8")
        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True,
        )
    except OSError:
        pass


# ==========================================
# 3. CSV DOSYASINI YÜKLEME
# ==========================================

if not CSV_FILE.exists():
    st.error("botanical_terms.csv dosyası bulunamadı.")
    st.info(
        "CSV dosyasını app.py dosyasıyla aynı "
        "klasöre yükleyin."
    )
    st.stop()

try:
    df = pd.read_csv(
        CSV_FILE,
        encoding="utf-8-sig",
        sep=",",
        quotechar='"',
        on_bad_lines="error",
    )

except Exception as exc:
    st.error("CSV dosyası okunamadı.")
    st.caption(f"Hata türü: {type(exc).__name__}")
    st.stop()


# ==========================================
# 4. SÜTUNLARI KONTROL ETME
# ==========================================

required_columns = [
    "latin",
    "answer",
    "options",
    "plant",
    "plant_name",
    "explanation",
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "CSV dosyasında gerekli sütunlar eksik: "
        + ", ".join(missing_columns)
    )
    st.caption(
        "Beklenen sütunlar: "
        + ", ".join(required_columns)
    )
    st.stop()

df = df[required_columns].fillna("")

df["latin"] = df["latin"].astype(str).str.strip()

df = df[df["latin"] != ""]

if df.empty:
    st.warning("CSV dosyasında gösterilecek veri bulunamadı.")
    st.stop()


# ==========================================
# 5. BAŞLIK
# ==========================================

st.title("🌿 Latince Botanik Terimleri")

st.caption(
    f"Botanik terimlerini keşfet, anlamlarını öğren. "
    f"Toplam {len(df)} terim."
)


# ==========================================
# 6. ARAMA
# ==========================================

search = st.text_input(
    "🔎 Terim veya bitki ara",
    placeholder="Örnek: Saturatus, Rosa, kırmızı...",
)

if search.strip():
    search_mask = df.apply(
        lambda column: column.astype(str).str.contains(
            search.strip(),
            case=False,
            regex=False,
            na=False,
        )
    ).any(axis=1)

    filtered_df = df[search_mask].copy()

else:
    filtered_df = df.copy()


# ==========================================
# 7. TABLO
# ==========================================

st.subheader("📋 Terim Tablosu")

if filtered_df.empty:
    st.warning("Aramanızla eşleşen bir terim bulunamadı.")
    st.stop()

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "latin": st.column_config.TextColumn(
            "Latince",
            help="Latince botanik terimi",
        ),
        "answer": st.column_config.TextColumn(
            "Anlamı",
        ),
        "options": st.column_config.TextColumn(
            "Seçenekler",
        ),
        "plant": st.column_config.TextColumn(
            "Bilimsel Bitki Adı",
        ),
        "plant_name": st.column_config.TextColumn(
            "Türkçe Bitki Adı",
        ),
        "explanation": st.column_config.TextColumn(
            "Açıklama",
        ),
    },
)


# ==========================================
# 8. DETAYLI AÇIKLAMA
# ==========================================

st.subheader("📚 Detaylı Açıklama")

terms = filtered_df["latin"].tolist()

selected_term = st.selectbox(
    "Bir terim seçin:",
    options=terms,
    key="selected_latin_term",
)

selected_rows = df[df["latin"] == selected_term]

if not selected_rows.empty:
    row = selected_rows.iloc[0]

    plant = html.escape(str(row["plant"]))
    plant_name = html.escape(str(row["plant_name"]))
    latin = html.escape(str(row["latin"]))
    answer = html.escape(str(row["answer"]))
    explanation = html.escape(str(row["explanation"]))

    st.markdown(
        f"""
        <div style="
            background-color: #1E293B;
            color: #F1F5F9;
            border: 1px solid #475569;
            border-left: 5px solid #38BDF8;
            border-radius: 10px;
            padding: 22px;
            margin-top: 12px;
            line-height: 1.8;
        ">
            <h3 style="
                color: #7DD3FC;
                margin-top: 0;
            ">
                🌱 {latin}
            </h3>

            <p style="color: #F1F5F9;">
                <strong style="color: #FFFFFF;">
                    Anlamı:
                </strong>
                {answer}
            </p>

            <p style="color: #F1F5F9;">
                <strong style="color: #FFFFFF;">
                    Örnek Bitki:
                </strong>
                <span style="color: #86EFAC;">
                    {plant}
                </span>
                ({plant_name})
            </p>

            <hr style="border-color: #475569;">

            <p style="
                color: #F1F5F9;
                white-space: pre-wrap;
            ">
                <strong style="color: #7DD3FC;">
                    📖 Açıklama
                </strong>
                <br>
                {explanation}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# 9. ALT BİLGİ
# ==========================================

st.divider()

st.caption(
    "🌿 Latince Botanik Terimleri | "
    "Veriler botanical_terms.csv dosyasından yüklenir."
)
