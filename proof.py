import pyttsx3


engine = pyttsx3.init('sapi5')

engine.setProperty("rate",180)          #velocidad de la voz
# voz = engine.getProperty("voices")
# for v in voz:
#     print(f"Voz: {v.name}")

engine.say('bienvenido, buenas soy jarvis, tu quien eres?')
engine.runAndWait()
voz = pyttsx3.voice.Voice
print(voz)
