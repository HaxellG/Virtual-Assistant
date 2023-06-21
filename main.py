from utils.manage_files import read_file
from combined_assistant import CombinedAssistant

CONFIG_PARAMS = read_file("config", "yaml")

def main():
    model = CONFIG_PARAMS["stt"]["model_size"]
    record_timeout = CONFIG_PARAMS["stt"]["recording_time"]
    phrase_timeout = CONFIG_PARAMS["stt"]["silence_break"]
    energy_threshold = CONFIG_PARAMS["stt"]["sensibility"]
    wake_word = CONFIG_PARAMS["asistente"]["wake_word"]

    ca = CombinedAssistant(model, record_timeout, phrase_timeout, energy_threshold, wake_word)
    ca.listen()
    ca.write_transcript()

if __name__ == "__main__":
    main()