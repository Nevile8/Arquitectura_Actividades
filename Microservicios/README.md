# Microservices Example

Este proyecto contiene una arquitectura de microservicios en Python usando Flask.

## Estructura
- `client/`: Interfaz de usuario (Flask, puerto 5000)
- `services/task_service/`: CRUD de tareas (puerto 5001)
- `services/storage_service/`: Persistencia (puerto 5002)
- `services/logging_service/`: Logs (puerto 5003)
- `services/notification_service/`: Notificaciones (puerto 5004, opcional)

## Requisitos
- Python 3.x
- Flask

## Instalación
```
pip install -r requirements.txt
```

## Ejecución
```
python start_services.py
```

Cada microservicio puede ejecutarse también por separado:
```
python client/app.py
python services/task_service/app.py
...
```
