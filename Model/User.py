from controllers.Id_generator import IdGenerator


class User:
    def __init__(self, name, s_name, login, password):
        self.login = login
        self.password = password
        gen = IdGenerator()
        self.id = gen.get_new_user_id()
        self.s_name = s_name
        self.name = name
        self.task_list = []
        self.assign_list = []
        self.exp = 0
