from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return {"status": "healthy", "service": "client"}

if __name__ == '__main__':
    print("Client Service iniciado en puerto 5000")
    print(" Accede a: http://localhost:5000")
    app.run(debug=True, port=5000)