import speech_recognition as sr
import pyttsx3 as py
import pywhatkit as ps
import datetime as dt
import wikipedia as wiki
import time
import py_search as sra
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

listne = sr.Recognizer()
eng = py.init()
voices = eng.getProperty('voices')
eng.setProperty('voice',voices[1].id)

def talk(text):
    eng.say(text)
    eng.runAndWait()
def take():
    try:
        with sr.Microphone() as source:
            print('Please Told Something...')
            voice = listne.listen(source)
            com = listne.recognize_google(voice)
            com = com.lower()
            if 'google' in com:
                com = com.replace('google','')
                print(com)
    except:
        pass
    return com

def run():
    com = take()
    print(com)
    if 'play' in com:
        song = com.replace('play','')
        """talk('Playing ' + song)"""
        ps.playonyt(song)
    elif 'time' in com:
        time = dt.datetime.now().strftime('%I:%M:%S %p')
        print(time)
        talk('Current time is ' + time)
    elif 'date' in com:
        dat = dt.date.now().date('%DD/%MM/%YY')
        print(dat)
        talk('Current time is ' + dat)
    elif 'google' in com:
        driver = webdriver.Chrome('I:\Virtual_Assistance\browser\chromedriver.exe')
        driver.maximize_window()
        driver.execute_script("window.open('');")
        window_list = driver.window_handles
        driver.switch_to_window(window_list[1])
        driver.get('https://google.com')
        while True:
            query = sr()
            if query != 'Error':
                break
        ele = driver.find_element_by_name('q')
        ele.clear()
        ele.send_keys(query)
        ele.send_keys(Keys.RETURN)
    elif 'search' in com:
        pr = com.replace('search', '')
        info = wiki.summary(pr,1)
        print(info)
        talk(info)
    else:
        print('My bad. Please say it again.')
while True:
    run()