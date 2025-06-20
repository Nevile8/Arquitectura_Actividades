from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

STORAGE_SERVICE_URL = "http://localhost:5002"
LOGGING_SERVICE_URL = "http://localhost:5003"

def log_action(action, task_data=None):
    """Envía logs al logging service"""
    try:
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "service": "task_service",
            "action": action,
            "data": task_data
        }
        requests.post(f"{LOGGING_SERVICE_URL}/logs", json=log_data, timeout=2)
    except:
        print(f"Warning: No se pudo enviar log para acción: {action}")

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Obtener todas las tareas"""
    try:
        response = requests.get(f"{STORAGE_SERVICE_URL}/storage/tasks")
        tasks = response.json()
        log_action("get_tasks", {"count": len(tasks)})
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks', methods=['POST'])
def create_task():
    """Crear nueva tarea"""
    try:
        data = request.json
        task = {
            "id": str(uuid.uuid4()),
            "title": data.get("title"),
            "description": data.get("description", ""),
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        
        # Obtener tareas actuales
        response = requests.get(f"{STORAGE_SERVICE_URL}/storage/tasks")
        tasks = response.json()
        
        # Agregar nueva tarea
        tasks.append(task)
        
        # Guardar
        requests.post(f"{STORAGE_SERVICE_URL}/storage/tasks", json=tasks)
        
        log_action("create_task", task)
        return jsonify(task), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Actualizar tarea"""
    try:
        data = request.json
        
        # Obtener tareas
        response = requests.get(f"{STORAGE_SERVICE_URL}/storage/tasks")
        tasks = response.json()
        
        # Buscar y actualizar tarea
        for task in tasks:
            if task["id"] == task_id:
                task.update(data)
                task["updated_at"] = datetime.now().isoformat()
                break
        else:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        # Guardar cambios
        requests.post(f"{STORAGE_SERVICE_URL}/storage/tasks", json=tasks)
        
        log_action("update_task", {"id": task_id, "changes": data})
        return jsonify(task)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/<task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    """Marcar tarea como completada"""
    try:
        # Obtener tareas
        response = requests.get(f"{STORAGE_SERVICE_URL}/storage/tasks")
        tasks = response.json()
        
        # Marcar como completada
        for task in tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                break
        else:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        # Guardar cambios
        requests.post(f"{STORAGE_SERVICE_URL}/storage/tasks", json=tasks)
        
        log_action("complete_task", {"id": task_id})
        return jsonify(task)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Eliminar tarea"""
    try:
        # Obtener tareas
        response = requests.get(f"{STORAGE_SERVICE_URL}/storage/tasks")
        tasks = response.json()
        
        # Eliminar tarea
        tasks = [task for task in tasks if task["id"] != task_id]
        
        # Guardar cambios
        requests.post(f"{STORAGE_SERVICE_URL}/storage/tasks", json=tasks)
        
        log_action("delete_task", {"id": task_id})
        return jsonify({"message": "Tarea eliminada"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "task_service"})

if __name__ == '__main__':
    print(" Task Service iniciado en puerto 5001")
    app.run(debug=True, port=5001)