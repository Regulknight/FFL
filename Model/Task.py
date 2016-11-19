class Task:
    def __init__(self, id, category_index, name, description, location, time, owner, status, weight=1):
        self.id = id
        self.category_index = category_index
        self.name = name
        self.description = description
        self.location = location
        self.time = time
        self.owner = owner
        self.members = []
        self.status = status
        self.weight = weight
