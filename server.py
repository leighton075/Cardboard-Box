from flask import Flask, request, jsonify, send_from_directory
from io import BytesIO
import requests
from PIL import Image
from ascii_magic import AsciiArt
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('/home/Leighton075/Cardboard-Box', 'index.html')

@app.route('/ascii', methods=['POST'])
def ascii_art():
    data = request.get_json()
    url = data.get('url')
    columns = int(data.get('columns', 400))
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        art = AsciiArt.from_pillow_image(img)
        html = art.to_html(columns=columns, full_color=True)
        return jsonify({'html': html})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)