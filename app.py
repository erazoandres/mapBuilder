from flask import Flask, send_from_directory
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'web')
IMAGES_DIR = os.path.join(BASE_DIR, 'python', 'images')

app = Flask(__name__, static_folder=WEB_DIR)

@app.route('/')
def index():
    return send_from_directory(WEB_DIR, 'index.html')

@app.route('/css/<path:filename>')
def css(filename):
    return send_from_directory(os.path.join(WEB_DIR, 'css'), filename)

@app.route('/js/<path:filename>')
def js(filename):
    return send_from_directory(os.path.join(WEB_DIR, 'js'), filename)

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory(IMAGES_DIR, filename)

@app.route('/aporta')
def aporta():
    return send_from_directory(WEB_DIR, 'aporta.html')

@app.route('/python/main.py')
def main_py():
    file_path = os.path.join(BASE_DIR, 'python', 'main.py')
    with open(file_path, 'rb') as f:
        content = f.read()
    return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(debug=True, port=5000) 