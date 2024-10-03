import numpy as np
from sklearn.linear_model import LinearRegression

# Data
X = np.array([50, 60, 70, 80, 90]).reshape(-1, 1)  # Luas rumah dalam m²
Y = np.array([300, 350, 400, 450, 500])            # Harga rumah dalam juta IDR

# Membuat model regresi linear
model = LinearRegression()
model.fit(X, Y)

# Fungsi untuk memprediksi harga rumah berdasarkan luas
def prediksi_harga(luas):
    harga = model.predict(np.array([[luas]]))  # Memasukkan luas ke dalam model
    return harga[0]  # Mengembalikan harga yang diprediksi

# Input dari pengguna
try:
    luas_input = float(input("Masukkan luas rumah dalam m²: "))
    harga_prediksi = prediksi_harga(luas_input)
    print(f"Harga yang diprediksi untuk rumah seluas {luas_input} m² adalah {harga_prediksi:.2f} juta IDR.")
except ValueError:
    print("Input tidak valid. Silakan masukkan angka yang benar.")
