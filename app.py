from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import io
import zipfile
from astrolabe import Mater, Plate, Rete, Back, Rule

app = Flask(__name__)
CORS(app)  # عشان بلوجر يقدر يكلمه

@app.route('/')
def home():
    return jsonify({
        "status": "شغال", 
        "message": "API مولد الأسطرلاب العربي",
        "usage": "/generate?lat=30.0444&name=القاهرة"
    })

@app.route('/generate', methods=['GET'])
def generate():
    try:
        # 1. خد الإحداثيات من الرابط
        lat = float(request.args.get('lat', 30.0444))
        name = request.args.get('name', 'مخصص')
        stars = int(request.args.get('stars', 15))
        
        # 2. ولّد كل الأجزاء
        radius = 1000
        images = {
            "mater.png": Mater(radius, f"أسطرلاب {name}").render(),
            "plate.png": Plate(radius, lat, name).render(),
            "rete.png": Rete(radius, stars).render(),
            "back.png": Back(radius).render(),
            "rule.png": Rule(radius).render()
        }
        
        # 3. حطهم في ملف zip واحد
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for filename, img in images.items():
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                zip_file.writestr(filename, img_bytes.getvalue())
        
        zip_buffer.seek(0)
        
        # 4. رجع الملف للتحميل
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'astrolabe_{name}_{lat}.zip'
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run()
