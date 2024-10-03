import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Membaca data dari file Excel
file_path = 'data_atm.xlsx'  # Ganti dengan path file Excel-mu
df = pd.read_excel(file_path)

# Pastikan kolomnya sesuai, misalnya 'tanggal' dan 'saldo'
df['tanggal'] = pd.to_datetime(df['tanggal'])  # Konversi kolom tanggal ke datetime
df = df.rename(columns={'tanggal': 'ds', 'saldo': 'y'})  # Sesuaikan dengan format Prophet

# Membuat model Prophet
model = Prophet()
model.fit(df)

# Memprediksi 15 hari ke depan
future = model.make_future_dataframe(periods=15)
forecast = model.predict(future)

# Menentukan kapan saldo mencapai 20% dari 800 juta (yaitu 160 juta)
threshold = 160
forecast_below_threshold = forecast[forecast['yhat'] <= threshold]

# Plot hasil prediksi
plt.figure(figsize=(10, 6))
plt.plot(df['ds'], df['y'], label='Saldo Aktual')
plt.plot(forecast['ds'], forecast['yhat'], label='Prediksi Saldo', linestyle='dashed')
plt.axhline(y=threshold, color='r', linestyle='--', label='Batas 20%')
plt.xlabel('Tanggal')
plt.ylabel('Saldo (Juta)')
plt.title('Prediksi Saldo ATM')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Menampilkan tanggal kapan saldo diprediksi mencapai atau di bawah 160 juta
if not forecast_below_threshold.empty:
    print("Saldo ATM diprediksi mencapai atau di bawah 160 juta pada tanggal berikut:")
    print(forecast_below_threshold[['ds', 'yhat']])
else:
    print("Saldo ATM tidak diprediksi mencapai 160 juta dalam periode prediksi.")
