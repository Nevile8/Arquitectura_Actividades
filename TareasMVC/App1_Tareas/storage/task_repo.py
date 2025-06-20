class TaskRepo:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def save_task(self, title, description):
        task = {
            'id': self.next_id,
            'title': title,
            'description': description,
            'completed': False
        }
        self.tasks.append(task)
        self.next_id += 1
        return task

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task['id'] != task_id]

    def get_all_tasks(self):
        return self.tasks