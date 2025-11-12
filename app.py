from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import joblib
import os
import requests
app = Flask(__name__)

# ======= MODEL FILE NAMES =======
PRICE_MODEL_PATH = 'price_model.pkl'
WORTH_MODEL_PATH = 'worth_model.pkl'
SCALER_PATH = 'feature_scaler.pkl'
WORTH_MAP_PATH = 'worth_mapping.pkl'
DATASET_PATH = 'House Price Prediction.csv'  # Path to your CSV dataset

def download_model_files():
    files = {
        "price_model.pkl": "https://raw.githubusercontent.com/Maunanm/house-ml-flask/main/price_model.pkl",
        "worth_model.pkl": "https://raw.githubusercontent.com/Maunanm/house-ml-flask/main/worth_model.pkl",
        "feature_scaler.pkl": "https://raw.githubusercontent.com/Maunanm/house-ml-flask/main/feature_scaler.pkl",
        "worth_mapping.pkl": "https://raw.githubusercontent.com/Maunanm/house-ml-flask/main/worth_mapping.pkl"
    }

    for filename, url in files.items():
        if not os.path.exists(filename):
            print(f"Downloading {filename}...")
            response = requests.get(url)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"{filename} downloaded.")
            else:
                print(f"Failed to download {filename} from {url}")

# Download all models before loading
download_model_files()

# ======= CEK & LOAD MODEL =======
def load_models():
    """
    Load pre-trained models and necessary files.
    Returns True if all files loaded successfully.
    """
    try:
        if not all(os.path.exists(p) for p in [PRICE_MODEL_PATH, WORTH_MODEL_PATH, SCALER_PATH, WORTH_MAP_PATH]):
            print("Error: One or more model files are missing.")
            return False
        
        global price_model, worth_it_model, scaler, worth_mapping
        price_model = joblib.load(PRICE_MODEL_PATH)
        worth_it_model = joblib.load(WORTH_MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        worth_mapping = joblib.load(WORTH_MAP_PATH)

        print("Models loaded successfully.")
        return True

    except Exception as e:
        print(f"Error loading models: {e}")
        return False

# Load models at startup
models_available = load_models()

# Dummy fallback (opsional, tidak akan digunakan kalau models_available True)
if not models_available:
    class DummyModel:
        def predict(self, X):
            return [0]

    price_model = worth_it_model = DummyModel()
    scaler = None
    worth_mapping = {'Worth it': 1, 'Tidak Worth it': 0}

# ======= PREDIKSI =======
def make_house_prediction(lb, lt, kt, km, grs):
    try:
        # Susun fitur input
        features = np.array([[lb, lt, kt, km, grs]])

        # Skala fitur jika scaler tersedia
        features_scaled = scaler.transform(features) if scaler else features

        # Prediksi harga dan klasifikasi worth it
        predicted_price = price_model.predict(features_scaled)[0]
        worth_class = worth_it_model.predict(features_scaled)[0]

        # Konversi kelas ke label
        worth_label = next((k for k, v in worth_mapping.items() if v == worth_class), str(worth_class))

        return {
            'success': True,
            'price': float(predicted_price),
            'formatted_price': f"IDR {predicted_price:,.0f}",
            'worth_it': int(worth_class),
            'worth_it_label': worth_label
        }

    except Exception as e:
        return {'success': False, 'error': str(e)}

# ======= LOAD DATASET =======
def load_dataset():
    """Load the dataset CSV file"""
    try:
        if os.path.exists(DATASET_PATH):
            df = pd.read_csv(DATASET_PATH)
            return df, None
        else:
            return None, "Dataset file not found"
    except Exception as e:
        return None, f"Error loading dataset: {str(e)}"

# ======= ROUTES =======
@app.route('/')
def home():
    return render_template('home.html', active_page='home', models_available=models_available)

@app.route('/prediction')
def prediction():
    return render_template('prediction.html', active_page='prediction', models_available=models_available)

@app.route('/visualization')
def visualization():
    return render_template('visualization.html', active_page='visualization')

@app.route('/dataset')
def dataset():
    df, error = load_dataset()
    
    if error:
        return render_template('dataset.html', active_page='dataset', error_message=error)
    
    # Convert DataFrame to HTML table with custom classes
    table_html = df.to_html(classes='dataset-table', index=False, 
                            float_format=lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x)
    
    return render_template('dataset.html', active_page='dataset', table_html=table_html)

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

# ======= API ENDPOINT PREDIKSI =======
@app.route('/predict', methods=['POST'])
def predict():
    if not models_available:
        return jsonify({'success': False, 'error': 'Models are not available.'}), 400

    try:
        data = request.json
        lb = float(data.get('building_area', 0))
        lt = float(data.get('land_area', 0))
        kt = int(data.get('bedrooms', 0))
        km = int(data.get('bathrooms', 0))
        grs = int(data.get('garages', 0))

        result = make_house_prediction(lb, lt, kt, km, grs)
        return jsonify(result) if result['success'] else (jsonify(result), 400)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    
# ======= API UNTUK VISUALISASI =======
@app.route('/api/land-area-data')
def land_area_data():
    df, error = load_dataset()
    if error:
        return jsonify({'success': False, 'error': error}), 500
    try:
        bins = [0, 50, 100, 150, 200, 250, 300, 500, 1000, df['LT'].max()]
        labels = ['<50', '50–100', '100–150', '150–200', '200–250', '250–300', '300–500', '500–1000', '>1000']
        df['land_bin'] = pd.cut(df['LT'], bins=bins, labels=labels, include_lowest=True)

        counts = df['land_bin'].value_counts().sort_index()
        
        return jsonify({
            'success': True,
            'labels': [str(label) for label in counts.index],
            'values': [int(val) for val in counts.values] 
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/bedroom-data')
def bedroom_data():
    df, error = load_dataset()
    if error:
        return jsonify({'success': False, 'error': error}), 500

    try:
        bins = [0, 2, 5, 8, 9, df['KT'].max()]
        labels = ['<3', '3-5', '6-8', '9-11', '>11']
        df['land_bin'] = pd.cut(df['KT'], bins=bins, labels=labels, include_lowest=True)
        counts = df['land_bin'].value_counts().sort_index()
        
        return jsonify({
            'success': True,
            'labels': list(counts.index.astype(str)),
            'values': counts.tolist()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/price-data')
def price_data():
    df, error = load_dataset()
    if error:
        return jsonify({'success': False, 'error': error}), 500

    try:
        bins = [0, 1000000000, 5000000000, 10000000000, 15000000000, 20000000000, df['HARGA'].max()]
        labels = ['<1M', '1M–5M', '5M–10M', '10M–15M', '15M–20M', '>20M']
        df['land_bin'] = pd.cut(df['HARGA'], bins=bins, labels=labels, include_lowest=True)
        counts = df['land_bin'].value_counts().sort_index()
        
        return jsonify({
            'success': True,
            'labels': list(counts.index.astype(str)),
            'values': counts.tolist()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

    
# ======= ERROR HANDLERS =======
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# ======= RUN APP =======
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
