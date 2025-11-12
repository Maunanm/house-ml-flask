from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Prediksi Harga Rumah</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
        * {
            box-sizing: border-box;
        }
        body {
            margin: 0;
            font-family: 'Montserrat', sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
            scroll-behavior: smooth;
        }
        header {
            background: linear-gradient(135deg, #6b73ff 0%, #000dff 100%);
            color: white;
            padding: 60px 20px 40px 20px;
            text-align: center;
        }
        header h1 {
            font-size: 3rem;
            margin-bottom: 12px;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.4);
        }
        header p {
            font-size: 1.5rem;
            margin-top: 0;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            color: #d3dbff;
        }
        nav {
            background: #1a237e;
            text-align: center;
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        nav a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
            font-weight: 600;
            font-size: 1rem;
            transition: color 0.3s ease;
        }
        nav a:hover {
            color: #ff7961;
        }
        section {
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
        }
        section#tujuan h2,
        section#prediksi h2,
        section#galeri h2 {
            font-size: 2.2rem;
            margin-bottom: 20px;
            border-left: 6px solid #000dff;
            padding-left: 10px;
            color: #000dff;
        }
        #tujuan p {
            font-size: 1.15rem;
            color: #444;
            max-width: 750px;
        }
        #galeri {
            text-align: center;
        }
        #galeri .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        #galeri img {
            width: 100%;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
            cursor: pointer;
        }
        #galeri img:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        form {
            background: white;
            border-radius: 12px;
            padding: 30px 25px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
            max-width: 500px;
            margin: 0 auto;
        }
        form label {
            display: block;
            font-weight: 600;
            margin-bottom: 6px;
            margin-top: 18px;
            color: #222;
        }
        form input[type="number"] {
            width: 100%;
            padding: 12px 15px;
            border-radius: 8px;
            border: 1px solid #ccc;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }
        form input[type="number"]:focus {
            border-color: #000dff;
            box-shadow: 0 0 6px #000dff;
        }
        form input[type="submit"] {
            margin-top: 30px;
            width: 100%;
            background-color: #000dff;
            border: none;
            padding: 16px;
            font-size: 1.2rem;
            font-weight: 700;
            color: white;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        form input[type="submit"]:hover {
            background-color: #0041c4;
        }
        .result {
            margin-top: 30px;
            text-align: center;
            background: #000dff;
            max-width: 500px;
            padding: 22px;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.2);
            font-size: 1.5rem;
            font-weight: 700;
            color: #ffd700;
            margin-left: auto;
            margin-right: auto;
        }
        footer {
            background: #000dff;
            color: white;
            text-align: center;
            padding: 18px 10px;
            font-size: 1rem;
            margin-top: 60px;
        }
        @media (max-width: 600px) {
            header h1 {
                font-size: 2.2rem;
            }
            header p {
                font-size: 1.1rem;
            }
            section#tujuan p {
                font-size: 1rem;
            }
            form {
                padding: 20px 15px;
            }
            .result {
                font-size: 1.3rem;
                padding: 18px;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>Prediksi Harga Rumah</h1>
        <p>Solusi cepat dan mudah untuk memperkirakan harga rumah Anda secara akurat!</p>
    </header>
    <nav>
        <a href="#tujuan">Tujuan</a>
        <a href="#galeri">Galeri</a>
        <a href="#prediksi">Prediksi</a>
    </nav>
    
    <section id="tujuan">
        <h2>Tujuan</h2>
        <p>
            Website ini bertujuan memberikan perkiraan harga rumah berdasarkan beberapa aspek penting seperti luas bangunan, jumlah kamar tidur, kamar mandi, dan jumlah lantai. Dengan informasi ini, Anda dapat membuat keputusan yang lebih baik sebelum membeli atau menjual rumah.
        </p>
        <p>
            Sistem prediksi ini menggunakan rumus perkiraan harga sederhana untuk memberikan gambaran awal yang cepat dan mudah dipahami oleh semua kalangan.
        </p>
    </section>
    
    <section id="galeri">
        <h2>Galeri Rumah</h2>
        <div class="gallery-grid">
            <img src="https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=350" alt="Rumah minimalis modern" loading="lazy" />
            <img src="https://images.pexels.com/photos/210617/pexels-photo-210617.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=350" alt="Rumah dengan taman" loading="lazy" />
            <img src="https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=350" alt="Rumah mewah dengan kolam renang" loading="lazy" />
            <img src="https://images.pexels.com/photos/2584472/pexels-photo-2584472.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=350" alt="Rumah bergaya kontemporer" loading="lazy" />
        </div>
    </section>
    
    <section id="prediksi">
        <h2>Prediksi Harga Rumah Anda</h2>
        <form method="POST" action="#prediksi">
            <label for="area">Luas Bangunan (m²)</label>
            <input type="number" id="area" name="area" min="10" max="1000" required placeholder="Contoh: 120" value="{{ area|default('') }}" />
            
            <label for="bedrooms">Jumlah Kamar Tidur</label>
            <input type="number" id="bedrooms" name="bedrooms" min="1" max="20" required placeholder="Contoh: 3" value="{{ bedrooms|default('') }}" />
            
            <label for="bathrooms">Jumlah Kamar Mandi</label>
            <input type="number" id="bathrooms" name="bathrooms" min="1" max="10" required placeholder="Contoh: 2" value="{{ bathrooms|default('') }}" />
            
            <label for="floor">Jumlah Lantai</label>
            <input type="number" id="floor" name="floor" min="1" max="5" required placeholder="Contoh: 1" value="{{ floor|default('') }}" />
            
            <input type="submit" value="Prediksi Harga" />
        </form>
        {% if prediction is defined %}
        <div class="result" role="alert" aria-live="polite">
            Harga diperkirakan: Rp {{ "{:,.0f}".format(prediction) }},-
        </div>
        {% endif %}
    </section>
    
    <footer>
        &copy; 2024 Prediksi Harga Rumah. Semua hak cipta dilindungi.
    </footer>
</body>
</html>
"""

def prediksi_harga(area, kamar_tidur, kamar_mandi, lantai):
    """
    Fungsi prediksi dummy berdasarkan formula sederhana:
    Harga = harga dasar + luas * 2,5 juta + kamar tidur * 50 juta + kamar mandi * 40 juta + lantai * 30 juta
    Nilai dalam Rupiah.
    """
    harga_dasar = 500_000_000  # harga dasar Rp 500 juta
    harga = harga_dasar + (area * 2_500_000) + (kamar_tidur * 50_000_000) + (kamar_mandi * 40_000_000) + (lantai * 30_000_000)
    return harga

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    context = {}
    if request.method == "POST":
        try:
            area = int(request.form.get("area", 0))
            kamar_tidur = int(request.form.get("bedrooms", 0))
            kamar_mandi = int(request.form.get("bathrooms", 0))
            lantai = int(request.form.get("floor", 0))

            if area <= 0 or kamar_tidur <= 0 or kamar_mandi <= 0 or lantai <= 0:
                raise ValueError("Input harus berupa angka positif.")

            prediction = prediksi_harga(area, kamar_tidur, kamar_mandi, lantai)
            context = {
                "prediction": prediction,
                "area": area,
                "bedrooms": kamar_tidur,
                "bathrooms": kamar_mandi,
                "floor": lantai
            }
        except Exception:
            context = {
                # Keep form filled with posted values if available, else empty
                "area": request.form.get("area", ""),
                "bedrooms": request.form.get("bedrooms", ""),
                "bathrooms": request.form.get("bathrooms", ""),
                "floor": request.form.get("floor", "")
            }
    return render_template_string(HTML_TEMPLATE, **context)

if __name__ == "__main__":
    app.run(debug=True)
