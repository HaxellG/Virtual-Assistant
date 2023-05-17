import time
import webbrowser
import pyautogui as automate

def send_message(contact, message):
    webbrowser.open(f"https://web.whatsapp.com/send?phone={contact}&text={message}")
    time.sleep(10)
    automate.press("enter")