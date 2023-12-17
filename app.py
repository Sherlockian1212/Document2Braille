# app.py

from flask import Flask, render_template, request, jsonify
from models.Process import process
from models.Text2Braille import Text2Braille
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        data = request.get_json()
        input_text = data.get('text', '')
        braille_result = Text2Braille(input_text).text_to_braille()
        return jsonify({'braille_result': braille_result})
    return render_template('user.html')

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'})

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'})

    if image:
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        image.save(os.path.join(upload_folder, 'temp.png'))
        return jsonify({'message': 'Image uploaded successfully'})

@app.route('/api/process', methods=['GET'])
def process_image():
    currpath = current_directory = os.getcwd()
    path = os.path.join(current_directory, "uploads\\temp.jpg")
    braille_result = process(path)
    return jsonify({'braille_result': braille_result})

if __name__ == '__main__':
    app.run(debug=True)