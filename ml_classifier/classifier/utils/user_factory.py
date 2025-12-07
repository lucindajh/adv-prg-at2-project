class User:
    def __init__(self, name):
        self.name = name

    def role(self):
        return "Generic User"


class Admin(User):
    def role(self):
        return "Admin"


def create_user(user_type, name):
    user_type = user_type.lower()
    if user_type == "admin":
        return Admin(name)
    else:
        return User(name)
