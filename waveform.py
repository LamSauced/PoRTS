import speech_recognition as sr
import queue
import threading
import subprocess
import datetime

# Function to transcribe audio segment
def transcribe_segment(segment, recognizer):
    try:
        text = recognizer.recognize_google(segment)
        return text
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        pass

# Function to listen to microphone and segment audio
def listen_and_segment_microphone(q, recognizer):
    microphone = sr.Microphone()
    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... (Press Ctrl+C to stop)")
        while True:
            audio_data = recognizer.listen(source, phrase_time_limit=3)  # Adjust phrase_time_limit as needed
            q.put(audio_data)

# Main function for transcription
def transcribe_microphone_segments():
    recognizer = sr.Recognizer()
    segments_queue = queue.Queue()

    # Start a separate thread to continuously listen to the microphone and put audio segments into the queue
    listen_thread = threading.Thread(target=listen_and_segment_microphone, args=(segments_queue, recognizer), daemon=True)
    listen_thread.start()

    # Process audio segments from the queue and transcribe them
    while True:
        segment = segments_queue.get()  
        transcription = transcribe_segment(segment, recognizer)
        if transcription is None:
            pass
        else:
            commands(transcription)

def record_audio(filename, duration):
    print(f"Recording audio for {duration} seconds...")
    subprocess.run(["arecord", "-d", str(duration), "-f", "S16_LE", "-r", "44100", "-c", "2", filename])
    print("Recording finished.")

def commands(transcript):
    
    if "secure shell" in transcript:
        subprocess.call(["ssh", "xxxx@xxxx"])
        print("Attempted SSH Connection")
    if "make a note" in transcript:
        with open("transcription.txt", "w") as file:
            file.write(transcript)
        print("Note successfully saved to transcription.txt")
    if "read note" in transcript:
        with open("transcription.txt", "r") as file:
            print(file.read())
    if "waveform" in transcript:
        subprocess.Popen(["alacritty", "-e", "cava"])
        print("Waveform generated")
    if "record" in transcript:
        duration = 10  # Example duration for recording (in seconds)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"recorded_audio_{timestamp}.wav"
        record_audio(filename, duration)
        print(f"Audio recorded and saved as {filename}")
    if "default" in transcript:
        print("No command detected")
    else:
        print("Transcription:", transcript)

# Call the main function to start transcription
transcribe_microphone_segments()