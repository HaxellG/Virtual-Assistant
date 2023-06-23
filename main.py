import signal
import sys

from decouple import Config, Csv
from typing import Any, Dict
from utils.manage_files import read_file
from combined_assistant import CombinedAssistant

# Load the environment variables
CONFIG_PARAMS = read_file("config", "yaml")

def main() -> None:
    """
    Main function that initializes and runs the CombinedAssistant. 
    It also sets up the signal handler for SIGINT and SIGTERM signals.
    """
    model = CONFIG_PARAMS["stt"]["model_size"]
    record_timeout = CONFIG_PARAMS["stt"]["recording_time"]
    phrase_timeout = CONFIG_PARAMS["stt"]["silence_break"]
    energy_threshold = CONFIG_PARAMS["stt"]["sensibility"]
    wake_word = CONFIG_PARAMS["asistente"]["wake_word"]
    global global_assistant
    global_assistant = CombinedAssistant(model, record_timeout, phrase_timeout, energy_threshold, wake_word)
    signal.signal(signal.SIGINT, global_assistant.handle_signal)
    signal.signal(signal.SIGTERM, global_assistant.handle_signal)
    global_assistant.listen()
    global_assistant.write_transcript()

if __name__ == "__main__":
    main()