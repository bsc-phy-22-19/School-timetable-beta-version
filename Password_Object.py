class Object:
    def __init__(self, username, password):
        self.password = password
        self.username = username
        self.question = "What is your name"
        self.answer = ""

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_question(self):
        return self.question
    
    def get_answer(self):
        return self.answer

    def set_username(self, val):
        self.username = val

    def set_password(self, val):
        self.password = val

    def set_question(self, val):
        self.question = val

    def set_answer(self, val):
        self.answer = val

    
class Password_Data:
    def __init__(self):
        self.all_files = []

    def append(self, obj):
        for item in self.all_files:
            if item.get_username() == obj.get_username() and item.get_password() == obj.get_password():
                self.remove(item)
        self.all_files.append(obj)

    def get_all_files(self):
        return self.all_files

    def pop(self, index):
        self.all_files.pop(index)

    def remove(self, obj):
        self.all_files.remove(obj)

    def save(self, path=None):
        print("Saving")

    def load(self, path = None):
        print("Loading")


class Compare_Data:
    def __init__(self):
        self.username_exist = False
        self.password_exist = False

    def is_valid(self, all_users_passwords_obj, username, password):
        for item in all_users_passwords_obj:
            # print(item.get_password(), password, item.get_username(), username)
            if item.get_username() == username:
                self.username_exist = True

            if item.get_password() == password:
                self.password_exist = True

            if item.get_password() == password and item.get_username() == username:
                return True
        return False

    def get_username_exist(self):
        return self.username_exist

    def get_password_exist(self):
        return self.password_exist
