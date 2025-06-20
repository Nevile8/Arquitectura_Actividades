# filepath: e:\colegio\Arquitectura\App1_Tareas\views\task_view.py

class TaskView:
    def display_tasks(self, tasks):
        if not tasks:
            print("No tasks available.")
            return
        print("Task List:")
        for task in tasks:
            status = "✓" if task.completed else "✗"
            print(f"[{status}] {task.title}: {task.description}")

    def prompt_user_input(self, prompt):
        return input(prompt)