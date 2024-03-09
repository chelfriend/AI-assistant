import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize WolframAlpha API
app_id = "YOUR_WOLFRAMALPHA_APP_ID"  # Replace with your WolframAlpha app ID
client = wolframalpha.Client(app_id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print("User:", query)
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand what you said.")
        except sr.RequestError as e:
            speak(f"Sorry, I couldn't retrieve results due to a network error: {e}")
    return ""

def search_web(query):
    webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Multiple results found. Here are the options: {', '.join(e.options)}")
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find any information.")

def wolframalpha_query(query):
    try:
        res = client.query(query)
        answer = next(res.results).text
        speak("According to WolframAlpha")
        speak(answer)
    except Exception as e:
        speak(f"Sorry, I couldn't retrieve results: {e}")

def main():
    speak("Hello! How can I assist you today?")
    while True:
        query = get_audio()
        if "search in wikipedia" in query:
            speak("What do you want to search?")
            search_query = get_audio()
            search_wikipedia(search_query)
        elif "search on the web" in query:
            speak("What do you want to search?")
            search_query = get_audio()
            search_web(search_query)
        elif "ask wolfram" in query:
            speak("What do you want to ask?")
            question = get_audio()
            wolframalpha_query(question)
        elif "exit" in query:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I couldn't understand your command. Please try again.")

if __name__ == "__main__":
    main()
