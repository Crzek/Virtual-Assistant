#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pyttsx3                      #texto to audio
import datetime
import speech_recognition as sr     #audio to txt
import wikipedia
import requests                     #noticias
import json                         #noticias
import webbrowser                   #https://docs.python.org/es/3/library/webbrowser.html
import os
#import pyaudio
from programas import App

# configuration
'''
https://ichi.pro/es/introduccion-a-pyttsx3-un-conversor-de-texto-a-voz-para-python-81905511310787
espeak.py  for ubuntu
nsss.py for Macs
sapi5   for Windows
'''
engine = pyttsx3.init('sapi5')
voices  = engine.getProperty('voices')
# print(voices)
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 180)
# print(voice[0].id)

app_l = []
userpath = os.environ["USERPROFILE"]
programPath = "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"

wikipedia.set_lang("es")

def speak(audio):
    """conversor de texto plano a audio

    :audio: str
    :returns: audio

    """
    engine.say(audio)
    engine.runAndWait()

def yosoy():
    """
    funcion para que sepa que hora es, poder personalizar en saludo.

    """

    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <12:
        speak("Buenos Dias")
    elif hour >= 12 and hour < 18:
        speak("Buenas Tardes")
    else:
        speak("Buenas Noches")

    speak(f"Bienvenido {autor}, Soy Jarvis, un Asistente virtual")

def listen():
    """Hablar para que capte informacion y la escriba

    input:
    output: query de lo que dice el usurio
    """
    rec = sr.Recognizer()
    with sr.Microphone() as fuente:
        print("Escuchando...")
        rec.pause_threshold = 1.5
        audio = rec.listen(fuente)

    try:
        print("Reconociendo...")
        query = rec.recognize_google(audio, language="es-ES")
        print(f"User Said:{query} \n") # muestra lo que has escrito
        return query.lower()

    except Exception as e:
        print(f"Disculpa {autor}, puedes repetir...")
        return None

def wiki(query):
    """ Buscara en Wikipedia.

    :arg1: consulta, en txt
    :returns: texto de wikipedia

    """
    speak("Buscadno en Wikipedia...")
    query = query.replace("wikipedia", "")          #remplaza la palabra wikipedia por ""
    result = wikipedia.summary(query, sentences=2)
    speak("Segun mi Busqueda...")
    print(result)
    speak(result)



def news(query):
    """busca noticias actuales, atreves de un API
    :query: consulta  en  texto
    :returns: retorna texto para hablr o None

    """
    speak("Titulares..")
    query = query.replace("noticias","")
    url = "https://newsapi.org/v2/top-headlines?country=mx&apiKey=e38b0e82f33240dd86adee6acc978b26"
    noticias = requests.get(url).text
    noticias = json.loads(noticias)
    art = noticias["articles"]
    for articulo in art:
        print(articulo["title"])
        speak(articulo["title"])
        # speak (articles["description"])
        speak("Siguiente Noticia...")


def search(query):
    """cuando escuche la palabra busca  o buscar, entrara en esta funcion

    :query: str
    :returns: la busqueda, ya sea por buscador

    """
    l = ("https://search.brave.com/search?q=",          #brave
         "https://www.google.com/search?q=",            #google
         "https://duckduckgo.com/?q="                   #bing

         )

    if (type(query) is None) or (query is None) or (query != ""):
        speak(f"Buscando..., {query} en google")
        # speak(" en google...")
        webbrowser.open(f"{l[1]}{query}")
    else:
        speak("Que te gustaria Buscar?")
        query = listen()
        speak(f"Bucando..., {query} en google")
        # speak(" en google...")
        webbrowser.open(f"{l[1]}{query}")



def abrir(query):
    """Abre aplicaciones

    :query: str
    :returns: abre app

    """
    #falta
    with os.chdir(f"{userpath}{programPath}") as Path:
        apps = os.listdir()
        speak(f"abriendo, {query}")

def onlyExe(lista):
    """limpia la lista, para quitar direcctorio ysolo poner archivos .exe"""
    exes = []
    for el in lista:
        if ".exe" in el:            #si el --> str contine ".exe"
            Pg = App(el[:-4], )
            exes.apped(el)

def prettieQuery(query, remove = None ):
    """convierte la consulta en una  pero mas limpia

    :query: str
    :remove: lista o str
    :returns: remove, son las palbras que eliminara de la consulta, por eso se puede utilizar un conjunto de palbras (lista)

    """
    if type(remove) is list:             #remove es un lista
        for r in remove:
            query = query.replace(r,"")
    else:                                   #remove es un str
        query = query.replace(remove, "")
    return query

def option(query):
    """diferente tareas que puede realizar JARVIS

    ::query: str
    :returns: TODO

    """

    if ("wikipedia" and  "quién") in query:
        query = prettieQuery(query,"wikipedia")
        wiki(query)

    elif "noticias" in query:
        query = prettieQuery(query,["noticias"])
        news(query)

    elif ("busca" in query) or ("buscar" in query):
        query = prettieQuery(query,["buscar", "busca"])
        search(query)

    elif "dirección ip" in query:
        ip = requests.get("https://api.ipify.org").text
        print(f"Tu direción IP: {ip}")
        speak(f"Tu direción IP: {ip}")


    elif ("abre" in query) or ("abrir" in query):
        query = prettieQuery(query,["abre", "abrir"])
        abrir(query)


def main():
    yosoy()
    some = listen()
    option(some)


autor = "Erick"
if __name__ == "__main__":
    main()
