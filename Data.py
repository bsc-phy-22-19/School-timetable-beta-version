import os, pickle
class More_Functions:
    def __init__(self):
        self.save_load = Save_Load()
        self.days = ["mon", "monday", "tue", "tuesday", "wed", "wednesday", "wesday", "thu", "thursday", "fri", "friday", "sat", "satuday", "sun", "sunday"]
        self.sample_time = ["7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
        self.rooms_available = [""]
        self.all_courses = [""]
        self.colors = ["lightblue", "blue", "darkblue", "skyblue", "aqua", "gray", "darkgray", "silver", "khaki", "thistle", "lightyellow", "white", "lightgreen", "darkgreen", "green", "#f34f56", "red", "brown", "darkred", "pink", "deeppink", "magenta", "purple", "violet", "orange", "gold", "yellow", "tan", "peachpuff"]
        self.questions_array = ["Mother's surname", "First CD I bought", "Primary school's name", "Name of car I want", "Favorite side-dish", ""]

    def get_rooms(self):
        return self.rooms_available

    def get_questions(self):
        return self.questions_array

    def add_room(self, val):
        if val not in self.rooms_available:
            self.rooms_available.append(val)

    def get_all_courses(self):
        return self.all_courses

    def get_colors(self):
        return self.colors
    
    def add_course(self, val):
        if val not in self.all_courses:
            self.all_courses.append(val)
    
    def get_wdir(self):
        return os.getcwd().replace("\\", "/")

    @staticmethod
    def get_row(time):
        if time == "7:00":
            return 0
        elif time == "8:00":
            return 1
        elif time == "9:00":
            return 2
        elif time == "10:00":
            return 3
        elif time == "11:00":
            return 4
        elif time == "12:00":
            return 5
        elif time == "13:00":
            return 6
        elif time == "14:00":
            return 7
        elif time == "15:00":
            return 8
        elif time == "16:00":
            return 9
        elif time == "17:00":
            return 10
        elif time == "18:00":
            return 11
        elif time == "19:00":
            return 12
        elif time == "20:00":
            return 13
        return 14

    @staticmethod
    def get_row_rev(row):
        if row == 0:
            return "7:00"
        elif row == 1:
            return "8:00"
        elif row == 2:
            return "9:00"
        elif row == 3:
            return "10:00"
        elif row == 4:
            return "11:00"
        elif row == 5:
            return "12:00"
        elif row == 6:
            return "13:00"
        elif row == 7:
            return "14:00"
        elif row == 8:
            return "15:00"
        elif row == 9:
            return "16:00"
        elif row == 10:
            return "17:00"
        elif row == 11:
            return "18:00"
        elif row == 12:
            return "19:00"
        elif row == 13:
            return "20:00"
        return "21:00"

    @staticmethod 
    def get_col(day):
        if day.lower() == "mon" or day.lower() == "monday":
            return 1
        elif day.lower() == "tue" or day.lower() == "tuesday":
            return 2
        elif day.lower() == "wed" or day.lower() == "wednesday" or day.lower() == "wesday":
            return 3
        elif day.lower() == "thu" or day.lower() == "thursday":
            return 4
        elif day.lower() == "fri" or day.lower() == "friday":
            return 5
        elif day.lower() == "sat" or day.lower() == "sataday":
            return 6
        elif day.lower() == "sun" or day.lower() == "sunday":
            return 7
        else:
            return 8

    @staticmethod 
    def get_col_rev(col):
        if col == 1:
            return "Monday"
        elif col == 2:
            return "Tuesday"
        elif col == 3:
            return "Wednesday"
        elif col == 4:
            return "Thursday"
        elif col == 5:
            return "Friday"
        elif col == 6:
            return "Sataday"
        elif col == 7:
            return "Sunday"
        else:
            return "Unknown day"

    @staticmethod
    def rename(path, file_name, extension):
        file_name_tmp = file_name
        counter = 1
        while os.path.exists(f"{path}/{file_name_tmp}.{extension}"):
            file_name_tmp = f"{file_name}+{counter}" 
            counter += 1
        return f"{file_name_tmp}.{extension}"

    def is_valid_day(self, day_name):
        day_name = day_name.lower()
        return day_name in self.days

    @staticmethod
    def is_valid_time(time):
        time = time.replace(" ", "")
        if time.strip() == "" or time[-1] == ":" or time[-1] == "." or time[0] == ":" or time[0] == ".":
            return False
        time_res = [":", "."]
        if time.count(":") >= 3 or time.count(".") >= 2:
            return False
        for t in time:
            if (t.isnumeric() or t in time_res) == False:
                return False
        return time.find(":") + 1 != time.rfind(":")

    @staticmethod
    def get_full_day_name(day):
        day = day.lower().strip()

        return ("Monday" if day == "mon" or day == "monday" else "Tuesday" if day == "tue" or day == "tuesday" else "Wednesday" if day == "wed" or day == "wesday" or day == "wednesday" else "Thursday" if day == "thu" or day == "thursday" else "Friday" if day == "fri" or day == "friday" else "Satuday" if day == "sat" or day == "satuday" else "Sunday" if day == "sun" or day == "sunday" else None)

    @staticmethod
    def to_seconds(time):
        seconds = 0
        if time.count(":") <= 0:
            seconds = float(time) * 60 * 60
        elif time.count(":") == 1:
            seconds = (float(time[:time.find(":")]) * 60 * 60 ) + (float(time[time.find(":")+1:]) * 60)
        elif time.count(":") == 2:
            seconds = (float(time[:time.find(":")]) * 60 * 60 ) + (float(time[time.find(":")+1:time.rfind(":")]) * 60) + float(time[time.rfind(":")+1:])
        else:
            return None
        return seconds

    @staticmethod
    def  from_seconds(seconds):
        minutes = 0
        hours = 0
        while seconds >= 60:
            if seconds >= 60:
                seconds -= 60
                minutes += 1
            if minutes >= 60:
                minutes = 0
                hours += 1
        return ("{}:{}".format(More_Functions.zero_format(hours), More_Functions.zero_format(minutes)), More_Functions.zero_format(seconds))   

    def add_seconds(seconds1, seconds2):
        seconds = seconds1 + seconds2
        hours = 0
        minutes = 0
        day = 0
        while seconds >= 60:
            if seconds >= 60:
                seconds -= 60
                minutes += 1
            if minutes >= 60:
                minutes = 0
                hours += 1
            if hours >= 24:
                hours = 0
                day += 1
        return (day, hours, minutes, seconds)

    @staticmethod
    def zero_format(number):
        if number >= 10:
            return f"{number}"
        else:
            return f"0{number}"

    def sort_time(self, time_obj):
        time = time_obj.get_time().get_time()
        start_time = time
        if time.count("-") == 1:
            start_time = time.split("-")[0]
        start_time = More_Functions.to_seconds(start_time)
        return start_time

    @staticmethod
    def get_repeate_number(repeate):
        repeate = repeate.lower()
        if repeate == "no repeate":
            return 0
        if len(repeate.split(" ")) > 1:
            return int(repeate.split(" ")[0])
        else:
            number
            for i in repeate:
                if i.isnumeric():
                    number += i
                else:
                    return number
            return number

    @staticmethod
    def get_repeate_duration(word):
        seconds = 0
        if len(word.split(" ")) > 1:
            if word.split(" ")[1] == "mins":
                seconds = More_Functions.to_seconds("0:" + word.split(" ")[0])
            elif word.split(" ")[1] == "hour" or word.split(" ")[1] == "hours":
                seconds = More_Functions.to_seconds(word.split(" ")[0])
        return int(seconds)

    @staticmethod
    def get_number_of_days(year, month):
        try:
            month = month.lower()
        except:pass
        if month == "feb" or month == 2:
            return 29 if More_Functions.is_leap(year) else 28
        elif (month == "sep" or month == 9) or (month == "apr" or month == 4) or (month == "jun" or month == 6) or (month == "nov" or month == 11):
            return 30
        else:
            return 31

    @staticmethod
    def is_leap(year):
        return (year%4 == 0 and (year%100 != 0 or year%400 == 0))

    @staticmethod
    def get_month_name_array(start = "jan"):
        try:
            start = start.title()
            isDigit = False
        except:isDigit = True
        array = []
        found = False
        for i, month in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
            if isDigit and (found or i >= start):
                found = True
                array.append(month)
            elif isDigit == False and (month == start or found):
                found = True
                array.append(month)
        return array

    @staticmethod
    def get_days_array(year, month, current_day = 1):
        array = []
        for n in range(current_day, More_Functions.get_number_of_days(year, month) + 1):
            array.append(More_Functions.zero_format(n))
        return array

    def save(self):
        self.save_load.set_path( _main_path + "/AppData/Roaming/BE Softwares/Timetable")
        self.save_load.set_file_name("helping data.byke")
        self.save_load.save({"rooms":self.get_rooms(), "courses":self.get_all_courses()})
    
    def load(self):
        self.save_load.set_path( _main_path + "/AppData/Roaming/BE Softwares/Timetable")
        self.save_load.set_file_name("helping data.byke")
        data = self.save_load.load()
        if data is not None:
            self.get_rooms().clear()
            self.get_all_courses().clear()
            self.get_rooms().extend(data["rooms"])
            self.get_all_courses().extend(data["courses"])





class Login_State:
    def __init__(self):
        self.id_text = ""
        self.password_text = ""
        self.forget_btn_shown = False
        self.forgot_password_label_shown = False

    def set_state(self, id, password, forg_btn, forg_lbl):
        self.id_text = id
        self.password_text = password
        self.forget_btn_shown = forg_btn
        self.forgot_password_label_shown = forg_lbl

    def get_state(self):
        return [self.id_text, self.password_text, self.forget_btn_shown, self.forgot_password_label_shown]











class Timetable_Object:
    def __init__(self, course_name, room, time):
        self.set_course_name(course_name)
        self.set_room(room)
        self.set_time(time)
        self.notes = "Notes:"
        self.notes_privacy = "public"
        self.lectures = []
        self.room_abreviation = val = ""
        self.course_learn_time_counter = 0

    def set_notes(self, val):
        self.notes = val

    def set_notes_privacy(self, val):
        self.notes_privacy = val.lower()

    def set_course_name(self, course_name):
        self.course_name = course_name

    def set_room(self, room):
        self.room = room

    def set_room_abreviation(self, val):
        self.room_abreviation = val

    def set_counter(self, val):
        self.course_learn_time_counter = val

    def set_time(self, time):
        self.time = Day_Time(time.split(", ")[0], time.split(", ")[1])

    def set_lecture(self, lectures):
        self.lectures.extend(lectures)

    def get_course_name(self):
        return self.course_name.title()
    
    def get_room(self):
        return self.room

    def get_room_abreviation(self):
        return self.room_abreviation

    def get_time(self):
        return self.time

    def get_notes(self):
        return self.notes

    def get_notes_privacy(self):
        return self.notes_privacy.title()

    def get_counter(self):
        return self.course_learn_time_counter

    def get_lectures(self):
        names = ""
        for i, lecture in enumerate(self.lectures):
            names += lecture
            if len(self.lectures) > 1:
                if i == len(self.lectures) - 2:
                    names += " and "
                else:
                    names += ", " if i < len(self.lectures) - 2 else ""
        return names
    
    def lecture_len(self):
        return len(self.lectures)

    def add_lecture(self, lecture):
        self.lectures.append(lecture)

    def remove_lecture(self, lecture):
        self.remove(lecture)
        








class Timetable_Object_Data:
    def __init__(self):
        self.all_data = []
        self.save_load = Save_Load()
        self.class_start_time = 7 * 60 * 60
        self.period_duration = 3600

    def set_class_start_time(self, hour_minutes):
        if More_Functions.is_valid_time(hour_minutes):
            self.class_start_time = More_Functions.to_seconds(hour_minutes)

    def set_period_duration(self, seconds):
        self.period_duration = seconds
        
    def add_obj(self, obj):
        self.all_data.append(obj)

    def extend_obj(self, array):
        self.all_data.extend(array)

    def remove_item(self, obj):
        self.all_data.remove(obj)

    def remove_course(self, course_name, day_name, start_time):
        for data in self.get_all_data():
            if data.get_course_name().lower() == course_name.lower() and data.get_time().get_day_name().lower() == day_name.lower() and data.get_time().get_start_time() == start_time:
                self.remove_item(data)

    def get_all_data(self):
        return self.all_data

    def get_specific_object(self, start_time, day, duration):
        sec = More_Functions.to_seconds
        for obj in self.all_data:
            if(sec(obj.get_time().get_start_time()) >= sec(start_time) and sec(obj.get_time().get_start_time()) < sec(start_time)+duration) and obj.get_time().get_day_name().lower() == day.lower():
                return obj
        return None

    def get_all_in_day(self, day_name):
        data = []
        for obj in self.all_data:
            if obj.get_time().get_day_name().lower() == day_name.lower():
                data.append(obj)
        return data

    def get_class_start_time(self):
        return self.class_start_time

    def get_period_duration(self):
        return self.period_duration

    def replace_object(self, obj):
        for object_data in self.get_all_data():
            if (object_data.get_course_name() == obj.get_course_name() and object_data.get_time().get_time() == obj.get_time().get_time() and 
                object_data.get_time().get_day_name() == obj.get_time().get_day_name()):
                self.all_data.remove(object_data)
                self.add_obj(obj)
                print("Replaced")

    def save(self):
        self.save_load.set_path( _main_path + "/AppData/Roaming/BE Softwares/Timetable")
        self.save_load.set_file_name("timetable_objects.byke")
        self.save_load.save({"objects":self.get_all_data()})
    
    def load(self):
        self.save_load.set_path( _main_path + "/AppData/Roaming/BE Softwares/Timetable")
        self.save_load.set_file_name("timetable_objects.byke")
        data = self.save_load.load()
        if data is not None:
            self.all_data.clear()
            self.extend_obj(data["objects"])
            









class Day_Time:
    def __init__(self, day_name, time):
        self.set_day_name(day_name)
        self.set_time(time)
        self.date = [14, 4, 2021]

    def set_day_name(self, day_name):
        self.day_name = More_Functions.get_full_day_name(day_name)

    def _set_start_time(self, start_time):
        self.start_time = start_time

    def _set_end_time(self, end_time):
        self.end_time = end_time

    def _set_day_date(self, day):
        if day <= 31 and day > 0:
            self.date[0] = day

    def _set_month_date(self, month):
        if month > 0 and month <= 12:
            self.date[1] = month

    def _set_year_date(self, year):
        self.date[2] = year

    def set_date(self, date):
        self._set_day_date(date.split("-")[0])
        self._set_month_date(date.split("-")[1])
        self._set_year_date(date.split("-")[2])

    def _get_day_date(self):
        return self.date[0]

    def _get_month_date(self):
        return self.date[1]

    def _get_year_date(self):
        return self.date[2]

    def get_date(self):
        return self.date

    def get_day_name(self):
        return self.day_name

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_time(self):
        return f"{self.start_time}-{self.end_time}"

    def set_time(self, time):
        if len(time) > 0:
            if time.count("-") > 0:
                self._set_start_time(time.split("-")[0])
                self._set_end_time(time.split("-")[1])
            else:
                self._set_start_time(time)
                self._set_end_time("0")
        else:
            self._set_start_time("0")
            self._set_end_time("0")

    
    def __eq__(self, obj):
        return More_Functions.to_seconds(self.get_start_time()) == More_Functions.to_seconds(obj.get_start_time()) and More_Functions.to_seconds(self.get_end_time()) == More_Functions.to_seconds(obj.get_end_time()) and self.get_day_name().lower() == self.get_day_name().lower()        
        

class Remainder:
    def __init__(self, content = ""):
        self.set_content(content)
        self.remainder_date = ""
        self.remainder_time = ""
        self.repeate_count = 0
        self.repeate_duration = 180
        self.ringtone = ""

    def set_content(self, val):
        if val.strip() != "":
            self.content = val
        else:
            self.content = "nothing here"

    def set_remainder_date(self, year, month, day):
        self.remainder_date = f"{day}-{month}-{year}"

    def set_remainder_time(self, hour, minute):
        self.remainder_time = f"{hour}:{minute}"

    def set_repeate_count(self, count):
        self.repeate_count = count

    def set_repeate_duration(self, duration):
        self.repeate_duration = duration

    def set_rington(self, ringtone):
        self.ringtone = ringtone

    def get_content(self):
        return self.content

    def get_remainder_date(self):
        return self.remainder_date

    def get_remainder_time(self):
        return self.remainder_time

    def get_repeate_count(self):
        return self.repeate_count

    def get_repeate_duration(self):
        return self.repeate_duration

    def get_rington(self):
        return self.ringtone

    def update_remainder(self):
        self.repeate_count -= 1
        new_time = More_Functions.add_seconds(More_Functions.to_seconds(self.get_remainder_time()), self.get_repeate_duration())
        if new_time[0] <= 0:
            self.set_remainder_time(f"{More_Functions.zero_format(new_time[1])}", f"{More_Functions.zero_format(new_time[2] + round(new_time[3]/60))}")
    
class Portal_Activity:
    def __init__(self, division, group):
        self.division = division
        self.group = group
        self.content = ""
    
    def set_division(self, division):
        self.division = division

    def set_group(self, group):
        self.group = group

    def set_content(self, content):
        self.content = content

    def get_divison(self):
        return self.division

    def get_group(self):
        return self.group

    def get_content(self):
        return self.content


class Portal_Activities:
    def __init__(self):
        self.all_activities = []
        self.save_load = Save_Load()

    def add_portal_activity(self, portal_activity):
        self.all_activities.append(portal_activity)

    def extend_activities(self, array):
        self.all_activities.extend(array)

    def get_all_activities(self):
        return self.all_activities

    def get_group_activities(self, group_name, division_name):
        array = []
        for activity in self.all_activities:
            if activity.get_group().lower() == group_name.lower() and (division_name.lower() == "all" or activity.get_divison().lower() == division_name.lower()):
                array.append(activity)
        return array

    def get_group_activity_names(self, division_name):
        array = []
        for activity in self.all_activities:
            if activity.get_group() not in array and (division_name.lower() == "all" or activity.get_divison().lower() == division_name.lower()):
                array.append(activity.get_group())
        return array

    def get_divison_activities(self, division_name):
        array = []
        for activity in self.all_activities:
            if activity.get_divison().lower() == division_name.lower():
                array.append(activity)
        return array

    def get_divison_activity_names(self):
        array = []
        for activity in self.all_activities:
            if activity.get_divison() not in array:
                array.append(activity.get_divison())
        array.append("All")
        return array

    def save(self):
        self.save_load.set_path( _main_path + "/AppData/Roaming/BE Softwares/Timetable")
        self.save_load.set_file_name("Portal Activities.byke")
        self.save_load.save({"activities":self.get_all_activities()})
    
    def load(self):
        self.save_load.set_path( _main_path + "/AppData/Roaming/BE Softwares/Timetable")
        self.save_load.set_file_name("Portal Activities.byke")
        data = self.save_load.load()
        if data is not None:
            self.all_activities.clear()
            self.extend_activities(data["activities"])

class Settings:
    def __init__(self):
        self.privacy = "public"
        self.view = "weekly"
        self.background_color = "lightblue"
        self.show_empty_spaces = True
        self.number_of_empty_spaces = 15

    def set_view(self, val):
        self.view = val

    def set_privacy(self, val):
        self.privacy = val

    def set_background_color(self, color):
        self.background_color = color
    
    def set_show_empty_spaces(self, show_space_bool):
        self.show_empty_spaces = show_space_bool

    def set_number_of_empty_spaces(self, number):
        self.number_of_empty_spaces = number

    def get_view(self):
        return self.view

    def get_privacy(self):
        return self.privacy

    def get_background_color(self):
        return self.background_color

    def get_show_empty_spaces(self):
        return self.show_empty_spaces
    
    def get_number_of_empty_spaces(self):
        return self.number_of_empty_spaces



class Message:
    def __init__(self, sender_id, receiver_id, content):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.time_date = Message_Time()
    
    def get_sender(self):
        return self.sender_id

    def get_receiver(self):
        return self.receiver_id

    def get_content(self):
        return self.content

class Message_Options:
    def __init__(self):
        self.all_messages = []
        self.save_load = Save_Load()
        self.load()
        self.message_count = len(self.all_messages)

    def send_message(self, message, user):
        user.add_message(message)
        self.all_messages.append(message)
        self.message_count = len(self.all_messages)
        self.save()

    def receive_messages(self, user, time_date):
        messages = self.get_messages(user.security.get_username(), time_date)
        user.extend_messages(messages)
        self.message_count = len(self.all_messages)
        return len(messages)

    def get_messages(self, current_user_id, time_date):
        array = []
        i = len(self.all_messages) // 2
        while i >= 0:
            for message in self.all_messages:
                if message.get_receiver().lower() == current_user_id.lower():
                    message.time_date.set_receive_date(time_date.date())
                    message.time_date.set_receive_time(f"{time_date.hour}:{time_date.minute}:{time_date.second}")
                    array.append(message)
                    self.all_messages.remove(message)
            i -= 1
        self.save()
        return array
    
    def message_len_changes(self):
        return False
        self.load()
        if self.message_count != len(self.all_messages):
            self.message_count = len(self.all_messages)
            return True
        return False

    def save(self):
        self.save_load.set_path( _main_path + "/AppData/Roaming/BE Softwares/Timetable/Messages")
        self.save_load.set_file_name("all_messages.byke")
        self.save_load.save({"messages":self.all_messages})
    
    def load(self):
        self.save_load.set_path( _main_path + "/AppData/Roaming/BE Softwares/Timetable/Messages")
        self.save_load.set_file_name("all_messages.byke")
        data = self.save_load.load()
        if data is not None:
            self.all_messages.extend(data["messages"])



class Message_Time:
    def __init__(self):
        self.sent_time = ""
        self.receive_time = ""
        self.sent_date = ""
        self.receive_date = ""

    def set_sent_time(self, time):
        self.sent_time = time

    def set_receive_time(self, time):
        self.receive_time = time

    def set_sent_date(self, date):
        self.sent_date = date

    def set_receive_date(self, date):
        self.receive_date = date

    def get_sent_time(self):
        return self.sent_time

    def get_receive_time(self):
        return self.receive_time

    def get_sent_date(self):
        return self.sent_date

    def get_receive_date(self):
        return self.receive_date

class Message_Coordinate:
    def __init__(self):
        self.start_y_coordinate = 5
        self.friend_name = ""
    
    def get_y_start_coordinate(self):
        return self.start_y_coordinate

    def get_friend_name(self):
        return self.friend_name
    
    def set_y_coordinate(self, int_val):
        self.start_y_coordinate = int_val

    def set_friend_name(self, name):
        self.friend_name = name

class User_Message_Coordinates:
    def __init__(self):
        self.all_coordinates = []

    def add_coordinate(self, message_coor):
        for coordinate in self.all_coordinates:
            if coordinate.get_friend_name().lower() == message_coor.get_friend_name().lower():
                self.all_coordinates.remove(coordinate)
        self.all_coordinates.append(message_coor)

    def get_coordinate(self, friend_name):
        for coordinate in self.all_coordinates:
            if coordinate.get_friend_name().lower() == friend_name.lower():
                return coordinate
        return Message_Coordinate()



class Time_Table_Row_Manager:
    def __init__(self):
        self.counter = 0
        self.all_row_time = [[]]

    def get_row(self, start_time, show_blank_space, class_start, duration):
        if show_blank_space:
            i = -1
            sec = More_Functions.to_seconds
            if (sec(start_time) >= class_start) or (sec(start_time) <= (class_start + duration)) == False:
                i = 0
            while (sec(start_time) >= class_start) and (sec(start_time) < (class_start + duration)) == False:
                class_start += duration
                i += 1
            return (i, True)
        else:
            for data in self.all_row_time:
                if start_time in data:
                    return (data[1], False)
            self.all_row_time.append([start_time, self.counter])
            self.counter += 1
            return (self.counter - 1, True)

    def get_start_time(self, row, show_blank_space, class_start, duration):
        if show_blank_space:
            return More_Functions.from_seconds((row * duration ) + class_start)[0]
        else:
            for data in self.all_row_time:
                if row in data:
                    return data[0]
            return -1

    def clear_data(self):
        self.all_row_time.clear()
        self.counter = 0





class Save_Load:
    def __init__(self):
        self.path = _main_path + "/AppData/Roaming/BE Softwares/Timetable"
        self.file_name = "Data.byke"

    def get_path(self):
        os.makedirs(self.path, exist_ok=True)
        return self.path

    def set_path(self, val):
        self.path = val

    def set_file_name(self, val):
        self.file_name = val

    def get_file_name(self):
        return self.file_name

    def save(self, files):
        try:
            data_save = open(f"{self.get_path()}/{self.get_file_name()}", "wb")
            pickle.dump(files, data_save)
            data_save.close()
        except: print("Save Failed")

    def load(self):
        try:
            data_load = open(f"{self.get_path()}/{self.get_file_name()}", "rb")
            data = pickle.load(data_load)
            data_load.close()
            return data
        except: print("Load Failed")
        return None

    




_main_path = os.path.expanduser("~").replace("\\", "/")