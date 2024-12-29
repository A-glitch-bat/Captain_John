import speech_recognition as sr

"""
pip install SpeechRecognition
pip install PyAudio
pip install pygame
"""
recognizer = sr.Recognizer()

# List all microphones
print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")

def record_audio():
    with sr.Microphone(device_index=1) as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Speak something!")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google API: {e}")

if __name__ == "__main__":
    audio = record_audio()
