#DoorInABox
#Python Script
#Developed by FCEO all rights reserved 
#Date 5/12/2022
#Version 1.0

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
toggle_btn_off = b'iVBORw0KGgoAAAANSUhEUgAAAGQAAAA1CAMAAACA7r40AAAACXBIWXMAABYlAAAWJQFJUiTwAAAAP1BMVEX6+vr4+Pj19fX29vbz8/Pv7+/t7e3x8fFzc3N0dHTl5eW1tbVpaWnIyMiEhIR5eXmRkZHY2Njq6uqcnJypqalIAPceAAAESElEQVRYw61YiXarIBBFZEdW/f9vfTOADUSTSs8ba9pYMzf3zsIg4afJq91dm7TimvAHJiX7cjRP3e1w8P4i+cbkPxC6Bal/wCnMHyyXj1Yy8kWGXIhKnpPdfdBaK6WD0jMW4uGMkKe3e7mY5Onw4NvHuO/RI075gRNffzG8F4Bcbu5umMA1kXYV/JGElJQxKrMDyOZe/0oKIfAu5Z3o82GQS5gjhD1JttJm68ok4OIHi4vvLM6/4OaYMMPEAFLfJQ//ZAww1pdRtqa4PRGrAwTRrKixESMTp72TDJwOtgCidGp7IFevnFa7GeVCIsKqaCijhcXyMnzLmAlbi796CqKjkdU1aRhCAkY+aSzLiLIwmv2mJjQrMdyN4KKXy2nAYIixIMY7Dltz3DalpgRTu+jlEiZ4gxDLBaCC0JWiYmoCA09bdCLlVYgY0sJ+dLrAYL6xhFRmckyFkICLbEycsgu70ekHBHOMHptSkykWBRhB1WT2kb/HG4y8xZ9PCVZbABQFJxh94bRjAwapx4hCqds2PVeVQCXLAoJEoD4+kjgVo9JvSk0Vvw5JVrlSsFiDI0YlM+olLcR+Ti518CqXDYa+hYTcRR/SeNsmmWgvKkiMfS8hb0ePMq+X0omjXCYcjN4k14UI1MqBoZ9KMChIBEnaDV3xnkopIubmgoJ2FLmcTmUJ+cCgw6lVrx8rVhpYxOwSEPcB5GNQoFLMrFwYeWCCIH1EqldCzlLsmFCaAWROL4UgPNuQ1xGFFIyb9GICQWYyWGmfr0zO7/9DpY8JMpnrxMAkl8CHNCRw+/6ELO9E/hKTEviSXfKSXeQk1eHA5OK2yWrUehcEV0VtGb3NrkvFU9tiop92YaVsYcJ9hGlxvauQMfTwReJcg8TTFSZy94KtH5gMXWUVaq5BAkww2FYELL6O3fUuMqYWqOXmkqstwAXE+J2+OuQ9EQRhMs4nlxOl4gU/YFa5TnWXgUWm2h7V4zVLKW/qoiWgDwMVunwFoTDC7ttc9sLdFvxjq4efQyX5C0grEj01RQIRkXmVC6ICCUa/gYCWdRyeWuIxIqIxwQQ7ZNuV3I2QOAyzfWIgahW748BdA492aCtZWyDPSXLtZ2Fein1qrtcgVmUiChORo3L0doHEOZ+WaehhXhX/pQ4dP0FKVGCciNqubHlpVuuwbelwgpichRRM2+X7F5BKRQDKnpeyCyqV2U7IbcbyTPK2eMAWGDclfUwAKR+waYRNChv2pYAhXZjL3YJRefBOrvICznBvLIEOxpquZQXguPl93hZbOPZcNlcDE14Pc8BXsEZixkIWMCqN9ecnHyIhj+j4j9uRCf7O5vCQert1Ljlnd9+Gp0cPI1puhQglKDuvPZN20Th8fKP+Yhofytj0456/skv0kjWg5OwfzDmThSxO+InQg9RL5b+y5QHnYsqqFvXBgOBdGMj1rk7MBvzL08Mzaz6i/wMmHoe06O7zzgAAAABJRU5ErkJggg=='
toggle_btn_on = b'iVBORw0KGgoAAAANSUhEUgAAAGQAAAA1CAMAAACA7r40AAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAJcEhZcwAAFiUAABYlAUlSJPAAAADnUExURfn6+SGm2/Dw8+7v7u3t7iGm2e3t7CKl2/Dw8Pj4+Pj4+vj5+CKl3SOm3PDz9vf3+DKhz8/1/935/ySj1+vu7mi42fLy8WCoxyGk2uXx9/L3+S6i0O/4/OPx9Sel2ev6//b29vn3+VaYsuzx8+bw8uDy+uX6/+D8/2ajvSii1DieyNj3/9Pz/77v/0Gdwt72/16dt06auSOn2ub2/ZzK3S+j1L7m9TGPtJ3V69r0/oXF4bPo/Mfv/SaczHu71o7M50GStKbd8yiSvcn2/4u8z1CixCOWxLTe7nKxyzCWwXqyyV2szWmuysKwv4IAAAc5SURBVFjDnZgNY7FuF8BTEiNJPW6SSlJRaN4mzGbs3uv3/zz/c65qsrGb50zCcv067+dC5VKSTSSXYxgZP5G/nqNXcJKT9wyDl8F1+CTja1gBr2Fy34Q6eidns0wun812LKt1hTTiswUCOITI5yHRfchWNwx98WrxRd8LW7KclcEmsnwCko20BMDIW2+Xm88/V4gby/t++uKPui1LzmbTmqTeAUVu+KuHj2G/X7lC+v3h8NYMAtcNTPP2drPdhRaY/bByGiLLrXC+ee43exrHsWM4WA6kdPZg2TqnzSr94cdyO9jtxN1usHr4vDXdqd9NK0MlcZVjZCtcL4f9iqaxPMdzdYTwXCbDcRn258GRm+B7lbfb5brq2LYOYoM44tQ13a3f6mRJsEE8fkHycsPbghbauA7L87A0x6MmCMFzcqBEr3lurDXfbhdiVVcUQ7gRDAMehqJXxYVr7tddtNkxRG6JD8NKj00WQkHAKcHPJYmTtPu7jejoarlMlkeBs6rqtrc33UFopc0FelkNfzmcSRkw9O+QUin+XJNmb48LR1dw/YKAgs9FQygKZb26DYIXcAyJp0STlrhEU7FoohL3u9Q5nq/zWu/tdjVSwVBCsXCQIrwRbhTdnrtIwTIQQ8DnD8MZW2eJtf4FiUjAGNgqatHGtVOcdlsQDMVeucGgK6NfKFIBrHALtqqXvswTeYZlT3sFYo7V/j6u7DKsBnoYgLi5abcjxg2oQoFrnHng+g0scRSphd3Bn4oU2/sfkDqBjKX7u62j1sBURUS02wkEXxGzlVV7YU79FlRQKiczWcvb9LUSRn+plHYw3DD7004lrj4eQ1xVwR+gR/HIVKBRDCkKenVvrrqgCkI63TkYqzQGlx9DMqcgmOlS7+l2rUPgEkdTBwRFIFQEUSbr4DW0OgBhcpa46Uu4ZIrxa3CNIUGmDsRu4bwApKxWH0yIsBwFHac1eG7W0f4XMbCigCKeCl4v/CaQP/ouePcaAJGZ0UNfOxtJJ811f7e0FUGgSFacEvBLGwJPdfYQxgxoIvsfswhyygOnIOO/jwOd6HEe0iaQydxcdNHxjfmwJ/Hc5cJLT4GnG0fGEhKJ9UAxBEUdua8hFEi5u+hLLHcNpPf07kCun2IcIEUsaIq9CXyLYqxw02e50qUEuBSSZGpDzSoUhdOQlOshIeddKmf5r5XxVRAI4LmuGGmPCMIJjICQFQQxlWuIn5UrrAXO0/7erVVFiC1/FgL/hyAemNMRlWvt/gDkCseXpL+PfgIRfkKEA0QgkBA02T1XrvJ7HQqwr9wYpN4WzkPa+H+EeGiuP1dD7nwVsuAEBNpvAqGgKkeaAKRFIKXzHf1bf6+zxCdCjTjeKH5X5St/AGLUbGIu2fIguuqXQzKoyQtEF0Ud9d3EVDGjaCAkiS5rtO9fYS6AsHGeCFThBCTJd2gBRpQnLUjG6zKejENP71UVJq3CbxBSWBRnE4SQ8XJrPtQkNpohLiqRULtMTzUOxooa7/d8xzRRPfeVVGHL/7jX+CsgHA4RemrF9k2syzfNYJqMqjCUeugnvcxhfLgg6aHD28ZRGf5Z8rGoYD9ZNxhKlunu4HlWugICM9fTowg5XxDSI93PzqjYg2DvNVCTfCPEHp85uPbQhn9i66T93t/todifb73opbaghEtz3ugghEwrTY27HILTyuNgovza5LGZwLQy6mQJBFrKst+Lth0XDSwsjCtPn46Ko12BDHPJ9JgYD+YiKCneO3R4mokgTHf90dficesSCMuRoQgpZyGK6kyhpMDIHUM6k5fnplZK9Yx/JGSJhXq/tZUyOpyiqGOQUYTQUp0X89UHj8SQWr4zWgybEnchJYPbGHDL3FaVIrbhYhpCNkOgxypw12isGAIzd8N7SJyPzub/ZS6oLTDhwcyt4PYKG5gQjamks2OGvATBvNuh6fwBQk88spur8zzHXuAT7A29t8epYyOmQLZZX4iyqlenprsCRj6C5OGPydOdhrd4rvRgE3Uo+ulz+sASxGd4CdLldeCoZaMWtxKDHLA1Hbybr+tuJw8SmwvOwKM7o9VHvwJ7+DomJu6Bf4NkMthZYPe7FJ2JriooN4qCu1LHnwbmctctM4iAAzVhYuc3uuISN9kaKZUQzWTOL0Xn1MFFW28I9rEE+/jhciU6tq6CwE7eEVfLwHRfwkk5uvnE8WgxGjTrNMIBYCqVZq+nSRfKrNJ/DDaL+dr3/fV8sXdN83Mr2iR2I1USn0QClMlIXLw+448rzdkMfzhpNs8dM5AmvsTfVoa3kZimu5+H9gRcflj3S5PoM5qmyxNvt1os//d/yGb5sB2I1UkZliEej9clPoliAC2Yr9WAMpmMqvA3ql4kI7wQH6NwNILvdpBB/9QkH9kOTrV8nq6RiyCPynQZvvDrEV3a6eDNYTTRZIk8gRxrchCartVqoA485WvwZfpCyeOjTCwRf7mWxC/If1fxUhEeiBl9AAAAAElFTkSuQmCC'
    

#-----------------------------------------------------------------------------------------------------
#--------------------//Global Variables a initial Config Definition//---------------------------------
#-----------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------
#--------------------//Layout screen definition//-----------------------------------------------------
#-----------------------------------------------------------------------------------------------------

menu_def = [['&Mode', ['Manual Mode','Automatic Mode','Configuration']],
            ['&Help', '&About...'], ]
layoutManual = [
    [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
    [sg.Text('Day / Night Testing', text_color = '#04284e',background_color = '#efefef')],
    [sg.Slider((3, 500), size=(40, 40), text_color = '#04284e', orientation='h',background_color = '#efefef', disabled=False, key='slider',enable_events=True)],[sg.Text('Close Door Testing',text_color = '#04284e',background_color = '#efefef'),sg.Button('', image_data = toggle_btn_off, key='-TOGGLE-GRAPHIC-DOOR-', button_color=('#efefef'), border_width=0,)],
    [sg.Text('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------',background_color = '#efefef',text_color = '#04284e')],
    [sg.Text('Presence Testing',text_color = '#04284e',background_color = '#efefef'),sg.Button('', image_data = toggle_btn_off, key='-TOGGLE-GRAPHIC-PRESENCE-', button_color=('#efefef'), border_width=0)],
    [sg.Text('----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------',background_color = '#efefef',text_color = '#04284e')],
    [sg.Button(button_text ='Exit',size = (10, 3), button_color=('#04284e'))],
    ]

layoutAutomatic = [
    [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
    [sg.Text('Cobaya Script yeahh!! alv', text_color = '#04284e',background_color = '#efefef')]
    [sg.Button(button_text ='Exit',size = (10, 3), button_color=('#04284e'))],
    ]

layoutConfiguration = [
    [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
    [sg.Button(button_text ='Exit',size = (10, 3), button_color=('#04284e'))],
    ]
#-----------------------------------------------------------------------------------------------------
#--------------------//Layout screen definition//-----------------------------------------------------
#-----------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------
#--------------------//Initialization//---------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
p = GPIO.PWM(servopin, 50)               # GPIO for PWM with 50Hz
p.start(2.5)
p.ChangeDutyCycle(12.5)
DayNightControl = GPIO.PWM(DayNightControlpin, 100) 
DayNightControl.start(0)
windowManual = sg.Window('Door in a Box - &&Manual Mode', layoutManual, background_color = '#efefef', size=(700, 350), finalize = True, grab_anywhere = False)
windowAutomatic = sg.Window('Door in a Box - &&Automatic Mode', layoutAutomatic, background_color = '#efefef', size=(700, 350),finalize = True, grab_anywhere = False)
windowConfiguration = sg.Window('Door in a Box - &&Configuration Mode', layoutConfiguration, background_color = '#efefef', size=(700, 350),finalize = True, grab_anywhere = False)
graphic_off = True
precenceDoorRight = False
precenceDoorLeft = True
windowManual.UnHide()
windowAutomatic.hide()
windowConfiguration.hide()
currentwindow = windowManual
#-----------------------------------------------------------------------------------------------------
#--------------------//Initialization//---------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------


def main():
    global windowManual
    global windowAutomatic
    global windowConfiguration
    global currentwindow

    while True:             # Event Loop
        event, values = currentwindow.read()
        print(event,values)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Manual Mode' and currentwindow!=windowManual:
            windowManual.move_to_center()
            windowManual.UnHide()
            currentwindow.hide()
            currentwindow = windowManual
        elif event == 'Automatic Mode' and currentwindow!=windowAutomatic:
            windowAutomatic.move_to_center()
            windowAutomatic.UnHide()
            currentwindow.hide()
            currentwindow = windowAutomatic
        elif event == 'Configuration' and currentwindow!=windowConfiguration:
            windowConfiguration.move_to_center()
            windowConfiguration.UnHide()
            currentwindow.hide()
            currentwindow = windowConfiguration
        elif event == 'About...':
            about()
        else:
            executeEvent(event,values,currentwindow)
    
    GPIO.cleanup()        
    p.stop()
    windowManual.close()
    windowAutomatic.close()
    windowConfiguration.close()


def executeEvent(key,value,Workingwindow):
    global graphic_off
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
    elif key == 'slider':
            val = value["slider"]
            val  = int(val)
            mapValue = ( (val - 3) / (500 - 3) ) * (100 - 0) + 0
            mapValue  = int(mapValue)
            print(mapValue)
            DayNightControl.ChangeDutyCycle(mapValue) 
    return


def about(): #About Application PopOut
    sg.popup_ok('information', 'Version 1.0',
    'Dor in a Box', sg.version)

if __name__ == '__main__': #Images must be image64 format
    main()   