class Task:
    def __init__(self, index, category_index, description, location, time, owner, status, weight=1):
        self.index = index
        self.category_index = category_index
        self.description = description
        self.location = location
        self.time = time
        self.owner = owner
        self.members = []
        self.status = status
        self.weight = weight
