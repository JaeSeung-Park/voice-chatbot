import os
from openai import OpenAI
from IPython.display import Audio
from playsound import playsound
import wave, pyaudio
import librosa
import soundfile as sf
from scipy.io import wavfile
import speech_recognition as sr
import threading
from pydub import AudioSegment


client = OpenAI(
    api_key='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',
)

def update_list(message, pl):
    pl.append(message)


def create_prompt(message, pl):
    p_message = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt = ''.join(pl)
    return prompt

def get_api_response(prompt):
    try:
        response = client.chat.completions.create(
        model="gpt-4",
        messages = [
        {
            "role": "system",
            "content": prompt
        },
        # {
        #     "role": "user",
        #     "content": prompt
        # }
        ],
        # prompt=prompt,
        max_tokens=100,
        temperature=0.8,
        stop=[' Human:', ' AI:']
        )
        return response.choices[0].message.content
    except Exception as e:
        print('error', e)
        
def get_bot_response(message, pl):
    prompt = create_prompt(message, pl)
    bot_response = get_api_response(prompt)
    if bot_response:
        update_list(bot_response, pl)
        pos = bot_response.find("\nAI: ")
        # bot_response = bot_response[pos + 4:]
        bot_response = bot_response[pos + 4:]
    else:
        bot_response = "Something went wrong..."
    return bot_response

i = 0
# path = f"chatbot\output{i}.mp3"

def audio_play():
    # Audio("chatbot\output.wav", rate=20000)
    
    # fs, data = wavfile.read("chatbot\output.wav")
    global i
    audio_file = f"chatbot\output{i}.mp3"
    playsound(audio_file)
    
    # chunk = 1024
    # with wave.open("chatbot\output.wav", 'rb') as f:
    #     p = pyaudio.PyAudio()
    #     stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
    #                     channels=f.getnchannels(),
    #                     rate= f.getframerate(),
    #                     output=True)
    #     data = f.readframes(chunk)
    #     while data:
    #         stream.write(data)
    #         data = f.readframes(chunk)
            
    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()
    
    # x,_ = librosa.load('chatbot\output.wav', sr=16000)
    # sf.write('tmp.wav', x, 16000)
    # wave.open('tmp.wav','r')
    
    # file_path = "chatbot\output.wav"

    # # Read and rewrite the file with soundfile
    # data, samplerate = sf.read(file_path)
    # sf.write(file_path, data, samplerate)

    # # Now try to open the file with wave
    # with wave.open(file_path) as file:
    #     print('File opened!')

def tts(bot_response):
    global i
    i += 1
    try:
        response = client.audio.speech.create(
        model='tts-1-hd',
        voice="alloy",
        input=bot_response,
        speed=1,
        response_format = 'mp3'
        )
        response.stream_to_file(f"chatbot\output{i}.mp3")
        return audio_play() 
    except Exception as e:
        print('error', e)
        

k = 0
j = 0

def record_voice():    
    global k, j
    k += 1
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 30
    WAVE_OUTPUT_FILENAME = f"chatbot\input.wav"

    p= pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("녹음 시작")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("녹음 완료")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    # 오디오 파일 로드
    
    j = k - 1
    if j == 0:
        # sound1 = AudioSegment.from_wav("chatbot\input{j}.wav")
        sound2 = AudioSegment.from_wav("chatbot\input.wav")
        # combined_sounds = sound1 + sound2
        sound2.export("chatbot\conversation.wav", format="wav")
    else:
        sound1 = AudioSegment.from_wav("chatbot\conversation.wav")
        sound2 = AudioSegment.from_wav("chatbot\input.wav")
        combined_sounds = sound1 + sound2
        combined_sounds.export("chatbot\conversation.wav", format="wav")

    # print("파일 재생")
    # playsound(WAVE_OUTPUT_FILENAME)

stop_flag = False
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 30
WAVE_OUTPUT_FILENAME = f"chatbot\input.wav"
p= pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
frames = []
def record():
    global stop_flag, frames
    stop_flag = False
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p= pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []    
    while not stop_flag:
        # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        
    # return frames   

def speech_recognition():
    global k, j, stop_flag, frames
    k += 1
    frames = []
    
    # t1 = threading.Thread(target=record_voice, daemon=True)
    t1 = threading.Thread(target=record, daemon=True)
    try:
        while True:
            r = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("말하는 중입니다...")
                t1.start()
                print("녹음 시작")
                
                # r.pause_threshold = 1
                audio = r.listen(source)
                print("말하기 멈춤")
                stop_flag = True
                print("녹음 완료")
                t1.join()

                stream.stop_stream()
                stream.close()
                p.terminate()

                wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                
                j = k - 1
                if j == 0:
                    # sound1 = AudioSegment.from_wav("chatbot\input{j}.wav")
                    sound2 = AudioSegment.from_wav("chatbot\input.wav")
                    # combined_sounds = sound1 + sound2
                    sound2.export("chatbot\conversation.wav", format="wav")
                else:
                    sound1 = AudioSegment.from_wav("chatbot\conversation.wav")
                    sound2 = AudioSegment.from_wav("chatbot\input.wav")
                    combined_sounds = sound1 + sound2
                    combined_sounds.export("chatbot\conversation.wav", format="wav")
                
            try:
                print(r.recognize_google(audio, language='ko-KR'))
                with open("chatbot\conversation.html", 'a') as f:
                    f.write(r.recognize_google(audio, language='ko-KR'))
                return r.recognize_google(audio, language='ko-KR')
            except sr.UnKnownValueError:
                print("음성 이해 불가")
            except sr.RequestError as e:
                print(f"ERROR: {e}")
    except KeyboardInterrupt:
        pass    