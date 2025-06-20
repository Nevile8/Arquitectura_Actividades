from models.task import Task


class TaskController:
    def __init__(self, task_repo):
        self.task_repo = task_repo

    def add_task(self, title, description):
        task = Task(title=title, description=description)
        self.task_repo.save_task(task)

    def remove_task(self, task_id):
        self.task_repo.delete_task(task_id)

    def list_tasks(self):
        return self.task_repo.get_all_tasks()