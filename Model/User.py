from controllers.Id_generator import IdGenerator


class User:
    def __init__(self, id, name, s_name, login, password):
        self.login = login
        self.password = password
        self.id = id
        self.s_name = s_name
        self.name = name
        self.task_list = []
        self.assign_list = []
        self.exp = 0
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = False

    def get_id(self):
        return self.id

