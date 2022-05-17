#DoorInABox
#Python Script
#Developed by FCEO all rights reserved 
#Date 5/12/2022
#Version 1.0

from tkinter import TRUE, Canvas
from turtle import window_height
import PySimpleGUI as sg # https://pysimplegui.readthedocs.io/en/latest/#license  free source code 
import RPi.GPIO as GPIO # https://pypi.org/policy/terms-of-use/  free source code 


#-----------------------------------------------------------------------------------------------------
#--------------------//Global Variables a initial Config Definition//--------------------------------------------------
#----------------------------------------------------------------------------------------------------

RightPresencepin = 7    #Pin for Led to test right presence
LeftPresencepin = 11    #Pin for Led to test left presence
DayNightControlpin = 24 #PWM pGlobal Variables a initial Config Definitionin for control LEDs intensity
servopin = 18           #Pin for servo control

GPIO.setmode(GPIO.BCM) #BCM pin out mode for Raspberry pi (PWM Control)
GPIO.setwarnings(False) # Disable GPIO Warings (PinOut use/re-use)

GPIO.setup(RightPresencepin,GPIO.OUT)       #setting pin as Output
GPIO.setup(LeftPresencepin,GPIO.OUT)        #setting pin as Output
GPIO.setup(servopin, GPIO.OUT)              #setting pin as Output
GPIO.setup(DayNightControlpin, GPIO.OUT)    #setting pin as Output

GPIO.output(RightPresencepin,GPIO.LOW)   #Initialize signal in low state
GPIO.output(LeftPresencepin,GPIO.LOW)    #Initialize signal in low state
startbtn = b'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'
stopbtn = b'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'
toggle_btn_off = b'iVBORw0KGgoAAAANSUhEUgAAAGQAAAA1CAMAAACA7r40AAAACXBIWXMAABYlAAAWJQFJUiTwAAAAP1BMVEX6+vr4+Pj19fX29vbz8/Pv7+/t7e3x8fFzc3N0dHTl5eW1tbVpaWnIyMiEhIR5eXmRkZHY2Njq6uqcnJypqalIAPceAAAESElEQVRYw61YiXarIBBFZEdW/f9vfTOADUSTSs8ba9pYMzf3zsIg4afJq91dm7TimvAHJiX7cjRP3e1w8P4i+cbkPxC6Bal/wCnMHyyXj1Yy8kWGXIhKnpPdfdBaK6WD0jMW4uGMkKe3e7mY5Onw4NvHuO/RI075gRNffzG8F4Bcbu5umMA1kXYV/JGElJQxKrMDyOZe/0oKIfAu5Z3o82GQS5gjhD1JttJm68ok4OIHi4vvLM6/4OaYMMPEAFLfJQ//ZAww1pdRtqa4PRGrAwTRrKixESMTp72TDJwOtgCidGp7IFevnFa7GeVCIsKqaCijhcXyMnzLmAlbi796CqKjkdU1aRhCAkY+aSzLiLIwmv2mJjQrMdyN4KKXy2nAYIixIMY7Dltz3DalpgRTu+jlEiZ4gxDLBaCC0JWiYmoCA09bdCLlVYgY0sJ+dLrAYL6xhFRmckyFkICLbEycsgu70ekHBHOMHptSkykWBRhB1WT2kb/HG4y8xZ9PCVZbABQFJxh94bRjAwapx4hCqds2PVeVQCXLAoJEoD4+kjgVo9JvSk0Vvw5JVrlSsFiDI0YlM+olLcR+Ti518CqXDYa+hYTcRR/SeNsmmWgvKkiMfS8hb0ePMq+X0omjXCYcjN4k14UI1MqBoZ9KMChIBEnaDV3xnkopIubmgoJ2FLmcTmUJ+cCgw6lVrx8rVhpYxOwSEPcB5GNQoFLMrFwYeWCCIH1EqldCzlLsmFCaAWROL4UgPNuQ1xGFFIyb9GICQWYyWGmfr0zO7/9DpY8JMpnrxMAkl8CHNCRw+/6ELO9E/hKTEviSXfKSXeQk1eHA5OK2yWrUehcEV0VtGb3NrkvFU9tiop92YaVsYcJ9hGlxvauQMfTwReJcg8TTFSZy94KtH5gMXWUVaq5BAkww2FYELL6O3fUuMqYWqOXmkqstwAXE+J2+OuQ9EQRhMs4nlxOl4gU/YFa5TnWXgUWm2h7V4zVLKW/qoiWgDwMVunwFoTDC7ttc9sLdFvxjq4efQyX5C0grEj01RQIRkXmVC6ICCUa/gYCWdRyeWuIxIqIxwQQ7ZNuV3I2QOAyzfWIgahW748BdA492aCtZWyDPSXLtZ2Fein1qrtcgVmUiChORo3L0doHEOZ+WaehhXhX/pQ4dP0FKVGCciNqubHlpVuuwbelwgpichRRM2+X7F5BKRQDKnpeyCyqV2U7IbcbyTPK2eMAWGDclfUwAKR+waYRNChv2pYAhXZjL3YJRefBOrvICznBvLIEOxpquZQXguPl93hZbOPZcNlcDE14Pc8BXsEZixkIWMCqN9ecnHyIhj+j4j9uRCf7O5vCQert1Ljlnd9+Gp0cPI1puhQglKDuvPZN20Th8fKP+Yhofytj0456/skv0kjWg5OwfzDmThSxO+InQg9RL5b+y5QHnYsqqFvXBgOBdGMj1rk7MBvzL08Mzaz6i/wMmHoe06O7zzgAAAABJRU5ErkJggg=='
toggle_btn_on = b'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'
dayImage = b'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'
nightImage = b'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'
#--------------------//Global Variables a initial Config Definition//---------------------------------
#-----------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------
#--------------------//Layout screens definition//-----------------------------------------------------
#-----------------------------------------------------------------------------------------------------
sg.theme('Reddit')
sg.SetOptions('global',font= ('Default', 10))

menu_def_Manual = [['& MODE', ['Automatic Mode','Configuration']],
            ['& INFORMATION', 'About...'], ]
menu_def_Auto = [['& MODE', ['Manual Mode','Configuration']],
            ['& INFORMATION', 'About...'], ]
menu_def_config = [['& MODE', ['Manual Mode','Automatic Mode']],
            ['& INFORMATION', 'About...'], ]



sliderconf = [
            [sg.Image(source = nightImage),sg.Push(),sg.Slider((3, 500), size=(42, 42), orientation='h', key='SLIDER',enable_events=True),sg.Push(),sg.Image(source = dayImage)],
            ]
DoorStateConfig= [
            [sg.Push(),sg.Text('Lock / Unlock'), sg.Button('', image_data = toggle_btn_off, key='-TOGGLE-GRAPHIC-DOOR-',border_width=0),sg.Push()],
                ]
MotionSenConfig = [
            [sg.Push(),sg.Text('   Presence   '), sg.Button('', image_data = toggle_btn_off, key='-TOGGLE-GRAPHIC-PRESENCE-',border_width=0),sg.Push()],
                ]

layoutManual =  [
                [sg.Menu(menu_def_Manual, tearoff=False, pad=(200, 1),font= ('Helvetica', 13))],
                [sg.Frame('MANUAL TESTING',[[sg.Frame('--Optical Sensor--', sliderconf, element_justification = 'CENTER')],[sg.Frame('--Door State Sensor--',DoorStateConfig,element_justification = 'CENTER'),sg.Frame('--Motion Sensor--',MotionSenConfig,element_justification = 'CENTER',)],
                [sg.Button(button_text ='Exit',size = (10, 3))]],expand_x = True, expand_y = True, border_width = 5,element_justification = 'left')]
                ]



sz=(245,376)
col1 = [
        [sg.Button('', image_data = startbtn, key='-STARTBTN_DOOR_TEST-',border_width=0,button_color ='#ffffff'),sg.Button('', image_data = stopbtn, key='-STOPBTN_DOOR_TEST-',border_width=0,disabled = True, button_color ='#ffffff')],
        [sg.Text('-------------------------------------------------------------------------------------------------------')],
        [sg.Text('Actual Cycles: '),sg.Text('1 of 35 Total'),sg.Push()],
        [sg.Text('-------------------------------------------------------------------------------------------------------')],
        [sg.VPush()],
        [sg.Text('Door Open Time:   '),sg.Push(),sg.Input(default_text = "",key = '-TIME_DOOR_OPEN-', size = (7, 5),disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Door Closed Time: '),sg.Push(),sg.Input(default_text = "",key = '-TIME_DOOR_CLOSED-', size = (7, 5),disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Total Cycles:       '),sg.Push(),sg.Input(default_text = "",key = '-CYCLES_DOOR_TEST-', size = (7, 5),disabled = False,justification = 'left',background_color = 'white')],
        [sg.Button('Save Values', key='-SAVE_DOOR_TEST-',border_width=0,size = (300, 1))]
        ]

col2 = [
        [sg.Button('', image_data = startbtn, key='-STARTBTN_MOTION_TEST-',border_width=0,button_color ='#ffffff'),sg.Button('', image_data = stopbtn, key='-STOPBTN_MOTION_TEST-',border_width=0,disabled = True, button_color ='#ffffff')],
        [sg.Text('-------------------------------------------------------------------------------------------------------')],
        [sg.Text('Actual Cycles: '),sg.Text('1 of 35 Total'),sg.Push()],
        [sg.Text('-------------------------------------------------------------------------------------------------------')],
        [sg.VPush()],
        [sg.VPush()],
        [sg.Text('Cycle Time:   '),sg.Push(),sg.Input(default_text = "",key = '-CYCLE_TIME_MOTION-', size = (5, 5),disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Motion Source Time: '),sg.Push(),sg.Input(default_text = "",key = '-MOTION_SOURCE_TIME-', size = (5, 5),disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Total Cycles:       '),sg.Push(),sg.Input(default_text = "",key = '-CYCLES_MOTION_TEST-', size = (5, 5),disabled = False,justification = 'left',background_color = 'white')],
        [sg.Button('Save Values', key='-SAVE_MOTION_TEST-',border_width=0,size = (330, 1))],
        ]

col3 = [
        [sg.Button('', image_data = startbtn, key='-STARTBTN_OPTICAL_TEST-',border_width=0,button_color ='#ffffff'),sg.Button('', image_data = stopbtn, key='-STOPBTN_OPTICAL_TEST-',border_width=0,disabled = True, button_color ='#ffffff')],
        [sg.Text('-------------------------------------------------------------------------------------------------------')],
        [sg.Text('Actual Cycles: '),sg.Text('1 of 35 Total'),sg.Push()],
        [sg.Text('-------------------------------------------------------------------------------------------------------')],
        [sg.VPush()],
        [sg.VPush()],
        [sg.Text('Night Light Level:   '),sg.Push(),sg.Input(default_text = "",key = '-NIGHT_LIGHT_LEVEL-', size = (5, 5),disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Day Light Level: '),sg.Push(),sg.Input(default_text = "",key = '-DAY_GHT_LIGHT_LEVEL-', size = (5, 5),disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Rate Changue:'),sg.Push(),sg.Input(default_text = "",key = '-RATE_CHANGUE_NIGHT_DAY-', size = (5, 5),disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Night Cycle Time:'),sg.Push(),sg.Input(default_text = "",key = '-NIGHT_CYCLE_TIME-', size = (5, 5),disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Day Cycle Time:'),sg.Push(),sg.Input(default_text = "",key = '-DAY_CYCLE_TIME-', size = (5, 5),disabled = False,justification = 'left',background_color = 'white')],
        [sg.Text('Total Cycles:       '),sg.Push(),sg.Input(default_text = "",key = '-CYCLES_OPTICAL_TEST-', size = (5, 5),disabled = False,justification = 'left',background_color = 'white')],
        [sg.Button('Save Values', key='-SAVE_OPTICAL_TEST-',border_width=0,size = (330, 1))],
        ]

layout = [[sg.Frame('Door State Sensor',col1, element_justification='c', size=sz ), sg.Frame('Motion Sensor',col2, element_justification='c', size=sz)
          , sg.Frame('Optical Sensor',col3, element_justification='c', size=sz)],[sg.Button(button_text ='Exit',size = (10, 3)),sg.Button(button_text ='Manual Operation',size = (20, 3))]]

layoutAutomatic =   [
                    [sg.Menu(menu_def_Auto, tearoff=False, pad=(200, 1),font= ('Helvetica', 13))],
                    [sg.Frame('AUTOMATIC OPERATION',layout,expand_x = True, expand_y = True, border_width = 1,element_justification = 'C')]
                    ]


layoutConfig = [
                [sg.Button(button_text ='Exit',size = (10, 3), pad = (730,350))],
                ]
layoutConfiguration =   [
                        [sg.Menu(menu_def_config, tearoff=False, pad=(200, 1),font= ('Helvetica', 13))],
                        [sg.Button(button_text ='Exit',size = (10, 3), pad = (0,50))],
                        ]

#-----------------------------------------------------------------------------------------------------
#--------------------//Layout screens definition//-----------------------------------------------------
#-----------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------
#--------------------//Initialization//---------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
p = GPIO.PWM(servopin, 50)               # GPIO for PWM with 50Hz
p.start(2.5)
p.ChangeDutyCycle(12.5)
DayNightControl = GPIO.PWM(DayNightControlpin, 100) 
DayNightControl.start(0)
graphic_off = True
precenceDoorRight = False
precenceDoorLeft = True
#-----------------------------------------------------------------------------------------------------
#--------------------//Initialization//---------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------




#-----------------------------------------------------------------------------------------------------
#--------------------//Main Loop//--------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def main():
    windowManual = sg.Window('Door in a Box - Manual Mode', layoutManual, size=(800, 390), finalize = True,resizable=True, location=(0,0))
    currentwindow = windowManual
    currentwindow.Maximize()
    windowAutomatic = None
    windowConfiguration = None

    while True:             # Event Loop
        event, values = currentwindow.read()
        print(event,values)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Manual Mode' and currentwindow!=windowManual:
            windowManual.Maximize()
            windowManual.UnHide()
            currentwindow.hide()
            currentwindow = windowManual
        elif event == 'Automatic Mode' and currentwindow!=windowAutomatic:
            if windowAutomatic == None:
                windowAutomatic = sg.Window('Door in a Box - Automatic Mode', layoutAutomatic, size=(800, 390), finalize = True,resizable=True, location=(0,0))
            windowAutomatic.Maximize()
            windowAutomatic.UnHide()
            currentwindow.hide()
            currentwindow = windowAutomatic
        elif event == 'Configuration' and currentwindow!=windowConfiguration:
            if windowConfiguration == None:
                windowConfiguration = sg.Window('Door in a Box - Configuration Mode', layoutConfiguration, size=(800, 390), finalize = True, resizable=True, location=(0,0))
            windowConfiguration.Maximize()
            windowConfiguration.UnHide()
            currentwindow.hide()
            currentwindow = windowConfiguration
        elif event == 'About...':
            about()
        else:
            executeEvent(event,values,currentwindow)
    
    GPIO.cleanup()        
    p.stop()
    if windowManual!=None:
        windowManual.close()
    if windowAutomatic!=None:
        windowAutomatic.close()
    if windowConfiguration!=None:  
        windowConfiguration.close()

#-----------------------------------------------------------------------------------------------------
#--------------------//Main Loop//--------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------
#--------------------//About App Popout//-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def about(): #About Application PopOut
    sg.popup_ok('Information', 'Version 1.0',
    'Dor in a Box', sg.version)
#-----------------------------------------------------------------------------------------------------
#--------------------//About App Popout//-------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------
#--------------------//Event Handler Control//--------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def executeEvent(key,value,Workingwindow):
    global graphic_off
    global precenceDoorRight
    if key == '-TOGGLE-GRAPHIC-DOOR-':   # if the graphical button that changes images
        graphic_off = not graphic_off
        Workingwindow['-TOGGLE-GRAPHIC-DOOR-'].update(image_data=toggle_btn_off if graphic_off else toggle_btn_on)
        if(graphic_off):
            p.start(2.5)
            p.ChangeDutyCycle(12.5)
        else:
            p.ChangeDutyCycle(5)
    elif key == '-TOGGLE-GRAPHIC-PRESENCE-':
        precenceDoorRight = not precenceDoorRight
        if(precenceDoorRight):
            print(precenceDoorRight)
            Workingwindow['-TOGGLE-GRAPHIC-PRESENCE-'].update(image_data=toggle_btn_on)
            GPIO.output(RightPresencepin,GPIO.HIGH)
        else:
            Workingwindow['-TOGGLE-GRAPHIC-PRESENCE-'].update(image_data=toggle_btn_off)
            GPIO.output(RightPresencepin,GPIO.LOW)
            print(precenceDoorRight)
    elif key == 'SLIDER':
            val = value["SLIDER"]
            val  = int(val)
            mapValue = ( (val - 3) / (500 - 3) ) * (100 - 0) + 0
            mapValue  = int(mapValue)
            print(mapValue)
            DayNightControl.ChangeDutyCycle(mapValue) 
    return
#-----------------------------------------------------------------------------------------------------
#--------------------//Event Handler Control//--------------------------------------------------------
#-----------------------------------------------------------------------------------------------------


if __name__ == '__main__': 
    main()   