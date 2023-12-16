# app.py

from flask import Flask, render_template, request, jsonify
from models.Text2Braille import Text2Braille

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

if __name__ == '__main__':
    app.run(debug=True)