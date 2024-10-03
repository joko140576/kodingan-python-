import pandas as pd
from tkinter import Tk, Button, Label, filedialog, Text
from tkinter import ttk
from prophet import Prophet
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Fungsi untuk membaca file Excel
def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        df = pd.read_excel(file_path)
        display_data(df)
        make_prediction(df)

# Fungsi untuk menampilkan data ke dalam tabel
def display_data(df):
    # Clear the treeview for new data
    for i in tree.get_children():
        tree.delete(i)
    
    tree["column"] = list(df.columns)
    tree["show"] = "headings"
    
    for col in tree["column"]:
        tree.heading(col, text=col)
    
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tree.insert("", "end", values=row)

# Fungsi untuk membuat prediksi dan menampilkan grafik
def make_prediction(df):
    # Clear the previous result
    result_text.delete(1.0, "end")
    
    # Konversi kolom ke format yang sesuai untuk Prophet
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    df = df.rename(columns={'tanggal': 'ds', 'saldo': 'y'})
    
    # Membuat model dan prediksi
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    
    # Menentukan kapan saldo mencapai 160 juta
    threshold = 160
    forecast_below_threshold = forecast[forecast['yhat'] <= threshold]
    
    if not forecast_below_threshold.empty:
        refill_date = forecast_below_threshold.iloc[0]['ds']
        result_text.insert("end", f"Saldo ATM diprediksi mencapai atau di bawah 160 juta pada: {refill_date.date()}")
    else:
        result_text.insert("end", "Saldo ATM tidak diprediksi mencapai 160 juta dalam periode prediksi.")
    
    # Membuat grafik prediksi
    figure = plt.Figure(figsize=(6, 5), dpi=100)
    ax = figure.add_subplot(111)
    ax.plot(df['ds'], df['y'], label='Saldo Aktual')
    ax.plot(forecast['ds'], forecast['yhat'], label='Prediksi Saldo', linestyle='dashed')
    ax.axhline(y=threshold, color='r', linestyle='--', label='Batas 20%')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Saldo (Juta)')
    ax.set_title('Prediksi Saldo ATM')
    ax.legend()

    # Display the plot in Tkinter window
    canvas = FigureCanvasTkAgg(figure, window)
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
    canvas.draw()

# Membuat antarmuka Tkinter
window = Tk()
window.title("Prediksi Pengisian ATM")
window.geometry("800x600")

# Tombol untuk upload file Excel
upload_button = Button(window, text="Unggah File Excel", command=upload_file)
upload_button.pack(pady=10)

# Text box untuk menampilkan hasil prediksi
result_text = Text(window, height=2, width=50)
result_text.pack(pady=10)

# Tabel untuk menampilkan data Excel
tree = ttk.Treeview(window)
tree.pack(pady=20)

# Mulai aplikasi
window.mainloop()
