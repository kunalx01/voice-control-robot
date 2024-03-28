import socket   
import speech_recognition as sr
import pyttsx3
import sys

from threading import Thread
    
esp32_ip = "192.168.0.100"
esp32_port = 8002 

esp32_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
esp32_socket.connect((esp32_ip, esp32_port))

# Initialize the TTS engine
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  
engine.setProperty('rate', 140)

global text
text = ''
global command 
command = ''

def send_command(command):
    esp32_socket.sendall((command + "\n").encode())

def movement():
    global text
    while True:
        if text:
            if text == 'go forward':  
                send_command("RUN_FORWARD")
                engine.say("Going Forward")
            elif text == 'go backward':
                send_command("RUN_BACKWARD")
                engine.say("going backward")
            elif text == 'turn right': 
                send_command("LEFT")
                engine.say("turning right")
            elif text == 'turn left':
                send_command("RIGHT")
                engine.say("turning left")
            elif text == 'stop': 
                send_command("STOP") 
                engine.say("bot is stopped")
            
          # Reset text after processing
        

def sound():
    global text
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source :
            #try:
                print("Listening...")
                audio = r.listen(source)
    
                try:
                    
                    text = r.recognize(audio)
                    print("You Said : {}".format(text))
                
            #except:
                #engine.say("unable to listen , speak something")               
                    if text == 'stop listening' or text == 'stop':
                        break
                    
                except LookupError:
                    engine.say("speak again")

if __name__ == '__main__':
    Thread(target=movement).start()
    Thread(target=sound).start()
    sys.exit()