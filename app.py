import os
from flask import Flask, render_template, request, jsonify
import ta

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    # Hii inasoma templates/index.html na kuiweka hewani
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "Bot backend is running!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
