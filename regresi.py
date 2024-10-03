import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Data
X = np.array([50, 60, 70, 80, 90]).reshape(-1, 1)  # Luas
Y = np.array([300, 350, 400, 450, 500])            # Harga

# Membuat model regresi linear
model = LinearRegression()
model.fit(X, Y)

# Koefisien
b0 = model.intercept_
b1 = model.coef_[0]

print(f"Intersep (b0): {b0}")
print(f"Koefisien (b1): {b1}")

# Membuat prediksi
prediksi = model.predict(X)

# Visualisasi
plt.scatter(X, Y, color='blue', label='Data Asli')
plt.plot(X, prediksi, color='red', label='Regresi Linear')
plt.xlabel('Luas (m²)')
plt.ylabel('Harga (juta IDR)')
plt.title('Regresi Linear: Harga Rumah vs Luas')
plt.legend()
plt.show()
