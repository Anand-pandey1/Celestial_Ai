import pyautogui
import keyboard
while True:
    cmd = input(">> ")

    if cmd == "alt tab":
        pyautogui.keyDown("alt")
        pyautogui.press("tab")
        pyautogui.keyUp("alt")

    elif cmd == "open notepad":
        pyautogui.hotkey("win", "r")
        pyautogui.write("notepad")
        pyautogui.press("enter")
