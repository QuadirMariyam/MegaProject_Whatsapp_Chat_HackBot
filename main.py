import pyautogui
import time
import pyperclip
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import requests
import json


# Define the local API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"


instruction = (
    "### Instruction:\n"
    "You are a person named Mariyam Quadir who speaks hindi as well as english."
    "You are from India. Your tone should be based on the upper chats of Mariyam Quadir only. Give short responses based on the chat\n\n"
)


def is_last_message_from_sender(chat_log):
    #split the chat log into individual messages
    message = chat_log.strip().split("/2025] ")[-1]
    if "Mariyam Quadir" not in message:
        return True
    return False



# Step 1 - clicking on the whatsapp icon at coordinates
pyautogui.click(1376, 1044)

time.sleep(2) # wait for 2 sec to ensure the click is registered


while True:

    # step 2 - Drag the mouse from top to bottom to select the text
    pyautogui.moveTo(711, 197)
    pyautogui.dragTo(1109, 947, duration = 1.0, button = 'left') # drag for 1 sec

    # step 3 - copy to clipboard
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.click(1109, 947)
    time.sleep(1) # wait for 1 sec to ensure the copy chat_history

    # step 4 - retrieve the text from clipboard and store in a variable
    chat_history = pyperclip.paste()

    # print the copied text
    print(chat_history)

    #call the func to check whether the last message is from sender or not
    if is_last_message_from_sender(chat_history):
        # Combine into final prompt
        full_prompt = f"{instruction}\n\n{chat_history}"

        # Send request to local Mistral API
        response = requests.post(OLLAMA_URL, json={
            "model": "mistral",  # or whatever model name you're running locally
            "prompt": full_prompt,
            "stream": False
        })

        # Extract and print response
        result = response.json()
        reply = result['response'].strip()
        pyperclip.copy(reply)

        # Step 5 - click at coordinates of whatsapp reply box
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1) 

        #step 7 - press enter
        pyautogui.press('enter')

else:
        print("No new message from other person.")
        time.sleep(2)



'''
[2:28 pm, 01/08/2025] Ammi 😨😱😵: Aaj nawed ka birthday hai
[2:37 pm, 01/08/2025] Ammi 😨😱😵: Who send that sms
[2:38 pm, 01/08/2025] Mariyam Quadir: Apologies for the delay in response, Ma. Nawaab ka birthday hai yaar. Unko bahut bhool gaye hain, kuch toh nikalna padega. (Nawaab's birthday is today. Seems we forgot about it, something needs to be done.)
[2:39 pm, 01/08/2025] Ammi 😨😱😵: Kya nikalogey??
[2:39 pm, 01/08/2025] Ammi 😨😱😵: Jab woh aayega tab ice lejana
'''