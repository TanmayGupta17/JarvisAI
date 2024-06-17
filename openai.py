import os
import datetime
import speech_recognition as sr
import webbrowser
import pywhatkit as kit
import smtplib
from email.message import EmailMessage
import requests
import shlex
import google.generativeai as genai
import pyttsx3

# Initialize pyttsx3
engine = pyttsx3.init()

memory = {}
try:
    from achar import LoadData
    messages = LoadData()
    assert type(messages) == list
except:
    messages = []

try:
    from achar import SaveData
except:
    def SaveData(data, path="JarvisAI//chat.log"):
        with open(path, "w") as f:
            if type(data) == str:
                f.write(f'"""{data}"""')
            else:
                f.write(str(data))
        return True

def mytext(text):
    # Use pyttsx3 to convert text to speech
    engine.say(text)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        mytext("Good Morning sir")
    elif hour >= 12 and hour < 18:
        mytext("Good Afternoon sir")
    else:
        mytext("Good evening SIR")

import speech_recognition as sr

def takecommand():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"User Said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return "None"
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return "None"
    except Exception as e:
        print(f"Error: {str(e)}")
        return "None"



def open_application(app_name):
    if app_name == 'calculator':
        os.system("open -a Calculator")
    elif app_name == 'notepad':
        os.system("open -a TextEdit")
    elif app_name == 'safari':
        os.system("open -a Safari")
    elif app_name == 'spotify':
        os.system("open -a Spotify")
    elif app_name == 'calendar':
        os.system("open -a Calendar")
    else:
        print(f"Sorry, I cannot open {app_name}")

def send_email():
    try:
        mytext("To whom do you want to send the email?")
        recipient = input("Recipient's email address: ")

        mytext("What is the subject of the email?")
        subject = takecommand()

        mytext("What is the message content?")
        message_content = takecommand()

        msg = EmailMessage()
        msg['From'] = 'tanmaygupta1706@gmail.com'
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.set_content(message_content)

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login('tanmaygupta1706@gmail.com', 'talp orxo btqu sldh')
            smtp.sendmail('tanmaygupta1706@gmail.com', recipient, msg.as_string())

        print(f"Email sent successfully to {recipient}")
        mytext("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        mytext("Failed to send email. Please try again later.")

def get_news_headlines():
    newsapi_key = "8d8b867acc184e19b9230729c6837471"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["status"] == "ok":
            articles = data["articles"]
            head = []
            for article in articles:
                head.append(article["description"])

            for i in range(min(10, len(head))):  # Ensure not to go out of bounds
                print(f"{i + 1}. {head[i]}\n")
                mytext(head[i])  # Speak out the description

        else:
            print("Failed to retrieve news.")

    except Exception as e:
        print(f"Error fetching news: {str(e)}")

def ai(prompt):
    genai.configure(api_key="AIzaSyBY1EO15DG9W7eXZeI7PAHtIK5gOA5xxWo")

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[]
    )
    response = chat_session.send_message(prompt)
    remember_item(response.text)
    print(response.text)
    mytext(response.text)
    edit_response(response.text)

def chat(prompt):
    genai.configure(api_key="AIzaSyBY1EO15DG9W7eXZeI7PAHtIK5gOA5xxWo")

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    messages.append({
        "parts": [{"text": prompt}],
        "role": "user"
    })

    response = model.generate_content(messages)

    messages.append({
        "parts": [{"text": response.text}],
        "role": "model"
    })

    SaveData(messages)
    print(response.text)
    mytext(response.text)
    return response.text

def weather():
    api_key = "d77cf8e5b99a14df07bee5b3391bf979"
    mytext("Which city's weather would you like to know?")
    city = takecommand()

    if city == "none":
        return

    url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = url + "appid=" + api_key + "&q=" + city

    try:
        response = requests.get(complete_url)
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            weather_info = f'Today\'s temperature in {city} is {temp - 273.15:.2f}°C with {desc}.'
            mytext(weather_info)
            print(weather_info)
        else:
            print(f"Failed to retrieve weather data for {city}. Error: {data.get('message')}")
            mytext(f"Failed to retrieve weather data for {city}.")
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        mytext("Error fetching data.")

def replace_placeholders(letter, replacements):
    for placeholder, replacement in replacements.items():
        letter = letter.replace(placeholder, replacement)
    return letter

def edit_response(response):
    print("Do you want to make changes?")
    mytext("Do you want to make changes?")
    user_response = takecommand()
    if "yes" in user_response or "edit" in user_response:
        replacement = {}
        while True:
            mytext("Do you want to change a word or add your custom text?")
            r = takecommand()
            if "replace" in r:
                while True:
                    mytext("What word needs to be replaced?")
                    word_to_change = takecommand()
                    mytext("What word should it be replaced with?")
                    word_with_changed = takecommand()
                    replacement[word_to_change] = word_with_changed
                    mytext("Add another replacement? Say 'yes' or 'no'.")
                    rep = takecommand()
                    new_response = replace_placeholders(response, replacement)
                    if 'no' in rep:
                        break
            elif 'custom text' in r:
                mytext("What custom text would you like to add?")
                custom_text = takecommand()
                response += f" {custom_text}"
                ai(response)
                return
    return

# Generalized function to remember an item
def remember_item(item):
    mytext("What is the name for the item you want to store?")
    name = takecommand()
    memory[name] = item
    print(f"Stored {item} under {name}.")

# Generalized function to retrieve an item
def retrieve_item():
    mytext("What is the name of the item you want to retrieve?")
    name = takecommand()
    if name in memory:
        item = memory[name]
        print(f"The item for {name} is {item}.")
        mytext(f"The item for {name} is {item}.")
    else:
        print(f"No item found for {name}.")
        mytext(f"No item found for {name}.")

if __name__ == "__main__":
    wishme()
    mytext("How can I help you today?")
    chat_history = []
    run = True
    while run:
        query = takecommand().lower()

        if 'open youtube' in query:
            print("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in query:
            print("Opening Google...")
            mytext("Sir, what should I search?")
            search_query = takecommand().lower()
            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)
        elif 'open reddit' in query:
            print("Opening Reddit...")
            webbrowser.open("https://www.reddit.com/")
        elif 'open spotify' in query:
            print("Opening Spotify...")
            open_application('spotify')
        elif 'open calendar' in query:
            print("Opening Calendar...")
            open_application('calendar')
        elif 'send message' in query:
            mytext("Whom do you want to send the message to?")
            recipient = takecommand().lower()

            mytext("What's the message?")
            message = takecommand()

            try:
                kit.sendwhatmsg_instantly(recipient, message)
                print(f"Message sent successfully to {recipient}")
            except Exception as e:
                print(f"Failed to send message: {str(e)}")
                mytext("Failed to send message. Please try again later.")
        elif 'send email' in query:
            send_email()
        elif 'tell me the latest news' in query:
            get_news_headlines()
        elif 'weather today' in query:
            weather()
        elif 'use ai' in query:
            ai(query)
        elif 'quit' in query:
            print("Have a good day, sir")
            mytext("Have a good day, sir")
            break
        else:
            chat(query)
