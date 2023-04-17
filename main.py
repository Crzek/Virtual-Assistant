#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# APP class
from programas import App

# reed your apps in Windows
from config import AUTOR, APP_LIST, START_PATH, PROGRAM_PATH, ENGINE, voices, LANGUAGE



import datetime
import speech_recognition as sr     #audio to txt
import wikipedia
import requests                     #noticias
import json                         #noticias
import webbrowser                   #https://docs.python.org/es/3/library/webbrowser.html
import os
#import pyaudio

#funtions
def change_rute(path,old = "\\",caracter = "/"):
    """TODO: C:sers\ERICK
            C:/Users/ERICK

    :path: Ruta
    :returns: path corregido

    """
    return path.replace(old, caracter)

def speak(audio):
    """conversor de texto plano a audio

    :audio: str
    :returns: audi\o

    """
    ENGINE.say(audio)
    ENGINE.runAndWait()

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

    speak(f"Bienvenido {AUTOR}, Soy Jarvis, un Asistente virtual")

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
        query = rec.recognize_google(audio, language=LANGUAGE)
        print(f"User Said:{query} \n") # muestra lo que has escrito
        return query.lower()

    except Exception as e:
        print(f"Disculpa {AUTOR}, puedes repetir...")
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

def gopath(appPath):
    """ si una app tiene un ruta, esta la devuelve en su directorios

    ejemplo: brave.lnk  ---->acceso directo
    :ruta :C:ers\ERICK\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Brave.lnk
    :devuelve: C:ers\ERICK\AppData\Roaming\Microsoft\Windows\Start Menu\Programs

    appPath: es el paht del app

    """

    i = 0
    path = False
    while (-len(appPath) < i) and (not path):
        if appPath[i] == "\\":
            path = True
        else:
            i = i -1
    if path:
        return appPath[:i], appPath[i+1:]       #path, nombre app
    else:
        print("NO se puee volver al path anterior")
def abrir(query):
    """Abre aplicaciones

    :query: str
    :returns: abre app

    """
    #falta
    if len(APP_LIST) != 0:
        pro = busca_appl(query)         #busca la app en lista de APP_LIST
        dir, name = gopath(pro.get_path())        #dirrectoria de programas
        os.chdir(dir)
        speak(f"abriendo..., {query}")
        os.system(name)
    else:
        speak("NO, tienes aplicaciones guardadas")

def busca_appl(name, Alias = None):
    """ itera la appl para buscar EL nombre que conincide con la query

    :Name : sera la query
    :Alias : por defecto es None, pero si el progrma tiene self.ALias ---> se buscara por ahi

    """
    """algoritmo de Busqueda

    :name es el objeto que se busca o progrma
    :returns devuelve e; pbjeto progrma

    """

    i = 0
    trobat = False
    while (len(APP_LIST) > i) and (not trobat):
        if (APP_LIST[i].get_name() == name) or (APP_LIST[i].get_alias() == Alias):
            trobat = True
        else:
            i = i +1
    if trobat:
        return APP_LIST[i]        #devuelve la posicon de la lista( i ) o el objeto (APP_LIST[i]) 
    else:
        print("No se ha encontrado elemento")

def sayAPPS(l_prg):
    """te dice en audo que progrmas tiene a su disposicion para abrir

    :l_prg: lista de la clase programas
    :returns: TODO

    """
    speak("los programas que tienes a disposicion son:")
    for app in l_prg:
        ap = app.get_name()
        speak(ap)
        print(ap)

def cargaAPP():
    """Lee los directorios del prgrama para guardarlos en en una lista

    :arg1: TODO
    :returns: abre app

    """
    #falta
    speak("Cargaré unos Programas para tenerlos a tu disposición")
    for path in [START_PATH,PROGRAM_PATH]:
        apps = os.listdir(path)
        #with os.listdir(path) as apps:
        Exes = onlyLNK(apps, path)
        APP_LIST.extend(Exes)          #APP_LIST = APP_LIST + Exes

    if len(APP_LIST) >= 1:
        speak(f"Programas cargados, se han cargado {len(APP_LIST)} Aplicaciones")
    else:
        speak("No se ha cargado, ninguna Aplicación")


def onlyLNK(lista, path):
    """limpia la lista, para quitar direcctorio y solo quedarme con los accesos directos
        lista: ["breve.lnk", "dicorbs"]
        path :current work directory
        return: lista de la clase APP
    """
    exes = []
    for el in lista:
        if ".lnk" in el:
            new_p = path + el
            Prg = App(el[:-4], new_p)
            exes.append(Prg)
    return exes


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
    return query.strip()    #elimina los espacion en blanco

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

    elif ("programa" in query) or ("tengo" in query):
        sayAPPS(APP_LIST)
        speak("cual programa quieres que habra?")


def main():
    yosoy()
    cargaAPP()
    some = listen()
    option(some)



if __name__ == "__main__":
    main()
