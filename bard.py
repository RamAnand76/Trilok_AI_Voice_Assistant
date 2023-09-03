from Bard import Chatbot
import bardapi
from playsound import playsound
import pygame
import speech_recognition as sr
from os import system
#import whisper
import warnings
import sys


# Suppress warnings from the SpeechRecognition library
warnings.filterwarnings("ignore")


# Initialize pygame
pygame.mixer.init()


Secure_1PSID =  'aQiYsp3ayAApTzLdu9MOtCGMNPpp2n2mffBupUR_vCBRjBTQo1xEnJavHCWshGzD3lyhIw.'
Secure_1PSIDTS = 'sidts-CjIBSAxbGa3nr9lVzTVcapiZ8JZx2e64G6Wxh4vRPCfcS91Owt70aua8GpGPq4X0EYgjpRAA'
                    
chatbot = Chatbot(Secure_1PSID, Secure_1PSIDTS)
#bard = bardapi.Bard("aQiYsp3ayAApTzLdu9MOtCGMNPpp2n2mffBupUR_vCBRjBTQo1xEnJavHCWshGzD3lyhIw.")

r = sr.Recognizer()


#tiny_model = whisper.load_model('tiny')
#base_model = whisper.load_model('base')

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)


#<<<<<<<<<<<<<<<<<<<<<<<< Function Definitions >>>>>>>>>>>>>>>>>>>>>

def prompt_bard(prompt):
    response = chatbot.ask(prompt)
    return response['content']


def speak(text):
    #if sys.platform != darwin: #Mac
    engine.say(text)
    engine.runAndWait()

def main():
    r = sr.Recognizer()

    while True:  # Keep listening for a wake word
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            
            try:
                print('\nSay "hi" to wake me up.\n')
                audio = r.listen(source)
                text_input = r.recognize_google(audio, language='en-IN')

                pygame.mixer.music.load('wake_detected.mp3')
                pygame.mixer.music.play()
                print("Wake word detected!")  # Debugging print
                if 'hi' in text_input.lower().strip():
                    break
                else:
                    print("No wake word found. Try again.")

            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print("Error transcribing audio:", e)
                continue


    print("AI : Hi I am Bard. What can i do for you?.\n")
    speak("Hi I am Bard. What can i do for you?.")
    
    while True:  # Keep listening for user input
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)

            try:
                '''print("AI : Hi I am Bard. What can i do for you?.\n")
                speak("Hi I am Bard. What can i do for you?.")'''
                print("\nListening.........\n")
                audio = r.listen(source, timeout=20)

                result = r.recognize_google(audio, language='en-IN')
                user_prompt = result.strip()
                prompt_text = result.strip()+ " You must provide a polite response."
                print("You : ", user_prompt, '\n')
                if 'exit' in result:
                    print("BARD: Thank You! Have a Nice Day!")
                    speak("Thank You! Have a Nice Day!")
                    exit()

                if len(prompt_text) == 0:
                    print("\nNo input detected. Please repeat the command or say 'exit' to exit\n")
                    continue

            except sr.UnknownValueError:
                print("No speech detected.")
                continue
            except sr.RequestError as e:
                print("Error transcribing audio:", e)
                continue

            response = prompt_bard(prompt_text)
            print("BARD:", response)
            speak(response)

if __name__ == "__main__":
    main()