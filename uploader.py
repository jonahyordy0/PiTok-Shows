import os
import pyautogui
import webbrowser
import time
import pyperclip


url = 'https://www.tiktok.com/upload?lang=en'
clipsloc = r'home/jonah/Desktop/tt/ '

def upload(filename, account):
    os.system("killall chromium-browser")
    time.sleep(2)
    sW, sH = pyautogui.size()
    print(sW,sH)
    
    print(account)
    
    os.system('chromium-browser tiktok.com/upload --profile-directory="Profile ' + str(account) +'" &')
    time.sleep(20)
    for i in range(5): # Open Upload Prompt
        pyautogui.press('tab')
        time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)
    print(clipsloc+filename)
    pyautogui.press('/')
    pyperclip.copy(clipsloc+filename)
    time.sleep(3)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(2)
    print("loading")
    time.sleep(120)

    pyautogui.hotkey('shift', 'tab')
    print("okay")
    time.sleep(3)
    pyautogui.moveTo(sW*0.475,sH*0.475)
    time.sleep(3)
    
    t = pyautogui.locateOnScreen('button.png', confidence=0.8)
    
    if t is not None:
        print("Upload Success")
        # Upload Video
        pyautogui.press('enter')
        time.sleep(15)
        os.system("killall chromium-browser")
    else:
        print("Upload Failed Trying Again")
        time.sleep(5)
        upload(filename, account)

if __name__ == "__main__":
    upload("#rick #rickandmorty #foryou #fyp #morty #movie #game #❤️❤️.mp4", 2)