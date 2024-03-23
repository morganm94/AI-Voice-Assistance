import pyttsx3
import datetime
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import webbrowser
import pyautogui
import wikipedia
import os
import psutil
import wolframalpha
from time import sleep
from fbchat import Client
from fbchat.models import *

def speak(audio):
    print(audio)
    engine = pyttsx3.init()
    engine.say(audio)
    engine.runAndWait()

def click():
    pyautogui.click()

def username():
    username = psutil.users()
    for user_name in username:
        first_name = user_name[0]
        speak(f"Sir, this computer is signed to mayur as a username.")
    
def screenshot():
    pyautogui.screenshot(f"C://Users//mayur//Desktop//screenshot.png")

def battery():
    battery = psutil.sensors_battery()
    battery_percentage = str(battery.percent)
    plugged = battery.power_plugged
    speak(f"Sir, it is {battery_percentage} percent.")
    if plugged:
        speak("and It is charging....")
    if not plugged:
        if battery_percentage <= "95%":
            speak("Sir, plug charger.")

def shutDown():
    speak(f'Ok Sir   ')
    speak('Initializing shutdown protocol ')
    click()
    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('alt')
    pyautogui.press('enter')
    sleep(3)
    pyautogui.press('enter')

def restart():
    speak("Ok Sir    ")
    speak("Restarting your computer")
    click()
    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('enter')
    sleep(3)
    pyautogui.press('r')
    pyautogui.press('enter')

def Sleep():
    speak('Ok sir    ')
    speak("Initializing sleep mode")
    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('alt')
    sleep(2)
    pyautogui.press('s')
    pyautogui.press('s')
    pyautogui.press('enter')

def weather():
    speak("Checking the details for weather...")
    URL = "https://weather.com/weather/today/l/26.62,87.36?par=google&temp=c"
    header = {"User-Agent":'your user agent'}
    page = requests.get(URL, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    temperature_element = soup.find(class_="CurrentConditions--tempValue--3KcTQ")
    if temperature_element is not None:
        temperature = temperature_element.get_text()
    else:
        temperature = "Temperature information not available"

    description_element = soup.find(class_="CurrentConditions--phraseValue--2xXSr")
    if description_element is not None:
        description = description_element.get_text()
    else:
        description = "Description information not available"

    temp = "Sir, the temperature is " + temperature + " celcius." + ' and it is ' + description + ' outside.'
    speak(temp)
    if temperature < '20°':
        speak("It will be better if you wear woolen clothes, sir.")
    elif temperature <= '14°':
        speak("Sir, it is very cold outside. If you want to go outside, wear woolen clothes.")
    elif temperature >= '25°':
        speak("Sir, you donot need to wear woolen clothes to go outside.")

def message():
    speak("Checking for messages....")
    userID = "your email"
    psd = 'your password'
    useragent = "you user agent"

    cli = Client(userID, psd, user_agent=useragent, max_tries=1)
    if cli.isLoggedIn():
        threads = cli.fetchUnread()
        if len(threads) == 1:
            speak(f"Sir, You have {len(threads)} message.")
            info = cli.fetchThreadInfo(threads[0])[threads[0]]
            speak("You have message from {}".format(info.name))
            msg = cli.fetchThreadMessages(threads[0], 1)
            for message in msg:
                speak("Sir, the message is {}".format(message.text))
        elif len(threads) >= 2:
            speak(f"Sir, You have {len(threads)} messages.")
            for thread in threads:
                initial_number = 0
                info = cli.fetchUserInfo(thread[initial_number])[thread[initial_number]]
                initial_number += 1
                speak("Sir, you have message from {}".format(info.name))
                msg = cli.fetchThreadMessages(thread[initial_number], 1)
                msg.reverse()
                for message in msg:
                    speak(f"The message is {message.text}.")
        else:
            speak("Sir, You have no messages.")
    else:
        print("Not logged in")

def time():
    time = datetime.datetime.now().strftime('%I:%M:%S')
    speak(f"Sir, the current time is {time}.")

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak(f"Sir, the current year is {year}, current month is {month} and the current date is {date}")

def google_search(audio_data):
    url = "https://www.google.com/?#q=" + audio_data
    webbrowser.open(url)
    speak(f"Sir, getting the result for {audio_data} from google.com")

def youtube_search(audio_data):
    url = "https:www.youtube.com/?#query=" + audio_data
    webbrowser.open(url)
    speak(f"Sir, getting the result for {audio_data} from youtube.com")

def calculate(audio_data):
    app_id = '8REQUG-YQ7JGY96T8'
    client = wolframalpha.Client(app_id)
    res = client.query(audio_data)
    answer = next(res.results).text
    speak(answer)

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 400
        r.dynamic_energy_threshold = True
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio)
        print(query)
        if 'Jarvis' in query:
            speak("Yes, Sir")
        elif 'tell me the date' in query or 'tell me date' in query:
            date()
        elif 'tell me the time' in query or 'what time is it' in query or 'tell time' in query:
            time()
        elif 'thank you' in query:
            speak('No problem sir')
        elif 'open Google' in query:
            webbrowser.open("https://www.google.com")
            speak("Opening google...")
        elif 'Google search' in query:
            speak('What do you want to search')
            audio_data = command()
            google_search(audio_data)
        elif 'open YouTube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("Opening Youtube....")
        elif 'YouTube search' in query:
            speak('What do you want to search?')
            audio_data = command()
            youtube_search(audio_data)
        elif 'open Facebook' in query:
            webbrowser.open_new_tab("https://www.facebook.com")
            speak("Opening Facebook")
        elif 'open Gmail' in query:
            webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
            speak("Opening Gmail..")
        elif 'open maps' in query or 'show my location' in query:
            webbrowser.open("https://www.google.com/maps/@26.6235458,87.3614451,16z")
            speak("Opening Maps...")
        elif 'calculate' in query:
            speak('Tell me sir')
            audio_data = command()
            calculate(audio_data)
        elif 'tell me' in query:
            audio_data = query.replace('tell me', '')
            calculate(audio_data)
        elif "what's the weather" in query or 'tell me the temperature' in query or "what's the temperature" in query:
            weather()
        elif 'click the mouse' in query or 'click mouse' in query or 'click' in query:
            click()
        elif 'take a screenshot' in query or 'take screenshot' in query:
            screenshot()
        elif 'Wikipedia' in query:
            query = query.replace("Wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak('Acoording to wikipedia, ')
            speak(results)
        elif 'close current window' in query:
            pyautogui.keyDown('alt')
            pyautogui.press('f4')
            pyautogui.keyUp('alt')
            speak('Current window is closed.')
        elif 'battery percentage' in query or 'percentage in battery' in query or 'percent in my pc' in query:
            battery()
        elif 'shutdown' in query or 'shut down' in query or 'close my PC' in query:
            shutDown()
        elif 'sleep' in query or 'sleep mode' in query:
            Sleep()
        elif 'check message' in query or 'check messages' in query or 'check new messages' in query or 'check new message' in query or 'any new messages' in query or 'any new messages' in query or 'any new message' in query or 'any messages' in query or 'any message' in query:
            message()
        elif 'username' in query or 'user' in query or 'user name' in query:
            username()

    except:
        return None
    return query

def greeting():
    speak('Welcome back sir.')
    time()
    date()

if __name__ == '__main__':
    greeting()
    weather()
    speak("Getting battery information....")
    battery()
    while True:
        command()