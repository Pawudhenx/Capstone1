import pandas as pd
import os

# 1. SETUP PATH OTOMATIS
# Cari folder base di mana file .py ini berada
base_dir = os.path.dirname(os.path.abspath(__file__))

# Path otomatis ke file input & output
input_path = os.path.join(base_dir, "../Raw Data/data_requirements.csv")
output_path = os.path.join(base_dir, "../Cleaned Data/requirements_clean.csv")

# Buat folder output kalau belum ada
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# === 2. EXTRACT DATA ===
if os.path.exists(input_path):
    df = pd.read_csv(input_path)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    print("File ditemukan dan berhasil dibaca.")
else:
    raise FileNotFoundError(f"File tidak ditemukan di: {input_path}")

# 3. TRANSFORM DATA

df['company_founded'] = pd.to_numeric(df['company_founded'], errors='coerce').astype('Int64')

df['dates'] = pd.to_datetime(df['dates'], errors='coerce', utc=True)
df['dates'] = df['dates'].dt.tz_convert('Asia/Jakarta')

# 4. SIMPAN DAN TAMPILKAN HASIL
df.to_csv(output_path, index=False)

print(f"Data berhasil dibersihkan dan disimpan ke:\n{output_path}")

# Tampilkan ringkasan hasil
print("\n===== INFORMASI DATA CLEANED =====")
print(df.info())

print("\n===== 5 BARIS PERTAMA HASIL CLEANING =====")
print(df.head())