##!/usr/bin/env python3
# -*- coding: utf-8 -* 

import pyttsx3        # text to audio
import os
import wikipedia




#configuration
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

wikipedia.set_lang("es")

APP_LIST = []
USER_PATH = os.environ["USERPROFILE"]
START_PATH = f"{userpath}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\"
PROGRAM_PATH = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\"

