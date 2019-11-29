import datetime
import os
import time

import pyttsx3
import speech_recognition as sr
from fuzzywuzzy import fuzz

options = {
    "alias": ('василий', 'вася', 'васечка', 'васёчек', 'васька', 'вась', 'уася'),
    "toBeRemoved": ('скажи', 'пожалуйста', 'расскажи', 'покажи', 'произнеси', 'посмотри'),
    "commands": {
        "time": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи радио', 'воспроизведи радио', 'вруби радио'),
    }
}

# Simple code for searching microphone`s index
"""
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for 'Microphone(device_index={0})'".format(index, name))
"""


# functions
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startwith(options["alias"]):
            commands = voice

            for x in options["alias"]:
                commands = commands.replace(x, "").strip()

            for x in options["toBeRemoved"]:
                commands = commands.replace(x, "").strip()

                commands = recognize_cmd(commands)
                execute_cmd(commands["commands"])


    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка! Проверьте Ваше интернет соединение.")


def recognize_cmd(commands):
    RC = {'commands': '', 'percent': 0}
    for c, v in options['commands'].items():

        for x in v:
            vrt = fuzz.ratio(commands, x)
            if vrt > RC['percent']:
                RC['commands'] = c
                RC['percent'] = vrt
    return RC


def execute_cmd(commands):
    if commands == 'time':
        now = datetime.datetime.now()
        speak("Сейчас: " + str(now.hour) + ":" + str(now.minute))

    elif commands == 'radio':
        os.system("путь к аудиофайлу")

    else:
        print('Команда не распознана, повторите!')


# start
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[4].id)

speak("Здравствуйте, повелитель")
speak("Меня зовут Василий, чем я могу помочь?")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1)  # infinity loop
