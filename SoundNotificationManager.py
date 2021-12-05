import os, time
from threading import Thread
from win10toast import ToastNotifier
#add path so that python-vlc works fine
os.environ['PYTHON_VLC_MODULE_PATH'] = "./textures"
os.environ['PYTHON_VLC_LIB_PATH'] = "./textures/VLC/libvlc.dll"
from vlc import Media, MediaPlayer

class PlaySound:
    def __init__(self, path):
        self.player = MediaPlayer()
        self.path = ""
        if path is not None:
            self.set_path(path)
        self.volume = 100

    def set_volume(self, volume):
        if volume <= 1:
            self.volume = volume * 100
        elif volume <= 100:
            self.volume = volume
        elif volume <= 1_000:
            self.volume = volume / 10

    def get_volume(self):
        return self.volume
    
    def set_path(self, path):
        path = path.replace("\\", "/")
        if os.path.exists(path):
            self.path = path

    def get_path(self):
        return self.path.replace("\\", "/")

    def play(self, seconds):
        if os.path.exists(self.get_path()):
            Thread(target=self.player_thread, args=(seconds,), daemon=True, name="Player").start()       
        

    def player_thread(self, seconds):
        media = Media(self.get_path())
        self.player.set_media(media)
        self.player.play()
        new_volume = 1
        self.player.audio_set_volume(1)
        while seconds >= 0:
            if self.volume >= new_volume:
                self.player.audio_set_volume(new_volume)
                new_volume += 1
            if self.player.is_playing() == False:
                self.player.set_media(media)
                self.player.play()
                print(seconds)
            time.sleep(0.2)
            seconds -= 0.2
        self.player.stop()

    def pause(self):
        self.player.pause()
        

class Notification:
    def __init__(self):
        self.main_notification = ToastNotifier()

    def show_notification(self, title, message, duration, icon):
        Thread(target=self.write_notification, args=(title, message, duration, icon), daemon=True, name="Notification").start()

    def write_notification(self, title, message, duration, icon):
        self.main_notification.show_toast(title, message, icon, duration)
        
