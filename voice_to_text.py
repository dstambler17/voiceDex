from gtts import gTTS
import speech_recognition as sr
import os
import time
from get_poke_info import Pokedex
from langdetect import detect_langs

def listen_for_response(recognizer, microphone):
    '''
    Given Audio input, returns text
    '''
    with microphone as source:
        print('Listening for response...')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        print("Identified Response, transcribing...")
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["success"] = False
        response["error"] = "Unable to recognize speech"

    return response

def speak(text, lang):
    '''
    Outputs audio given a text
    '''
    language = lang
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("test.mp3")
    os.system("start test.mp3")

def voice_command():
    #test_text = 'Welcome! Please say a number between 1 and 807'
    #speak(test_text, 'en')
    #time.sleep(5)
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    #while True:
    response = listen_for_response(recognizer, microphone)

    if not response['success']:
        print(response["error"])
        return None, None, None
    else:
        if response['transcription'].strip() == 'exit' or response['transcription'].strip() == 'quit':
            print('Exiting')
            #break
        else:
            print(response['transcription'])
            dex_num = response['transcription'].strip()
            poke_name, poke_description = Pokedex.get_poke_info(dex_num)
            
            lang = str(detect_langs(poke_description)[0])[0:2]
            text_to_speak = 'Name: {}, Description: {}'.format(poke_name, poke_description)
            speak(text_to_speak, lang)
            #time.sleep(10)
            return poke_name, poke_description, dex_num

    print('\n')


#if __name__ == "__main__":
#    voice_command()
