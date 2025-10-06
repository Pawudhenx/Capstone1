import pandas as pd
import os

# === 1. SETUP PATH OTOMATIS ===
# Cari folder base di mana file .py ini berada
base_dir = os.path.dirname(os.path.abspath(__file__))

# Path otomatis ke file input & output
input_path = os.path.join(base_dir, "../Raw Data/Car Parts.csv")
output_path = os.path.join(base_dir, "../Cleaned Data/CarParts_Clean.csv")

# Buat folder output kalau belum ada
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# === 2. EXTRACT DATA ===
if os.path.exists(input_path):
    df = pd.read_csv(input_path)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    print("✅ File ditemukan dan berhasil dibaca.")
else:
    raise FileNotFoundError(f"❌ File tidak ditemukan di: {input_path}")

# === 3. TRANSFORM DATA ===

# --- ratings ---
if 'ratings' in df.columns:
    df['ratings'] = (
        df['ratings'].astype(str)
        .str.replace(',', '.', regex=False)
        .pipe(pd.to_numeric, errors='coerce')
    )

# --- no_of_ratings ---
if 'no_of_ratings' in df.columns:
    df['no_of_ratings'] = (
        df['no_of_ratings']
        .astype(str)
        .str.replace(',', '', regex=True)
        .pipe(pd.to_numeric, errors='coerce')
        .astype('Int64')
    )

# --- rename kolom harga ---
rename_map = {
    'discount_price': 'discount_price(Rupee)',
    'actual_price': 'actual_price(Rupee)'
}
df.rename(columns=rename_map, inplace=True)

# --- bersihkan simbol ₹ dan koma ---
for col in rename_map.values():
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace('[₹,]', '', regex=True)
            .pipe(pd.to_numeric, errors='coerce')
        )

# === 4. SIMPAN DAN TAMPILKAN HASIL ===
df.to_csv(output_path, index=False)

print(f"\n✅ Data berhasil dibersihkan dan disimpan ke:\n{output_path}")

# Tampilkan ringkasan hasil
print("\n===== INFORMASI DATA CLEANED =====")
print(df.info())

print("\n===== 5 BARIS PERTAMA HASIL CLEANING =====")
print(df.head())