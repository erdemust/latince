from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
input_file = BASE_DIR / "botanical_terms.csv"

if not input_file.exists():
    st.error(f"CSV dosyası bulunamadı: {input_file}")
    st.stop()

df = pd.read_csv(
    input_file,
    encoding="utf-8-sig",
    dtype=str
).fillna("")

st.title("🌿 Latince Bitki Terimleri")
st.dataframe(df, use_container_width=True, hide_index=True)
