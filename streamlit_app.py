import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(
    page_title="Botanik Latince Öğrenme",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 Botanik Latince Öğrenme")
st.write("Latince bitki terimlerini öğren, bilgini test et!")

st.divider()

# CSV dosyasını yükle
uploaded_file = st.file_uploader(
    "📂 CSV dosyanızı yükleyin",
    type=["csv"]
)

# CSV dosyasını oku
if uploaded_file is not None:
    try:
        df = pd.read_csv(
            uploaded_file,
            encoding="utf-8-sig"
        )
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        df = pd.read_csv(
            uploaded_file,
            encoding="latin-1"
        )
    except Exception as e:
        st.error(f"CSV dosyası okunamadı: {e}")
        st.stop()

else:
    st.info("Lütfen botanical_terms.csv dosyasını yükleyin.")
    st.stop()

# Gerekli sütunları kontrol et
required_columns = [
    "latin",
    "answer",
    "options",
    "plant",
    "plant_name",
    "explanation"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "CSV dosyasında eksik sütunlar var: "
        + ", ".join(missing_columns)
    )
    st.stop()

# Boş satırları temizle
df = df.dropna(subset=["latin", "answer"])

# Sayısal özetler
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Toplam Terim", len(df))

with col2:
    st.metric("Farklı Bitki", df["plant"].nunique())

with col3:
    st.metric("Açıklamalar", df["explanation"].notna().sum())

st.divider()

# Arama alanı
st.subheader("🔎 Terim Ara")

search = st.text_input(
    "Latince terim, Türkçe anlam veya bitki adı yazın"
)

filtered_df = df.copy()

if search:
    mask = filtered_df[
        [
            "latin",
            "answer",
            "plant",
            "plant_name",
            "explanation"
        ]
    ].fillna("").astype(str).apply(
        lambda column: column.str.contains(
            search,
            case=False,
            regex=False
        )
    ).any(axis=1)

    filtered_df = filtered_df[mask]

st.caption(f"{len(filtered_df)} kayıt bulundu.")

# Görüntülenecek sütunlar
display_columns = [
    "latin",
    "answer",
    "options",
    "plant",
    "plant_name",
    "explanation"
]

# Tablo
st.subheader("📚 Botanik Terimleri Tablosu")

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True,
    column_config={
        "latin": st.column_config.TextColumn(
            "Latince Terim",
            width="medium"
        ),
        "answer": st.column_config.TextColumn(
            "Türkçe Anlam",
            width="medium"
        ),
        "options": st.column_config.TextColumn(
            "Seçenekler",
            width="large"
        ),
        "plant": st.column_config.TextColumn(
            "Bilimsel Bitki Adı",
            width="medium"
        ),
        "plant_name": st.column_config.TextColumn(
            "Bitkinin Türkçe Adı",
            width="medium"
        ),
        "explanation": st.column_config.TextColumn(
            "Açıklama",
            width="large"
        )
    }
)

st.divider()

# Terim ayrıntıları
st.subheader("🌱 Terim Ayrıntıları")

if not filtered_df.empty:
    selected_term = st.selectbox(
        "Bir Latince terim seçin",
        filtered_df["latin"].tolist()
    )

    selected_row = filtered_df[
        filtered_df["latin"] == selected_term
    ].iloc[0]

    st.markdown(f"### {selected_row['latin']}")

    st.success(f"**Anlamı:** {selected_row['answer']}")

    st.markdown(
        f"**Bilimsel bitki adı:** "
        f"{selected_row['plant']}"
    )

    st.markdown(
        f"**Türkçe bitki adı:** "
        f"{selected_row['plant_name']}"
    )

    st.info(
        f"**Açıklama:** {selected_row['explanation']}"
    )

    st.markdown(
        f"**Cevap seçenekleri:** {selected_row['options']}"
    )
else:
    st.warning("Aramanızla eşleşen terim bulunamadı.")

st.divider()

# CSV indirme
csv_data = filtered_df[display_columns].to_csv(
    index=False,
    encoding="utf-8-sig"
)

st.download_button(
    label="⬇️ Filtrelenmiş tabloyu CSV olarak indir",
    data=csv_data,
    file_name="botanical_terms_filtered.csv",
    mime="text/csv"
)

st.caption("🌿 Botanik Latince Öğrenme")
