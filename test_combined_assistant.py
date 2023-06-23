import combined_assistant
from unittest.mock import MagicMock, patch
import pytest
from datetime import datetime

# Define constants
MODEL = 'base'
RECORD_TIMEOUT = 5
PHRASE_TIMEOUT = 2
ENERGY_THRESHOLD = 4000
WAKE_WORD = 'hello'
TEST_MESSAGE = 'test message'
TEST_RESPONSE = 'test response'

# Define constants for testing
TEST_TRANSCRIPTION = 'test transcription'
TEST_COMMAND = 'test command'
TEST_SONG = 'test song'
TEST_INFO = 'test info'
TEST_JOKE = 'test joke'
TEST_CONTACT = 'test contact'


@pytest.fixture
def assistant():
    """
    Pytest fixture to create and return a CombinedAssistant instance with some pre-defined parameters.
    """
    return combined_assistant.CombinedAssistant(MODEL, RECORD_TIMEOUT, PHRASE_TIMEOUT, ENERGY_THRESHOLD, WAKE_WORD)

def test_init(assistant):
    """
    Test case for checking if the CombinedAssistant instance is being initialized with correct parameters.
    """
    assert assistant.record_timeout == RECORD_TIMEOUT
    assert assistant.phrase_timeout == PHRASE_TIMEOUT
    assert assistant.wake_word == WAKE_WORD

@patch('combined_assistant.openai.ChatCompletion.create')
def test_call_gpt(mock_create, assistant):
    """
    Test case for testing the 'call_gpt' method of the CombinedAssistant class.
    """
    mock_create.return_value = {'choices': [{'message': {'content': TEST_RESPONSE}}]}
    response = assistant.call_gpt(TEST_MESSAGE)
    assert response == TEST_RESPONSE


@patch('combined_assistant.wf')
def test_write_transcript(mock_wf, assistant):
    """
    Test case for testing the 'write_transcript' method of the CombinedAssistant class.
    """
    assistant.transcription = [TEST_TRANSCRIPTION]
    assistant.write_transcript()
    mock_wf.assert_called_once_with(TEST_TRANSCRIPTION, 'transcript', 'txt')
