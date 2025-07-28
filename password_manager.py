import random
import string
import json
import os
import time
import sys
import pyperclip #for copying it to clipboard...
import keyboard #for typing animation....

"""Animation functions : """
def type_text(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def load_animation_mini(text):
    load_str = text
    loading_char = "."
    for i in range(4):
        sys.stdout.write("\r" + load_str + loading_char * i)
        sys.stdout.flush()
        time.sleep(0.2)
    print()

def load_animation(text):
    for i in range(101):
        bar = f"\r{text}: [{('=' * (i // 2)).ljust(50)}] {i}%"
        sys.stdout.write(bar)
        sys.stdout.flush()
        time.sleep(0.01)
    type_text("\nDone!\n")
"""=========================================================================="""

type_text("""Do you want to encrypt or decrypt your password?? (E\\D): """)
ask = input().lower()
length_of_toppings =7
filename = "passwords.json"

if 'e' in ask:
    try:
        if os.path.exists(filename):
            with open(filename, "r") as file:
                passwords = json.load(file)
        else:
            passwords = {}
    except json.JSONDecodeError:
        passwords = {}

    type_text("Very well!!\n")
    type_text("Enter your password : ")
    password = input()
    words= password.split()
    ency_words = []

    for word in words:
        chunks = word
        allowed_chars = (string.ascii_letters + string.digits + string.punctuation).replace('`', '@')
        r1 = ''.join(random.choices(allowed_chars, k=length_of_toppings))
        r2 = ''.join(random.choices(allowed_chars, k=length_of_toppings))
        r3 = ''.join(random.choices(allowed_chars, k=length_of_toppings))
        encrypted = r1+chunks[1:]+r3+chunks[0]+r2
        ency_words.append(encrypted)

    load_animation("Encrypting")
    encrypted_password = '`'.join(ency_words)
    encrypted_password = ''.join(reversed(encrypted_password))
    type_text("Enter any hint to the site (for eg:- new mail): ")
    hint = input()
    passwords[hint] = encrypted_password
    with open("passwords.json", "w") as file:
        json.dump(passwords, file, indent=4)
    type_text("All set.. 👍")
    print()
    type_text("Your file is updated...✅\n")
    type_text("wanna check it? (Y\\N): ")
    ask2 = input().upper()
    if 'Y' in ask2:
        max_key_length = max(len(key) for key in passwords) #sabse lambe key ka length nikalne ke liye
        for key, value in passwords.items():
            print(f"{key.ljust(max_key_length)} : {value}") #pura file type_text karna
    else:
        type_text("No problem.. See you soon.. 😊")

elif 'd' in ask:
    passwords = {}
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r") as file:
            passwords = json.load(file)
                
    if not passwords:
        print("⚠️ No credentials stored yet.")
        exit()

    credentials = list(passwords.items())

    max_key_length = max(len(key) for key in passwords)
    type_text("Available Pairs... :")
    print("📜 \n")
    for index, (key, value) in enumerate(credentials):
        print(f"{index+1}. {key.ljust(max_key_length)} => {value}") #pura file type_text karna

    type_text("Enter the number of the pair you want to extract: ")
    choice = int(input())-1
    if 0<=choice<len(credentials):
        selected_key, selected_value = credentials[choice]
    else:
        type_text("⚠️ Invalid Input 😒")
        
    encrypted_message = selected_value
    encrypted_message = ''.join(reversed(encrypted_message))
    encrypted_words= encrypted_message.split('`')
    words =[]
    for ency in encrypted_words:
        stage1 = ency[length_of_toppings:-length_of_toppings]
        stage2 = stage1[:-(length_of_toppings+1)]+ stage1[-1:]
        stage3 = stage2[-1]+stage2[0:-1]
        words.append(stage3)

    load_animation("Decrypting")
    message = ' '.join(words)
    type_text(f"{selected_key} => {message}")
    print()
    pyperclip.copy(message)
    load_animation_mini("wait a little bit")
    type_text("I have already copied it in your clipboard for you...😎.\n")
    load_animation_mini("See...")
    time.sleep(1)
    keyboard.press_and_release('windows+v')
    type_text("\nAdios!!")

else:
    type_text(f"⚠️ Invalid Input. What's this {ask} 😒??")
