#DoorInABox
#Python Script
#Developed by FCEO all rights reserved 
#Date 5/12/2022
#Version 1.0

import time
from time import ctime, struct_time # library module for Get current Time
from threading import Thread
import PySimpleGUI as sg # https://pysimplegui.readthedocs.io/en/latest/#license  free source code 
import RPi.GPIO as GPIO # https://pypi.org/policy/terms-of-use/  free source code 
import configparser  #Library for config files read / write
import os #Library for logs creation


#-----------------------------------------------------------------------------------------------------
#--------------------//Global Variables a initial Config Definition//--------------------------------------------------
#----------------------------------------------------------------------------------------------------

RightPresencepin = 7    #Pin for Led to test right presence
LeftPresencepin = 11    #Pin for Led to test left presence
DayNightControlpin = 24 #PWM pGlobal Variables a initial Config Definitionin for control LEDs intensity
servopin = 18           #Pin for servo control
graphic_off = True      #Variable for graphic button updates
precenceDoorRight = False #Variable for graphic button updates
precenceDoorLeft = True   #Variable for graphic button updates
TestDoor_exit_flag = False #Variable for control TestDoor Stop execution
TestMotion_exit_flag = False #Variable for control TestMotion Stop execution
TestOptical_exit_flag = False #Variable for control TestOptical Stop execution
LogFileCreation = True
fileName = ''  #config Name
ConfigReader = configparser.ConfigParser()  #Read / write config initialization
threads = []                        #Async execution (threads) array
DoorTestLog = '----------------------Door Test Status----------------------------------------\n------------------------------------------------------------------------------\n\n'
MotionTestLog = '----------------------Motion Test Status--------------------------------------\n------------------------------------------------------------------------------\n\n'
OpticalTestLog = '----------------------Optical Test Status-------------------------------------\n------------------------------------------------------------------------------\n\n'

GPIO.setmode(GPIO.BCM) #BCM pin out mode for Raspberry pi (PWM Control)
GPIO.setwarnings(False) # Disable GPIO Warings (PinOut use/re-use)

GPIO.setup(RightPresencepin,GPIO.OUT)       #setting pin as Output
GPIO.setup(LeftPresencepin,GPIO.OUT)        #setting pin as Output
GPIO.setup(servopin, GPIO.OUT)              #setting pin as Output
GPIO.setup(DayNightControlpin, GPIO.OUT)    #setting pin as Output

GPIO.output(RightPresencepin,GPIO.LOW)   #Initialize signal in low state
GPIO.output(LeftPresencepin,GPIO.LOW)    #Initialize signal in low state
DayNightControl = GPIO.PWM(DayNightControlpin, 100) 
ServoMotor = GPIO.PWM(servopin, 100)               # GPIO for PWM with 50Hz
ServoMotor.start(0)   
ServoMotor.ChangeDutyCycle(12.5)                # Servommotor Initial Position
DayNightControl.start(0)                        # Initial Day/Night intensity



# Base64 code Images
startbtn = b'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'
startedbtn = b'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'
toggle_btn_off = b'iVBORw0KGgoAAAANSUhEUgAAAGQAAAA1CAMAAACA7r40AAAACXBIWXMAABYlAAAWJQFJUiTwAAAAP1BMVEX6+vr4+Pj19fX29vbz8/Pv7+/t7e3x8fFzc3N0dHTl5eW1tbVpaWnIyMiEhIR5eXmRkZHY2Njq6uqcnJypqalIAPceAAAESElEQVRYw61YiXarIBBFZEdW/f9vfTOADUSTSs8ba9pYMzf3zsIg4afJq91dm7TimvAHJiX7cjRP3e1w8P4i+cbkPxC6Bal/wCnMHyyXj1Yy8kWGXIhKnpPdfdBaK6WD0jMW4uGMkKe3e7mY5Onw4NvHuO/RI075gRNffzG8F4Bcbu5umMA1kXYV/JGElJQxKrMDyOZe/0oKIfAu5Z3o82GQS5gjhD1JttJm68ok4OIHi4vvLM6/4OaYMMPEAFLfJQ//ZAww1pdRtqa4PRGrAwTRrKixESMTp72TDJwOtgCidGp7IFevnFa7GeVCIsKqaCijhcXyMnzLmAlbi796CqKjkdU1aRhCAkY+aSzLiLIwmv2mJjQrMdyN4KKXy2nAYIixIMY7Dltz3DalpgRTu+jlEiZ4gxDLBaCC0JWiYmoCA09bdCLlVYgY0sJ+dLrAYL6xhFRmckyFkICLbEycsgu70ekHBHOMHptSkykWBRhB1WT2kb/HG4y8xZ9PCVZbABQFJxh94bRjAwapx4hCqds2PVeVQCXLAoJEoD4+kjgVo9JvSk0Vvw5JVrlSsFiDI0YlM+olLcR+Ti518CqXDYa+hYTcRR/SeNsmmWgvKkiMfS8hb0ePMq+X0omjXCYcjN4k14UI1MqBoZ9KMChIBEnaDV3xnkopIubmgoJ2FLmcTmUJ+cCgw6lVrx8rVhpYxOwSEPcB5GNQoFLMrFwYeWCCIH1EqldCzlLsmFCaAWROL4UgPNuQ1xGFFIyb9GICQWYyWGmfr0zO7/9DpY8JMpnrxMAkl8CHNCRw+/6ELO9E/hKTEviSXfKSXeQk1eHA5OK2yWrUehcEV0VtGb3NrkvFU9tiop92YaVsYcJ9hGlxvauQMfTwReJcg8TTFSZy94KtH5gMXWUVaq5BAkww2FYELL6O3fUuMqYWqOXmkqstwAXE+J2+OuQ9EQRhMs4nlxOl4gU/YFa5TnWXgUWm2h7V4zVLKW/qoiWgDwMVunwFoTDC7ttc9sLdFvxjq4efQyX5C0grEj01RQIRkXmVC6ICCUa/gYCWdRyeWuIxIqIxwQQ7ZNuV3I2QOAyzfWIgahW748BdA492aCtZWyDPSXLtZ2Fein1qrtcgVmUiChORo3L0doHEOZ+WaehhXhX/pQ4dP0FKVGCciNqubHlpVuuwbelwgpichRRM2+X7F5BKRQDKnpeyCyqV2U7IbcbyTPK2eMAWGDclfUwAKR+waYRNChv2pYAhXZjL3YJRefBOrvICznBvLIEOxpquZQXguPl93hZbOPZcNlcDE14Pc8BXsEZixkIWMCqN9ecnHyIhj+j4j9uRCf7O5vCQert1Ljlnd9+Gp0cPI1puhQglKDuvPZN20Th8fKP+Yhofytj0456/skv0kjWg5OwfzDmThSxO+InQg9RL5b+y5QHnYsqqFvXBgOBdGMj1rk7MBvzL08Mzaz6i/wMmHoe06O7zzgAAAABJRU5ErkJggg=='
toggle_btn_on = b'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'
dayImage = b'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'
nightImage = b'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'
toggle_btn_off_log = b'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'
toggle_btn_on_log = b'iVBORw0KGgoAAAANSUhEUgAAADwAAAAgCAYAAABO6BuSAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAAnbSURBVFhHvVhrbxXHGX5291yNjQ3YYJsYFwIY2zTQNhFJidKkUkTURorURlWlfIj6x6rmQ1U1X6q2qKoaVbRJG0orkRCKaTFgAvgC2D42ts91L32emd1z83HBLc5ztGdn5/LOe5v3nRlnaWkxwpZw4qcJ/Az5F7kOQo5MWiOWWBt/Nb471QvtbSqTJKKIJcf2CVl262U7RjA1bBPcyHDDSjO4hWYnPEFgCxGJXA8B3+tIo+A7KPkhKvGkOwkrnIRqwOG0Gc9FV9rFHtdHFysc9rHCk1d21ncnUOAlDu/AeKIxvje8LkyXXFyemcf1xTUsFgMUgxB+sPMCp8IaMmEVmchHd1hG2vOQSaXYEsGjS2R29eDk6DBOHd6PA06Abr9k2iw289dBYKnHum3JzeJOMcJHN+bx6d0CHiKHsptB4HjsE4+hOiOHvSPXfmvwpona61RWf73jtvhlaTnISsDqOo7tyeHkgW5MDO3DSH8P8im6PrtW+RQrEW7NPcK/7i9g8dESxg8N4dtjoxjO+MiGAYnxiSEvFdpcWpVcm9TcspPH724t4/z1OSxEWVS8DMKQ7bJ8bP1kSCT1UGDrSqqUZ6jcUEZk3C4eEMPW6ZsNamQ/j7R2VddwIlfDj1+ZwOTALuxzQy6kkG0CacpdYx5CvtedDBbKPj65fhc3787itVNj+NZQH3qCEslaoUPHGqRJYMtIzU1h3cvj51/M4vztVay4OWPRViu2oiHo08IK2TzOI2MpCpLfWMIPTw7j3dOj2J+KkDaWorBu4hHNsHS4eknLQZEErzxcw68vXcPk6BC+NzaMLi4Dre0ELRaOqIVFWvaX/1zAr26vYCPVBcYnkqVW2W4F3pZkT4QisiKz1mlvcQnvv3QY75wYxm6nhhTn0txGrq1gZTYPTcIl52GuFOKDP32G8ZH9+O7RQWNp04HzGJNJO4Is+4c7Kzg/s4o1lgM6kRGSmqu7nv5p7Wbo2zRvE0ZY/hzOlCkW8P7Lx/CD8UHsobD0KXVoE9Y1fFheYhiWbD+X7pJjkHsuC7z3+ml8fus+vni4jgrjTpLqXE2nXOfTlW+v+/jt1CzduIvr2OiCUMemCQg7YXO93lYZTwNZVGNszqXbbqzgzdFefP/4ALq05mQJ8mSoJ1MYaBnYpwHx2eBF4zI0wNdyHt4+M4kLn1/HXJg1KRX0YJPXNXyDFr0wvcBGWjaZzKBRaqC9rlOfrZFoG2QsVa3gOaeI986MoY+ROU1hXO1AOqKTUlXHp2mIhqdDHxMDvTjQ34+/Tt1ChYFNHkOB5VYO5msOLt4roORw5chFDQU9McFNaNRL4S1u9lSw68ktruCNY4MYzTlcs0SijASdpm5BzIfxmhjih3+9XBrnXhrDzfsPUCB17daM3/o09afT88yz+ZYJIyZyS3AnQJYYgbv9Il6bOMIMz1jLqc3s29VdHRoYr3MWWcIgtTiyfy9uLpeY9ejSIcV+HKZxdZ7WVZDSj4Hqf7PadsCdkl/D4e4URnsZZZg66rruoGMZsNPTQDJYAdQ2yMqKCScODuDq9B3UqAJXUhdqERbLAQIGLuvKOw8tJbdWxjiZkXX//1klZEMDoi+aacaFgb29KKytYy1KU2BacYN74rLZRdnOXwUcmifyfYwMDZApRWtNvn0GWq3cjAat3nyO+/4AZR54XHktvRs1Cq2xdbfaYSgluXS3vkyKjtb5ZPO06Cy01rF9eLAyR80Kl69JANzB1QW1OfIrAOeTmD6nU+Q0+2Orcj7bwWZ+jaBGDhqxSR6d4bnxALKc0eM8dir7v5PxyrJgPapQLHNTwL0wGbNu3WCwGYlBNkNWjIsxwrDhMVJkVZZlrMrxmzIzX6Vc7JaZY60ILZuZZw0yqDDlZPL4cmGRmwIxTce21xpbol0wfds6+UijUYqLaEpjXR58VjdKPEe76KaM3GpH6Oa5a18+zRMLO5l9sX0EG+KfrfQm5fEXprK4du8BSgqYqterw1RPTo/JcmgCx0hgnwLPL61ioK8XPdxXmDW8i+fNUwf7kfV5fqS2TOLWAHK2k5aOvDTmqg6meKSTTMbBOqBZ3sSq1rKdIToSVim25KUwzZ3W6aOHtHC48WAj0z7O8hh1KMMttjGsqCUUm8vCVjNtXzM6jm6ke/DR1VtY19Yvrt8M0t5q2g5IlFGlda+t1LC8toEjfTmS0FpmI89K2O/W8OroPh6YZWXLfLsr2c/OM7eeYJ4Oxqpdu3HxyyVcXwvMTmgrK29Hn6KhGPGYO8ePL0/h+KFh7ImqjNC6Koh75HlIfsNYmSeW+FqkMYu62e2mXS+bsdVtyH+DBA68DAq5vfjg4ytY5F6gec9lFW7pPnEdq9mYVlldFwEu/jGzgEq5jLPHR5h6rUx1LlPs+3w+wk++MYIDKJrrFktFUNkKalPHs4KYc1HLdePSoo+fXprBcuShEuvbxBA9yiXxvEl8aUcYMNDScCH5rnCpXF0u449XpnHuxUn0o6Iepl9d4Ii5KxVU8OJgD340OYy9weNNq8pEbxJ9dkLLZfRQ6K4+/ObfD/Czv99EgXt6OqDJp+Zpug6WEtqXj0k/erNviet2aqWMD/98GW99cwJjPSlkm3h2lgvLcW++VOlmsEY3O39zCR9encUCj4y1+IrE7oaelbBi3tJLLObx0N5VKuDNg3m8+/I4nudJKu9X2UPBxt5ZCmIzUbzJ3USFClp10rg4fR+fTM3gOy+M4dWDu3la8s148W7idl1gQrnRUOPgopvG35Z8/OLybcysh9jwcgwqnrnClYJt0LeMit82pdfrmt9Ca13iQWq0HXheRRfPyEPhOs59/TBeP9qPgVwGu9hXHqdx6qnUrR1ajfwWfGC+sI4LV26gVAvw1isvYDLvIBOUdcNh3NwarElgY3JTUtlu56tOCrNVD3+ZXcHvr93FgyBDoR1TH9F1jHItn/WxBk11dWV0rGtuIJJPMmbup7nEhrMhjuVqmDwyiomhPeil8MosRZ585leLuH33Hm48KKBGDZw9eRRnRvaij1knHXLdGi/QqpWFRZzk6wLzJ6slsNbm5l5X4NwgLFMDn91n+lguYe5xFY9KvnEj9atfdrOs5C7bC6Koi3KeQTvWNfc3SuCXoBZBfVJhQMvqCi5CNqyZ+hQVlU+n0Zv1MNCTwzgVMTm4jztG9ucS0ClMVhU2yVUoFCw7ZEK/pKPg0oqaXsk6ZNqppjI83bgoc3ygUWKSZb1JwGjUvIWk3P7u1NapTm8V+YTUQ9yL3xSAbbJyho+ySzasmm1xQy4FV7tm21EX2Hy0aUOQ0Mbd6/V2auMiptpFwLcuh1qYFdoF6FT3pP6ESlS5+TdtehjgLF+N7vVAFhst+U7KAPAf+vHEi9avD44AAAAASUVORK5CYII='
#--------------------//Global Variables a initial Config Definition//---------------------------------
#-----------------------------------------------------------------------------------------------------




#-----------------------------------------------------------------------------------------------------
#--------------------//Layout screens definition//-----------------------------------------------------
#-----------------------------------------------------------------------------------------------------
sg.theme('Reddit')
sg.SetOptions('global',font= ('Default', 10))

menu_def_Auto = [['& OPEN', ['CONFIG FILE']], # Menu information and options
            ['& INFORMATION', 'ABOUT...'], ]




sliderconf = [
            [sg.Image(source = nightImage),sg.Push(),sg.Slider((3, 500), size=(42, 42), orientation='h', key='SLIDER',enable_events=True),sg.Push(),sg.Image(source = dayImage)],
            ]
DoorStateConfig= [
            [sg.Push(),sg.Text('Close / Open'), sg.Button('', image_data = toggle_btn_off, key='-TOGGLE-GRAPHIC-DOOR-',border_width=0),sg.Push()],
                ]
MotionSenConfig = [
            [sg.Push(),sg.Text('   Motion   '), sg.Button('', image_data = toggle_btn_off, key='-TOGGLE-GRAPHIC-PRESENCE-',border_width=0),sg.Push()],
                ]

layoutManual =  [ #Layout for manual window
                [sg.Frame('MANUAL TESTING',[[sg.Frame('--Optical Sensor--', sliderconf, element_justification = 'CENTER')],[sg.Frame('--Door State Sensor--',DoorStateConfig,element_justification = 'CENTER'),sg.Frame('--Motion Sensor--',MotionSenConfig,element_justification = 'CENTER',)],
                [sg.Button(button_text ='Exit Manual Mode',size = (10, 3))]],expand_x = True, expand_y = True, border_width = 5,element_justification = 'left')]
                ]


# Global Variables for Layouts elements information and sizes
sizeFrame=(245,358)
Combovalues = ['sec','min','hrs']
sizeCombo = (3, 5)
sizeInput = (7,5)
col1 = [
        [sg.Button('', image_data = startbtn, key='-STARTBTN_DOOR_TEST-',border_width=0,button_color ='#ffffff'),sg.Text('Cycles: Waiting For Start...', key = '-TXT_CYCLES_DOOR_TEST-')],
        [sg.Text('-------------------------------------------------------------------------------------------------------')],
        [sg.Text('-------------------------------------------------------------------------------------------------------')],
        [sg.Text('Time Open:',key = '-TXT_OPEN-'),sg.Push(),sg.Input(default_text = "",key = '-TIME_DOOR_OPEN-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white'),sg.Combo(Combovalues,key = '-UNITS_DOOR_OPEN-', default_value = 'sec',size = sizeCombo,readonly = True)],
        [sg.Text('Time Closed:',key = '-TXT_CLOSED-'),sg.Push(),sg.Input(default_text = "",key = '-TIME_DOOR_CLOSED-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white'),sg.Combo(Combovalues,key = '-UNITS_DOOR_CLOSED-', default_value = 'sec',size = sizeCombo, readonly = True)],
        [sg.Text('Total Cycles:     '),sg.Input(default_text = "",key = '-CYCLES_DOOR_TEST-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white'),sg.Push()],
        ]

col2 = [
        [sg.Button('', image_data = startbtn, key='-STARTBTN_MOTION_TEST-',border_width=0,button_color ='#ffffff'),sg.Text('Cycles: Waiting For Start...',key = '-TXT_CYCLES_MOTION_TEST-')],
        [sg.Text('-------------------------------------------------------------------------------------------------------')],
        [sg.Text('-------------------------------------------------------------------------------------------------------')],
        [sg.Text('No Motion Time:',key = '-TXT_NO_MOTION-'),sg.Input(default_text = "",key = '-CYCLE_TIME_MOTION-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white'),sg.Combo(Combovalues,key = '-UNITS_TIME_MOTION-', default_value = 'sec',size = sizeCombo, readonly = True)],
        [sg.Text('Motion Time: ',key = '-TXT_MOTION-'),sg.Push(),sg.Input(default_text = "",key = '-MOTION_SOURCE_TIME-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white'),sg.Combo(Combovalues,key = '-UNITS_MOTION_SOURCE_TIME-', default_value = 'sec',size = sizeCombo, readonly = True)],
        [sg.Text('Total Cycles:     '),sg.Input(default_text = "",key = '-CYCLES_MOTION_TEST-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white')],
        ]

col3 = [
        [sg.Button('', image_data = startbtn, key='-STARTBTN_OPTICAL_TEST-',border_width=0,button_color ='#ffffff'),sg.Text('Cycles: Waiting For Start...',key = '-TXT_CYCLES_OPTICAL_TEST-')],
        [sg.Text('Night Level:      ',key = 'NIGHT'),sg.Input(default_text = "",key = '-NIGHT_LIGHT_LEVEL-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Dawn Level:      ',key = 'DAWN'),sg.Input(default_text = "",key = '-DAWN_LIGHT_LEVEL-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Day Level:         ',key = 'DAY'),sg.Input(default_text = "",key = '-DAY_GHT_LIGHT_LEVEL-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Dusk Level:       ',key = 'DUSK'),sg.Input(default_text = "",key = '-DUSK_LIGHT_LEVEL-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Rate Change:',key = 'RATE'),sg.Push(),sg.Input(default_text = "",key = '-RATE_CHANGUE_NIGHT_DAY-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white'),sg.Combo(Combovalues,key = '-UNITS_RATE_CHANGE-', default_value = 'sec',size = sizeCombo, readonly = True)],
        [sg.Text('Night Time:'),sg.Push(),sg.Input(default_text = "",key = '-NIGHT_CYCLE_TIME-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white'),sg.Combo(Combovalues,key = '-UNITS_NIGHT_TIME-', default_value = 'sec',size = sizeCombo, readonly = True)],
        [sg.Text('Dawn Time:'),sg.Push(),sg.Input(default_text = "",key = '-DAWN_CYCLE_TIME-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white'),sg.Combo(Combovalues,key = '-UNITS_DAWN_TIME-', default_value = 'sec',size = sizeCombo, readonly = True)],
        [sg.Text('Day Time:'),sg.Push(),sg.Input(default_text = "",key = '-DAY_CYCLE_TIME-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white'),sg.Combo(Combovalues, key = '-UNITS_DAY_TIME-',default_value = 'sec',size = sizeCombo, readonly = True)],
        [sg.Text('Dusk Time:'),sg.Push(),sg.Input(default_text = "",key = '-DUSK_CYCLE_TIME-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white'),sg.Combo(Combovalues, key = '-UNITS_DUSK_TIME-',default_value = 'sec',size = sizeCombo, readonly = True)],
        [sg.Text('Total Cycles:      '),sg.Input(default_text = "",key = '-CYCLES_OPTICAL_TEST-', size = sizeInput,disabled = False,justification = 'left',background_color = 'white')],
        ]

layout = [[sg.Frame('Door State Sensor',col1, element_justification='l', size=sizeFrame ), sg.Frame('Motion Sensor',col2, element_justification='l', size=sizeFrame)
          , sg.Frame('Optical Sensor',col3, element_justification='l', size=sizeFrame)],[sg.Button(button_text ='Manual Operation',key = '-MANUAL_MODE-',size = (20, 3)),sg.Button('Save Values', key='-SAVE_PARAMETERS-',border_width=0,size = (20, 3)),sg.Text('Log File'), sg.Button('', image_data = toggle_btn_on_log, key='-LOG_FILE_CREATION-',border_width=0), sg.Push(),sg.Button(button_text ='Exit',size = (10, 3))]]

layoutAutomatic =   [ #layout for Automatic window
                    [sg.Menu(menu_def_Auto, tearoff=False, pad=(200, 1),font= ('Default', 11))],
                    [sg.Frame('AUTOMATIC OPERATION',layout,expand_x = True, expand_y = True, border_width = 5,element_justification = 'C')]
                    ]
#-----------------------------------------------------------------------------------------------------
#--------------------//Layout screens definition//-----------------------------------------------------
#-----------------------------------------------------------------------------------------------------





#-----------------------------------------------------------------------------------------------------
#--------------------//Main Loop//--------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def main():
#local Variables
    DoorTest = False
    MotionTest = False
    OpticalTest = False

    DoorTestexecution = False
    MotionTestexecution = False
    OpticalTestexecution = False

    TestDataDoorTest = []
    TestDataMotionTest = []
    TestDataOpticalTest = []


#global Variables manage
    global fileName
    global LogFileCreation
    global TestDoor_exit_flag
    global TestMotion_exit_flag
    global TestOptical_exit_flag
    global DoorTestLog
    global MotionTestLog
    global OpticalTestLog


#Window Initialization    

    windowAutomatic = sg.Window('Door in a Box - Automatic Mode', layoutAutomatic, size=(800, 390), finalize = True,resizable=True, location=(0,0))
    windowAutomatic.Maximize()
    windowManual = None
    TestStarted = False
    fileName = LoadConfigFile("Select Config File")
    if fileName!='()':
        FillParameters(fileName,windowAutomatic)
    else:
        fileName = 'DoorInABoxConfig.cfg'  #config Name

    while True:             # Event Loop
        try:
            if (not DoorTest and not MotionTest and not OpticalTest): #Buttons Disable and enable
                disableBtn(False,windowAutomatic)
                disabled = False
                if LogFileCreation and TestStarted:
                    TestStarted = False
                    LogName = "/home/masoniteuser/Desktop/DoorInABoox/Logs/Log " + LogtimeName + ".txt"
                    file = open(LogName, "w")
                    file.write(DoorTestLog + MotionTestLog + OpticalTestLog)
                    file.close()
                DoorTestLog = '----------------------Door Test Status----------------------------------------\n------------------------------------------------------------------------------\n\n'
                MotionTestLog = '----------------------Motion Test Status--------------------------------------\n------------------------------------------------------------------------------\n\n'
                OpticalTestLog = '----------------------Optical Test Status-------------------------------------\n------------------------------------------------------------------------------\n\n'    
                    
            else:
                if(disabled == False):
                    disableBtn(True,windowAutomatic)
                    disabled = True
                    if LogFileCreation:
                        TestStarted = True
                        Logtime = ctime()
                        LogtimeName = Logtime.replace(':','_')
                        


            event, values = windowAutomatic.read(timeout=0) #Window events Reading process / Timeout = 0 for real time window updates
 
            if event== 'Exit':
                break

            elif event== '-MANUAL_MODE-':  #manual mode event execution
                if windowManual == None:
                    windowManual = sg.Window('Door in a Box - Manual Mode', layoutManual, size=(800, 390), finalize = True,resizable=True, location=(0,0))
                ManualOperation(windowManual)

            elif event== '-SAVE_PARAMETERS-': #input Data validation and saving parameters to config File 
                SaveParameters(fileName,values)

            elif event == '-LOG_FILE_CREATION-': #input Data validation and saving parameters to config File
                LogFileCreation = not LogFileCreation
                if(LogFileCreation):
                    windowAutomatic['-LOG_FILE_CREATION-'].update(image_data=toggle_btn_on_log)
                else:
                    windowAutomatic['-LOG_FILE_CREATION-'].update(image_data=toggle_btn_off_log)

            elif event== 'CONFIG FILE':  #upload config files
                fileName = LoadConfigFile("Select Config File")
                if fileName!='()':
                    FillParameters(fileName,windowAutomatic)

            elif event== 'ABOUT...':  #About this application event
                about()

            elif event== '-UPDATE_VALUES_DOOR_TEST-':  #update Screen for Door Test (cycles, current test step)
                DoorTestUpdate = Thread( target=UpdateValuesDoorTest, args=(values[event],windowAutomatic), daemon=True)
                DoorTestUpdate.start()

            elif event== '-UPDATE_VALUES_MOTION_TEST-':   #update Screen for Motion Test (cycles, current test step)
                MotionTestUpdate = Thread( target=UpdateValuesMotionTest, args=(values[event],windowAutomatic), daemon=True)
                MotionTestUpdate.start()

            elif event== '-UPDATE_VALUES_OPTICAL_TEST-':    #update Screen for Optical Test (cycles, current test step)
                OpticalTestUpdate = Thread( target=UpdateValuesOpticalTest, args=(values[event],windowAutomatic), daemon=True)
                OpticalTestUpdate.start()

    # ---------------- events for button and start tests-----------------------------------
            elif event== '-STARTBTN_DOOR_TEST-':   #start / Stop Door Test execution
                if(not DoorTest):
                    DoorTest,TestDataDoorTest = GetTestValues(event,values) #Input data validation  / ensure correct values for test
                    if(DoorTest):
                        windowAutomatic[event].update(image_data=startedbtn)
                        DoorTestexecution = Thread( target=StepsDoorTest, args=(TestDataDoorTest, windowAutomatic), daemon=True)
                        DoorTestexecution.start() 
                        TestDoor_exit_flag = False  
                else:
                    TestDoor_exit_flag = True
                    windowAutomatic[event].update(image_data=startbtn)
                    windowAutomatic['-TXT_CLOSED-'].update(background_color = 'white')
                    windowAutomatic['-TXT_OPEN-'].update(background_color = 'white')
                    DoorTest = False

            elif event== '-STARTBTN_MOTION_TEST-':      #start / Stop Motion Test execution
                if(not MotionTest):
                    MotionTest,TestDataMotionTest = GetTestValues(event,values) #Input data validation  / ensure correct values for test
                    if(MotionTest):
                        windowAutomatic[event].update(image_data=startedbtn)
                        MotionTestexecution = Thread(target=StepsMotionTest, args= (TestDataMotionTest,windowAutomatic),daemon=True)
                        MotionTestexecution.start() 
                        TestMotion_exit_flag = False
                else:
                    TestMotion_exit_flag = True
                    windowAutomatic[event].update(image_data=startbtn)
                    windowAutomatic['-TXT_NO_MOTION-'].update(background_color = 'white')
                    windowAutomatic['-TXT_MOTION-'].update(background_color = 'white')
                    MotionTest = False
            
            elif event== '-STARTBTN_OPTICAL_TEST-': #start / Stop Optical Test execution
                if(not OpticalTest):
                    OpticalTest,TestDataOpticalTest = GetTestValues(event,values)  #Input data validation  / ensure correct values for test
                    if(OpticalTest):
                        windowAutomatic[event].update(image_data=startedbtn)
                        OpticalTestexecution = Thread(target=StepsOpticalTest, args= (TestDataOpticalTest,windowAutomatic),daemon=True)
                        OpticalTestexecution.start() 
                        TestOptical_exit_flag = False   
                else:
                    TestOptical_exit_flag = True
                    windowAutomatic[event].update(image_data=startbtn)
                    windowAutomatic['NIGHT'].update(background_color = 'white')
                    windowAutomatic['DAWN'].update(background_color = 'white')
                    windowAutomatic['DAY'].update(background_color = 'white')
                    windowAutomatic['DUSK'].update(background_color = 'white')
                    windowAutomatic['RATE'].update(background_color = 'white')
                    OpticalTest = False
  
        except Exception as exception:
            sg.popup_error('ERROR!', 'Exception: ' + exception.__class__.__name__)

    GPIO.cleanup()        
    ServoMotor.stop()
    DayNightControl.stop()
    windowAutomatic.close()
#-----------------------------------------------------------------------------------------------------
#--------------------//Main Loop//--------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------




#--------------------//UpdateValuesDoorTest//--------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def UpdateValuesDoorTest(EventData,windowAutomatic):
    if(EventData == 'OPEN'):
        windowAutomatic['-TXT_CLOSED-'].update(background_color = 'white')
        windowAutomatic['-TXT_OPEN-'].update(background_color = '#69e345')
    elif(EventData == 'CLOSED'):
        windowAutomatic['-TXT_OPEN-'].update(background_color = 'white')
        windowAutomatic['-TXT_CLOSED-'].update(background_color = '#69e345')
    else:     
        windowAutomatic['-TXT_CYCLES_DOOR_TEST-'].update(EventData) 

    return


#--------------------//UpdateValuesMotionTest//--------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def UpdateValuesMotionTest(EventData,windowAutomatic):

    if(EventData == 'CYCLE_TIME'):
        windowAutomatic['-TXT_MOTION-'].update(background_color = 'white')
        windowAutomatic['-TXT_NO_MOTION-'].update(background_color = '#69e345')
    elif(EventData == 'MOTION_TIME'):
        windowAutomatic['-TXT_NO_MOTION-'].update(background_color = 'white')
        windowAutomatic['-TXT_MOTION-'].update(background_color = '#69e345')
    else:
        windowAutomatic['-TXT_CYCLES_MOTION_TEST-'].update(EventData) 

    return 


#--------------------//UpdateValuesMotionTest//--------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def UpdateValuesOpticalTest(EventData,windowAutomatic):

    
        if EventData== '1':
            windowAutomatic['DUSK'].update(background_color = 'white')
            windowAutomatic['NIGHT'].update(background_color = '#69e345')
            windowAutomatic['RATE'].update(background_color = 'white')
        elif EventData =='2':
            windowAutomatic['NIGHT'].update(background_color = '#69e345')
            windowAutomatic['DAWN'].update(background_color = '#69e345')
            windowAutomatic['RATE'].update(background_color = '#69e345')
        elif EventData == '3':
            windowAutomatic['NIGHT'].update(background_color = 'white')
            windowAutomatic['DAWN'].update(background_color = '#69e345')
            windowAutomatic['RATE'].update(background_color = 'white')
        elif EventData == '4':
            windowAutomatic['DAWN'].update(background_color = '#69e345')
            windowAutomatic['DAY'].update(background_color = '#69e345')
            windowAutomatic['RATE'].update(background_color = '#69e345')
        elif EventData =='5':
            windowAutomatic['DAWN'].update(background_color = 'white')
            windowAutomatic['DAY'].update(background_color = '#69e345')
            windowAutomatic['RATE'].update(background_color = 'white')
        elif EventData == '6':
            windowAutomatic['DAY'].update(background_color = '#69e345')
            windowAutomatic['DUSK'].update(background_color = '#69e345')
            windowAutomatic['RATE'].update(background_color = '#69e345')
        elif EventData == '7':
            windowAutomatic['DAY'].update(background_color = 'white')
            windowAutomatic['DUSK'].update(background_color = '#69e345')
            windowAutomatic['RATE'].update(background_color = 'white')
        elif EventData == '8':
            windowAutomatic['DUSK'].update(background_color = '#69e345')
            windowAutomatic['NIGHT'].update(background_color = '#69e345')
            windowAutomatic['RATE'].update(background_color = '#69e345')
        else:
            windowAutomatic['-TXT_CYCLES_OPTICAL_TEST-'].update(EventData) 

        return



#--------------------//Door Test Execution Sequence//--------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def StepsDoorTest(DataForTest,windowAutomatic):
    global TestDoor_exit_flag
    global DoorTestLog
    Step = 1
    CycleOnProcess = False
    TimeOpen = int(DataForTest[0])
    TimeClosed = int(DataForTest[1])
    Logtime = ctime()
    DoorTestLog = DoorTestLog + 'Test Started at: ' + Logtime + '\n\n'

    
    
    ServoMotor.start(5)
    for num in range(1, int(DataForTest[2] + 1), 1): 
        CountingString = 'Cycles: ' + str(num) + ' of ' +  str(DataForTest[2]) + ' Total'
        windowAutomatic.write_event_value('-UPDATE_VALUES_DOOR_TEST-', CountingString)
        CycleOnProcess = True
        DoorTestLog = DoorTestLog + '>>Cycle: ' + str(num)  + '\n'
        Step = 1
        actualStep = 0
        InitialTime = time.time()
        while(CycleOnProcess == True):
            if(Step == 1):
                if actualStep!=Step:
                    actualStep = Step
                    Logtime = ctime()
                    DoorTestLog = DoorTestLog + 'Door Open: ' + Logtime  + '\n'
                    windowAutomatic.write_event_value('-UPDATE_VALUES_DOOR_TEST-', 'OPEN')
                    ServoMotor.ChangeDutyCycle(12.5)
                ActualTime = time.time()
                if(ActualTime - InitialTime) > TimeOpen:
                    Step = Step + 1
                    InitialTime = time.time()
            elif(Step == 2):
                if actualStep!=Step:
                    actualStep = Step
                    Logtime = ctime()
                    DoorTestLog = DoorTestLog + 'Door Closed: ' + Logtime  + '\n'
                    windowAutomatic.write_event_value('-UPDATE_VALUES_DOOR_TEST-', 'CLOSED')
                    ServoMotor.ChangeDutyCycle(5)
                ActualTime = time.time()
                if((ActualTime - InitialTime) > TimeClosed ):
                    Step = Step + 1
                    InitialTime = time.time()
            elif(Step == 3):
                  CycleOnProcess = False
            if TestDoor_exit_flag == True:
                Logtime = ctime()
                DoorTestLog = DoorTestLog + '\nTest Stoped at: ' + Logtime + '\n\n'
                return

    Logtime = ctime()
    DoorTestLog = DoorTestLog + '\nTest Ended at: ' + Logtime + '\n\n'            
    windowAutomatic.write_event_value('-STARTBTN_DOOR_TEST-','TEST_DONE')

    return



#--------------------//Motion Test Execution Sequence//--------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def StepsMotionTest(DataForTest,windowAutomatic):
    global TestMotion_exit_flag
    global MotionTestLog
    Step = 1
    CycleOnProcess = False
    Cycletime = int(DataForTest[0])
    MotionTime = int(DataForTest[1])
    Logtime = ctime()
    MotionTestLog = MotionTestLog + 'Test Started at: ' + Logtime + '\n\n'


    for num in range(1, int(DataForTest[2] + 1), 1): 
        CountingString = 'Cycles: ' + str(num) + ' of ' +  str(DataForTest[2]) + ' Total'
        windowAutomatic.write_event_value('-UPDATE_VALUES_MOTION_TEST-', CountingString)
        actualStep = 0
        CycleOnProcess = True
        MotionTestLog = MotionTestLog + '>>Cycle: ' + str(num)  + '\n'
        Step = 1
        InitialTime = time.time()
        while(CycleOnProcess == True):
            if(Step == 1):

                if actualStep!=Step:
                    actualStep = Step
                    Logtime = ctime()
                    MotionTestLog = MotionTestLog + 'No Motion Time: ' + Logtime  + '\n'
                    windowAutomatic.write_event_value('-UPDATE_VALUES_MOTION_TEST-', 'CYCLE_TIME')
                    GPIO.output(RightPresencepin,GPIO.HIGH)
                ActualTime = time.time()
                if(ActualTime - InitialTime) >= Cycletime:
                    Step = Step + 1
                    InitialTime = time.time()
            elif(Step == 2):
                if actualStep!=Step:
                    actualStep = Step
                    Logtime = ctime()
                    MotionTestLog = MotionTestLog + 'Motion Time: ' + Logtime  + '\n'
                    windowAutomatic.write_event_value('-UPDATE_VALUES_MOTION_TEST-', 'MOTION_TIME')
                    GPIO.output(RightPresencepin,GPIO.LOW)
                ActualTime = time.time()
                if(ActualTime - InitialTime) >= MotionTime:
                    Step = Step + 1
                    InitialTime = time.time()
            elif(Step == 3):
                CycleOnProcess = False

            if TestMotion_exit_flag == True:
                Logtime = ctime()
                MotionTestLog = MotionTestLog + '\nTest Stoped at: ' + Logtime + '\n\n'
                return
    
    Logtime = ctime()
    MotionTestLog = MotionTestLog + '\nTest Ended at: ' + Logtime + '\n\n' 
    windowAutomatic.write_event_value('-STARTBTN_MOTION_TEST-','TEST_DONE')
    return



#--------------------//Optical Test Execution Sequence//--------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def StepsOpticalTest(DataForTest,windowAutomatic):
    
    global TestOptical_exit_flag
    global OpticalTestLog
    Step = 1
    CycleOnProcess = False
    Diference = 0
    NightValue = ( (int(DataForTest[0]) - 3) / (500 - 3) ) * (100 - 0) + 0 # Mapped Values
    DawnValue  = ( (int(DataForTest[1]) - 3) / (500 - 3) ) * (100 - 0) + 0 # Mapped Values
    DayValue = ( (int(DataForTest[2]) - 3) / (500 - 3) ) * (100 - 0) + 0 # Mapped Values
    DuskValue = ( (int(DataForTest[3]) - 3) / (500 - 3) ) * (100 - 0) + 0 # Mapped Values
    ChangeTime  = int(DataForTest[4])
    NightTime = int(DataForTest[5])
    Dawntime = int(DataForTest[6])
    DayTime = int(DataForTest[7])
    DuskTime = int(DataForTest[8])
    Logtime = ctime()
    OpticalTestLog = OpticalTestLog + 'Test Started at: ' + Logtime + '\n\n'

    for num in range(1, int(DataForTest[9] + 1), 1): 
        CountingString = 'Cycles: ' + str(num) + ' of ' +  str(DataForTest[9]) + ' Total'
        windowAutomatic.write_event_value('-UPDATE_VALUES_OPTICAL_TEST-', CountingString)
        CycleOnProcess = True
        OpticalTestLog = OpticalTestLog + '>>Cycle: ' + str(num)  + '\n'
        Step = 1
        actualStep = 0
        InitialTime = time.time()
        while(CycleOnProcess == True):
            if TestOptical_exit_flag == True:
                Logtime = ctime()
                OpticalTestLog = OpticalTestLog + '\nTest Stoped at: ' + Logtime + '\n\n'
                return
            if(Step == 1):
                if actualStep!=Step:
                    actualStep = Step
                    Logtime = ctime()
                    OpticalTestLog = OpticalTestLog + 'Night: ' + Logtime  + '\n'
                    windowAutomatic.write_event_value('-UPDATE_VALUES_OPTICAL_TEST-', str(Step))
                    DayNightControl.ChangeDutyCycle(NightValue)
                ActualTime = time.time()
                if (ActualTime - InitialTime) >= NightTime:
                    Step = Step + 1
                    InitialTime = time.time()
            elif(Step == 2):
                if actualStep!=Step:
                    actualStep = Step
                    Diference = DawnValue - NightValue
                    Increace = Diference / ChangeTime
                    Logtime = ctime()
                    OpticalTestLog = OpticalTestLog + 'Transition: ' + Logtime  + '\n'
                    windowAutomatic.write_event_value('-UPDATE_VALUES_OPTICAL_TEST-', str(Step))
                ActualTime = time.time()
                ValueToWrite = int(((ActualTime - InitialTime) * Increace) + NightValue)
                DayNightControl.ChangeDutyCycle(ValueToWrite)
                if ((ActualTime - InitialTime) > ChangeTime or ValueToWrite >= DawnValue):
                    Step = Step + 1
                    InitialTime = time.time()
            if TestOptical_exit_flag == True:
                Logtime = ctime()
                OpticalTestLog = OpticalTestLog + '\nTest Stoped at: ' + Logtime + '\n\n'
                return
            elif(Step == 3):
                if actualStep!=Step:
                    actualStep = Step
                    Logtime = ctime()
                    OpticalTestLog = OpticalTestLog + 'Dawn: ' + Logtime  + '\n'
                    windowAutomatic.write_event_value('-UPDATE_VALUES_OPTICAL_TEST-', str(Step))
                    DayNightControl.ChangeDutyCycle(DawnValue)
                ActualTime = time.time()
                if (ActualTime - InitialTime) >= Dawntime:
                    Step = Step + 1
                    InitialTime = time.time()
            elif(Step == 4):
                if actualStep!=Step:
                    actualStep = Step
                    Diference = DayValue - DawnValue
                    Increace = Diference / ChangeTime
                    Logtime = ctime()
                    OpticalTestLog = OpticalTestLog + 'Transition: ' + Logtime  + '\n'
                    windowAutomatic.write_event_value('-UPDATE_VALUES_OPTICAL_TEST-', str(Step))
                ActualTime = time.time()
                ValueToWrite = int(((ActualTime - InitialTime) * Increace) + DawnValue)
                DayNightControl.ChangeDutyCycle(ValueToWrite)
                if ((ActualTime - InitialTime) > ChangeTime or ValueToWrite >= DayValue):
                    Step = Step + 1
                    InitialTime = time.time()        
            elif(Step == 5):
                if actualStep!=Step:
                    actualStep = Step
                    Logtime = ctime()
                    OpticalTestLog = OpticalTestLog + 'Day: ' + Logtime  + '\n'
                    windowAutomatic.write_event_value('-UPDATE_VALUES_OPTICAL_TEST-', str(Step))
                    DayNightControl.ChangeDutyCycle(DayValue)
                ActualTime = time.time()
                if (ActualTime - InitialTime) >= DayTime:
                    Step = Step + 1
                    InitialTime = time.time()
            elif(Step == 6):
                if actualStep!=Step:
                    actualStep = Step
                    Diference = DayValue - DuskValue
                    Increace = Diference / ChangeTime
                    Logtime = ctime()
                    OpticalTestLog = OpticalTestLog + 'Transition: ' + Logtime  + '\n'
                    windowAutomatic.write_event_value('-UPDATE_VALUES_OPTICAL_TEST-', str(Step))
                ActualTime = time.time()
                ValueToWrite =  DayValue - int(((ActualTime - InitialTime) * Increace))
                DayNightControl.ChangeDutyCycle(ValueToWrite)
                if ((ActualTime - InitialTime) > ChangeTime or ValueToWrite <= DuskValue):
                    Step = Step + 1
                    InitialTime = time.time()   
            elif(Step == 7):
                if actualStep!=Step:
                    actualStep = Step
                    Logtime = ctime()
                    OpticalTestLog = OpticalTestLog + 'Dusk: ' + Logtime  + '\n'
                    windowAutomatic.write_event_value('-UPDATE_VALUES_OPTICAL_TEST-', str(Step))
                    DayNightControl.ChangeDutyCycle(DuskValue)
                ActualTime = time.time()
                if (ActualTime - InitialTime) >= DuskTime:
                    Step = Step + 1
                    InitialTime = time.time()   
            elif(Step == 8):
                if actualStep!=Step:
                    actualStep = Step
                    Diference = DuskValue - NightValue 
                    Increace = Diference / ChangeTime
                    Logtime = ctime()
                    OpticalTestLog = OpticalTestLog + 'Transition: ' + Logtime  + '\n'
                    windowAutomatic.write_event_value('-UPDATE_VALUES_OPTICAL_TEST-', str(Step))
                ActualTime = time.time()
                ValueToWrite =  DuskValue - int(((ActualTime - InitialTime) * Increace))
                DayNightControl.ChangeDutyCycle(ValueToWrite)
                if ((ActualTime - InitialTime) > ChangeTime or ValueToWrite <= NightValue):
                    Step = Step + 1
                    InitialTime = time.time()                       
            elif(Step == 9):
                CycleOnProcess = False
            if TestOptical_exit_flag == True:
                Logtime = ctime()
                OpticalTestLog = OpticalTestLog + '\nTest Stoped at: ' + Logtime + '\n\n'
                return
    
    Logtime = ctime()
    OpticalTestLog = OpticalTestLog + '\nTest Ended at: ' + Logtime + '\n\n' 
    windowAutomatic.write_event_value('-STARTBTN_OPTICAL_TEST-',"TEST_DONE")
    return


def disableBtn(state,windowAutomatic):
    if state:
        windowAutomatic['-SAVE_PARAMETERS-'].update(disabled = True)
        windowAutomatic['-MANUAL_MODE-'].update(disabled = True)
        windowAutomatic['-LOG_FILE_CREATION-'].update(disabled = True)
    else:
        windowAutomatic['-MANUAL_MODE-'].update(disabled = False)
        windowAutomatic['-SAVE_PARAMETERS-'].update(disabled = False)
        windowAutomatic['-LOG_FILE_CREATION-'].update(disabled = False)

def GetTestValues(Button,Data):


    DataValues = [] 

    for Dato in Data:
        Result = Data[Dato]
        DataValues.append(Result)

    DataValues.remove(None)

    TestData = []

    for Result in DataValues:
            print(Result)
            if Result !='sec' and Result !='min' and Result !='hrs':
                try:
                    Result = int(Result)
                    if(Result<1):
                        sg.popup_error('ERROR!', 'Error -3: Invalid Input Value',"Input Values must be greater than 0")
                        return False,None
                except:
                    sg.popup_error('ERROR!', 'Error -2: Invalid Input Value',"Input must be Numeric (An exception occurred while Trying to Run Test)")
                    return False,None


    if(Button == '-STARTBTN_DOOR_TEST-'):
        
        value = int(DataValues[0])
        units = DataValues[1]
        if(units == 'min'):
            value = value*60
        elif units == 'hrs':
            value = value*60*60

        TestData.append(value)
        
        value = int(DataValues[2])
        units = DataValues[3]

        if(units == 'min'):
            value = value*60
        elif units == 'hrs':
            value = value*60*60    
        TestData.append(value)

        value = int(DataValues[4])
        TestData.append(value)

    elif(Button == '-STARTBTN_MOTION_TEST-'):
        value = int(DataValues[5])
        units = DataValues[6]
        if(units == 'min'):
            value = value*60
        elif units == 'hrs':
            value = value*60*60    
        TestData.append(value)
        
        value = int(DataValues[7])
        units = DataValues[8]

        if(units == 'min'):
            value = value*60
        elif units == 'hrs':
            value = value*60*60    
        TestData.append(value)

        value = int(DataValues[9])
        TestData.append(value)

    elif(Button == '-STARTBTN_OPTICAL_TEST-'):
        value = int(DataValues[10])
        TestData.append(value)

        value = int(DataValues[11])
        TestData.append(value)

        value = int(DataValues[12])
        TestData.append(value)

        value = int(DataValues[13])
        TestData.append(value)
        
        value = int(DataValues[14])
        units = DataValues[15]
        if(units == 'min'):
            value = value*60
        elif units == 'hrs':
            value = value*60*60
        TestData.append(value)

        value = int(DataValues[16])
        units = DataValues[17]
        if(units == 'min'):
            value = value*60
        elif units == 'hrs':
            value = value*60*60
        TestData.append(value)

        value = int(DataValues[18])
        units = DataValues[19]
        if(units == 'min'):
            value = value*60
        elif units == 'hrs':
            value = value*60*60
        TestData.append(value)

        value = int(DataValues[20])
        units = DataValues[21]
        if(units == 'min'):
            value = value*60
        elif units == 'hrs':
            value = value*60*60
        TestData.append(value)

        value = int(DataValues[22])
        units = DataValues[23]
        if(units == 'min'):
            value = value*60
        elif units == 'hrs':
            value = value*60*60
        TestData.append(value)

        value = int(DataValues[24])
        TestData.append(value)

    return True,TestData



#-----------------------------------------------------------------------------------------------------
#--------------------//Manual Screen Operation//------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def ManualOperation(windowManual):
    global graphic_off
    global precenceDoorRight
    graphic_off = True
    precenceDoorRight = False
    windowManual.Maximize()
    windowManual.UnHide()
    GPIO.output(RightPresencepin,GPIO.LOW)
    DayNightControl.ChangeDutyCycle(0)
    ServoMotor.ChangeDutyCycle(12.5)

    while True:

        event, values = windowManual.read()
        if event == '-TOGGLE-GRAPHIC-DOOR-':   # if the graphical button that changes images
            graphic_off = not graphic_off
            windowManual['-TOGGLE-GRAPHIC-DOOR-'].update(image_data=toggle_btn_off if graphic_off else toggle_btn_on)
            if(graphic_off):
                ServoMotor.ChangeDutyCycle(12.5)
            else:
                ServoMotor.ChangeDutyCycle(5)
        elif event == '-TOGGLE-GRAPHIC-PRESENCE-':
            precenceDoorRight = not precenceDoorRight
            if(precenceDoorRight):
                print(precenceDoorRight)
                windowManual['-TOGGLE-GRAPHIC-PRESENCE-'].update(image_data=toggle_btn_on)
                GPIO.output(RightPresencepin,GPIO.HIGH)
            else:
                windowManual['-TOGGLE-GRAPHIC-PRESENCE-'].update(image_data=toggle_btn_off)
                GPIO.output(RightPresencepin,GPIO.LOW)
                print(precenceDoorRight)
        elif event == 'SLIDER':
                val = values["SLIDER"]
                val  = int(val)
                mapValue = ( (val - 3) / (500 - 3) ) * (100 - 0) + 0
                mapValue  = int(mapValue)
                print(mapValue)
                DayNightControl.ChangeDutyCycle(mapValue) 
        elif event == 'Exit Manual Mode':
            windowManual['-TOGGLE-GRAPHIC-PRESENCE-'].update(image_data=toggle_btn_off)
            windowManual['-TOGGLE-GRAPHIC-DOOR-'].update(image_data=toggle_btn_off)
            windowManual['SLIDER'].update(3)
            GPIO.output(RightPresencepin,GPIO.LOW)
            DayNightControl.ChangeDutyCycle(0)
            ServoMotor.ChangeDutyCycle(12.5)
            graphic_off = True
            precenceDoorRight = False
            windowManual.Hide()
            break

    return
#-----------------------------------------------------------------------------------------------------
#--------------------//Manual Screen Operation//------------------------------------------------------
#-----------------------------------------------------------------------------------------------------




#-----------------------------------------------------------------------------------------------------
#--------------------//About App Popout//-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def about(): #About Application PopOut
    sg.popup_ok('about', 'Version 1.0','Masonite',
    'Dor in a Box', sg.version)
    return
#-----------------------------------------------------------------------------------------------------
#--------------------//About App Popout//-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------
#--------------------//Load File Parameters Popout//-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def LoadConfigFile(msj):

    ConfigFileName = sg.popup_get_file(msj,
    title = 'Configuration',
    default_path = "/home/masoniteuser/Desktop/DoorInABoox/DoorInABoxConfig.cfg",
    default_extension = "cfg",
    save_as = False,
    multiple_files = False,
    file_types = (('ALL Files', '.cfg'),),
    no_window = True,
    size = (60, 25),
    button_color = None,
    background_color = None,
    text_color = None,
    icon = None,
    font = None,
    no_titlebar = False,
    grab_anywhere = True,
    keep_on_top = True,
    location = (None, None),
    relative_location = (None, None),
    initial_folder = None,
    image = None,
    files_delimiter = ";",
    modal = True,
    history = True,
    show_hidden = True,
    history_setting_filename = None)
    print('file Name')
    print(ConfigFileName)
    print('file Name')
    return str(ConfigFileName)
#-----------------------------------------------------------------------------------------------------
#--------------------//Load File Parameters Popout//-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------




#-----------------------------------------------------------------------------------------------------
#--------------------//Fill Parameters on interface//-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def FillParameters(fileName,Workingwindow):
    ConfigReader.read(fileName)
    Success = True

    try:
#-----------------------Door Estate Sensor
        Data = (ConfigReader['Door State Sensor']['Time Open']).split(',', 2)
        value = int(Data[0])
        units = Data[1]
        Workingwindow['-TIME_DOOR_OPEN-'].update(value)
        Workingwindow['-UNITS_DOOR_OPEN-'].update(units)
        
        Data = (ConfigReader['Door State Sensor']['Time Closed']).split(',', 2)
        value = int(Data[0])
        units = Data[1]
        Workingwindow['-TIME_DOOR_CLOSED-'].update(value)
        Workingwindow['-UNITS_DOOR_CLOSED-'].update(units)

        Workingwindow['-CYCLES_DOOR_TEST-'].update(ConfigReader['Door State Sensor']['Total Cycles'])


#--------------------------Motion Sensor
        Data = (ConfigReader['Motion Sensor']['Cycle Time']).split(',', 2)
        value = int(Data[0])
        units = Data[1]
        Workingwindow['-CYCLE_TIME_MOTION-'].update(value)
        Workingwindow['-UNITS_TIME_MOTION-'].update(units)

        Data = (ConfigReader['Motion Sensor']['Motion Time']).split(',', 2)
        value = int(Data[0])
        units = Data[1]
        Workingwindow['-MOTION_SOURCE_TIME-'].update(value)
        Workingwindow['-UNITS_MOTION_SOURCE_TIME-'].update(units)

        Workingwindow['-CYCLES_MOTION_TEST-'].update(ConfigReader['Motion Sensor']['Total Cycles'])


#--------------------------Optical Sensor
        Workingwindow['-NIGHT_LIGHT_LEVEL-'].update(ConfigReader['Optical Sensor']['Night Level'])
        Workingwindow['-DAWN_LIGHT_LEVEL-'].update(ConfigReader['Optical Sensor']['Dawn Level'])
        Workingwindow['-DAY_GHT_LIGHT_LEVEL-'].update(ConfigReader['Optical Sensor']['Day Level'])
        Workingwindow['-DUSK_LIGHT_LEVEL-'].update(ConfigReader['Optical Sensor']['Dusk Level'])

        Data = (ConfigReader['Optical Sensor']['Rate Changue']).split(',', 2)
        value = int(Data[0])
        units = Data[1]
        Workingwindow['-RATE_CHANGUE_NIGHT_DAY-'].update(value)
        Workingwindow['-UNITS_RATE_CHANGE-'].update(units)


        Data = (ConfigReader['Optical Sensor']['Night Time']).split(',', 2)
        value = int(Data[0])
        units = Data[1]
        Workingwindow['-NIGHT_CYCLE_TIME-'].update(value)
        Workingwindow['-UNITS_NIGHT_TIME-'].update(units)


        Data = (ConfigReader['Optical Sensor']['Dawn Time']).split(',', 2)
        value = int(Data[0])
        units = Data[1]
        Workingwindow['-DAWN_CYCLE_TIME-'].update(value)
        Workingwindow['-UNITS_DAWN_TIME-'].update(units)


        Data = (ConfigReader['Optical Sensor']['Day Time']).split(',', 2)
        value = int(Data[0])
        units = Data[1]
        Workingwindow['-DAY_CYCLE_TIME-'].update(value)
        Workingwindow['-UNITS_DAY_TIME-'].update(units)

        Data = (ConfigReader['Optical Sensor']['Dusk Time']).split(',', 2)
        value = int(Data[0])
        units = Data[1]
        Workingwindow['-DUSK_CYCLE_TIME-'].update(value)
        Workingwindow['-UNITS_DUSK_TIME-'].update(units)

        Workingwindow['-CYCLES_OPTICAL_TEST-'].update(ConfigReader['Optical Sensor']['Total Cycles'])

    except:
        print("An exception occurred while reading Config File")
        Success = False

    if Success==False:
        sg.popup_error('ERROR!', 'Error -1: Select a Valid Config File',"An exception occurred while reading Config File (review file Content)",fileName)
#-----------------------------------------------------------------------------------------------------
#--------------------//Fill Parameters on interface//-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------




#-----------------------------------------------------------------------------------------------------
#--------------------//Save Parameters to File//-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def SaveParameters(fileName,Data):

    Save = sg.popup_ok_cancel('Save in: ' + fileName)
    if(Save=='OK'):
        DataValues = [] 
        for Dato in Data:
            Result = Data[Dato]
            DataValues.append(Result)

        DataValues.remove(None)

        for Result in DataValues:
            print(Result)
            if Result !='sec' and Result !='min' and Result!='hrs':
                try:
                    Result = int(Result)
                    if(Result<1):
                        sg.popup_error('ERROR!', 'Error -3: Invalid Input Value',"Input Values must be greater than 0")
                        return
                except:
                    sg.popup_error('ERROR!', 'Error -2: Invalid Input Value',"An exception occurred while Writing Values to File : ",fileName)
                    return 
    

        try:
        #-----------------------Door State Sensor Writing Parameters
            ConfigReader.set('Door State Sensor','Time Open',str(Data['-TIME_DOOR_OPEN-']) + ',' + str(Data['-UNITS_DOOR_OPEN-']))
            ConfigReader.set('Door State Sensor','Time Closed',str(Data['-TIME_DOOR_CLOSED-']) + ',' + str(Data['-UNITS_DOOR_CLOSED-']))
            ConfigReader.set('Door State Sensor','Total Cycles', str(Data['-CYCLES_DOOR_TEST-']))


        #-----------------------Motion Sensor Writing Parameters
            ConfigReader.set('Motion Sensor','Cycle Time',str(Data['-CYCLE_TIME_MOTION-']) + ',' + str(Data['-UNITS_TIME_MOTION-']))
            ConfigReader.set('Motion Sensor','Motion Time', str(Data['-MOTION_SOURCE_TIME-']) + ',' + str(Data['-UNITS_MOTION_SOURCE_TIME-']))
            ConfigReader.set('Motion Sensor','Total Cycles', str(Data['-CYCLES_MOTION_TEST-']))


        #-----------------------Optical Sensor Writing Parameters
            ConfigReader.set('Optical Sensor','Night Level',str(Data['-NIGHT_LIGHT_LEVEL-']))
            ConfigReader.set('Optical Sensor','Dawn Level',str(Data['-DAWN_LIGHT_LEVEL-']))
            ConfigReader.set('Optical Sensor','Day Level',str(Data['-DAY_GHT_LIGHT_LEVEL-']))
            ConfigReader.set('Optical Sensor','Dusk Level',str(Data['-DUSK_LIGHT_LEVEL-']))
            ConfigReader.set('Optical Sensor','Rate Changue', str(Data['-RATE_CHANGUE_NIGHT_DAY-']) + ',' + str(Data['-UNITS_RATE_CHANGE-']))
            ConfigReader.set('Optical Sensor','Night Time', str(Data['-NIGHT_CYCLE_TIME-']) + ',' + str(Data['-UNITS_NIGHT_TIME-']))
            ConfigReader.set('Optical Sensor','Dawn Time', str(Data['-DAWN_CYCLE_TIME-']) + ',' + str(Data['-UNITS_DAWN_TIME-']))
            ConfigReader.set('Optical Sensor','Day Time', str(Data['-DAY_CYCLE_TIME-']) + ',' + str(Data['-UNITS_DAY_TIME-']))
            ConfigReader.set('Optical Sensor','Dusk Time', str(Data['-DUSK_CYCLE_TIME-']) + ',' + str(Data['-UNITS_DUSK_TIME-']))
            ConfigReader.set('Optical Sensor','Total Cycles',str(Data['-CYCLES_OPTICAL_TEST-']))

            with open(fileName, 'w') as configfile:    # save
                ConfigReader.write(configfile)
                sg.popup_auto_close('Succesfully Saved!')
        except:    
            sg.popup_error('ERROR!', 'Error -4: Invalid Input Value',"An exception occurred while Writing Values to File : ",fileName)
    else:
        return
#-----------------------------------------------------------------------------------------------------
#--------------------//Save Parameters to File//-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

if __name__ == '__main__': 
    main()