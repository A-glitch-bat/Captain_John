#--------------------------------

# Imports
import speech_recognition as sr
#--------------------------------
"""
pip install SpeechRecognition
pip install PyAudio
pip install pygame
# List all microphones
print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")
"""
voice_recognizer = sr.Recognizer()

def listener():
    with sr.Microphone(device_index=1) as source:
        print("Adjusting for ambient noise... Please wait.")
        voice_recognizer.adjust_for_ambient_noise(source)
        print("Speak something!")
        try:
            audio = voice_recognizer.listen(source)
            text = voice_recognizer.recognize_google(audio)
            print(f"You said: {text}")
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google API: {e}")

if __name__ == "__main__":
    audio = listener()
