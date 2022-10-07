from pynput.keyboard import Key, Listener, Controller
from random import random
import pyperclip, pyautogui
keyboard = Controller()

randomnes = 33.3
activated = False
actFlag = False
enterPressed = False
lastChar = ""
randomnesTypo = 10
typoInc = False

def activationMode(key):
    global actFlag
    global activated
    global randomnes
    try:  
        if(key.char == "q" and actFlag):
            if(activated):
                activated = False
                keyboard.release(Key.shift)
                print("Retarded deactivated")
                actFlag = False
            else:
                activated = True  
                print("Retarded activated")
                actFlag = False
                lastChar = ""
        else:
            pass
        if(key.char == "a" and actFlag):
            actFlag = False
            print("text modified")
            msg = pyperclip.paste()
            msg = msg.replace('"', "")
            newMsg = '"'
            for ch in msg:
                randomVal = random()*100
                if(randomVal < randomnes):
                    newMsg += ch.capitalize()
                    randomnes = 33.3
                else:
                    newMsg += ch.lower()
                    randomnes += 33.3
            newMsg += '"'
            print(newMsg)
            pyperclip.copy(newMsg)

    except Exception as e:
        pass


def on_press(key):
    global activated
    global randomnes
    global actFlag
    global enterPressed
    global lastChar
    global typoInc

    if(key == Key.enter and enterPressed):
        return

    if key == Key.alt_l:
        print("alt pressed")
        actFlag = True
        return

    activationMode(key)

    if(activated):
        if (key == Key.enter):
            enterPressed = True
            if(keyboard.pressed(Key.shift)):
                keyboard.tap(Key.backspace)
                keyboard.release(Key.shift)
                keyboard.tap(Key.enter)
            activated = False
            print("Retarded deactivated")
            enterPressed = False
            return

        if(key == Key.shift):
            return

        randomVal = random()*100
        if(randomVal < randomnes):
            keyboard.press(Key.shift)
            randomnes = 33.3
        else:
            if(keyboard.pressed(Key.shift)):
                keyboard.release(Key.shift)
                randomnes += 33.3

        try:
            if(random()*100 < randomnesTypo and lastChar != "" and typoInc == False):
                typoInc = True
                newChar = key.char
                keyboard.tap(Key.backspace)
                keyboard.tap(Key.backspace)
                keyboard.tap(newChar)
                keyboard.tap(lastChar)
                lastChar=newChar
                typoInc = False
            else:
                try:
                    lastChar=key.char
                    typoInc = False
                except Exception as e:
                    pass
        except:
            pass


def on_release(key):
    if key == Key.esc:
        keyboard.release(Key.shift)
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()