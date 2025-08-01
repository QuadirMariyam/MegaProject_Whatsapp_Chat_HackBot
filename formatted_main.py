import pyautogui
import time
import pyperclip
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
INSTRUCTION = (
    "### Instruction:\n"
    "You are a person named Mariyam Quadir who speaks Hindi and English. "
    "You're from India. Your tone should match the tone in Mariyam Quadir's older messages. "
    "give short responses like Mariyam Quadir based on the chat.\n\n"
)


def get_chat_history():
    pyautogui.moveTo(711, 197)
    pyautogui.dragTo(1109, 947, duration=1.0, button='left')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.click(1109, 947)
    time.sleep(1)
    return pyperclip.paste()


def is_last_message_from_user(chat_log, user_name="mariyam quadir"):
    last_message = chat_log.strip().split("/2025] ")[-1]
    return user_name.lower() in last_message.lower()


def send_to_model(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })
    return response.json()['response'].strip()


def send_reply_to_whatsapp(reply):
    pyperclip.copy(reply)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')


def main():
    pyautogui.click(1376, 1044)  # Open WhatsApp
    time.sleep(1)

    while True:
        chat_log = get_chat_history()
        if is_last_message_from_user(chat_log):
            full_prompt = INSTRUCTION + chat_log
            reply = send_to_model(full_prompt)
            send_reply_to_whatsapp(reply)
        else:
            print("No new message from other person.")
        time.sleep(5)


if __name__ == "__main__":
    main()
