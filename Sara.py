from combined_assistant import CombinedAssistant
from utils import read_file
import automatic
from datetime import datetime
import pywhatkit
import wikipedia
import pyjokes
import pyttsx3

class Sara:
    def __init__(self):
        CONFIG_PARAMS = read_file("config", "yaml")

        model = CONFIG_PARAMS["stt"]["model_size"]
        record_timeout = CONFIG_PARAMS["stt"]["recording_time"]
        phrase_timeout = CONFIG_PARAMS["stt"]["silence_break"]
        energy_threshold = CONFIG_PARAMS["stt"]["sensibility"]
        wake_word = CONFIG_PARAMS["asistente"]["wake_word"]

        self.ca = CombinedAssistant(model, record_timeout, phrase_timeout, energy_threshold, wake_word)
        self.voice = pyttsx3.init()
        self.voice.setProperty('rate', 178)
        self.voice.setProperty('volume', 1.0)

    def process_command(self, command):
        command = command.lower()
        if 'play' in command:
            song = command.replace('play', '')
            self.ca.tts('Playing ' + song)
            pywhatkit.playonyt(song)

        elif 'time' in command:
            time = datetime.now().strftime('%I:%M %p')
            self.ca.tts('Current time is ' + time)

        elif 'wikipedia' in command:
            info = command.replace('wikipedia', '')
            result = wikipedia.summary(info, 1)
            print(result)
            self.ca.tts(result)

        elif 'joke' in command:
            self.ca.tts(pyjokes.get_joke())

        elif 'message' in command:
            info = command.replace('message', '').split(' ')
            contact = info[0]
            message = ' '.join(info[1:])
            automatic.send_message(contact, message)

        else:
            result = self.ca.chat.get_response(command)
            self.ca.tts(str(result))

    def listen(self):
        self.ca.listen()

if __name__ == "__main__":
    sara = Sara()
    sara.listen()