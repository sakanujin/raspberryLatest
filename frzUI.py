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
from functools import partial 
################################################# 
# if you use the code for Raspberry Pi, turn into True,  if use PC pls put False

#RASPBERRY_CODE = True
RASPBERRY_CODE = False

if (RASPBERRY_CODE == True):
    import pt100
    import RPi.GPIO as GPIO

import time
################################################# 
#Config.set('graphics', 'width', '600')
#Config.set('graphics', 'width', '1016')
#Config.set('graphics', 'height', '100')
Window.fullscreen = 'auto'
#Window.fullscreen = True
################################################# 
#GPIO  Test 
if (RASPBERRY_CODE == True):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT) #CDU  
    GPIO.setup(16, GPIO.OUT) #AGI
    GPIO.setup(12, GPIO.IN)  #ERR State
    GPIO.setup(13, GPIO.OUT) #Buzzer out
################################################# 
#GLOBAL variables
glob_CDU_stat = 0
glob_AGI_stat = 1  #1 Renzoku,  2 Danzoku 
glob_current_temp = 25
glob_setting_temp = 25
glob_delay        = 3

################################################# 
#def control_OnOff_by_temp(now, setting, delta:float):
def control_OnOff_by_temp():
    print("#DEBUG# On/Off delay time is ", glob_delay)
    #print("now:{}, set:{}".format(now, setting))
    if (glob_current_temp >= (glob_setting_temp + 2)):
        print("************** CDU ON ************")
        glob_CDU_stat = 1
        if(RASPBERRY_CODE == True):
            GPIO.output(21, 1)
            if (glob_AGI_stat == 0):# AGI Danzoku 
                GPIO.output(16, 1)
    elif (glob_current_temp <= (glob_setting_temp - 2)):
        print("///////////// CDU OFF ////////////")
        glob_CDU_stat = 0
        if(RASPBERRY_CODE == True):
            GPIO.output(21, 0)
            if (glob_AGI_stat == 0):# AGI Danzoku 
                GPIO.output(16, 0)
################################################# 
 
class Display(BoxLayout):
    pass
 
class Screen_One(Screen): # 3rd Screen
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

    def btcDelaySet(self):  
        global glob_delay
        glob_delay = self.valMin 
        print("#DEBUG# delay time is set " ,glob_delay)
        

    def btRenzoku(self):  
        glob_AGI_stat = 0
        if(RASPBERRY_CODE == True):
            GPIO.output(16, 1) # always AGI ON  

    def btDanzoku(self):  
        glob_AGI_stat = 0

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
        #Clock.schedule_interval(self.on_countdown, 1.0) sec 
        Clock.schedule_interval(self.on_countdown, 60.0)  #min
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
        #self.temp_now = str(25)

        if (RASPBERRY_CODE == True):
            self.temp_now = str(pt100.pt100GetTmp())
        else: 
            self.temp_now = str(25)

        self.temp_set = self.temp_now
        self.set_num  = int(self.temp_set)

    def buttonClicked(self):  

        if self.text4 == "オン":

            self.text4 = "オフ"
            #print(self.text4)

        elif self.text4 == "オフ":
            self.text4 = "オン"
            #print(self.text4)


    def btc2(self): #UP  
        global glob_setting_temp  
        self.set_num = self.set_num + 1
        self.temp_set  = str(self.set_num)
        glob_setting_temp = self.set_num
        print("#DEBUG set TEMP push Plus:"  , self.set_num) 
        print("#DEBUG set grobal_setting_temp:"  , glob_setting_temp) 


    def btc3(self):  
        global glob_setting_temp  
        self.set_num = self.set_num - 1
        self.temp_set  = str(self.set_num)
        glob_setting_temp = self.set_num
        print("#DEBUG set TEMP push minus:"  , self.set_num) 
        print("#DEBUG set grobal_setting_temp:"  , glob_setting_temp) 

class SM02App(App):
    def build(self):
        Clock.schedule_interval(lambda dt: control_OnOff_by_temp(), glob_delay*60)
        return Display()

if __name__ == "__main__":
    SM02App().run()
