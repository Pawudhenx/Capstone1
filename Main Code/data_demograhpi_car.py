import pandas as pd
import numpy as np
import os

# =============== 1. EXTRACT DATA ===============
def extract_data(path: str, delete_index: bool = True) -> pd.DataFrame:
    """
    Membaca CSV ke DataFrame.
    Parameters:
        path (str) : lokasi file CSV
        delete_index (bool) : hapus kolom index jika ada
    Returns:
        pd.DataFrame
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File tidak ditemukan di path: {path}")

    df = pd.read_csv(path)
    if delete_index and 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    print(f"✅ File berhasil dibaca dari: {path}")
    return df


# =============== 2. DATA DEMOGRAFI ===============
def data_demographi(df: pd.DataFrame):
    """
    Menampilkan analisis demografi dataset produk.
    """
    print("\n===== 📊 DATA DEMOGRAFI PRODUK =====")

    # --- Struktur Data
    print(f"\nJumlah baris : {df.shape[0]}")
    print(f"Jumlah kolom : {df.shape[1]}")
    print("\nTipe Data per Kolom:")
    print(df.dtypes)
    
    # --- Missing Values
    print("\n--- Missing Value per Kolom ---")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.sum() > 0 else "Tidak ada missing values ✅")

    # --- Distribusi Kategori
    if 'main_category' in df.columns:
        print("\n--- Jumlah Produk per Main Category ---")
        print(df['main_category'].value_counts())

    if 'sub_category' in df.columns:
        print("\n--- Jumlah Produk per Sub Category (Top 10) ---")
        print(df['sub_category'].value_counts().head(10))

    # --- Statistik Rating
    if 'ratings' in df.columns:
        print("\n--- Statistik Rating ---")
        avg_rating = df['ratings'].mean()
        print(f"📈 Rata-rata rating keseluruhan: {avg_rating:.2f}")

    if 'no_of_ratings' in df.columns:
        avg_reviews = df['no_of_ratings'].mean()
        print(f"💬 Rata-rata jumlah review per produk: {avg_reviews:.0f}")

    # --- Statistik Harga & Diskon
    # --- Hitung Persentase Diskon & Tambahkan Kolom Baru ---
    if 'discount_price(Rupee)' in df.columns and 'actual_price(Rupee)' in df.columns:
        # Buat kolom persentase diskon baru
        df['discount_percent'] = np.where(
            (df['actual_price(Rupee)'] > 0) & (df['discount_price(Rupee)'] <= df['actual_price(Rupee)']),
            100 * (df['actual_price(Rupee)'] - df['discount_price(Rupee)']) / df['actual_price(Rupee)'],
            np.nan  # hindari pembagian 0 atau data tidak logis
        )

        # Bersihkan nilai aneh (misal negatif atau lebih dari 100%)
        df.loc[(df['discount_percent'] < 0) | (df['discount_percent'] > 100), 'discount_percent'] = np.nan

        avg_discount = df['discount_percent'].mean()
        print(f"💸 Rata-rata diskon produk: {avg_discount:.2f}%")

    # --- Hitung Persentase Diskon & Cari Produk Diskon Terbesar ---
    if 'discount_price(Rupee)' in df.columns and 'actual_price(Rupee)' in df.columns:
        # Hitung persentase diskon
        df['discount_percent'] = np.where(
            (df['actual_price(Rupee)'] > 0) & (df['discount_price(Rupee)'] <= df['actual_price(Rupee)']),
            100 * (df['actual_price(Rupee)'] - df['discount_price(Rupee)']) / df['actual_price(Rupee)'],
            np.nan
        )

        # Bersihkan nilai yang tidak logis (negatif atau >100%)
        df.loc[(df['discount_percent'] < 0) | (df['discount_percent'] > 100), 'discount_percent'] = np.nan



        # Produk dengan diskon terbesar
        print("\n💸 Top 5 Produk dengan Diskon Terbesar ---")
        top_discount = (
            df[['name', 'main_category', 'discount_price(Rupee)', 'actual_price(Rupee)', 'discount_percent']]
            .sort_values(by='discount_percent', ascending=False)
            .head(5)
        )
        print(top_discount.to_string(index=False))

    # --- Top 5 Produk Berdasarkan Rating
    if {'name', 'ratings'}.issubset(df.columns):
        print("\n--- Top 5 Produk dengan Rating Tertinggi ---")
        top_rated = df.sort_values(by='ratings', ascending=False).head(5)
        print(top_rated[['name', 'ratings', 'no_of_ratings']])

    # --- Validasi Data
    print("\n--- Validasi & Anomali ---")
    if 'actual_price(Rupee)' in df.columns:
        zero_price = (df['actual_price(Rupee)'] <= 0).sum()
        print(f"Produk dengan harga 0 atau negatif: {zero_price}")

    if 'name' in df.columns:
        duplicate_names = df['name'].duplicated().sum()
        print(f"Duplikasi nama produk: {duplicate_names}")

    print("\n--- Contoh Data ---")
    print(df.head(3))


# =============== 3. MAIN PROGRAM ===============
if __name__ == "__main__":
    # Lokasi file hasil cleaning
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "../Cleaned Data/CarParts_Clean.csv")

    # Extract data
    df = extract_data(file_path)

    # Analisis demografi
    data_demographi(df)
