# app.py - Notification Service (Port 5004)
from flask import Flask, request

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    # Aquí iría la lógica de notificación
    return {'status': 'notified', 'data': data}

if __name__ == '__main__':
    app.run(port=5004, debug=True)
