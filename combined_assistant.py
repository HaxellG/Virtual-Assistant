import io
import os
import time
import webbrowser
import sqlite3
import yaml
import speech_recognition as sr
import whisper
import openai
import gtts
import pygame
import pywhatkit
import wikipedia
import pyjokes
from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from utils.manage_files import write_file as wf
from database import get_questions_answers
from decouple import config
import automatic
import pyttsx3

# Do not forget to update the OpenAI API Key
openai.api_key = config('OPENAI_API_KEY')

class CombinedAssistant:
    def __init__(self, model, record_timeout, phrase_timeout, energy_threshold, wake_word):
        self.temp_file = NamedTemporaryFile().name
        self.transcription = ['']
        self.audio_model = whisper.load_model(model)
        self.phrase_time = None
        self.last_sample = bytes()
        self.data_queue = Queue() 
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = energy_threshold
        self.recorder.dynamic_energy_threshold = False
        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout
        self.wake_word = wake_word

        # Set up Sara's configurations
        self.voice = pyttsx3.init()
        self.voice.setProperty('rate', 178)
        self.voice.setProperty('volume', 1.0)
        self.attemts = 0

    def speak(self, text):
        self.voice.say(text)
        self.voice.runAndWait()

    def listen(self):
        self.source = sr.Microphone(sample_rate=16000)
        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)

            def record_callback(_, audio:sr.AudioData) -> None:
                """
                Threaded callback function to recieve audio data when recordings finish.
                audio: An AudioData containing the recorded bytes.
                """
                # Grab the raw bytes and push it into the thread safe queue.
                data = audio.get_raw_data(convert_rate=16000, convert_width=2)
                self.data_queue.put(data)

        #Microphone is left listening with the help of speech_recognition
        self.recorder.listen_in_background(self.source, record_callback, phrase_time_limit=self.record_timeout)
        start = datetime.utcnow()
        while True:
            try:
                now = datetime.utcnow()
                if ((now - start).total_seconds()%18) == 0:
                    self.write_transcript()
                # Pull raw recorded audio from the queue.
                if not self.data_queue.empty():
                    phrase_complete = False
                    if self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
                        self.last_sample = bytes()
                        phrase_complete = True
                    # This is the last time we received new audio data from the queue.
                    self.phrase_time = now

                    while not self.data_queue.empty():
                        data = self.data_queue.get()
                        self.last_sample += data

                    audio_data = sr.AudioData(self.last_sample, self.source.SAMPLE_RATE, self.source.SAMPLE_WIDTH)
                    wav_data = io.BytesIO(audio_data.get_wav_data())

                    with open(self.temp_file, 'w+b') as f:
                        f.write(wav_data.read())

                    result = self.audio_model.transcribe(self.temp_file, language='en')
                    text = result['text'].strip()

                    if phrase_complete:
                        self.transcription.append(text)
                    else:
                        self.transcription[-1] = text
                    
                    if self.wake_word in self.transcription[-1].lower():
                        # The wizard is activated
                        mensaje = self.transcription[-1].lower().replace(self.wake_word, "")
                        mensaje = "Human: " + mensaje
                        respuesta = self.call_gpt(mensaje)
                        print(respuesta)
                        self.tts(respuesta)
                        self.play_audio_pygame("audio.mp3")

                        # Do something with the recognized phrase
                        self.process_command(mensaje)
            except Exception as e:
                print(f"Error occurred: {e}")

    def chat(self, message):
        response = self.call_gpt(f"Human: {message}")
        return response

    def call_gpt(self, message):
        response = openai.ChatCompletion.create(
            model="gpt-4.0-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        return response['choices'][0]['message']['content']

    def tts(self, text):
        # Convert text to speech
        tts = gtts.gTTS(text, lang='en')
        tts.save("audio.mp3")

    def play_audio_pygame(self, filename):
        # Play the audio file
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    def write_transcript(self):
        # Write the transcript to a file
        wf(self.transcription, "transcript.txt")

    def process_command(self, command):
        command = command.lower()
        print(command)
        if 'play' in command:
            song = command.replace('play', '')
            self.tts('Playing ' + song)
            pywhatkit.playonyt(song)

        elif 'time' in command:
            time = datetime.now().strftime('%I:%M %p')
            self.tts('Current time is ' + time)

        elif 'wikipedia' in command:
            info = command.replace('wikipedia', '')
            result = wikipedia.summary(info, 1)
            print(result)
            self.tts(result)

        elif 'joke' in command:
            self.tts(pyjokes.get_joke())

        elif 'message' in command:
            info = command.replace('message', '').split(' ')
            contact = info[0]
            message = ' '.join(info[1:])
            automatic.send_message(contact, message)

        else:
            result = self.chat(command)
            self.tts(str(result))

if __name__ == '__main__':
    assistant = CombinedAssistant('whisper_model', 5, 2, 4000, 'hey assistant')
    assistant.listen()