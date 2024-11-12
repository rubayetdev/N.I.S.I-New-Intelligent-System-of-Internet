import speech_recognition as sr
import pyttsx3 as py
import pywhatkit as ps
import datetime as dt
import wikipedia as wiki
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

listne = sr.Recognizer()
eng = py.init()
voices = eng.getProperty('voices')
eng.setProperty('voice', voices[1].id)

# Initialize driver as a global variable
driver = None  # Initialize driver outside any function

def talk(text):
    eng.say(text)
    eng.runAndWait()

def take():
    com = ""  # Define a default empty string for 'com'
    try:
        with sr.Microphone() as source:
            print('Please say something...')
            voice = listne.listen(source)
            com = listne.recognize_google(voice)
            com = com.lower()
            print("You said:", com)
    except Exception as e:
        print("Error with voice input:", e)

    return com  # Return either the recognized voice command or an empty string

def close_browser():
    global driver  # Declare 'driver' as global so we can modify it
    if driver:
        driver.quit()  # Close the browser if it's open
        talk("Browser closed.")
        print("Browser closed.")
        driver = None  # Reset driver to None after closing
    else:
        talk("No browser is currently open.")
        print("No browser is currently open.")

def run():
    global driver  # Declare the global driver here at the beginning of the function
    com = take()

    # Check for the 'stop' command first and stop the program if it's found
    if 'stop' in com:
        talk('Stopping the program. Goodbye!')
        return False  # This will stop the loop and the program

    if 'play' in com:
        song = com.replace('play', '')
        talk('Playing ' + song)
        ps.playonyt(song)
    elif 'time' in com:
        current_time = dt.datetime.now().strftime('%I:%M:%S %p')
        print(current_time)
        talk('Current time is ' + current_time)
    elif 'date' in com:
        current_date = dt.date.today().strftime('%d/%m/%Y')
        print(current_date)
        talk('Today\'s date is ' + current_date)
    elif 'search for' in com and 'on google' in com:
        query = com.replace('search for', '').replace('on google', '').strip()

        # Use text input for search query if voice command doesn't specify one
        if not query:
            query = input("Enter text to search on Google: ")

        talk(f'Searching for {query} on Google.')

        # Correct initialization of ChromeDriver using Service
        service = Service(ChromeDriverManager().install())  # Automatically installs the correct version of ChromeDriver
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        driver.get('https://google.com')
        search_box = driver.find_element("name", "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for user input to keep the window open
        input("Press Enter to continue...")  # This will wait for user input before continuing
    elif 'close the browser' in com:
        close_browser()
    elif 'text option' in com:  # Trigger for text option
        talk('Please enter the text you want to search for.')
        query = input("Enter your search query: ")  # Let the user type the search query
        talk(f'Searching for {query} on Google.')

        # Correct initialization of ChromeDriver using Service
        service = Service(ChromeDriverManager().install())  # Automatically installs the correct version of ChromeDriver
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
        driver.get('https://google.com')
        search_box = driver.find_element("name", "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for user input to keep the window open
        input("Press Enter to continue...")  # This will wait for user input before continuing
    else:
        print('My bad. Please say it again.')

    return True  # Keep the program running unless 'stop' is said

while True:
    if not run():  # Stop the loop if run() returns False
        break
