import speech_recognition as sr
import pyttsx3
import pywhatkit
from datetime import datetime, date, timedelta
import wikipedia
import pyjokes
import json
import webbrowser
import automatic
from time import time
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import database

start_time = time()
voice = pyttsx3.init()

name = "sara"
attemts = 0
greeting = 0

blue_color = "\033[1;34;40m"
cian_color = "\033[1;36;40m"
green_color = "\033[1;32;40m"
yellow_color = "\033[1;33;40m"
normal_color = "\033[0;37;40m"

voices = voice.getProperty('voices')
voice.setProperty('voice', voices[0].id)
voice.setProperty('rate', 178)
voice.setProperty('volume', 1.0)

contacts = dict()

def speak(text):
    voice.say(text)
    voice.runAndWait()


def get_audio():
    r = sr.Recognizer()
    status = False

    with sr.Microphone() as source:
        print(f"{yellow_color}({attemts}) Escuchando...{normal_color}")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        rec = ""
        try:
            rec = r.recognize_google(audio, language='es-ES').lower()           
            if name in rec:
                status = True
            else:
                print(f"No logré comprender, repite por favor: {rec}")

        except:
            pass
    return {'text':rec, 'status':status}

def listen():
    listener = sr.Recognizer()    
    with sr.Microphone() as source:            
        listener.adjust_for_ambient_noise(source)
        print(f"{green_color}Escuchando(C)...{normal_color}")
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError:
        print("No te entendí, intenta de nuevo")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return rec


def conversar():
    chat = ChatBot("sara", database_uri=None)
    trainer = ListTrainer(chat)
    trainer.train(database.get_questions_answers())
    speak("Muy bien, vamos a conversar")
    while True:
        try:
            request = listen()
        except UnboundLocalError:
            continue
        
        print(f"{blue_color}Tú: {normal_color}({request})")
        answer = chat.get_response(request)
        print(f"{cian_color}Sara: {normal_color}({answer})")
        speak(answer)

        if "sara te presento" in request:
            request = request.replace("sara te presento a", "")
            speak("mucho gusto " + request + ", es un placer conocerte")

        if "desconectar" in request:
            speak("fue un placer conversar contigo. hora de volver a las tareas habituales")
            break


while True:
    rec_json = get_audio()
    rec = rec_json['text']
    status = rec_json['status']

    if (greeting == 0):
        speak("Estoy lista para las actividades del día de hoy")
        greeting = 1

    if status:
        if "hablar" in rec:
            conversar()

        if "me escuchas" in rec:
            speak("Por supuesto, aquí estoy")

        elif "reproduce" in rec:
            video = rec.replace("sara reproduce", " ")
            speak("reproduciendo" + video)
            pywhatkit.playonyt(video)

        elif "hora" in rec:
            speak("Déjame consultar")
            hour = datetime.now().strftime('%I:%M %p')
            speak(f"Son las {hour}")

        elif 'busca' in rec:
            speak("Consultando")
            order = rec.replace('sara busca', '')
            wikipedia.set_lang("es")
            info = wikipedia.summary(order, 1)
            speak(info)

        elif 'chiste' in rec:
            chiste = pyjokes.get_joke("es")
            speak("Muy bien, aquí va ")
            speak(chiste)
        
        elif "repite" in rec:
            repeat = rec.replace("sara repite", " ")
            speak(repeat)
            
        elif "abre" in rec:
            if "youtube" in rec:
                speak("Abriendo la página de Youtube")
                webbrowser.open("https://www.youtube.com/")     
            elif "mercadolibre" in rec:
                speak("Abriendo la página de mercadolibre")
                webbrowser.open("https://www.mercadolibre.com.co/")
            elif "google" in rec:
                speak("Abriendo la página de Google")
                webbrowser.open("https://www.google.com/")
            elif "universidad" in rec:
                speak("Abriendo tu página de cursos de Uninorte")
                webbrowser.open("https://cursos.uninorte.edu.co/d2l/home")
            elif "netflix" in rec:
                speak("Abriendo la página de Netflix")
                webbrowser.open("https://www.netflix.com/co/")
            elif "whatsapp" in rec:
                speak("Abriendo whatsapp web")
                webbrowser.open("https://web.whatsapp.com/")
            elif "chat" in rec:
                speak("Abriendo chat gpt")
                webbrowser.open("https://chat.openai.com/chat")
                
        elif 'desconectar' in rec:
            speak("Fue un gusto estar contigo, espero haber sido de ayuda")
            break

        else:
            print(f"No logré comprender, repite por favor: {rec}")
            speak("No logré comprender, repite por favor")
        attemts = 0
    else:
        attemts += 1