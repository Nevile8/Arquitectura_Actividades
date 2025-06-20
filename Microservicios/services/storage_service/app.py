from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

TASKS_FILE = 'tasks.json'

def load_tasks():
    """Cargar tareas desde archivo JSON"""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
    """Guardar tareas en archivo JSON"""
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error guardando tareas: {e}")
        return False

@app.route('/storage/tasks', methods=['GET'])
def get_tasks():
    """Obtener todas las tareas del archivo"""
    try:
        tasks = load_tasks()
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/storage/tasks', methods=['POST'])
def save_tasks_endpoint():
    """Guardar tareas en el archivo"""
    try:
        tasks = request.json
        if save_tasks(tasks):
            return jsonify({"message": "Tareas guardadas exitosamente"})
        else:
            return jsonify({"error": "Error al guardar tareas"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/storage/backup', methods=['GET'])
def backup_tasks():
    """Crear backup de las tareas"""
    try:
        tasks = load_tasks()
        backup_filename = f"backup_tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
        
        return jsonify({"message": f"Backup creado: {backup_filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "storage_service"})

if __name__ == '__main__':
    print("💾 Storage Service iniciado en puerto 5002")
    # Crear archivo inicial si no existe
    if not os.path.exists(TASKS_FILE):
        save_tasks([])
    app.run(debug=True, port=5002)