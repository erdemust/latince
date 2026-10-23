import pandas as pd

input_file = "bitki_terimleri.csv"
output_file = "bitki_terimleri_duzenlenmis.csv"

# CSV dosyasını oku
df = pd.read_csv(input_file, encoding="utf-8-sig")

# Yalnızca belirtilen sütunlardaki virgülleri | ile değiştir
columns_to_update = ["options", "explanation"]

for column in columns_to_update:
    df[column] = df[column].str.replace(",", "|", regex=False)

# Yeni CSV dosyasını kaydet
df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(f"İşlem tamamlandı: {output_file}")
