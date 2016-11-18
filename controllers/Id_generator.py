class IdGenerator:

    def __init__(self):
        self.id_task = 0
        self.id_user = 0

    def get_new_task_id(self):
        self.id_task += 1
        return self.id_task

    def get_new_user_id(self):
        self.id_user += 1
        return self.id_user
