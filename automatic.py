import time
import webbrowser
import pyautogui as automate
from utils.logger import logger

def send_message(contact, message):
    try:
        webbrowser.open(f"https://web.whatsapp.com/send?phone={contact}&text={message}")
        time.sleep(10)
        automate.press("enter")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")