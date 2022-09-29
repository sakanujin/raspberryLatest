from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.togglebutton import ToggleButton # for toggle
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.clock import Clock
################################################# 
import time
import RPi.GPIO as GPIO
################################################# 
#Config.set('graphics', 'width', '600')
#Config.set('graphics', 'width', '800')
#Config.set('graphics', 'height', '480')
Window.fullscreen = 'auto'
################################################# 
#GPIO  Test 
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)




################################################# 
 
class Display(BoxLayout):
    pass
 
class Screen_One(Screen): # 3rd Screen
    renzokku = 1
    danzok   = 0
    stMin =   StringProperty()
    valMin =   3

    def __init__(self, **kwargs):
        self.valMin = 3
        self.stMin = str(3)
        super(Screen_One, self).__init__(**kwargs)
        
    def btcUP(self): #UP  
        self.valMin = self.valMin + 1
        self.stMin  = str(self.valMin)

    def btcDOWN(self):  
        self.valMin = self.valMin - 1
        self.stMin  = str(self.valMin)
        #self.set_num = self.set_num - 1

    def btcSET(self):  
        pass

class Screen_KitchenTimer(Screen):
    is_countdown = BooleanProperty(False)
    left_time = NumericProperty(0)

    def on_command(self, command):
        if command == '+10 sec':
            self.left_time += 10
        elif command == '-10 sec':
            self.left_time -= 10
        elif command == 'start/stop':
            if self.is_countdown:
                self.stop_timer()
            elif self.left_time > 0:
                self.start_timer()
        elif command == 'reset':
            self.stop_timer()
            self.left_time   = 0

    def on_countdown(self, dt):
        self.left_time -=1
        if self.left_time == 0:
            self.is_countdown = False
            return False

    def start_timer(self):
        self.is_countdown = True
        Clock.schedule_interval(self.on_countdown, 1.0)
        pass

    def stop_timer(self):
        self.is_countdown = False
        Clock.unschedule(self.on_countdown)
        pass

################################################
class Screen_AGI(Screen):
    renzokku = 1
    danzok   = 0

    def __init__(self, **kwargs):
        super(Screen_AGI, self).__init__(**kwargs)

    pass
################################################
class Screen_Alert(Screen):

    def __init__(self, **kwargs):
        super(Screen_Alert, self).__init__(**kwargs)


    pass

################################################

class TextWidget(Screen):
    text1 = StringProperty()
    text2 = StringProperty()
    text3 = StringProperty()
    text4 = StringProperty()
    temp_now = StringProperty()
    temp_set = StringProperty()
    set_num  = 0   

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.text1 = 'オフ'
        self.text2 = 'UP'
        self.text3 = 'DOWN'
        self.text4 = 'オフ'
        self.temp_now = str(25)
        self.temp_set = self.temp_now
        self.set_num  = int(self.temp_set)

    def buttonClicked(self):  

        if self.text4 == "オン":

            self.text4 = "オフ"
            print(self.text4)

        elif self.text4 == "オフ":
            self.text4 = "オン"
            print(self.text4)


    def btc2(self): #UP  
        self.set_num = self.set_num + 1
        self.temp_set  = str(self.set_num)
        GPIO.output(21,1)


    def btc3(self):  
        self.set_num = self.set_num - 1
        self.temp_set  = str(self.set_num)
        GPIO.output(21,0)


class SM02App(App):
    def build(self):
        return Display()

if __name__ == "__main__":

    SM02App().run()

