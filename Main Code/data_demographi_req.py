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
        raise FileNotFoundError(f"File tidak ditemukan di path: {path}")

    df = pd.read_csv(path)
    if delete_index and 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    print(f"File berhasil dibaca dari: {path}")
    return df


# =============== 2. DATA DEMOGRAFI ===============
def data_demographi(df: pd.DataFrame):
    """
    Analisis demografi dataset perusahaan & pekerjaan.
    """
    print("=== DEMOGRAFI DATA PERUSAHAAN ===")
    print(f"Jumlah baris: {df.shape[0]}")
    print(f"Jumlah kolom: {df.shape[1]}")

    print("\n--- Missing Values ---")
    print(df.isnull().sum())

    # --- Statistik Rating Perusahaan ---
    if 'company_rating' in df.columns:
        df['company_rating'] = pd.to_numeric(df['company_rating'], errors='coerce')
        # Top 5 perusahaan dengan rating tertinggi
        top_rated = df[['company', 'company_rating']].dropna().sort_values(by='company_rating', ascending=False).head(5)
        print("Top 5 Perusahaan dengan Rating Tertinggi:")
        print(top_rated.to_string(index=False))

    # --- Distribusi Lokasi ---
    if 'location' in df.columns:
        print("\n--- 5 Lokasi dengan Jumlah Lowongan Terbanyak ---")
        print(df['location'].value_counts().head(5))

    # --- Industri Perusahaan ---
    if 'company_industry' in df.columns:
        print("--- 5 Industri Perusahaan Terbanyak ---")
        print(df['company_industry'].value_counts().head(5))

    # --- Tahun Berdiri Perusahaan ---
    if 'company_founded' in df.columns:
        df['company_founded'] = pd.to_numeric(df['company_founded'], errors='coerce')
        valid_founded = df.loc[df['company_founded'].between(1800, 2025), 'company_founded']
        oldest = valid_founded.min()
        newest = valid_founded.max()
        print(f"Perusahaan tertua berdiri tahun {oldest:.0f}, termuda tahun {newest:.0f}")

    # --- Pendapatan Perusahaan ---
    if 'company_revenue' in df.columns:
        print("\n--- Distribusi Pendapatan Perusahaan ---")
        print(df['company_revenue'].value_counts().head(5))


# =============== 3. MAIN PROGRAM ===============
if __name__ == "__main__":
    # Lokasi file hasil cleaning
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "../Cleaned Data/requirements_clean.csv")

    # Extract data
    df = extract_data(file_path)

    # Analisis demografi
    data_demographi(df)
