#!/usr/bin/env python3
import subprocess
import sys
import time
import os

def start_service(service_path, service_name):
    """Iniciar un servicio en una nueva terminal"""
    try:
        if sys.platform == "win32":
            # Windows
            cmd = f'start cmd /k "cd {service_path} && python app.py"'
            subprocess.run(cmd, shell=True)
        else:
            # Linux/Mac
            cmd = f'gnome-terminal -- bash -c "cd {service_path} && python app.py; exec bash"'
            subprocess.run(cmd, shell=True)
        
        print(f" {service_name} iniciado")
        time.sleep(1)
    except Exception as e:
        print(f" Error iniciando {service_name}: {e}")

def main():
    print(" Iniciando todos los microservicios...\n")
    
    services = [
        ("services/storage_service", "Storage Service (Puerto 5002)"),
        ("services/logging_service", "Logging Service (Puerto 5003)"),
        ("services/task_service", "Task Service (Puerto 5001)"),
        ("client", "Client Service (Puerto 5000)")
    ]
    
    for service_path, service_name in services:
        if os.path.exists(service_path):
            start_service(service_path, service_name)
        else:
            print(f"❌ No se encontró el directorio: {service_path}")
    
    print("\n Todos los servicios iniciados!")
    print("Accede a la aplicación: http://localhost:5000")
    print("APIs disponibles:")
    print("- Task Service: http://localhost:5001")
    print("- Storage Service: http://localhost:5002") 
    print("- Logging Service: http://localhost:5003")

if __name__ == "__main__":
    main()