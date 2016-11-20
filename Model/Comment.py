class Comment:
    def __init__(self, id, text, task_id, owner):
        self.owner = owner
        self.id = id
        self.text = text
        self.task_id = task_id
