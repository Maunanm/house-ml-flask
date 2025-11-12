import gradio as gr
import numpy as np
import pandas as pd
import joblib
import os

# ======= FILE MODEL =======
PRICE_MODEL_PATH = 'price_model.pkl'
WORTH_MODEL_PATH = 'worth_model.pkl'
SCALER_PATH = 'feature_scaler.pkl'
WORTH_MAP_PATH = 'worth_mapping.pkl'

# ======= LOAD MODEL =======
def load_models():
    try:
        if not all(os.path.exists(p) for p in [PRICE_MODEL_PATH, WORTH_MODEL_PATH, SCALER_PATH, WORTH_MAP_PATH]):
            return None, "❌ Model file tidak ditemukan."

        price_model = joblib.load(PRICE_MODEL_PATH)
        worth_model = joblib.load(WORTH_MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        worth_mapping = joblib.load(WORTH_MAP_PATH)

        return (price_model, worth_model, scaler, worth_mapping), None
    except Exception as e:
        return None, str(e)

loaded, error = load_models()

if error:
    print(error)
else:
    print("✅ Model berhasil dimuat.")

# ======= FUNGSI PREDIKSI =======
def predict(lb, lt, kt, km, grs):
    if error:
        return "Model belum tersedia atau gagal dimuat."

    try:
        price_model, worth_model, scaler, worth_mapping = loaded

        # Susun input dan scaling
        features = np.array([[lb, lt, kt, km, grs]])
        features_scaled = scaler.transform(features)

        predicted_price = price_model.predict(features_scaled)[0]
        worth_class = worth_model.predict(features_scaled)[0]
        worth_label = next((k for k, v in worth_mapping.items() if v == worth_class), str(worth_class))

        return f"""
        💰 **Prediksi Harga:** IDR {predicted_price:,.0f}
        🤔 **Kelayakan:** {worth_label}
        """
    except Exception as e:
        return f"Terjadi error saat prediksi: {str(e)}"

# ======= BUAT UI =======
iface = gr.Interface(
    fn=predict,
    inputs=[
        gr.Number(label="Luas Bangunan (m²)"),
        gr.Number(label="Luas Tanah (m²)"),
        gr.Number(label="Jumlah Kamar Tidur"),
        gr.Number(label="Jumlah Kamar Mandi"),
        gr.Number(label="Jumlah Garasi")
    ],
    outputs="markdown",
    title="🏠 Prediksi Harga & Kelayakan Rumah",
    description="Masukkan parameter rumah untuk memprediksi harga dan apakah 'worth it' atau tidak."
)

iface.launch()
