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
import threading
from utils.logger import setup_logger
import sys
from typing import Any
import tempfile
import numpy as np

# setup logger
logger = setup_logger('assistant_logger', 'assistant.log', fmt='%(asctime)s: [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Set OpenAI API Key
openai.api_key = config('OPENAI_API_KEY')
global_assistant = None  # Global variable

def validate_key():
    if not openai.api_key:
        raise ValueError("The OPENAI_API_KEY is not set. Please provide the API key.")
    else:
        print("OpenAI API key is set.")


class CombinedAssistant:
    def __init__(self, model, record_timeout, phrase_timeout, energy_threshold, wake_word):
        """
        Initialize the CombinedAssistant with the provided parameters.
        
        Parameters:
        model (str): the name of the model to use
        record_timeout (int): the maximum duration of a recording in seconds
        phrase_timeout (int): the maximum pause between phrases in seconds
        energy_threshold (int): the energy level threshold for the recognizer
        wake_word (str): the word that wakes up the assistant
        """
        validate_key()
        global global_assistant  # Use the global variable
        global_assistant = self
        self.has_started_transcribing = 0
        self.temp_file = io.BytesIO()
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
        self.stop_listening = False

    @staticmethod
    def handle_signal(sig: int, frame: Any) -> None:
        """
        Handle incoming SIGINT or SIGTERM signals and stop the CombinedAssistant instance gracefully.
        
        Parameters:
        sig (int): the incoming signal's identifier
        frame (Any): current stack frame
        """
        print('Signal received. Shutting down...')
        global_assistant.stop()  # Stop the CombinedAssistant instance
        sys.exit(0)

    def stop(self) -> None:
        """
        Clean up any resources before stopping the assistant.
        """
        print('Cleaning up resources...')
        self.stop_listening = True  # Stop the listen loop
    
    def speak(self, text):
        print(text)

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

        # Microphone is left listening with the help of speech_recognition
        self.recorder.listen_in_background(self.source, record_callback, phrase_time_limit=self.record_timeout)
        start = datetime.utcnow()
        while True:
            try:
                now = datetime.utcnow()
                if ((now - start).total_seconds() % 18) == 0:
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
                    
                    # Save as a WAV file using a temporary file
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                        temp_file.write(wav_data.read())
                        temp_file_path = temp_file.name
                    
                    # Load back the saved audio file as a numpy array
                    sr_audiofile = sr.AudioFile(temp_file_path)
                    with sr_audiofile as source:
                        audio = self.recorder.record(source)
                        numpy_audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)
                    
                    # Convert numpy_audio_data to float32
                    numpy_audio_data = numpy_audio_data.astype(np.float32)
                    
                    result = self.audio_model.transcribe(numpy_audio_data, language='en')
                    text = result['text'].strip()

                    if phrase_complete:
                        self.transcription.append(text)
                    else:
                        self.transcription[-1] = text
                    
                    # The wizard is activated
                    mensaje = self.transcription[-1].lower()
                    mensaje = "Human: " + mensaje
                    respuesta = self.call_gpt(mensaje)
                    print(respuesta)

                    # Do something with the recognized phrase
                    self.process_command(mensaje)
            except Exception as e:
                print(f"Error occurred: {e}")


    def chat(self, message):
        response = self.call_gpt(f"Human: {message}")
        return response

    def call_gpt(self, message):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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
        respuesta = response['choices'][0]['message']['content']
        return respuesta


    def tts(self, text):
        # Convert text to speech
        tts = gtts.gTTS(text, lang='en')

    def play_audio_pygame(self, filename):
        # Play the audio file
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    def write_transcript(self):
        if not self.has_started_transcribing:
            self.has_started_transcribing = True
        conversation = "\n".join(self.transcription)
        wf(conversation, "transcript", "txt")
    
    def process_command(self, command):
        """
        Process the given command (for now, just print it).

        Parameters:
        command (str): the command to process
        """
        print(f"Processing command: {command}")

if __name__ == '__main__':
    assistant = CombinedAssistant('whisper_model', 5, 2, 4000, 'hey assistant')
    assistant.listen()