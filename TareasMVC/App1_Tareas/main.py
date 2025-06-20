# filepath: e:\colegio\Arquitectura\App1_Tareas\main.py

from controllers.task_controller import TaskController
from storage.task_repo import TaskRepo

def main():
    repo = TaskRepo()
    controller = TaskController(repo)
    while True:
        print("\nTask List Application")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. List Tasks")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            controller.add_task(title, description)
        elif choice == '2':
            task_id = input("Enter task ID to remove: ")
            controller.remove_task(int(task_id))
        elif choice == '3':
            controller.list_tasks()
        elif choice == '4':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()