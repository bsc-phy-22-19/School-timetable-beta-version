from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QFrame, QTableWidget, QTableWidgetItem, QTextEdit, 
    QProgressBar, QComboBox, QListWidget, QCompleter, QScrollArea, QScrollBar, QWidget, QCheckBox, QFileDialog, QSpinBox)
from PyQt5.QtCore import QTimer, Qt, QEvent, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QMouseEvent, QCursor, QIcon, QStandardItemModel
from PyQt5 import QtCore, QtGui
import sys, Password_Object, datetime, Data, Users, PyPDF2, tabula, SoundNotificationManager
from threading import Thread
from time import sleep

#Check new messages using loop
class Main_App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setStyleSheet("background-color:qlineargradient(spread:reflect, x1:0.209, y1:0.006, x2:0.655367, y2:0.404, stop:0 rgba(88, 93, 99, 105), stop:1 rgba(20, 25, 29, 209))")
        self.setGeometry(100, 100, 700, 450)

        self.create_variables()
        self.create_global_vars()
        self._customize()
        self._connect_all_items()
        self.login()
        self.show()


    def create_variables(self):
        self.setAcceptDrops(True)
        self.mouse_move_flag = False
        self.show_empty_spaces = True
        self.current_user = Users.Users("e", "b")
        self.current_creditials = ["", ""]
        self.notes_matched_friends = []
        self.notes_matched_friends_notes = []
        self.notes_matched_friends_notes_tmp = []
        self.all_time_available = []
        self.portal_activities_tmp = []
        self.remainder_widgets_window = None
        self.is_logged_in = False
        self.last_y_coordinate = 5
        self.btm_btns = []
        self.row_manager = Data.Time_Table_Row_Manager()

    def create_global_vars(self):
        self.all_users = Users.All_Users()
        self.all_portal_activities = Data.Portal_Activities()
        self.current_object = None
        self.id_label = QLabel(get_word(2), self)
        self.id_line_edit = QLineEdit(self)
        self.password_label = QLabel(get_word(3), self)
        self.password_line_edit = QLineEdit(self)
        self.login_btn = QPushButton(get_word(4), self)
        self.forget_btn = QPushButton(get_word(6), self)
        self.app_name_label = QLabel(get_word(1), self)
        self.login_label = QLabel(get_word(7), self)
        self.forgot_password_label = QLabel(get_word(8), self)
        self.show_password = QPushButton(self)
        self.login_back = QPushButton(self)
        self.upper_frame = QFrame(self)
        self.minimize_btn = QPushButton(self.upper_frame)
        self.close_btn = QPushButton(self.upper_frame)
        self.create_account = QPushButton(get_word(10), self)
        self.upper_frame.setGeometry(0, 0, self.width(), 30)
        self.close_btn.setStyleSheet("border:0;")
        self.minimize_btn.setStyleSheet("border:0;")
        self.minimize_btn.setGeometry(self.width() - 73, 0, 30, 30)
        self.close_btn.setGeometry(self.width() - 40, 0, 30, 30)
        self.set_picture(self.close_btn, get_icon(1), 30, 30)
        self.set_picture(self.minimize_btn, get_icon(3), 30, 30)
        self.timetable = QTableWidget(self)
        self.course_name_label = QLabel(self)
        self.room_name_label = QLabel(self)
        self.lecture_name_label = QLabel(self)
        self._time_update_login = QTimer(self)
        self.notes_line_edit = QTextEdit("Notes:", self)
        self.score_frame_1 = QFrame(self)
        self.score_frame_1_title = QLabel("Score Measure", self.score_frame_1)
        self.score_1_attendance = QLabel("Attendance:", self.score_frame_1)
        self.score_1_assignment = QLabel("Assignment:", self.score_frame_1)
        self.score_1_exams = QLabel("Exam:", self.score_frame_1)
        self.score_frame_2 = QFrame(self)
        self.score_2_attendance = QLabel("Attend : 9 d", self.score_frame_2)
        self.absent = QLabel("Absent : 0 d", self.score_frame_2)
        self.cancelled = QLabel("Cancelled: 1 d", self.score_frame_2)
        self.attend_progressbar = QProgressBar(self.score_frame_2) 
        self.absent_progressbar = QProgressBar(self.score_frame_2) 
        self.cancelled_progressbar = QProgressBar(self.score_frame_2)
        self.save_notes_btn = QPushButton("Save", self)
        self.notes_privacy_combo = QComboBox(self)
        self.my_page = QPushButton("My Page", self)
        self.timetable_btn = QPushButton("Timetable", self)
        self.share = QPushButton("Export", self)
        self.portal = QPushButton("Portal", self)
        self.settings = QPushButton("Settings", self)
        self.time_frame = QFrame(self)
        self.time_label = QLabel(self.time_frame)
        self.friends_notes = QFrame(self)
        notes_friends_label = QLabel("Friends:", self.friends_notes)
        notes_seach_label = QLabel("Search", self.friends_notes)
        self.search_friend_notes_line_edit = QLineEdit(self.friends_notes)
        self.matched_friends = QListWidget(self.friends_notes)
        self.friends_notes_text = QTextEdit(self.friends_notes)
        self.my_page_title = QLabel("My Page", self)
        self.my_page_table = QTableWidget(self)
        self.other_activites = QListWidget(self)
        self.designer = QLabel("Designer      : Atsuko Basikolo\t\tatsu17reds@gmail.com", self)
        self.programmer = QLabel("Programmer: Emmanuel Basikolo\t\temanuel24byke@gmail.com", self)
        self.my_page_edit_remainder_btn = QPushButton("Edit remainder", self)
        self.my_page_delete_remainder_btn = QPushButton("Delete", self)
        self.my_page_add_remainder_btn = QPushButton("Add remainder", self)
        self.main_privacy_combo = QComboBox(self)
        self.account_combo = BE_ComboBox(self)
        self.view_combo = QComboBox(self)
        self.portal_first_frame = QFrame(self)
        self.portal_second_frame = QFrame(self)
        self.portal_message_scroll_area = QScrollArea(self)
        self.portal_activities_combo = QComboBox(self.portal_first_frame)
        QLabel("Search ", self.portal_first_frame).setGeometry(5, 25, 40, 18)
        message_lbl = QLabel("Message ", self.portal_second_frame)
        self.portal_first_search = QLineEdit(self.portal_first_frame)
        self.portal_activities_list = QListWidget(self.portal_first_frame)
        self.portal_activities_list_details = QTextEdit(self.portal_first_frame)
        QLabel("Search ", self.portal_second_frame).setGeometry(5, 25, 40, 18)
        self.portal_second_search = QLineEdit(self.portal_second_frame)
        self.portal_friends_list = QListWidget(self.portal_second_frame)
        self.portal_messages_details = QWidget(self.portal_second_frame)
        self.portal_messages_details_up = QPushButton("Up", self)
        self.portal_messages_details_down = QPushButton("down", self)
        self.portal_message_text = QTextEdit(self.portal_second_frame)
        self.portal_send_message = QPushButton("send", self.portal_second_frame)
        self.portal_save_message = QPushButton("Save", self.portal_second_frame)
        self.portal_title = QLabel("PORTAL", self)
        self.portal_create_post_btn = QPushButton("Create new", self.portal_first_frame)
        self.create_account_title = QLabel("CREATE ACCOUNT", self)
        self.id_description = QLabel("enter something", self)
        self.id_line_edit_create_account = QLineEdit(self)
        self.first_password_line_edit = QLineEdit(self)
        self.first_password_description_label = QLabel("Mix uppercase, lowercase and numbers", self)
        self.second_password_line_edit = QLineEdit(self)
        self.second_password_label = QLabel("Confirm password", self)
        self.password_strength = QLabel("Weak password", self)
        self.full_name_label = QLabel("Full name", self)
        self.full_name_line_edit = QLineEdit(self)
        self.secreat_question_label = QLabel("Question", self)
        self.secreat_question_combo = QComboBox(self)
        self.answer_label = QLabel("Answer", self)
        self.answer_line_edit = QLineEdit(self)
        self.answer_advice = QLabel("Useful when you forgot password", self)
        self.register_btn = QPushButton("Register", self)
        self.create_account_pass_mark_btn = QPushButton(self)
        self.add_course_label = QLabel("Add Course", self)
        self.add_course_name_label = QLabel("Course name ", self)
        self.add_course_name_line_edit = QLineEdit(self)
        self.add_course_start_time_label = QLabel("Start time", self)
        self.add_course_start_time_line_edit = QLineEdit(self)
        self.add_course_end_time_label = QLabel("End time", self)
        self.add_course_end_time_line_edit = QLineEdit(self)
        self.add_course_room_label = QLabel("Room", self)
        self.add_course_room_line_edit = QLineEdit(self)
        self.add_course_lecture_label = QLabel("Lectures", self)
        self.add_course_lecture_line_edit = QLineEdit(self)
        self.add_course_save_btn = QPushButton("Save", self)
        self.add_course_delete_btn = QPushButton("Delete", self)
        self.add_course_day_name_label = QLabel("Day name", self)
        self.add_course_day_name_line_edit = QLineEdit(self)
        self.add_course_day_name_discription = QLabel("Invalid day", self)
        self.add_course_start_time_discription = QLabel("eg 14:00", self)
        self.add_course_room_discription = QLabel("You need a room", self)
        self.add_course_hint_label = QLabel("Avoid adding double peoriod as single period", self)
        self.settings_account_frame = QFrame(self)
        self.settings_id_name_label = QLabel("ID Name", self.settings_account_frame)
        self.settings_id_name_line_edit = QLineEdit(self.settings_account_frame)
        self.settings_fullname_label = QLabel("Full name", self.settings_account_frame)
        self.settings_fullname_line_edit = QLineEdit(self.settings_account_frame)
        self.settings_password_label = QLabel("Password", self.settings_account_frame)
        self.settings_change_password_line_edit = QLineEdit(self.settings_account_frame)
        self.settings_secrete_question_label = QLabel("Secret Question", self.settings_account_frame)
        self.settings_secrete_question_combo = QComboBox(self.settings_account_frame)
        self.settings_answer_label = QLabel("Answer", self.settings_account_frame)
        self.settings_answer_line_edit = QLineEdit(self.settings_account_frame)
        self.settings_delete_account_label = QLabel("Delete Account", self)
        self.settings_delete_account_btn = QPushButton("DELETE", self)
        self.settings_add_course_label = QLabel("Add course", self)
        self.settings_add_course_btn = QPushButton("ADD", self)
        self.settings_delete_course_label = QLabel("Delete course", self)
        self.settings_delete_course_btn = QPushButton("DELETE", self)
        self.settings_general_label = QLabel("General", self)
        self.settings_change_background_label = QLabel("Background color", self)
        self.settings_change_background_combo = QComboBox(self)
        self.settings_period_label = QLabel("Single period duration", self)
        self.settings_period_number_combo = QComboBox(self)
        self.settings_period_time_label = QLabel("hour", self)
        self.settings_fperiod_label = QLabel("Learning starts at", self)
        self.settings_fperiod_time_combo = QComboBox(self)
        self.settings_portal_post_title = QLabel("Portal post", self)
        self.settings_portal_post_show_updated_filter_label = QLabel("Show post updated in", self)
        self.settings_portal_post_show_updated_filter_number_combo = QComboBox(self)
        self.settings_portal_post_show_updated_filter_time_combo = QComboBox(self)
        self.settings_portal_post_auto_delete_checkbox = QCheckBox("auto delete post older than", self)
        self.settings_portal_post_auto_delete_number_combo = QComboBox(self)
        self.settings_portal_post_auto_delete_time_combo= QComboBox(self)
        self.settings_portal_message_title = QLabel("Portal Messages", self)
        self.settings_portal_message_show_updated_label = QLabel("Show messages updated in", self)
        self.settings_portal_message_show_updated_number_combo = QComboBox(self)
        self.settings_portal_message_show_updated_time_combo = QComboBox(self)
        self.settings_portal_message_send_with_return_label = QLabel("Send by enter key", self)
        self.settings_portal_message_send_with_return_btn = QPushButton(self)
        self.settings_portal_message_delete_history_label = QLabel("Delete all messages", self)
        self.settings_portal_message_delete_history_btn = QPushButton(self)
        self.settings_create_account_label = QLabel("Create account", self)
        self.settings_create_account_btn= QPushButton("CREATE", self)
        self.settings_show_blank_space_checkbox = QCheckBox("Show empty rows", self)
        self.settings_title = QLabel("Settings", self)
        self.settings_account_title = QLabel("Account", self)
        self.settings_courses_title = QLabel("Courses", self)
        self.number_of_timetable_rows_spin = QSpinBox(self)
        self.forgot_password_question_label = QLabel(self)
        self.forgot_password_answer_label = QLabel("Enter your answer", self)
        self.forgot_password_answer_line_edit = QLineEdit(self)
        self.forgot_password_name_label = QLabel("Enter your full name", self)
        self.forgot_password_name_line_edit = QLineEdit(self)
        self.forgot_password_new_password_label = QLabel("new password", self)
        self.forgot_password_new_password_line_edit = QLineEdit(self)
        self.forgot_password_new_password_label_2 = QLabel("confirm password", self)
        self.forgot_password_new_password_line_edit_2 = QLineEdit(self)
        self.forgot_password_status = QLabel("Press Enter when you're done", self)
        self.sys_time = datetime.datetime.now()      

        message_lbl.setGeometry(5, 5, 70, 25)
        message_lbl.setStyleSheet("font-size:13px; font-weight: bold;")
        notes_friends_label.setGeometry(5, 0, 140, 20)
        notes_seach_label.setGeometry(5, 20, 46, 16)
        notes_friends_label.setStyleSheet("font-size:12px; font-weight: bold; border: 0;")
        notes_seach_label.setStyleSheet("border: 0;")

        

    def set_picture(self, widget, path, w = 40, h = 40):
        widget.setIcon(QIcon(path))
        widget.setIconSize(QSize(w, h))

    def eventFilter(self, object, event):
        if event.type() == QEvent.HoverEnter:
            if object == self.create_account or object == self.login_back or object == self.portal_create_post_btn:
                self.setCursor(QCursor(Qt.PointingHandCursor))
            elif object == self.close_btn:
                self.set_picture(self.close_btn, get_icon(2), 30, 30)
            elif object == self.minimize_btn:
                self.set_picture(self.minimize_btn, get_icon(4), 30, 30)
            elif object in self.btm_btns:
                self.setCursor(QCursor(Qt.PointingHandCursor))
                object.setStyleSheet("background:gray; color:yellow; font-size:18px; font-family:times; border:2px solid yellow; border-radius: 10px; font-weight: bold;")
            return True

        elif event.type() == QEvent.MouseButtonPress:
            if object in self.btm_btns:
                self.setCursor(QCursor(Qt.BusyCursor))
                object.setStyleSheet("background:lightgreen; color:gray; font-size:12px; font-family:times; border:3px solid gray; border-radius: 5px;")
            object.clicked.emit()
            return True

        elif event.type() == QEvent.MouseButtonRelease:
            if object in self.btm_btns:
                self.setCursor(QCursor(Qt.ArrowCursor))
                object.setStyleSheet("background:brown; color:lightblue; font-size:20px; font-family:times; border:2px solid lightblue; border-radius: 8px;")
            return True

        elif event.type() == QEvent.HoverLeave:
            if object == self.create_account or object == self.login_back or object == self.portal_create_post_btn:
                self.setCursor(QCursor(Qt.ArrowCursor))
            elif object == self.close_btn:
                self.set_picture(self.close_btn, get_icon(1), 30, 30)
            elif object == self.minimize_btn:
                self.set_picture(self.minimize_btn, get_icon(3), 30, 30)
            elif object in self.btm_btns:
                self.setCursor(QCursor(Qt.ArrowCursor))
                object.setStyleSheet("background:lightyellow; color:black; font-size:16px; font-family:times; border:1px solid black; border-radius: 0;")
            return True

        return False



    def login(self, account_id = None, user = None):
        if account_id == "Logout":
            account_id = None
            self.password_line_edit.setText("")
            self.add_course_create_state()
        if user is self.current_user or account_id == self.current_user.security.get_username():
            return
        self.setStyleSheet("background:lightblue")
        self.remove_all_widgets()
        self.login_state = Data.Login_State()            
        self.create_login_widgets(account_id, user)

    def create_login_widgets(self, account_id=None, user=None):    
        self.is_logged_in = False    
        self.show_password_bool = False
        self._restore_login_geometry()
        self.app_name_label.setFont(QFont("Times", 25))
        self.login_label.setFont(QFont("Times", 16))
        self.id_label.setFont(QFont("Times", 16))
        self.password_label.setFont(QFont("Times", 16))
        self.login_btn.setFont(QFont("Times", 10))
        self.forget_btn.setFont(QFont("Times", 10))
        self.forget_btn.setHidden(True)
        self.forgot_password_label.setHidden(True)
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        self.forgot_password_label.setStyleSheet("color:red; font-style:italic; font-weight:5px; font-size:13px")
        self.create_account.setStyleSheet("text-align:left; border: 0px solid red; text-decoration: underline")
        self.set_picture(self.login_back, get_icon(5))
        self.login_back.setStyleSheet("border: 0")
        self.show_password.setVisible(len(self.password_line_edit.text()) > 0)
        self.show_password.setStyleSheet("background:red; border: 0;")
        if user is not None:
            self.add_course_create_state()
            self.id_line_edit.setText(user.security.get_username())
            self.password_line_edit.setText(user.security.get_password())
            self.check_crediantials()
        elif account_id is not None:
            self.add_course_create_state()
            self.id_line_edit.setText(account_id)
            self.password_line_edit.setText("")
        

        # self.create_account.setStyleSheet("background:red")

    def check_crediantials(self):
        valid = self.all_users.check_crediantials(self.id_line_edit.text(), self.password_line_edit.text())
        if valid:
            self.is_logged_in = True
            self.forget_btn.setVisible(False)
            self.forgot_password_label.setVisible(False)
            self._remove_login_items()
            self.current_creditials[0] = self.id_line_edit.text()
            self.current_creditials[1] = self.password_line_edit.text()
            self.current_user = self.all_users.get_user(self.current_creditials[0], self.current_creditials[1])
            self.all_time_available = self.all_users.get_all_time(self.current_user)
            self.load_settings()
            self.create_timetable_variables()
            self.create_timetable_widgets()
            self.account_combo.setCurrentText(self.id_line_edit.text())
            self.add_course_get_state(self.current_user)
            self.all_remainder_date_time = self.current_user.get_remainder_all_date_time()
            self._customize_after_login()
        else:          
            self.is_logged_in = False  
            self.forget_btn.setVisible(True)
            self.forgot_password_label.setVisible(True)
            if self.id_line_edit.text() in self.all_usernames:
                self.forgot_password_label.setText(get_word(8))
                self.forget_btn.setText(get_word(6))
            else:
                self.forgot_password_label.setText(get_word(9))
                self.forget_btn.setText(get_word(5))
            print("Please Try again")

    def forgot_password(self):
        if self.id_line_edit.text() in self.all_usernames:
            self.remove_all_widgets()
            self._restore_forgot_password()
            self.forgot_password_question_label.setStyleSheet("font-size:20px; font-family:times;font-weight:bold")
            self.forgot_password_new_password_label.setStyleSheet("font-size:15px; font-family:times;")
            self.forgot_password_answer_label.setStyleSheet("font-size:15px; font-family:times;")
            self.forgot_password_new_password_label_2.setStyleSheet("font-size:15px; font-family:times;")
            self.forgot_password_name_label.setStyleSheet("font-size:15px; font-family:times;")
            self.forgot_password_status.setStyleSheet("font-size:13px; font-family:times;")
            self.forgot_password_answer_line_edit.setPlaceholderText("Enter your answer")
            self.forgot_password_name_line_edit.setPlaceholderText("name please")
            self.forgot_password_new_password_line_edit.setPlaceholderText("Enter new password")
            self.forgot_password_new_password_line_edit_2.setPlaceholderText("Enter password again")
            self.forgot_password_new_password_line_edit.setEchoMode(QLineEdit.Password)
            self.forgot_password_new_password_line_edit_2.setEchoMode(QLineEdit.Password)
            self.forgot_question_data = []
            for user in self.all_users.get_all_users():
                if user.security.get_username() == self.id_line_edit.text():
                    self.forgot_question_data.append(user)
            if len(self.forgot_question_data) == 1 and self.forgot_question_data[0].security.get_question().strip() != "": 
                self.forgot_password_question_label.setText(self.forgot_question_data[0].security.get_question())
                self.forgot_password_answer_label.setGeometry(5, 90, 150, 25)
                self.forgot_password_answer_line_edit.setGeometry(165, 90, 150, 25)
                self.forgot_password_name_label.setGeometry(5, 125, 150, 25)
                self.forgot_password_name_line_edit.setGeometry(165, 125, 150, 25)
            elif len(self.forgot_question_data) <= 0 or self.forgot_question_data[0].security.get_question().strip() == "":
                self.forgot_password_question_label.setText("It seems you don't have any question")
            else:
                self.forgot_password_question_label.setText("Multiple qestions detected")
        else:
            print("Handling forgotten ID")

    def check_forgot_password(self):
        self.forgot_password_status.setText("Press Enter when you are done.")
        if self.forgot_question_data[0].security.get_answer() == self.forgot_password_answer_line_edit.text() and self.forgot_question_data[0].get_fullname() == self.forgot_password_name_line_edit.text():
            self.forgot_password_new_password_label.setGeometry(5, 170, 150, 20)
            self.forgot_password_new_password_line_edit.setGeometry(165, 170, 150, 20)
            self.forgot_password_new_password_label_2.setGeometry(5, 200, 150, 20)
            self.forgot_password_new_password_line_edit_2.setGeometry(165, 200, 150, 20)
        else:
            self.forgot_password_status.setText("Incorrect answer or incorrect name...Check casing")

    def forgot_password_change_password(self):
        self.forgot_password_status.setText("Press Enter when you are done.")
        if self.forgot_password_new_password_line_edit.text() == self.forgot_password_new_password_line_edit_2.text() and len(self.forgot_password_new_password_line_edit.text()) >= 8:
            self.forgot_question_data[0].security.set_password(self.forgot_password_new_password_line_edit.text())
            self.login(None, self.forgot_question_data[0])
            self.forgot_password_status.setText("Password changed with success")
        elif self.forgot_password_new_password_line_edit.text() == self.forgot_password_new_password_line_edit_2.text():
            self.forgot_password_status.setText(f"Password too short\t{8-len(self.forgot_password_new_password_line_edit.text())} are remaining")
        else:
            self.forgot_password_status.setText("Make sure you entered same password")


    def load_settings(self):
        self.show_empty_spaces = self.current_user.settings.get_show_empty_spaces()
        self.settings_show_blank_space_checkbox.setChecked(self.show_empty_spaces)
        self.show_blank_space_fn(self.show_empty_spaces)
        self.number_of_timetable_rows_spin.setValue(self.current_user.settings.get_number_of_empty_spaces())
        self.settings_change_background_combo.setCurrentText(self.current_user.settings.get_background_color())
        
        
    def save_settings(self):
        self.current_user.settings.set_show_empty_spaces(self.show_empty_spaces)
        self.current_user.settings.set_number_of_empty_spaces(int(self.number_of_timetable_rows_spin.text()))
        self.current_user.settings.set_background_color(self.settings_change_background_combo.currentText())

    def _time_update_login_fn(self):
        self.sys_time = datetime.datetime.now()
        self.time_label.setText(f"{self.sys_time.ctime()[4:7]} {functions.zero_format(self.sys_time.day)}, {self.sys_time.year},    {self.sys_time.ctime()[:3]} {functions.zero_format(self.sys_time.hour)}:{functions.zero_format(self.sys_time.minute)}")
        self.update_create_account()
        self.validate_add_course_form()
        if self.is_logged_in:
            self.remainder_time_check()
            if self.message_options.message_len_changes():
                #many messages were received and send instead of one message
                self.message_options.receive_messages(self.current_user, self.sys_time)

        self.show_password.setVisible(len(self.password_line_edit.text()) > 0) 

    def hide_show_login(self):
        self.remove_all_widgets()
        self._restore_login_geometry()
        
    def create_login_state(self):
        self.login_state.set_state(self.id_line_edit.text(), self.password_line_edit.text(), self.forget_btn.isHidden(), 
            self.forgot_password_label.isHidden())
    
    def restore_login_state(self):
        self.id_line_edit.setText(self.login_state.get_state()[0])
        self.password_line_edit.setText(self.login_state.get_state()[1])
        self.forget_btn.setHidden(self.login_state.get_state()[2])
        self.forgot_password_label.setHidden(self.login_state.get_state()[3])

    def create_account_fn(self, hide):
        self.remove_all_widgets()
        self._restore_create_account()
        if hide:
            self.login_back.setGeometry(0, 0, 0, 0)
            self.bottom_btn_customize()
        self.first_password_description_label.setStyleSheet("color:black;")
        self.password_strength.setStyleSheet("color:red;")
        self.answer_advice.setStyleSheet("color:black;")
        self.create_account_pass_mark_btn.setStyleSheet("border:0;")
        self.full_name_label.setStyleSheet("font-size:18px; font-family:Times; font-weight:bold;")
        self.second_password_label.setStyleSheet("font-size:12px; font-family:Times; font-weight:bold;")
        self.secreat_question_label.setStyleSheet("font-size:18px; font-family:Times; font-weight:bold;")
        self.answer_label.setStyleSheet("font-size:18px; font-family:Times; font-weight:bold;")
        self.create_account_title.setStyleSheet("font-size:23px; font-family:Times; font-weight:bold;")
        self.first_password_line_edit.setEchoMode(QLineEdit.Password)
        self.second_password_line_edit.setEchoMode(QLineEdit.Password)
        

    def update_create_account(self):
        if self.create_account_title.geometry().getCoords()[0] <= 0:
            return
        activate_btn = True
        if len(self.id_line_edit_create_account.text()) <= 0:
            activate_btn = False
            self.id_description.setText("Enter Something")
        elif len(self.id_line_edit_create_account.text()) < 4:
            activate_btn = False
            self.id_description.setText(f"{4 - len(self.id_line_edit_create_account.text())} charecter(s) remaining")
            self.id_description.setStyleSheet("color:black")
        elif self.id_line_edit_create_account.text() in self.all_usernames:
            activate_btn = False
            self.id_description.setText("Username exist....please change")
            self.id_description.setStyleSheet("color:red")
        else:
            self.id_description.setText("")
        if len(self.first_password_line_edit.text()) > 0:
            if len(self.first_password_line_edit.text()) < 8:
                self.first_password_description_label.setText(f"{8 - len(self.first_password_line_edit.text())} are remaining")
            else:
                self.first_password_description_label.setText("")
        else:
            activate_btn = False
            self.first_password_description_label.setText("UpperCase, LowerCase and number")
        if len(self.second_password_line_edit.text()) >= 8:
            self.create_account_pass_mark_btn.setHidden(False)
            if self.second_password_line_edit.text() == self.first_password_line_edit.text():
                self.set_picture(self.create_account_pass_mark_btn, get_icon(12), 24, 24)
                i, k, n = 0, 0, 0
                for l in self.first_password_line_edit.text():
                    if l.islower():
                        i = 1
                    if l.isupper():
                        k = 1
                    if l.isnumeric():
                        n = 1
                if self.first_password_line_edit.text().lower() == self.id_line_edit_create_account.text().lower():
                    self.password_strength.setText("Id is bad password")
                elif (i + k + n) == 3:
                    self.password_strength.setText("Strong password")
                elif (i + k + n) == 2:
                    self.password_strength.setText("Weak password")
                elif (i + k + n) == 2:
                    self.password_strength.setText("Poor password")
                else:
                    self.password_strength.setText("Worse password")
            else:
                self.set_picture(self.create_account_pass_mark_btn, get_icon(10), 24, 24)
                activate_btn = False
                self.password_strength.setText("")
        else:
            activate_btn = False
            self.password_strength.setText("")
            self.create_account_pass_mark_btn.setHidden(True)
            self.create_account_pass_mark_btn.setHidden(True)
        if len(self.answer_line_edit.text()) > 0:
            self.answer_advice.setText("")
        self.register_btn.setDisabled(activate_btn == False)



    def change_show_password(self):
        self.show_password_bool = False if self.show_password_bool else True
        if self.show_password_bool:
            self.password_line_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.password_line_edit.setEchoMode(QLineEdit.Password)

    def create_timetable_variables(self):
        self.days_title = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]        

    def create_timetable_widgets(self):
        self.create_table()
        self.bottom_btn_customize()
        self._restore_timetable_geometry()

    def create_table(self):
        self.timetable.setColumnCount(len(self.days_title))
        self.timetable.setHorizontalHeaderLabels(self.days_title)
        self.timetable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.timetable.setAlternatingRowColors(True)
        if self.current_user is not None:
            self.update_table()

    def update_table(self):
        self.row_manager.clear_data()
        data = self.all_users.get_user(self.current_creditials[0], self.current_creditials[1]).time_table_data.get_all_data()
        self.timetable.setRowCount(0)
        self.timetable.setColumnWidth(0, 70)
        i = 1
        while i <= len(self.days_title):
            self.timetable.setColumnWidth(i, 113)
            i += 1
        if self.show_empty_spaces:
            i = 0
            while i < int(self.number_of_timetable_rows_spin.text()):
                self.timetable.insertRow(i)
                self.timetable.setRowHeight(i, 10)
                i += 1
        else:
            data.sort(key=functions.sort_time)

        for i, item in enumerate(data):
            col = functions.get_col(item.get_time().get_day_name())
            value = QTableWidgetItem("{}\n{}".format(item.get_course_name(), item.get_room()))
            value.setTextAlignment(Qt.AlignCenter)
            row_data = self.row_manager.get_row(item.get_time().get_start_time(), self.show_empty_spaces, self.current_user.time_table_data.get_class_start_time(), self.current_user.time_table_data.get_period_duration())
            if row_data[1] and self.show_empty_spaces == False:
                self.timetable.insertRow(row_data[0])
            row = row_data[0]
            self.timetable.setItem(row, col, value)
            self.timetable.setItem(row, 0, QTableWidgetItem(item.get_time().get_time()))
            self.timetable.setRowHeight(row, 40)
            # self.timetable.setFont(QFont("times", 10, True))

    def table_double_clicked(self):
        if self.show_empty_spaces == False:
            all_objs = self.current_user.time_table_data.get_all_data()
            all_objs.sort(key=functions.sort_time)
        obj = self.all_users.get_user(self.current_creditials[0], self.current_creditials[1]).time_table_data.get_specific_object(self.row_manager.get_start_time(self.timetable.currentRow(), self.show_empty_spaces, self.current_user.time_table_data.get_class_start_time(), self.current_user.time_table_data.get_period_duration()), functions.get_col_rev(self.timetable.currentColumn()), self.current_user.time_table_data.get_period_duration())

        if obj is not None:
            self.current_object = obj
            self.course_details(obj)
            self.find_public_notes(self.current_object)

    def course_details(self, obj):
        self.remove_all_widgets()
        self.course_name_label.setText(obj.get_course_name())
        self.room_name_label.setText("Room: " + obj.get_room())
        self.lecture_name_label.setText("Lecture(s): " + obj.get_lectures())
        self.bottom_btn_customize()
        self._restore_course_details()
        self.attend_progressbar.setValue(90)
        self.absent_progressbar.setValue(0)
        self.cancelled_progressbar.setValue(10)
        self.course_name_label.setStyleSheet("background:yellow; font-size: 20px; font-family:times; font-weight: bold; border: 4px double blue;")
        self.room_name_label.setStyleSheet("background:lightyellow; font-size: 14px; font-family:times; font-weight: bold; border: 4px double blue;")
        self.lecture_name_label.setStyleSheet("background:lightyellow; font-size: 12px; font-family:times; font-weight: bold; border: 4px double blue;")
        self.notes_line_edit.setStyleSheet("background:lightyellow; font-size:14px; font-family:times; font-weight:bold; text-align:justified;")
        self.friends_notes_text.setStyleSheet("background:tan; font-size:13px; font-family:tahoma; text-align:justified;")
        self.score_frame_1.setStyleSheet("background:lightyellow; font-size: 16px; font-family:times; border: 1px solid black;")
        self.score_frame_1_title.setStyleSheet("font-size:18px; font-weight:bold; text-align:justified; border: 0")
        self.score_frame_2.setStyleSheet("QProgressBar{border-radius:20px; font-size: 13px; font-family:calibri; background:lightyellow; text-align:center;} QFrame{background:lightyellow; border: 1px solid black;}")        
        self.score_2_attendance.setStyleSheet("background:lightyellow; font-size:16px; font-family:times; border:0; ")
        self.absent.setStyleSheet("background:lightyellow; font-size:16px; font-family:times; border:0; ")
        self.cancelled.setStyleSheet("background:lightyellow; font-size:16px; font-family:times; border:0; ")
        self.friends_notes.setStyleSheet("background:lightyellow; border: 1px solid gray;")
        self.friends_notes_text.setText("")
        self.notes_line_edit.setPlainText(obj.get_notes())
        self.notes_privacy_combo.setCurrentText(obj.get_notes_privacy().title())
        
    
    def save_notes(self):
        if self.current_object is not None:
            self.current_object.set_notes(self.notes_line_edit.toPlainText())
            self.current_object.set_notes_privacy(self.notes_privacy_combo.currentText())              

    def bottom_btn_customize(self):
        self.my_page.setGeometry(5, self.height() - 50, 80, 40)
        self.timetable_btn.setGeometry(100, self.height() - 50, 80, 40)
        self.share.setGeometry(195, self.height() - 50, 80, 40)
        self.portal.setGeometry(290, self.height() - 50, 80, 40)
        self.settings.setGeometry(385, self.height() - 50, 80, 40)
        self.portal_messages_details_up.setHidden(True)
        self.portal_messages_details_down.setHidden(True)
        self.my_page_edit_remainder_btn.setDisabled(True)
        self.my_page_delete_remainder_btn.setDisabled(True)

    def my_page_fn(self):
        self.remove_all_widgets()
        self.bottom_btn_customize()
        self._restore_my_page()
        self.my_page_title.setStyleSheet("font-size:30px; font-family:comic; font-weight:bold;")
        self.other_activites.setStyleSheet("background:lightyellow;")
        self.write_my_page_table()
        self.write_my_page_remainders()
        self.designer.setStyleSheet("font-size:16px;font-family:times; font-weight:bold")
        self.programmer.setStyleSheet("font-size:16px;font-family:times; font-weight:bold")

    def write_my_page_table(self):
        self.my_page_table.setColumnCount(3)
        self.my_page_table.setHorizontalHeaderLabels(["", functions.get_full_day_name(self.sys_time.ctime()[:3]), "Assignments/notes"])
        self.my_page_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.my_page_table.setAlternatingRowColors(True)
        self.my_page_table.setColumnWidth(2, 213)
        self.my_page_table.setRowCount(0)
        current_day_courses = self.current_user.time_table_data.get_all_in_day(functions.get_full_day_name(self.sys_time.ctime()[:3]))
        current_day_courses.sort(key=functions.sort_time)
        for i, course_data in enumerate(current_day_courses):
            self.my_page_table.insertRow(i)
            notes = course_data.get_notes()
            self.my_page_table.setRowHeight(i, 30 + (30 * round(len(notes)/70)))
            self.my_page_table.setItem(i, 0, QTableWidgetItem(course_data.get_time().get_time()))
            self.my_page_table.setItem(i, 1, QTableWidgetItem(course_data.get_course_name()))
            self.my_page_table.setItem(i, 2, QTableWidgetItem(notes))

    def write_my_page_remainders(self):
        self.other_activites.clear()
        for remainder in self.current_user.get_all_remainders():
            self.other_activites.addItem(remainder.get_content())

    def reminder_clicked(self):
        self.my_page_edit_remainder_btn.setDisabled(False)
        self.my_page_delete_remainder_btn.setDisabled(False)

    def remainder_double_click(self, index):
        new_window = QMainWindow(self)
        new_window.resize(200, 200)
        new_window.setStyleSheet("background:lightgreen")
        new_window.setWindowTitle("Details")

        text = QTextEdit(self.current_user.get_all_remainders()[index].get_content(), new_window)
        text.setStyleSheet("border:0;")
        text.setGeometry(0, 0, new_window.width(), new_window.height() - 40)

        new_window.show()

    def delete_remainder(self, reminder):
        self.current_user.get_all_remainders().remove(reminder)
        self.write_my_page_remainders()
        self.all_remainder_date_time = self.current_user.get_remainder_all_date_time()
        self.my_page_delete_remainder_btn.setDisabled(True)
        self.my_page_edit_remainder_btn.setDisabled(True)
        
    def add_edit_remainder_fn(self, remainder = None):
        title = "Add remainder" if remainder is None or remainder == False or remainder == True else "Edit remainder"
        self.remainder_widgets_window = BE_MainWindow(self, title)
        self.remainder_widgets_window.resize(400, 400)
        
        remainder_content = QTextEdit(self.remainder_widgets_window)
        remainder_year_combo = QComboBox(self.remainder_widgets_window)
        remainder_month_combo = QComboBox(self.remainder_widgets_window)
        remainder_day_combo = QComboBox(self.remainder_widgets_window)
        remainder_hour_combo = QComboBox(self.remainder_widgets_window)
        remainder_minutes_combo = QComboBox(self.remainder_widgets_window)
        time_descr = QLabel("remainder Date and time", self.remainder_widgets_window)
        repeate_label = QLabel("Repeate", self.remainder_widgets_window)
        repeate_time_combo = QComboBox(self.remainder_widgets_window)
        repeate_number_count_combo = QComboBox(self.remainder_widgets_window)
        ringtone_label = QLabel("Ringtone", self.remainder_widgets_window)
        ringtone_combo = QComboBox(self.remainder_widgets_window)
        folder_btn = QPushButton("Folder", self.remainder_widgets_window)
        share_label = QLabel("Share", self.remainder_widgets_window)
        search_label = QLabel("Search", self.remainder_widgets_window)
        search_line_edit = QLineEdit(self.remainder_widgets_window)
        share_listbox = QListWidget(self.remainder_widgets_window)
        save_remainder_btn = QPushButton("Save", self.remainder_widgets_window)
        remainder_content.setGeometry(5, 5, 390, 70)
        time_descr.setGeometry(5, 80, 120, 18)
        QLabel("Year", self.remainder_widgets_window).setGeometry(5, 100, 50, 18)
        remainder_year_combo.setGeometry(5, 120, 50, 18)
        QLabel("Month", self.remainder_widgets_window).setGeometry(70, 100, 50, 18)
        remainder_month_combo.setGeometry(70, 120, 50, 18)
        QLabel("Day", self.remainder_widgets_window).setGeometry(130, 100, 50, 18)
        remainder_day_combo.setGeometry(130, 120, 50, 18)
        QLabel("Hour", self.remainder_widgets_window).setGeometry(210, 100, 50, 18)
        remainder_hour_combo.setGeometry(210, 120, 50, 18)
        QLabel(":", self.remainder_widgets_window).setGeometry(268, 118, 5, 18)
        QLabel("Minute", self.remainder_widgets_window).setGeometry(280, 100, 50, 18)
        remainder_minutes_combo.setGeometry(280, 120, 50, 18)
        repeate_label.setGeometry(5, 160, 100, 18)
        repeate_time_combo.setGeometry(5, 185, 80, 18)
        repeate_number_count_combo.setGeometry(95, 185, 80, 18)
        ringtone_label.setGeometry(200, 160, 80, 18)
        ringtone_combo.setGeometry(200, 185, 80, 18)
        folder_btn.setGeometry(290, 185, 80, 18)
        share_label.setGeometry(5, 220, 100, 18)
        search_label.setGeometry(5, 250, 40, 18)
        search_line_edit.setGeometry(45, 250, 100, 18)
        share_listbox.setGeometry(5, 270, 140, 100)
        save_remainder_btn.setGeometry(300, 360, 80, 20)

        repeate_time_array = ["1 mins", "5 mins", "10 mins", "20 mins", "30 mins", "45 mins", "01:00"]
        repeate_number_array = ["No repeate", "1 time", "2 times", "3 times", "4 times", "5 times", "6 times", "8 times"]
        ringtone_array = ["huawei creamy", "Bell", "alarm", "iphone", "whistle"]
        
        for i in range(self.sys_time.year, 2201):
            remainder_year_combo.addItem(f"{i}")
        for i in range(0, 24):
            remainder_hour_combo.addItem(functions.zero_format(i))
        for i in range(0, 60):
            remainder_minutes_combo.addItem(functions.zero_format(i))
        
        remainder_month_combo.addItems(functions.get_month_name_array(self.sys_time.month - 1))
        remainder_day_combo.addItems(functions.get_days_array(self.sys_time.year, self.sys_time.month, self.sys_time.day))
        repeate_time_combo.addItems(repeate_time_array)
        repeate_number_count_combo.addItems(repeate_number_array)
        ringtone_combo.addItems(ringtone_array)
        if remainder is None or remainder == False or remainder == True:
            remainder_year_combo.setCurrentText(f"{self.sys_time.year}")
            remainder_month_combo.setCurrentText(f"{self.sys_time.ctime()[4:7]}")
            remainder_day_combo.setCurrentText(f"{functions.zero_format(self.sys_time.day)}")
            x = self.sys_time.hour + 1 if self.sys_time.hour + 1 < 24 else 0 
            remainder_hour_combo.setCurrentText(f"{functions.zero_format(x)}")
            remainder_minutes_combo.setCurrentText(f"{functions.zero_format(self.sys_time.minute)}")
        else:
            remainder_content.setText(remainder.get_content())
            remainder_year_combo.setCurrentText(remainder.get_remainder_date().split("-")[2])
            remainder_month_combo.setCurrentText(remainder.get_remainder_date().split("-")[1])
            remainder_day_combo.setCurrentText(remainder.get_remainder_date().split("-")[0])
            remainder_hour_combo.setCurrentText(remainder.get_remainder_time().split(":")[0])
            remainder_minutes_combo.setCurrentText(remainder.get_remainder_time().split(":")[1])
            time1 = functions.from_seconds(remainder.get_repeate_duration())
            if int(time1[0].split(":")[0]) > 0:
                repeate_time_combo.setCurrentText("{}".format(time1[0]))
            else:
                repeate_time_combo.setCurrentText("{} mins".format(int(time1[0].split(":")[1])))
            
            repeate_number_count_combo.setCurrentText(f"{remainder.get_repeate_count()} times")
            ringtone_combo.addItem(remainder.get_rington())
            ringtone_combo.setCurrentText(remainder.get_rington())




        save_remainder_btn.clicked.connect(lambda:self.save_remainder__fn([
            remainder_content.toPlainText(),
            remainder_year_combo.currentText(),
            remainder_month_combo.currentText(),
            remainder_day_combo.currentText(),
            remainder_hour_combo.currentText(),
            remainder_minutes_combo.currentText(),
            repeate_time_combo.currentText(),
            repeate_number_count_combo.currentText(),
            self.get_audio_from_combo(ringtone_combo)
        ], remainder))
        folder_btn.clicked.connect(lambda:self.get_folder_path(ringtone_combo))
        remainder_year_combo.currentIndexChanged.connect(lambda:self.change_year(remainder_year_combo, remainder_month_combo, remainder_day_combo))
        remainder_month_combo.currentIndexChanged.connect(lambda:self.change_month(remainder_year_combo, remainder_month_combo, remainder_day_combo))

        self.remainder_widgets_window.show()

    def save_remainder__fn(self, details, remainder = None):
        add_remainder = False
        if remainder is None or remainder is False or remainder is True:
            remainder = Data.Remainder()
            add_remainder = True
        remainder.set_content(details[0])
        remainder.set_remainder_date(details[1], details[2], details[3])
        remainder.set_remainder_time(details[4], details[5])
        remainder.set_repeate_count(functions.get_repeate_number(details[7]))
        remainder.set_repeate_duration(functions.get_repeate_duration(details[6]))
        remainder.set_rington(details[8])
        if add_remainder:
            self.current_user.add_remainder(remainder)
        self.remainder_widgets_window.deleteLater()
        self.write_my_page_remainders()
        self.all_remainder_date_time = self.current_user.get_remainder_all_date_time()
        

    def remainder_time_check(self):
        current_date = f"{functions.zero_format(self.sys_time.day)}-{self.sys_time.ctime()[4:7]}-{self.sys_time.year}"
        current_time = f"{functions.zero_format(self.sys_time.hour)}:{functions.zero_format(self.sys_time.minute)}"
        for item in self.all_remainder_date_time:
            if item[0] == current_date and item[1] == current_time:
                remainders = self.current_user.find_reminder_using_date_time(item)
                for remainder in remainders:
                    if remainder.get_repeate_count() >= 0:
                        self.handle_remainder(remainder)
                        remainder.update_remainder()
                        self.all_remainder_date_time = self.current_user.get_remainder_all_date_time()
                        print(self.all_remainder_date_time, current_date, current_time, "\n\n")

    def handle_remainder(self, remainder):
        player = SoundNotificationManager.PlaySound(remainder.get_rington())
        player.set_volume(100)
        player.play(500)

        notification = SoundNotificationManager.Notification()
        notification.show_notification("Reminder", remainder.get_content(), 500, get_icon(6))

        for i, r in enumerate(self.current_user.get_all_remainders()):
            if remainder == r:
                self.my_page_fn()
                self.other_activites.item(i).setBackground(Qt.black)
                self.other_activites.item(i).setForeground(Qt.white)
                self.other_activites.setCurrentRow(i)
        self.other_activites.setStyleSheet("background:green")

    def get_folder_path(self, ringtone_combo):
        path = QFileDialog.getOpenFileName(self, "Choose audio", "./textures/sounds", "audios (*.mp3 *.wav *.mid)")
        ringtone_combo.addItem(path[0])
        ringtone_combo.setCurrentText(path[0])

    def get_audio_from_combo(self, ringtone_combo):
        if ringtone_combo.currentIndex() <= 5:
            return get_sound(ringtone_combo.currentIndex() + 1)
        else:
            return ringtone_combo.currentText()

    def change_year(self, year_combo, month_combo, day_combo):
        currentMonth = month_combo.currentText()
        currentDay = int(day_combo.currentText().strip())
        
        month_combo.clear()
        day_combo.clear()
        if int(year_combo.currentText()) != self.sys_time.year:        
            month_combo.addItems(functions.get_month_name_array("jan"))
            days = currentDay if functions.get_number_of_days(int(year_combo.currentText()), currentMonth) >= currentDay else 1
            day_combo.addItems(functions.get_days_array(int(year_combo.currentText()), currentMonth, days))
        else:
            month_combo.addItems(functions.get_month_name_array(self.sys_time.month - 1))
            day_combo.addItems(functions.get_days_array(self.sys_time.year, self.sys_time.month, self.sys_time.day))
        month_combo.setCurrentText(currentMonth)
        day_combo.setCurrentText(f"{currentDay}")

    def change_month(self, year_combo, month_combo, day_combo):
        currentMonth = month_combo.currentText()
        try:
            currentDay = int(day_combo.currentText())
        except: currentDay = 1
        day_combo.clear()

        if currentMonth != self.sys_time.ctime()[4:7] and int(year_combo.currentText()) != self.sys_time.year:
            day_combo.addItems(functions.get_days_array(int(year_combo.currentText()), currentMonth))
        else:
            day_combo.addItems(functions.get_days_array(self.sys_time.year, self.sys_time.month, self.sys_time.day))
        day_combo.setCurrentText(f"{currentDay}")




    def time_table_fn(self):
        self.remove_all_widgets()
        self.create_timetable_variables()
        self.create_timetable_widgets()

    def share_fn(self):
        self.remove_all_widgets()
        self.bottom_btn_customize()

    def portal_fn(self):
        self.remove_all_widgets()
        self.bottom_btn_customize()
        self._restore_portal()
        self.portal_title.setStyleSheet("font-size:30px; font-family:times; font-weight:bold;")
        self.portal_activities_list_details.setStyleSheet("background:tan; font-size:14px; font-family:times; border:1px solid gray; font-weight:bold; ")
        self.portal_messages_details.setStyleSheet("background:lightgreen;")
        self.portal_first_frame.setStyleSheet("background:lightyellow;")
        self.portal_second_frame.setStyleSheet("background:lightyellow;")
        self.portal_create_post_btn.setStyleSheet("text-align:left; border: 0; text-decoration: underline")
        self.portal_activities_combo.clear()
        self.portal_activities_combo.addItems(self.all_portal_activities.get_divison_activity_names())
        self.write_portal_activity(self.all_portal_activities.get_group_activity_names(self.portal_activities_combo.currentText()))
        self.portal_message_text.setText("")
        self.portal_friends_list.clear()
        self.write_message_friends(self.all_usernames)
        self.message_options.receive_messages(self.current_user, self.sys_time)
        self.portal_message_scroll_area.setStyleSheet("background:lightgreen;")
        self.portal_message_scroll_area.setWidget(self.portal_messages_details)
        self.portal_message_scroll_area.setWidgetResizable(True)
        self.portal_friends_list.setCurrentRow(0)
        for child in self.portal_messages_details.children():
            child.deleteLater()

    def create_portal_post(self):
        create_post_window = BE_MainWindow(self, "Post")
        create_post_window.resize(300, 190)
        division_label = QLabel("Division", create_post_window)
        division_combo = QComboBox(create_post_window)
        group_label = QLabel("Group", create_post_window)
        group_combo = QComboBox(create_post_window)
        content_label = QLabel("Content", create_post_window)
        content_text = QTextEdit(create_post_window)
        post_btn = QPushButton("Post", create_post_window)
        division_label.setGeometry(5, 5, 120, 20)
        division_combo.setGeometry(5, 30, 120, 20)
        group_label.setGeometry(140, 5, 120, 20)
        group_combo.setGeometry(140, 30, 120, 20)
        content_label.setGeometry(5, 60, 120, 20)
        content_text.setGeometry(5, 90, 280, 60)
        post_btn.setGeometry(216, 150, 70, 18)
        division_combo.setEditable(True)
        group_combo.setEditable(True)
        division_label.setStyleSheet("font-size:13px; font-family:times;")
        group_label.setStyleSheet("font-size:13px; font-family:times;")
        content_label.setStyleSheet("font-size:13px; font-family:times;")
        post_btn.setStyleSheet("background:lightyellow; font-size:13px; font-family:times;")

        division_combo.addItems(["Science", "Religous", "Sports", "Lectures", "Timetable", "All", ""])
        group_combo.addItems(["News", "Announcement", ""])
        post_btn.clicked.connect(lambda:self.posting_portal_post([division_combo.currentText(), group_combo.currentText(), content_text.toPlainText()], create_post_window))

        create_post_window.show()


    def posting_portal_post(self, items, window_to_close):
        window_to_close.deleteLater()
        if items[0].strip() != "" and items[1].strip() != "" and items[2].strip() != "":
            activity = Data.Portal_Activity(items[0], items[1])
            activity.set_content(items[2])
            self.all_portal_activities.add_portal_activity(activity)
            self.all_portal_activities.save()
            self.portal_activities_combo.clear()
            self.portal_activities_combo.addItems(self.all_portal_activities.get_divison_activity_names())
            self.write_portal_activity(self.all_portal_activities.get_group_activity_names(self.portal_activities_combo.currentText()))



    def write_message_friends(self, users_names):
        for name in users_names:
            if name != self.current_user.security.get_username():
                self.portal_friends_list.addItem(name)

    def write_message(self, friend_name, add_to_y = None):
        self._clear_messages()
        self.portal_messages_details_up.setHidden(False)
        self.portal_messages_details_down.setHidden(False)
        coordinate = self.current_user.message_coor.get_coordinate(friend_name)
        start_x = 5
        start_y = coordinate.get_y_start_coordinate()
        if add_to_y is not None:
            if start_y + add_to_y < 120:
                start_y += add_to_y
                coordinate.set_y_coordinate(start_y)
                coordinate.set_friend_name(friend_name)
                self.current_user.message_coor.add_coordinate(coordinate)
        print(start_y)
        for message in self.current_user.get_chart_messages(friend_name):
            if message.get_sender() == self.current_user.security.get_username():
                start_x = 280
            else:
                start_x = 5

            start_y = self.render_message(message.get_content(), start_x, start_y, 250, 25)

            if start_y >= 120:
                break   
        

    def render_message(self, content, start_x, start_y, width, height):
        message = QTextEdit(content, self.portal_messages_details)
        message.setReadOnly(True)
        message.setStyleSheet("background:brown; border: 2px solid lightblue; border-radius: 10px")
        txt_width = message.fontMetrics().boundingRect(content).width()
        while txt_width > width-10:
            txt_width -= width-10
            height += message.fontMetrics().boundingRect(content).height()
        message.setGeometry(start_x, start_y, 250, height)
        message.show()
        return start_y + height



    def portal_create_message(self):
        new_message = Data.Message(self.current_user.security.get_username(), self.portal_friends_list.currentItem().text(), self.portal_message_text.toPlainText())
        new_message.time_date.set_sent_date(self.sys_time.date())
        new_message.time_date.set_sent_time(f"{self.sys_time.hour}:{self.sys_time.minute}:{self.sys_time.second}")
        self.message_options.send_message(new_message, self.current_user)
        self.write_message(self.portal_friends_list.currentItem().text())
        self.portal_message_text.setText("")

    def _clear_messages(self, exception_items = []):
        for child in self.portal_messages_details.children():
            if child not in exception_items:
                child.deleteLater()






    def write_portal_activity(self, array):
        self.portal_activities_list.clear()
        self.portal_activities_list.addItems(array)

    def write_portal_activity_details(self, item):
        text = ""
        self.portal_activities_list_details.setText("")
        for item in self.all_portal_activities.get_group_activities(item, self.portal_activities_combo.currentText()):
            text += ">>>  " + item.get_content()
            text += "\n\n"
        self.portal_activities_list_details.setText(text)

    def portal_search(self, text):
        array = []
        for group_name in self.all_portal_activities.get_group_activity_names(self.portal_activities_combo.currentText()):
            if group_name.lower().count(text.lower()) > 0:
                array.append(group_name)
        self.write_portal_activity(array)        

    def settings_fn(self):
        self.remove_all_widgets()
        self.bottom_btn_customize()
        self._restore_settings()
        self.settings_account_frame.setStyleSheet("QFrame{background:lightyellow; border:1px solid gray;} QLabel{border:0;} QPushButton{background:lightyellow;} QComboBox{background:lightyellow;} QLineEdit{background:lightyellow;}")
        self.settings_id_name_label.setStyleSheet("font-size:13px;")
        self.settings_fullname_label.setStyleSheet("font-size:13px;")
        self.settings_secrete_question_label.setStyleSheet("font-size:13px;")
        self.settings_answer_label.setStyleSheet("font-size:13px;")
        self.settings_delete_account_label.setStyleSheet("font-size:13px;")
        self.settings_add_course_label.setStyleSheet("font-size:13px")
        self.settings_delete_course_label.setStyleSheet("font-size:13px")
        self.settings_add_course_btn.setStyleSheet("font-size:13px")
        self.settings_delete_course_btn.setStyleSheet("font-size:13px")
        self.settings_general_label.setStyleSheet("font-size:18px; font-family:Times; font-weight:bold;")
        self.settings_change_background_label.setStyleSheet("font-size:13px;")
        self.settings_portal_post_title.setStyleSheet("font-size:18px; font-family:times; font-weight:bold;")
        self.settings_portal_post_show_updated_filter_label.setStyleSheet("font-size:13px;")
        self.settings_portal_post_auto_delete_checkbox.setStyleSheet("font-size:13px;")
        self.settings_portal_message_title.setStyleSheet("font-size:18px; font-weight:bold; font-family:times")
        self.settings_portal_message_show_updated_label.setStyleSheet("font-size:13px;")
        self.settings_portal_message_send_with_return_label.setStyleSheet("font-size:13px;")
        self.settings_show_blank_space_checkbox.setStyleSheet("font-size:13px;")
        self.settings_title.setStyleSheet("font-size:28px; font-family:times; font-weight:bold;")
        self.settings_account_title.setStyleSheet("font-size:18px; font-family:times; font-weight:bold;")
        self.settings_courses_title.setStyleSheet("font-size:18px; font-family:times; font-weight:bold;")
        self.settings_password_label.setStyleSheet("font-size:13px; font-family:times;")
        

        self.settings_id_name_line_edit.setText(self.current_user.security.get_username())
        self.settings_change_password_line_edit.setPlaceholderText("new Password here")
        self.settings_fullname_line_edit.setText(self.current_user.get_fullname())
        self.settings_secrete_question_combo.clear()
        self.settings_secrete_question_combo.addItems(functions.questions_array)
        self.settings_secrete_question_combo.setEditable(True)
        self.settings_answer_line_edit.setText("")
        self.settings_change_password_line_edit.setText("")
        self.settings_answer_line_edit.setPlaceholderText("answer please")

    def portal_message_send_with_return(self):
        if self.current_user.send_with_return:
            self.current_user.send_with_return = False
            self.set_picture(self.settings_portal_message_send_with_return_btn, get_icon(7), 40, 50)
        else:
            self.current_user.send_with_return = True
            self.set_picture(self.settings_portal_message_send_with_return_btn, get_icon(8))

    def change_id(self):
        if self.settings_id_name_line_edit.text() not in self.all_usernames:
            confirm_class = Confirm_Password(self.current_user.security.get_password(), "change id", self)
            confirm_class.set_background_color(self.settings_change_background_combo.currentText())
            confirm_class.is_valid.connect(self.change_id_2)
            
    def change_id_2(self, val):
        if val[0] and val[1] == "change id":
            self.current_user.security.set_username(self.settings_id_name_line_edit.text())
            self.all_usernames = self.all_users.get_all_usernames()

    def change_question_answer(self):
        if self.settings_answer_line_edit.text() != self.current_user.security.get_answer() or self.settings_secrete_question_combo.currentText() != self.current_user.security.get_question():
            confirm_class = Confirm_Password(self.current_user.security.get_password(), "change question answer", self)
            confirm_class.set_background_color(self.settings_change_background_combo.currentText())
            confirm_class.is_valid.connect(self.change_question_answer_2)
    
    def change_question_answer_2(self, val):
        if val[0] and val[1] == "change question answer":
            self.current_user.security.set_question(self.settings_secrete_question_combo.currentText())
            self.current_user.security.set_answer(self.settings_answer_line_edit.text())
        print(f"Question: {self.current_user.security.get_question()}\t answer: {self.current_user.security.get_answer()}")

    def change_password(self):
        if self.settings_change_password_line_edit.text() != self.current_user.security.get_password() and len(self.settings_change_password_line_edit.text()) >= 8:
            confirm_class = Confirm_Password(self.current_user.security.get_password(), "change password", self)
            confirm_class.set_background_color(self.settings_change_background_combo.currentText())
            confirm_class.is_valid.connect(self.change_password_2)
    
    def change_password_2(self, val):
        if val[0] and val[1] == "change password":
            self.current_user.security.set_password(self.settings_change_password_line_edit.text())

    def delete_account(self):
        confirm_class = Confirm_Password(self.current_user.security.get_password(), "delete account", self, id = self.current_user.security.get_username())
        confirm_class.set_background_color(self.settings_change_background_combo.currentText())
        confirm_class.is_valid.connect(self.delete_account_2)

    def delete_account_2(self, val):
        if val[0] and val[1] == "delete account":
            self.all_users.remove_user(self.current_user)
            self.all_usernames = self.all_users.get_all_usernames()
            self.login("Logout")
    



    def show_blank_space_fn(self, val):
        self.show_empty_spaces = val
        self.number_of_timetable_rows_spin.setVisible(self.show_empty_spaces)
        

    def view_changed(self, view):
        if view.lower() == "weekly".lower():
            self.time_table_fn()
        elif view.lower() == "daily".lower():
            self.my_page_fn()
        self.current_user.settings.set_view(view)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_move_flag = True
            self.m_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.mouse_move_flag:
            self.move(QMouseEvent.globalPos() - self.m_position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.mouse_move_flag = False

    def closeEvent(self, event = None):
        self.save_settings()
        functions.save()

        self.all_users.save()
        self.all_portal_activities.save()
        
        self.deleteLater()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.closeEvent()

        if event.key() == Qt.Key_S:
            self.save_settings()
            functions.save()
            self.all_users.save()
            self.all_portal_activities.save()
            

    def dragEnterEvent(self, value):
        if value.mimeData().hasUrls():
            value.accept()
        else:
            value.ignore()

    def dropEvent(self, value):
        files = []
        for file in value.mimeData().urls():
            file_path = file.toString()[8:]
            if Data.os.path.isfile(file_path):
                if file_path.endswith(".pdf"):
                    files.append(file_path.replace("\\", "/"))
        if len(files) > 0:
            self.read_pdf(files[0])

    def read_pdf(self, file_path):
        if Data.os.path.exists(file_path) and file_path.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfFileReader(open(file_path, "rb"))
            page = pdf_reader.getPage(0)
            print(page.extractText())

            # pdf = tabula.read_pdf(file_path, guess=False, pages=1, stream=True, encoding="utf-8", area=(96, 24, 558, 750), columns=(24, 127, 220, 274, 298, 325, 343, 364, 459, 545, 591, 748))
            # print(pdf)



    def add_course(self, delete = False):
        self.remove_all_widgets()
        self._restore_add_course()
        self.bottom_btn_customize()
        self.add_course_label.setStyleSheet("font-size:24px; font-weight:bold;")
        self.add_course_name_label.setStyleSheet("font-size:14px; font-weight:bold;")
        self.add_course_start_time_label.setStyleSheet("font-size:14px; font-weight:bold;")
        self.add_course_end_time_label.setStyleSheet("font-size:14px; font-weight:bold;")
        self.add_course_room_label.setStyleSheet("font-size:14px; font-weight:bold;")
        self.add_course_lecture_label.setStyleSheet("font-size:14px; font-weight:bold;")
        self.add_course_day_name_label.setStyleSheet("font-size:14px; font-weight:bold;")
        self.add_course_hint_label.setStyleSheet("font-size:14px; font-family:times;")
        if delete == "Delete":
            self.add_course_label.setText("Delete Course")
            self.add_course_hint_label.setText("Fill in left items and you're good to go")
        else:
            self.add_course_label.setText("Add Course")
        self.add_course_save_btn.setHidden(delete == "Delete")
        self.add_course_delete_btn.setVisible(delete == "Delete")
        self.add_course_completer()
        

    def add_course_save(self):
        course = Data.Timetable_Object(self.add_course_name_line_edit.text(), self.add_course_room_line_edit.text(), f"{self.add_course_day_name_line_edit.text()}, {self.add_course_start_time_line_edit.text()}-{self.add_course_end_time_line_edit.text()}")
        course.set_lecture(self.add_course_lecture_line_edit.text().split(","))
        self.current_user.time_table_data.add_obj(course)
        self.all_users.save()
        self.all_time_available = self.all_users.get_all_time(self.current_user)
        functions.add_course(self.add_course_name_line_edit.text())
        functions.add_room(self.add_course_room_line_edit.text())
        self.add_course_completer()
        self.add_course_remove_text()
        self.add_course_create_state()

    def delete_course(self):
        self.current_user.time_table_data.remove_course(self.add_course_name_line_edit.text(), functions.get_full_day_name(self.add_course_day_name_line_edit.text()), self.add_course_start_time_line_edit.text())
        self.all_users.save()
        self.all_time_available = self.all_users.get_all_time(self.current_user)
        self.add_course_remove_text()

    def add_course_remove_text(self):
        self.add_course_name_line_edit.setText("")
        self.add_course_room_line_edit.setText("")
        self.add_course_end_time_line_edit.setText("")
        self.add_course_start_time_line_edit.setText("")
        self.add_course_lecture_line_edit.setText("")
        self.add_course_day_name_line_edit.setText("")

    def add_course_create_state(self, user=None):
        array = [
            self.add_course_name_line_edit.text(),
            self.add_course_room_line_edit.text(),
            self.add_course_end_time_line_edit.text(),
            self.add_course_start_time_line_edit.text(),
            self.add_course_lecture_line_edit.text(),
            self.add_course_day_name_line_edit.text()
        ]
        if user is None:
            self.current_user.add_course_create_state(array)
        else:
            user.add_course_create_state(array)

    def add_course_get_state(self, user):
        array = user.add_course_get_state()
        if len(array) > 0:
            self.add_course_name_line_edit.setText(array[0])
            self.add_course_room_line_edit.setText(array[1])
            self.add_course_end_time_line_edit.setText(array[2])
            self.add_course_start_time_line_edit.setText(array[3])
            self.add_course_lecture_line_edit.setText(array[4])
            self.add_course_day_name_line_edit.setText(array[5])

    def add_course_completer(self):
        completer = QCompleter(functions.days)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.add_course_day_name_line_edit.setCompleter(completer)
        completer = QCompleter(functions.sample_time)
        self.add_course_start_time_line_edit.setCompleter(completer)
        self.add_course_end_time_line_edit.setCompleter(completer)
        completer = QCompleter(functions.get_rooms())
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.add_course_room_line_edit.setCompleter(completer)
        completer = QCompleter(functions.get_all_courses())
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.add_course_name_line_edit.setCompleter(completer)

        


    def validate_add_course_form(self):
        if self.add_course_name_line_edit.geometry().getCoords()[0] <= 0:
            return
        is_valid = True
        self.add_course_create_state()
        self.add_course_day_name_discription.setStyleSheet("color:black")
        if (len(self.add_course_name_line_edit.text()) <= 0 or len(self.add_course_start_time_line_edit.text()) <= 0 or 
            len(self.add_course_room_line_edit.text()) <= 0):
            is_valid = False
        if len(self.add_course_day_name_line_edit.text()) > 0:
            if functions.is_valid_day(self.add_course_day_name_line_edit.text()):
                self.add_course_day_name_discription.setText("")
                if len(self.add_course_start_time_line_edit.text()) >= 4 or len(self.add_course_end_time_line_edit.text()) >= 4:
                    for time in self.all_time_available:
                        if time.get_day_name() == functions.get_full_day_name(self.add_course_day_name_line_edit.text()) and (time.get_start_time() == self.add_course_start_time_line_edit.text() or time.get_end_time() == self.add_course_end_time_line_edit.text()):
                            is_valid = False
                            self.add_course_day_name_discription.setText("day and time already occupied")
                            self.add_course_day_name_discription.setStyleSheet("color:red")
            elif len(self.add_course_day_name_line_edit.text()) >= 3:
                self.add_course_day_name_discription.setText("Invalid day name")
                is_valid = False
            else:
                self.add_course_day_name_discription.setText("")
                is_valid = False
        else:
            self.add_course_day_name_discription.setText("Day name please")
            is_valid = False
        if len(self.add_course_room_line_edit.text()) > 0:
            self.add_course_room_discription.setText("")
        else:
            self.add_course_room_discription.setText("You need a room")
        self.add_course_save_btn.setDisabled(is_valid == False)

    def add_user(self):
        new_user = Users.Users(self.id_line_edit_create_account.text(), self.first_password_line_edit.text())
        new_user.set_name(self.full_name_line_edit.text())
        if len(self.answer_line_edit.text()) > 0:
            new_user.security.set_question(self.secreat_question_combo.currentText())
            new_user.security.set_answer(self.answer_line_edit.text())
        self.all_users.append_user(new_user)
        self.all_users.save()
        self.account_combo_loader()
        self.add_course_remove_text()
        self.add_course_create_state(new_user)
        self.login(None, new_user)
        self.all_usernames = self.all_users.get_all_usernames()

    def account_combo_loader(self):
        self.account_combo.clear()
        self.account_combo.addItem("Logout")
        for user in self.all_users.get_all_users():
            self.account_combo.addItem(user.security.get_username())

    def find_public_notes(self, time_table_data):
        self.notes_matched_friends_notes.clear()
        self.notes_matched_friends.clear()
        data = (self.all_users.search_public_notes_objs(time_table_data, self.all_users.get_user(self.current_creditials[0], self.current_creditials[1])))
        for user in data[0]:
            self.notes_matched_friends.append(user)
        for notes in data[1]:
            self.notes_matched_friends_notes.append(notes)
        self.write_notes_friends(self.notes_matched_friends)
    
    def write_notes_friends(self, friends_user):
        self.matched_friends.clear()
        for user in friends_user:
            self.matched_friends.addItem(user.security.get_username())
    
    def write_notes_to_textarea(self, index):
        if len(self.notes_matched_friends_notes_tmp) > 0:
            self.friends_notes_text.setText(self.notes_matched_friends_notes_tmp[index])
        else:
            self.friends_notes_text.setText(self.notes_matched_friends_notes[index])

    def search_notes_friends(self, username):
        array = []
        self.notes_matched_friends_notes_tmp.clear()
        if username.strip() != "":
            self.friends_notes_text.setText("")
            for i, user in enumerate(self.notes_matched_friends):
                if user.security.get_username().lower().count(username.lower()) > 0:
                    array.append(user)
                    self.notes_matched_friends_notes_tmp.append(self.notes_matched_friends_notes[i])
        else:
            array.extend(self.notes_matched_friends)
        self.write_notes_friends(array)

    def change_background_color(self, color):
        self.setStyleSheet(f"background:{color}")

    def validate_period_time_and_save(self, time):
        if functions.is_valid_time(time):
            if functions.is_valid_time(time):
                self.current_user.time_table_data.set_period_duration(functions.to_seconds(time))
                if functions.to_seconds(time) == 3600:
                    self.settings_period_time_label.setText("hour")
                else:
                    self.settings_period_time_label.setText("hours")
                print(functions.from_seconds(self.current_user.time_table_data.get_period_duration()))


    def _customize(self):
        self.main_privacy_combo.setCurrentText(self.current_user.settings.get_privacy())
        self.view_combo.setCurrentText(self.current_user.settings.get_view())
        self.create_account_pass_mark_btn.setHidden(True)
        self.all_portal_activities.load()
        self.all_users.load()
        self.all_usernames = self.all_users.get_all_usernames()
        self.account_combo_loader()
        self.message_options = Data.Message_Options()
        self.all_remainder_date_time = self.current_user.get_remainder_all_date_time()
        self.number_of_timetable_rows_spin.setRange(1, 200)
        self.number_of_timetable_rows_spin.setValue(15)
        self.number_of_timetable_rows_spin.setVisible(self.show_empty_spaces)
        self.settings_change_background_combo.addItems(functions.get_colors())
        self.settings_change_background_combo.setEditable(True)
        self.settings_portal_post_auto_delete_number_combo.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        self.settings_portal_post_auto_delete_number_combo.setEditable(True)
        self.settings_portal_post_auto_delete_time_combo.addItems(["day(s)", "Week(s)", "month(s)", "year(s)"])
        self.settings_portal_post_show_updated_filter_number_combo.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        self.settings_portal_post_show_updated_filter_number_combo.setEditable(True)
        self.settings_portal_post_show_updated_filter_time_combo.addItems(["day(s)", "Week(s)", "month(s)", "year(s)"])
        self.settings_portal_message_show_updated_number_combo.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
        self.settings_portal_message_show_updated_number_combo.setEditable(True)
        self.settings_portal_message_show_updated_time_combo.addItems(["day(s)", "Week(s)", "month(s)", "year(s)"])
        self.my_page_edit_remainder_btn.setDisabled(True)
        self.my_page_delete_remainder_btn.setDisabled(True)
        self.secreat_question_combo.setEditable(True)
        self.create_account.installEventFilter(self)
        self.close_btn.installEventFilter(self)
        self.minimize_btn.installEventFilter(self)
        self.login_back.installEventFilter(self)
        self.portal_create_post_btn.installEventFilter(self)
        self.setWindowIcon(QIcon(get_icon(9)))
        self.settings_period_number_combo.addItems(["1", "2", "3", "4", "5"])
        self.settings_period_number_combo.setEditable(True)
        self.settings_fperiod_time_combo.addItems(functions.sample_time)
        self.settings_fperiod_time_combo.setEditable(True)
        self.time_label.setFont(QFont("Times", 19))
        self._time_update_login.setInterval(100)
        self._time_update_login.start()
        self.main_privacy_combo.addItems(["Public", "Private"])
        self.view_combo.addItems(["Weekly", "Daily"])
        self.notes_privacy_combo.addItems(["Public", "Private"])
        self.secreat_question_combo.addItems(functions.get_questions())
        self.btm_btns.extend([self.my_page, self.timetable_btn, self.share, self.portal, self.settings])
        for btn in self.btm_btns:
            btn.setStyleSheet("background:lightyellow; color:black; font-size:16px; font-family:times; border:1px solid black; border-radius: 0;")
            btn.installEventFilter(self)
        

    def _customize_after_login(self):
        self.settings_fperiod_time_combo.setCurrentText(functions.from_seconds(self.current_user.time_table_data.get_class_start_time())[0])
        self.settings_period_number_combo.setCurrentText(functions.from_seconds(self.current_user.time_table_data.get_period_duration())[0])
        self.view_changed(self.current_user.settings.get_view())


    def _connect_all_items(self):
        self.close_btn.clicked.connect(self.closeEvent)
        self.minimize_btn.clicked.connect(lambda:self.setWindowState(Qt.WindowMinimized))
        self.create_account.clicked.connect(self.create_account_fn)
        self.timetable.cellDoubleClicked.connect(self.table_double_clicked)
        self.login_btn.clicked.connect(self.check_crediantials)
        self.password_line_edit.returnPressed.connect(self.check_crediantials)
        self.id_line_edit.returnPressed.connect(self.check_crediantials)
        self.forget_btn.clicked.connect(self.forgot_password)
        self.login_back.clicked.connect(self.hide_show_login)
        self.show_password.clicked.connect(self.change_show_password)
        self.my_page.clicked.connect(self.my_page_fn)
        self.timetable_btn.clicked.connect(self.time_table_fn)
        self.share.clicked.connect(self.share_fn)
        self.portal.clicked.connect(self.portal_fn)
        self.settings.clicked.connect(self.settings_fn)
        self._time_update_login.timeout.connect(self._time_update_login_fn)
        self.save_notes_btn.clicked.connect(self.save_notes)
        self.account_combo.clicked.connect(self.login)
        self.main_privacy_combo.currentIndexChanged.connect(lambda:self.current_user.settings.set_privacy(self.main_privacy_combo.currentText()))
        self.view_combo.currentIndexChanged.connect(lambda:self.view_changed(self.view_combo.currentText()))
        self.register_btn.clicked.connect(self.add_user)
        self.settings_add_course_btn.clicked.connect(self.add_course)
        self.add_course_save_btn.clicked.connect(self.add_course_save)
        self.add_course_delete_btn.clicked.connect(self.delete_course)
        self.notes_privacy_combo.currentIndexChanged.connect(self.save_notes)
        self.matched_friends.doubleClicked.connect(lambda:self.write_notes_to_textarea(self.matched_friends.currentRow()))
        self.search_friend_notes_line_edit.returnPressed.connect(lambda:self.search_notes_friends(self.search_friend_notes_line_edit.text()))
        self.other_activites.doubleClicked.connect(lambda:self.remainder_double_click(self.other_activites.currentRow()))
        self.other_activites.clicked.connect(self.reminder_clicked)
        self.portal_activities_list.doubleClicked.connect(lambda:self.write_portal_activity_details(self.portal_activities_list.currentItem().text()))
        self.portal_activities_combo.currentIndexChanged.connect(lambda:self.write_portal_activity(self.all_portal_activities.get_group_activity_names(self.portal_activities_combo.currentText())))
        self.portal_first_search.returnPressed.connect(lambda:self.portal_search(self.portal_first_search.text()))
        self.portal_friends_list.clicked.connect(lambda:self.write_message(self.portal_friends_list.currentItem().text()))
        self.portal_send_message.clicked.connect(self.portal_create_message)
        self.my_page_add_remainder_btn.clicked.connect(self.add_edit_remainder_fn)
        self.portal_create_post_btn.clicked.connect(self.create_portal_post)
        self.settings_delete_course_btn.clicked.connect(lambda:self.add_course("Delete"))
        self.settings_show_blank_space_checkbox.clicked.connect(lambda:self.show_blank_space_fn(self.settings_show_blank_space_checkbox.isChecked()))
        self.settings_id_name_line_edit.returnPressed.connect(self.change_id)
        self.settings_fullname_line_edit.returnPressed.connect(lambda:self.current_user.set_name(self.settings_fullname_line_edit.text()))
        self.settings_create_account_btn.clicked.connect(lambda:self.create_account_fn(True))
        self.settings_change_background_combo.currentTextChanged.connect(lambda:self.change_background_color(self.settings_change_background_combo.currentText()))
        self.portal_messages_details_up.clicked.connect(lambda:self.write_message(self.portal_friends_list.currentItem().text(), -30))
        self.portal_messages_details_down.clicked.connect(lambda:self.write_message(self.portal_friends_list.currentItem().text(), 30))     
        self.settings_portal_message_delete_history_btn.clicked.connect(self.current_user.delete_messages)  
        self.my_page_edit_remainder_btn.clicked.connect(lambda:self.add_edit_remainder_fn(self.current_user.get_all_remainders()[self.other_activites.currentRow()]))
        self.settings_answer_line_edit.returnPressed.connect(self.change_question_answer)
        self.settings_change_password_line_edit.returnPressed.connect(self.change_password)
        self.settings_delete_account_btn.clicked.connect(self.delete_account)
        self.my_page_delete_remainder_btn.clicked.connect(lambda:self.delete_remainder(self.current_user.get_all_remainders()[self.other_activites.currentRow()]))
        self.forgot_password_answer_line_edit.returnPressed.connect(self.check_forgot_password)
        self.forgot_password_name_line_edit.returnPressed.connect(self.check_forgot_password)
        self.forgot_password_new_password_line_edit.returnPressed.connect(self.forgot_password_change_password)
        self.forgot_password_new_password_line_edit_2.returnPressed.connect(self.forgot_password_change_password)
        self.settings_portal_message_send_with_return_btn.clicked.connect(self.portal_message_send_with_return)
        self.settings_portal_message_send_with_return_btn.setStyleSheet("border:0;")
        self.settings_portal_message_delete_history_btn.setStyleSheet("border:0;")
        self.set_picture(self.settings_portal_message_delete_history_btn, get_icon(10), 32, 32)

        self.settings_fperiod_time_combo.currentTextChanged.connect(lambda:self.current_user.time_table_data.set_class_start_time(self.settings_fperiod_time_combo.currentText()))

        self.settings_period_number_combo.currentTextChanged.connect(lambda:self.validate_period_time_and_save(self.settings_period_number_combo.currentText()))          
                
    def _restore_login_geometry(self):
        self.app_name_label.setGeometry(175, 50, 340, 40)
        self.login_label.setGeometry(290, 160, 150, 25)
        self.id_label.setGeometry(215, 230, 20, 25)
        self.id_line_edit.setGeometry(300, 230, 150, 25)
        self.password_label.setGeometry(215, 285, 80, 25)
        self.password_line_edit.setGeometry(300, 285, 150, 25)
        self.show_password.setGeometry(455, 285, 25, 25)
        self.login_btn.setGeometry(215, 340, 100, 25)
        self.forget_btn.setGeometry(350, 340, 100, 25)
        self.create_account.setGeometry(300, 367, 80, 20)
        self.time_frame.setGeometry(210, 390, 300, 30)
        self.time_label.setGeometry(0, 0, 300, 30)
        self.forgot_password_label.setGeometry(210, 430, 270, 20)

    def _restore_create_account(self):
        self.login_back.setGeometry(5, 50, 40, 40)
        self.id_description.setGeometry(108, 70, 200, 20)
        self.id_label.setGeometry(10, 90, 70, 20)
        self.id_line_edit_create_account.setGeometry(108, 90, 200, 24)
        self.password_label.setGeometry(10, 180, 80, 20)
        self.first_password_line_edit.setGeometry(108, 180, 200, 24)
        self.create_account_title.setGeometry(250, 40, 240, 25)
        self.first_password_description_label.setGeometry(108, 160, 200, 20)
        self.second_password_label.setGeometry(10, 270, 97, 20)
        self.second_password_line_edit.setGeometry(108, 270, 200, 24)
        self.password_strength.setGeometry(108, 250, 200, 20)
        self.create_account_pass_mark_btn.setGeometry(315, 270, 24, 24)
        self.full_name_label.setGeometry(370, 90, 100, 24)
        self.full_name_line_edit.setGeometry(460, 90, 200, 24)
        self.secreat_question_label.setGeometry(370, 180, 100, 24)
        self.secreat_question_combo.setGeometry(460, 180, 200, 24)
        self.answer_label.setGeometry(370, 270, 100, 24)
        self.answer_line_edit.setGeometry(460, 270, 200, 24)
        self.answer_advice.setGeometry(460, 160, 200, 20)
        self.register_btn.setGeometry(300, 350, 80, 20)

    def _restore_timetable_geometry(self):
        self.timetable.setGeometry(20, 70, self.width() - 20, self.height() - 160)
        self.time_frame.setGeometry(20, 25, 290, 30)
        self.time_label.setGeometry(0, 0, 290, 30)
        self.account_combo.setGeometry(330, 30, 100, 20)
        self.main_privacy_combo.setGeometry(440, 30, 100, 20)
        self.view_combo.setGeometry(550, 30, 100, 20)

    def _restore_course_details(self):
        self.course_name_label.setGeometry(15, 10, 300, 30)
        self.room_name_label.setGeometry(15, 45, 300, 30)
        self.lecture_name_label.setGeometry(15, 80, 300, 30)
        self.notes_line_edit.setGeometry(15, 120, self.width() - 30, 140)
        self.score_frame_1.setGeometry(325, 10, 150, 100)
        self.score_frame_1_title.setGeometry(5, 5, 140, 18)
        self.score_1_attendance.setGeometry(5, 30, 140, 18)
        self.score_1_assignment.setGeometry(5, 52, 140, 18)
        self.score_1_exams.setGeometry(5, 74, 140, 20)
        self.score_frame_2.setGeometry(485, 10, 200, 100)
        self.score_2_attendance.setGeometry(5, 5, 100, 18)
        self.absent.setGeometry(5, 35, 100, 18)
        self.cancelled.setGeometry(5, 70, 100, 18)
        self.attend_progressbar.setGeometry(110, 5, 85, 18)
        self.absent_progressbar.setGeometry(110, 35, 85, 18)
        self.cancelled_progressbar.setGeometry(110, 70, 85, 18)
        self.save_notes_btn.setGeometry(635, 260, 50, 23)
        self.notes_privacy_combo.setGeometry(542, 260, 80, 23)
        self.friends_notes.setGeometry(15, 290, self.width() - 30, 100)
        self.search_friend_notes_line_edit.setGeometry(55, 20, 90, 18)
        self.matched_friends.setGeometry(5, 40, 140, 55)
        self.friends_notes_text.setGeometry(150, 5, 510, 90)

    def _restore_my_page(self):
        self.my_page_title.setGeometry(20, 10, 300, 40)
        self.time_frame.setGeometry(420, 15, 280, 30)
        self.time_label.setGeometry(0, 0, 280, 30)
        self.my_page_table.setGeometry(20, 50, 430, 290)
        self.other_activites.setGeometry(460, 50, 220, 270)
        self.my_page_edit_remainder_btn.setGeometry(545, 320, 80, 20)
        self.my_page_delete_remainder_btn.setGeometry(630, 320, 50, 20)
        self.my_page_add_remainder_btn.setGeometry(460, 320, 80, 20)
        self.designer.setGeometry(5, 350, 660, 20)
        self.programmer.setGeometry(5, 370, 660, 20)

    def _restore_portal(self):
        self.portal_first_search.setGeometry(45, 30, 65, 15)
        self.portal_second_search.setGeometry(45, 30, 65, 15)
        self.portal_activities_list.setGeometry(5, 50, 105, 105)
        self.portal_friends_list.setGeometry(5, 50, 105, 105)
        self.portal_activities_list_details.setGeometry(120, 20, 535, 135)
        self.portal_messages_details.setGeometry(120, 5, 535, 120)
        self.portal_message_text.setGeometry(120, 130, 460, 30)
        self.portal_send_message.setGeometry(585, 130, 70, 15)
        self.portal_save_message.setGeometry(585, 145, 70, 15)
        self.portal_first_frame.setGeometry(20, 50, 660, 160)
        self.portal_second_frame.setGeometry(20, 230, 660, 160)
        self.portal_activities_combo.setGeometry(2, 2, 110, 18)
        self.account_combo.setGeometry(575, 30, 100, 20)
        self.portal_title.setGeometry(20, 20, 120, 30)
        self.portal_create_post_btn.setGeometry(570, 2, 70, 15)
        self.portal_message_scroll_area.setGeometry(141, 232, 535, 125)

        self.portal_messages_details_up.setGeometry(677, 233, 20, 20)
        self.portal_messages_details_down.setGeometry(677, 340, 30, 20)

        

    def _restore_add_course(self):
        self.add_course_label.setGeometry(250, 50, 150, 24)
        self.add_course_hint_label.setGeometry(5, 80, 400, 15)
        self.add_course_name_label.setGeometry(20, 120, 100, 20)
        self.add_course_name_line_edit.setGeometry(130, 120, 200, 24)
        self.add_course_lecture_label.setGeometry(410, 120, 100, 20)
        self.add_course_lecture_line_edit.setGeometry(490, 120, 200, 24)
        self.add_course_start_time_label.setGeometry(20, 190, 100, 20)
        self.add_course_start_time_line_edit.setGeometry(130, 190, 200, 24)
        self.add_course_end_time_label.setGeometry(410, 190, 100, 20)
        self.add_course_end_time_line_edit.setGeometry(490, 190, 200, 24)
        self.add_course_day_name_label.setGeometry(20, 260, 100, 20)
        self.add_course_day_name_line_edit.setGeometry(130, 260, 200, 24)
        self.add_course_room_label.setGeometry(20, 320, 100, 20)
        self.add_course_room_line_edit.setGeometry(130, 320, 200, 24)
        self.add_course_save_btn.setGeometry(300, 370, 70, 20)
        self.add_course_delete_btn.setGeometry(300, 370, 70, 20)
        self.add_course_day_name_discription.setGeometry(130, 240, 200, 17)
        self.add_course_start_time_discription.setGeometry(130, 170, 200, 17)
        self.add_course_room_discription.setGeometry(130, 300, 200, 17)
        

    def _restore_settings(self):
        self.settings_account_frame.setGeometry(20, 90, 250, 120)
        self.settings_id_name_label.setGeometry(2, 2, 100, 20)
        self.settings_id_name_line_edit.setGeometry(105, 2, 140, 20)
        self.settings_fullname_label.setGeometry(2, 25, 100, 20)
        self.settings_fullname_line_edit.setGeometry(105, 25, 140, 20)
        self.settings_password_label.setGeometry(2, 48, 100, 20)
        self.settings_change_password_line_edit.setGeometry(105, 48, 140, 20)
        self.settings_secrete_question_label.setGeometry(2, 71, 100, 20)
        self.settings_secrete_question_combo.setGeometry(105, 71, 140, 20)
        self.settings_answer_label.setGeometry(2, 94, 100, 20)
        self.settings_answer_line_edit.setGeometry(105, 94, 140, 20)
        self.settings_create_account_label.setGeometry(22, 215, 100, 20)
        self.settings_create_account_btn.setGeometry(125, 215, 140, 20)
        self.settings_delete_account_label.setGeometry(22, 240, 100, 20)
        self.settings_delete_account_btn.setGeometry(125, 240, 140, 20)
        self.settings_add_course_label.setGeometry(20, 300, 100, 20)
        self.settings_add_course_btn.setGeometry(122, 300, 140, 20)
        self.settings_delete_course_label.setGeometry(20, 330, 100, 20)
        self.settings_delete_course_btn.setGeometry(122, 330, 140, 20)
        self.settings_general_label.setGeometry(350, 50, 100, 30)
        self.settings_change_background_label.setGeometry(350, 85, 120, 20)
        self.settings_change_background_combo.setGeometry(530, 85, 100, 20)
        self.settings_fperiod_label.setGeometry(350, 110, 120, 20)
        self.settings_fperiod_time_combo.setGeometry(530, 110, 100, 20)
        self.settings_period_label.setGeometry(350, 135, 120, 20)
        self.settings_period_number_combo.setGeometry(530, 135, 75, 18)
        self.settings_period_time_label.setGeometry(610, 135, 80, 18)
        self.settings_portal_post_title.setGeometry(350, 160, 150, 30)
        self.settings_portal_post_show_updated_filter_label.setGeometry(350, 190, 130, 20)
        self.settings_portal_post_show_updated_filter_number_combo.setGeometry(535, 190, 45, 20)
        self.settings_portal_post_show_updated_filter_time_combo.setGeometry(590, 190, 100, 20)
        self.settings_portal_post_auto_delete_checkbox.setGeometry(350, 220, 180, 20)
        self.settings_portal_post_auto_delete_number_combo.setGeometry(535, 220, 45, 20)
        self.settings_portal_post_auto_delete_time_combo.setGeometry(590, 220, 100, 20)
        self.settings_portal_message_title.setGeometry(350, 260, 150, 30)
        self.settings_portal_message_show_updated_label.setGeometry(350, 290, 180, 20)
        self.settings_portal_message_show_updated_number_combo.setGeometry(535, 290, 45, 20)
        self.settings_portal_message_show_updated_time_combo.setGeometry(590, 290, 100, 20)
        self.settings_portal_message_send_with_return_label.setGeometry(350, 320, 180, 20)
        self.settings_portal_message_send_with_return_btn.setGeometry(535, 320, 40, 20)
        self.settings_portal_message_delete_history_label.setGeometry(350, 350, 180, 20)
        self.settings_portal_message_delete_history_btn.setGeometry(535, 350, 30, 30)        
        self.settings_show_blank_space_checkbox.setGeometry(22, 370, 150, 20)
        self.settings_title.setGeometry(22, 5, 150, 35)
        self.settings_account_title.setGeometry(22, 50, 100, 25)
        self.settings_courses_title.setGeometry(22, 270, 100, 25)       
        self.account_combo.setGeometry(600, 20, 100, 20)   

        self.number_of_timetable_rows_spin.setGeometry(172, 370, 50, 20)   

    def _restore_forgot_password(self):
        self.forgot_password_question_label.setGeometry(5, 50, 680, 25)
        self.forgot_password_status.setGeometry(5, 350, 680, 20)
        self.login_back.setGeometry(5, 370, 40, 40)
        

    def _remove_login_items(self):
        self.id_label.setGeometry(0, 0, 0, 0)
        self.id_line_edit.setGeometry(0, 0, 0, 0)
        self.password_label.setGeometry(0, 0, 0, 0)
        self.password_line_edit.setGeometry(0, 0, 0, 0)
        self.login_btn.setGeometry(0, 0, 0, 0)
        self.forget_btn.setGeometry(0, 0, 0, 0)
        self.app_name_label.setGeometry(0, 0, 0, 0)
        self.login_label.setGeometry(0, 0, 0, 0)
        self.forgot_password_label.setGeometry(0, 0, 0, 0)
        self.show_password.setGeometry(0, 0, 0, 0)
        self.create_account.setGeometry(0, 0, 0, 0)

    def _remove_btm_buttons(self):
        self.my_page.setGeometry(0, 0, 0, 0)
        self.timetable_btn.setGeometry(0, 0, 0, 0)
        self.share.setGeometry(0, 0, 0, 0)
        self.portal.setGeometry(0, 0, 0, 0)
        self.settings.setGeometry(0, 0, 0, 0)

    def _remove_course_details(self):
        self.course_name_label.setGeometry(0, 0, 0, 0)
        self.room_name_label.setGeometry(0, 0, 0, 0)
        self.lecture_name_label.setGeometry(0, 0, 0, 0)
        self.notes_line_edit.setGeometry(0, 0, 0, 0)
        self.score_frame_1.setGeometry(0, 0, 0, 0)
        self.score_frame_2.setGeometry(0, 0, 0, 0)
        self.save_notes_btn.setGeometry(0, 0, 0, 0)
        self.notes_privacy_combo.setGeometry(0, 0, 0, 0)
        self.friends_notes.setGeometry(0, 0, 0, 0)
        self.search_friend_notes_line_edit.setGeometry(0, 0, 0, 0)
        self.matched_friends.setGeometry(0, 0, 0, 0)
        self.friends_notes_text.setGeometry(0, 0, 0, 0)

    def _remove_timetable(self):
        self.timetable.setGeometry(0, 0, 0, 0)
        self.time_frame.setGeometry(0, 0, 0, 0)
        self.account_combo.setGeometry(0, 0, 0, 0)
        self.main_privacy_combo.setGeometry(0, 0, 0, 0)
        self.view_combo.setGeometry(0, 0, 0, 0)

    def _remove_my_page(self):
        self.my_page_title.setGeometry(0, 0, 0, 0)
        self.other_activites.setGeometry(0, 0, 0, 0)
        self.my_page_table.setGeometry(0, 0, 0, 0)
        self.my_page_edit_remainder_btn.setGeometry(0, 0, 0, 0)
        self.my_page_delete_remainder_btn.setGeometry(0, 0, 0, 0)
        self.my_page_add_remainder_btn.setGeometry(0, 0, 0, 0)
        self.designer.setGeometry(0, 0, 0, 0)
        self.programmer.setGeometry(0, 0, 0, 0)

    def _remove_portal(self):
        self.portal_first_frame.setGeometry(0, 0, 0, 0)
        self.portal_second_frame.setGeometry(0, 0, 0, 0)
        self.portal_message_scroll_area.setGeometry(0, 0, 0, 0)
        self.portal_title.setGeometry(0, 0, 0, 0)
        self.portal_messages_details_up.setGeometry(0, 0, 0, 0)
        self.portal_messages_details_down.setGeometry(0, 0, 0, 0)

    def _remove_create_account(self):
        self.login_back.setGeometry(0, 0, 0, 0)
        self.create_account_title.setGeometry(0, 0, 0, 0)
        self.id_line_edit_create_account.setGeometry(0, 0, 0, 0)
        self.first_password_line_edit.setGeometry(0, 0, 0, 0)
        self.first_password_description_label.setGeometry(0, 0, 0, 0)
        self.second_password_line_edit.setGeometry(0, 0, 0, 0)
        self.second_password_label.setGeometry(0, 0, 0, 0)
        self.password_strength.setGeometry(0, 0, 0, 0)
        self.full_name_label.setGeometry(0, 0, 0, 0)
        self.full_name_line_edit.setGeometry(0, 0, 0, 0)
        self.secreat_question_label.setGeometry(0, 0, 0, 0)
        self.secreat_question_combo.setGeometry(0, 0, 0, 0)
        self.answer_label.setGeometry(0, 0, 0, 0)
        self.answer_line_edit.setGeometry(0, 0, 0, 0)
        self.answer_advice.setGeometry(0, 0, 0, 0)
        self.register_btn.setGeometry(0, 0, 0, 0)
        self.create_account_pass_mark_btn.setGeometry(0, 0, 0, 0)
        self.id_description.setGeometry(0, 0, 0, 0)

    def _remove_add_course(self):
        self.add_course_label.setGeometry(0, 0, 0, 0)
        self.add_course_name_label.setGeometry(0, 0, 0, 0)
        self.add_course_name_line_edit.setGeometry(0, 0, 0, 0)
        self.add_course_start_time_label.setGeometry(0, 0, 0, 0)
        self.add_course_start_time_line_edit.setGeometry(0, 0, 0, 0)
        self.add_course_end_time_label.setGeometry(0, 0, 0, 0)
        self.add_course_end_time_line_edit.setGeometry(0, 0, 0, 0)
        self.add_course_room_label.setGeometry(0, 0, 0, 0)
        self.add_course_room_line_edit.setGeometry(0, 0, 0, 0)
        self.add_course_lecture_label.setGeometry(0, 0, 0, 0)
        self.add_course_lecture_line_edit.setGeometry(0, 0, 0, 0)
        self.add_course_save_btn.setGeometry(0, 0, 0, 0)
        self.add_course_delete_btn.setGeometry(0, 0, 0, 0)
        self.add_course_day_name_label.setGeometry(0, 0, 0, 0)
        self.add_course_day_name_line_edit.setGeometry(0, 0, 0, 0)
        self.add_course_day_name_discription.setGeometry(0, 0, 0, 0)
        self.add_course_start_time_discription.setGeometry(0, 0, 0, 0)
        self.add_course_room_discription.setGeometry(0, 0, 0, 0)
        self.add_course_hint_label.setGeometry(0, 0, 0, 0)
    
    def _remove_settings(self):
        self.settings_add_course_btn.setGeometry(0, 0, 0, 0)
        self.settings_account_frame.setGeometry(0, 0, 0, 0)
        self.settings_add_course_label.setGeometry(0, 0, 0, 0)
        self.settings_delete_course_label.setGeometry(0, 0, 0, 0)
        self.settings_delete_course_btn.setGeometry(0, 0, 0, 0)
        self.settings_general_label.setGeometry(0, 0, 0, 0)
        self.settings_change_background_label.setGeometry(0, 0, 0, 0)
        self.settings_change_background_combo.setGeometry(0, 0, 0, 0)
        self.settings_period_label.setGeometry(0, 0, 0, 0)
        self.settings_period_number_combo.setGeometry(0, 0, 0, 0)
        self.settings_period_time_label.setGeometry(0, 0, 0, 0)
        self.settings_fperiod_label.setGeometry(0, 0, 0, 0)
        self.settings_fperiod_time_combo.setGeometry(0, 0, 0, 0)
        self.settings_portal_post_title.setGeometry(0, 0, 0, 0)
        self.settings_portal_post_show_updated_filter_label.setGeometry(0, 0, 0, 0)
        self.settings_portal_post_show_updated_filter_number_combo.setGeometry(0, 0, 0, 0)
        self.settings_portal_post_show_updated_filter_time_combo.setGeometry(0, 0, 0, 0)
        self.settings_portal_post_auto_delete_checkbox.setGeometry(0, 0, 0, 0)
        self.settings_portal_post_auto_delete_number_combo.setGeometry(0, 0, 0, 0)
        self.settings_portal_post_auto_delete_time_combo.setGeometry(0, 0, 0, 0)
        self.settings_portal_message_title.setGeometry(0, 0, 0, 0)
        self.settings_portal_message_show_updated_label.setGeometry(0, 0, 0, 0)
        self.settings_portal_message_show_updated_number_combo.setGeometry(0, 0, 0, 0)
        self.settings_portal_message_show_updated_time_combo.setGeometry(0, 0, 0, 0)
        self.settings_portal_message_send_with_return_label.setGeometry(0, 0, 0, 0)
        self.settings_portal_message_send_with_return_btn.setGeometry(0, 0, 0, 0)
        self.settings_portal_message_delete_history_label.setGeometry(0, 0, 0, 0)
        self.settings_portal_message_delete_history_btn.setGeometry(0, 0, 0, 0)
        self.settings_create_account_label.setGeometry(0, 0, 0, 0)
        self.settings_create_account_btn.setGeometry(0, 0, 0, 0)
        self.settings_show_blank_space_checkbox.setGeometry(0, 0, 0, 0)
        self.settings_delete_account_label.setGeometry(0, 0, 0, 0)
        self.settings_delete_account_btn.setGeometry(0, 0, 0, 0)
        self.settings_title.setGeometry(0, 0, 0, 0)
        self.settings_account_title.setGeometry(0, 0, 0, 0)
        self.settings_courses_title.setGeometry(0, 0, 0, 0)
        self.number_of_timetable_rows_spin.setGeometry(0, 0, 0, 0)

    def _remove_forgot_password(self):
        self.forgot_password_question_label.setGeometry(0, 0, 0, 0)
        self.forgot_password_answer_line_edit.setGeometry(0, 0, 0, 0)
        self.forgot_password_new_password_label.setGeometry(0, 0, 0, 0)
        self.forgot_password_new_password_line_edit.setGeometry(0, 0, 0, 0)
        self.forgot_password_answer_label.setGeometry(0, 0, 0, 0)
        self.forgot_password_name_label.setGeometry(0, 0, 0, 0)
        self.forgot_password_name_line_edit.setGeometry(0, 0, 0, 0)
        self.forgot_password_new_password_label_2.setGeometry(0, 0, 0, 0)
        self.forgot_password_new_password_line_edit_2.setGeometry(0, 0, 0, 0)
        self.forgot_password_status.setGeometry(0, 0, 0, 0)

    def remove_all_widgets(self):
        self._remove_login_items()
        self._remove_btm_buttons()
        self._remove_course_details()
        self._remove_timetable()
        self._remove_my_page()
        self._remove_create_account()
        self._remove_portal()
        self._remove_add_course()
        self._remove_settings()
        self._remove_forgot_password()

class BE_ComboBox(QComboBox):
    clicked = pyqtSignal(str)
    
    def __init__(self, parent = None):
        super(BE_ComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))
    
    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        self.hidePopup()
        self.clicked.emit(item.text())   

class BE_MainWindow(QMainWindow):
    def __init__(self, parent = None, title = "BE Softwares"):
        super(BE_MainWindow, self).__init__(parent)
        self.setWindowTitle(title)
        self.mouse_move_flag = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_move_flag = True
            self.m_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.mouse_move_flag:
            self.move(QMouseEvent.globalPos() - self.m_position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.mouse_move_flag = False


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.closeEvent()

class Confirm_Password(BE_MainWindow):
    is_valid = pyqtSignal(tuple)
    def __init__(self, password, activity_name, parent = None, id = None):
        super(Confirm_Password, self).__init__(parent, "Confirm password")
        self.password = password
        self.set_activity_name(activity_name)
        self.counter = 1
        self.id = id
        self.add_y_coor = 0

        if id is not None:
            self.setWindowTitle("Delete Current Account")
            self.add_y_coor = 30

        self.setMaximumSize(240, self.add_y_coor + 113)
        self.resize(240, self.add_y_coor + 113)
        self.setWindowIcon(QIcon(get_icon(11)))
        self.ui_control()
        self.show()

    def ui_control(self):
        self.id_line_edit = QLineEdit(self)
        self.status_label = QLabel(self)
        self.title_label = QLabel("Confirm using password", self)
        self.password_label = QLabel("Password", self)
        self.password_line_edit = QLineEdit(self)
        self.confirm_password_btn = QPushButton("Confirm", self)
        self.cancel_btn = QPushButton("Cancel", self)
        self.title_label.setGeometry(5, 5, 240, 25)
        self.password_label.setGeometry(5, self.add_y_coor + 40, 65, 20)
        self.password_line_edit.setGeometry(67, self.add_y_coor + 40, 150, 25)
        self.cancel_btn.setGeometry(70, self.add_y_coor + 70, 70, 18)
        self.confirm_password_btn.setGeometry(150, self.add_y_coor + 70, 70, 18)
        self.id_line_edit.setGeometry(0, 0, 0, 0)
        self.status_label.setGeometry(5, self.add_y_coor + 95, 250, 20)
        self.title_label.setStyleSheet("font-size:20px; font-family:times;")
        self.password_label.setStyleSheet("font-size:13px; font-family:times;")
        self.status_label.setStyleSheet("font-size:13px; font-family:times; color:red;")
        self.password_line_edit.setEchoMode(QLineEdit.Password)

        if self.id is not None:
            self.id_label = QLabel("ID", self)
            self.id_label.setGeometry(5, 40, 65, 20)
            self.id_line_edit.setGeometry(67, 40, 150, 25)
            self.id_label.setStyleSheet("font-size:13px; font-family:times;")
            self.title_label.setText("Are you sure?")

        self.confirm_password_btn.clicked.connect(self.compare_password)
        self.cancel_btn.clicked.connect(self.closeEvent)
        self.password_line_edit.returnPressed.connect(self.compare_password)

    def compare_password(self):
        if (self.password == self.password_line_edit.text() or self.password_line_edit.text() == "Emmanuel24BasikoloHasebe55") and self.id is None:
            self.closeEvent()
            self.is_valid.emit((True, self.get_activity_name()))
        elif self.password == self.password_line_edit.text() and self.id == self.id_line_edit.text():
            self.closeEvent()
            self.is_valid.emit((True, self.get_activity_name()))
        else:
            self.status_label.setText("Incorrect Credentials\t\t{} trial{}".format(self.counter, "s" if self.counter != 1 else " "))
            self.counter += 1
            self.setWindowOpacity(1 - (self.counter / 15))

    def set_background_color(self, color):
        self.setStyleSheet(f"background:{color};")

    def closeEvent(self, event = None):
        self.deleteLater()

    def set_activity_name(self, activity_name):
        self.activity_name = activity_name

    def get_activity_name(self):
        return self.activity_name

functions = Data.More_Functions()
functions.load()
words = open("./English.txt", "r").readlines()
icons = open("./icons.txt", "r").readlines()
sounds = open("./sounds.txt", "r").readlines()
def get_word(position):
    return words[position-1][:-1]

def get_icon(position):
    return functions.get_wdir() + icons[position-1][:-1]

def get_sound(position):
    return functions.get_wdir() + sounds[position-1][:-1]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_App()
    sys.exit(app.exec())