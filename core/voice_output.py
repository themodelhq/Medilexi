
import pyttsx3

def speak(text, lang='en'):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Try matching a language voice
    for voice in voices:
        if lang in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    engine.say(text)
    engine.runAndWait()
