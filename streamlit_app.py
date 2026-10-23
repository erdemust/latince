from pathlib import Path

import pandas as pd
import streamlit as st

# Uygulama yapılandırması
st.set_page_config(
    page_title="Latince Botanik Terimleri",
    page_icon="🌿",
    layout="wide",
)

# Proje klasörü
BASE_DIR = Path(__file__).resolve().parent

# CSS dosyasını yükle
css_file = BASE_DIR / "style.css"

if css_file.exists():
    css = css_file.read_text(encoding="utf-8")
    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )
else:
    st.warning("style.css dosyası bulunamadı.")

# CSV dosyasını yükle
csv_file = BASE_DIR / "botanical_terms.csv"

try:
    df = pd.read_csv(csv_file, encoding="utf-8-sig")
except FileNotFoundError:
    st.error(
        "botanical_terms.csv dosyası bulunamadı. "
        "CSV dosyasını streamlit_app.py ile aynı klasöre koyun."
    )
    st.stop()

# Başlık
st.title("🌿 Latince Botanik Terimleri")
st.caption("Botanik terimlerini keşfet ve anlamlarını öğren.")

# Arama
search = st.text_input(
    "🔎 Terim, bitki adı veya anlam ara",
    placeholder="Örneğin: Saturatus, Rosa veya yoğun renkli",
)

# Arama işlemi
if search.strip():
    mask = df.astype(str).apply(
        lambda column: column.str.contains(
            search.strip(),
            case=False,
            na=False,
            regex=False,
        )
    ).any(axis=1)

    filtered_df = df[mask]
else:
    filtered_df = df

# Tablo
st.subheader("📋 Botanik Terimleri Tablosu")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
)

# Detaylı açıklama
st.subheader("📚 Detaylı Açıklama")

if filtered_df.empty:
    st.info("Aramanızla eşleşen bir terim bulunamadı.")
else:
    selected_term = st.selectbox(
        "Açıklamasını görmek istediğiniz terimi seçin:",
        filtered_df["latin"].tolist(),
    )

    selected_row = df.loc[
        df["latin"] == selected_term
    ].iloc[0]

    plant = selected_row["plant"]
    plant_name = selected_row["plant_name"]
    explanation = selected_row["explanation"]

    st.markdown(
        f"""
        <div class="detail-card">
            <h3>🌱 {selected_term}</h3>
            <p>
                <strong>Örnek Bitki:</strong>
                <span class="plant-name">{plant}</span>
                ({plant_name})
            </p>
            <p>
                <strong>Açıklama:</strong><br>
                {explanation}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
