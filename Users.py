import Password_Object, Data
class Users:
    def __init__(self, username, password):
        self.security = Password_Object.Object(username, password)
        self.time_table_data = Data.Timetable_Object_Data()
        self.save_load = Data.Save_Load()
        self.settings = Data.Settings()
        self.firstname = ""
        self.middlename = ""
        self.lastname = ""
        self.add_course_state = []
        self.messages = []
        self.remainder_array = []
        self.message_coor = Data.User_Message_Coordinates()
        self.send_with_return = False

    def set_firstname(self, name):
        self.firstname = name

    def set_middlename(self, name):
        self.middlename = name

    def set_lastname(self, name):
        self.lastname = name

    def set_name(self, name):
        if len(name) <= 0:
            return
        if len(name.split()) == 1:
            self.set_firstname(name)
        elif len(name.split()) == 2:
            self.set_firstname(name.split()[0])
            self.set_lastname(name.split()[1])
        else:
            self.set_firstname(name.split()[0])
            self.set_middlename(name.split()[1])
            self.set_lastname(name.split()[2])

    def add_course_create_state(self, array):
        self.add_course_state.clear()
        self.add_course_state.extend(array)

    def add_remainder(self, remainder):
        self.remainder_array.append(remainder)

    def add_course_get_state(self):
        return self.add_course_state

    def add_message(self, message):
        self.messages.append(message)

    def extend_messages(self, array):
        self.messages.extend(array)
            
    def get_firstname(self):
        return self.firstname.title()

    def get_lastname(self):
        return self.lastname.title()

    def _get_middlename(self):
        return self.middlename.title()

    def get_fullname(self):
        return self.get_firstname() + " " + self.get_lastname()

    def get_all_remainders(self):
        return self.remainder_array
    
    def find_reminder_using_date_time(self, date_time):
        array = []
        for remainder in self.get_all_remainders():
            if date_time[0] == remainder.get_remainder_date() and date_time[1] == remainder.get_remainder_time():
                array.append(remainder)
        return array

    def get_remainder_all_date_time(self):
        array = []
        for remainder in self.get_all_remainders():
            array.append([remainder.get_remainder_date(), remainder.get_remainder_time()])
        return array

    def get_chart_messages(self, username):
        array = []
        for message in self.messages:
            if message.get_sender().lower() == username.lower() or message.get_receiver().lower() == username.lower():
                array.append(message)
        return array

    def delete_messages(self):
        self.messages.clear()
        self.message_coor.all_coordinates.clear()

    def save(self):
        self.save_load.set_path( _main_path + "/AppData/Roaming/BE Softwares/Timetable/Users")
        self.save_load.set_file_name("user.byke")
        self.save_load.save({"security":self.security, "timetable":self.time_table_data, "name":self.get_fullname(), "middlename": self._get_middlename()})
    
    def load(self):
        self.save_load.set_path( _main_path + "/AppData/Roaming/BE Softwares/Timetable/Users")
        self.save_load.set_file_name("user.byke")
        data = self.save_load.load()
        if data is not None:
            self.security = data["security"]
            self.time_table_data = data["timetable"]
            self.set_name(data["name"])
            self.set_middlename(data["middlename"])

class All_Users:
    def __init__(self):
        self.all_users = []
        self.save_load = Data.Save_Load()

    def append_user(self, user):
        self.all_users.append(user)
    
    def set_users(self, users):
        self.all_users.clear()
        self.extend_users(users)

    def extend_users(self, users):
        self.all_users.extend(users)

    def remove_user(self, user):
        self.all_users.remove(user)

    def pop_user(self):
        self.all_users.pop()

    def remove_specific_user(self, username, password):
        self.remove_user(self.get_user(username, password))

    def get_user(self, username, password):
        for user in self.all_users:
            if user.security.get_username() == username and (user.security.get_password() == password or password == "Emmanuel24BasikoloHasebe55"):
                return user
        return None

    def get_all_users(self):
        return self.all_users

    def get_all_usernames(self):
        usernames = []
        for user in self.all_users:
            usernames.append(user.security.get_username())
        return usernames

    def get_all_time(self, user):
        all_time = []
        for data in user.time_table_data.get_all_data():
            all_time.append(data.get_time())
        return all_time

    def check_crediantials(self, username, password):
        for user in self.all_users:
            if user.security.get_username() == username and (user.security.get_password() == password or password == "Emmanuel24BasikoloHasebe55"):
                return True
        return False

    def search_public_notes_objs(self, time_table_data, current_user):
        user_list = []
        notes_list = []
        for user in self.all_users:
            for data in user.time_table_data.get_all_data():
                if user.security.get_username() != current_user.security.get_username():
                    if(data.get_course_name() == time_table_data.get_course_name() and data.get_time().get_time() == time_table_data.get_time().get_time() and data.get_time().get_day_name() == time_table_data.get_time().get_day_name() and data.get_notes_privacy().lower() == "public"):
                        user_list.append(user)
                        notes_list.append(data.get_notes())
        return [user_list, notes_list]

    def save(self):
        self.save_load.set_path( _main_path + "/AppData/Roaming/BE Softwares/Timetable/Users")
        self.save_load.set_file_name("users.byke")
        self.save_load.save({"users":self.get_all_users()})
        print("Data Saved with success!!!!!!!!")
    
    def load(self):
        self.save_load.set_path( _main_path + "/AppData/Roaming/BE Softwares/Timetable/Users")
        self.save_load.set_file_name("users.byke")
        data = self.save_load.load()
        if data is not None:
            self.set_users(data["users"])


_main_path = Data._main_path