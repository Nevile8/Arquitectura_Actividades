from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

LOG_FILE = 'log.txt'

def write_log(log_entry):
    """Escribir entrada de log al archivo"""
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{log_entry}\n")
        return True
    except Exception as e:
        print(f"Error escribiendo log: {e}")
        return False

@app.route('/logs', methods=['POST'])
def add_log():
    """Agregar nueva entrada de log"""
    try:
        data = request.json
        timestamp = data.get('timestamp', datetime.now().isoformat())
        service = data.get('service', 'unknown')
        action = data.get('action', 'unknown')
        extra_data = data.get('data', {})
        
        log_entry = f"[{timestamp}] {service.upper()}: {action}"
        if extra_data:
            log_entry += f" | Data: {json.dumps(extra_data, ensure_ascii=False)}"
        
        if write_log(log_entry):
            return jsonify({"message": "Log registrado exitosamente"})
        else:
            return jsonify({"error": "Error al escribir log"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logs', methods=['GET'])
def get_logs():
    """Obtener logs recientes"""
    try:
        if not os.path.exists(LOG_FILE):
            return jsonify([])
        
        lines = request.args.get('lines', 50, type=int)
        
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        return jsonify([line.strip() for line in recent_lines])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logs/clear', methods=['DELETE'])
def clear_logs():
    """Limpiar archivo de logs"""
    try:
        with open(LOG_FILE, 'w') as f:
            f.write("")
        return jsonify({"message": "Logs limpiados"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "logging_service"})

if __name__ == '__main__':
    print("📝 Logging Service iniciado en puerto 5003")
    # Crear archivo de log inicial
    if not os.path.exists(LOG_FILE):
        write_log(f"[{datetime.now().isoformat()}] SYSTEM: Logging service iniciado")
    app.run(debug=True, port=5003)