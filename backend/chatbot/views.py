from ast import Global
from django.shortcuts import render
from rest_framework.decorators import api_view
from .chatbotService.chartBotService import get_bot_response, tts, audio_play, record_voice, speech_recognition
from rest_framework.response import Response
from .chatbotService.chartBotService import *

import os
import json
import requests
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse, HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage

import numpy as np
import scipy.io.wavfile
import math
# import librosa
import tempfile
from io import BytesIO
from pydub import AudioSegment
import io
import moviepy.editor as moviepy

# from IPython.display import Audio
# from playsound import playsound
name = '김숙자'
sex = 'female'
age = 60
interest = '임영웅', '봄', '강아지'
diasease = '당뇨'
prompt_list = [
                '너는 혼자계신 시니어분의 말동무 역할을 수행하게 될거야. 사용자의 정보를 알려줄게',
                f'시니어 분의 성별은 {sex}이고 나이는 {age}세 이시며 관심사로는 {interest}등이 있고 {diasease}와 같은 질병을 앓고 계셔',
                '위 정보를 참고해서 이 분이 심심하지 않으시게 일상생활의 간단한 질문이나 대답을 해주면 되',
                '너무 자세하게 질문과 대답을 하기보단 호응해주고 맞춰주는 식으로 대화를 해줘',
                '무조건 존댓말로 대답해줘',
                ]

# @api_view(['POST'])
# def chatbot_controller(request):
#         # print(request.data, 'request.data::')
#         global prompt_list
#         # global name, age, interest, diasease
#         f = open("chatbot\conversation.html", 'w')
#         f.close()
#         while True:
#             try:
#                 # user_input = request.data['prompt']
#                 user_input = speech_recognition()
#                 # if(user_input == 'exit'):
#                 #     prompt_list = [
#                 #         '너는 혼자계신 시니어분의 말동무 역할을 수행하게 될거야. 사용자의 정보를 알려줄게',
#                 #         f'시니어 분의 성별은 {sex}이고 나이는 {age}세 이시며 관심사로는 {interest}등이 있고 {diasease}와 같은 질병을 앓고 계셔',
#                 #         '위 정보를 참고해서 이 분이 심심하지 않으시게 일상생활의 간단한 질문이나 대답을 해주면 되',
#                 #         '너무 자세하게 질문과 대답을 하기보단 호응해주고 맞춰주는 식으로 대화를 해줘',
#                 #         '무조건 존댓말로 대답해줘',
#                 #     ]
#                 response = get_bot_response(user_input, prompt_list)
#                 tts(response)
#                 # audio_play()
#                 print(f'AI {response}')
#                 # return Response(response, status=200)
#             except Exception as e:
#                 print('err:', e)
#                 # return Response('error', status=500)

# @csrf_exempt

@api_view(["GET"])
def wav(request):
    fname = 'media/news.wav'
    f = open(fname, "rb")
    response = FileResponse(f)
    response.set_headers(f)
    # response['Content-Type'] = 'audio/wav'
    # response['Content-Length'] = os.path.getsize(fname)
    return response


@api_view(['GET'])
def startConversation(request):
    print("대화 시작")
    
    return Response({'message': '대화가 시작되었습니다.'})

@api_view(['GET'])
def endConversation(request):
    print("대화 종료")
    
    return Response({'message': '대화가 종료되었습니다.'})

@api_view(['GET'])
def getSummary(request):
    print("대화 요약")
    with open('media/text.txt', "r", encoding='utf-8') as f:
        conversation = f.read()
    print(conversation)
    
    command = ['다음 내용은 혼자 계신 시니어와 말동무 역할인 음성 챗봇간의 일상 생활',
                '관련 대화 답변 내용이야. 이를 참고해서 혼자 계신 시니어의 일상 활동을',
                '간략하게 한줄정도로 요약해줘']
    
    prompt = create_prompt(conversation, command)
    print(prompt)
    response = client.chat.completions.create(
    model="gpt-4",
    messages = [
    {
        "role": "system",
        "content": prompt
    },
    ],
    max_tokens=100,
    temperature=0.8,
    stop=[' Human:', ' AI:']
    )
    print(response)
    if response.choices:
        bot_response = response.choices[0].message.content 
    else:
        bot_response = "No response from the model."
    
    # if bot_response:
    #     pos = bot_response.find("\ncontent: ")
    #     bot_response = bot_response[pos + 8:]
    # else:
    #     bot_response = "Something went wrong..."
    print(f'요약: {bot_response}')
    summary_path = os.path.join(settings.MEDIA_ROOT, 'summary.txt')
    with open(summary_path, 'a', encoding='utf-8') as f:
            f.write(bot_response)
            
    return Response({'message': '대화가 요약 완료.'})

@api_view(['POST'])
def chatbot(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        print(text)
        
        # audio_chunks = []
        # for i in range(len(request.FILES)):
        #     audio_chunk = request.FILES.get(f'audio_chunk_{i}')
        #     if audio_chunk:
        #         audio_chunks.append(audio_chunk.read())
        # print(audio_chunks)
        
        audio = request.FILES.get('audio')
        print(audio)
        
        # Check if previous audio and text files exist
        audio_path = os.path.join(settings.MEDIA_ROOT, 'input.webm')
        input_audio_path = os.path.join(settings.MEDIA_ROOT, 'input.wav')
        text_path = os.path.join(settings.MEDIA_ROOT, 'text.txt')
        # output_audio_path = os.path.join(settings.MEDIA_ROOT, 'output.wav')
        
        
        if not os.path.exists(audio_path):
            open(audio_path, 'wb').close()
        if not os.path.exists(text_path):
            open(text_path, 'w', encoding='utf-8').close()

        # clip = moviepy.VideoFileClip(audio)
        # clip.audio.write_audiofile(audio_path)


        # Append new audio data
        with open(audio_path, 'ab') as f:
            for chunk in audio.chunks():
                f.write(chunk)
        
        # with tempfile.NamedTemporaryFile(delete=False) as tmp_wav:
        #     for chunk in audio.chunks():
        #         tmp_wav.write(chunk)
        
        # if audio:
        #     with open(audio_path, 'ab') as f:
        #         for chunk in audio.chunks():
        #             f.write(chunk)
        
        # opus_data = BytesIO(audio)
        # sound = AudioSegment.from_file(opus_data, codec="webm")
        
        
        # rate = 44100
        # input_audio, _ = librosa.load(sound, sr=rate)
        # scipy.io.wavfile.write(audio_path, rate, input_audio.astype(np.int16))
        # # os.unlink(tmp_wav.name)
        
        # # 오디오 데이터를 BytesIO 객체로 변환
        # audio_bytes = io.BytesIO(audio.read())

        # # BytesIO 객체를 파일로 저장
        # with open(audio_path, 'wb') as f:
        #     f.write(audio_bytes.read())

        # # AudioSegment로 변환
        sound = AudioSegment.from_file(audio_path, format="webm")
        
        # # AudioSegment를 numpy 배열로 변환
        # audio_np = np.array(sound.get_array_of_samples())
        
        # # 오디오 샘플링 주파수가 44100이 아닌 경우 재샘플링
        if sound.frame_rate != 44100:
            sound = sound.set_frame_rate(44100)
        #     audio_np = np.array(sound.get_array_of_samples())
        sound.export(input_audio_path, format="wav")
        # # numpy 배열을 WAV 파일로 저장
        # rate = 44100
        # scipy.io.wavfile.write(audio_path, rate, audio_np.astype(np.int16))
        
        
        # Append new text data
        with open(text_path, 'a', encoding='utf-8') as f:
            f.write(text + '\n')
            
        user_input = text
        prompt = create_prompt(user_input, prompt_list)
        response = client.chat.completions.create(
        model="gpt-4",
        messages = [
        {
            "role": "assistant",
            "content": prompt
        },
        ],
        max_tokens=10,
        temperature=0.8,
        stop=[' Human:', ' AI:']
        )
        
        
        print(response)
        # if isinstance(response, str):
        #     json_data = json.loads(response)
        # else:
        #     json_data = response.json()

        # choices = json_data.get('choices', [])
        # if choices:
        #     reply = choices[0].get('message', {}).get('content', '')
        # else:
        #     reply = "No response from the model."
        
        if response.choices:
        # 선택지가 존재하는 경우 처리
            bot_response = response.choices[0].message.content  # 첫 번째 선택지의 내용을 reply에 할당
        else:
        # 선택지가 존재하지 않는 경우 처리
            bot_response = "No response from the model."
        
        # if response.status_code == 200:
            # reply = response.json()['choices'][0]['text']
        # else:
            # reply = "Error processing the request."
        
        # bot_response = response.choices[0].message.content
        # if bot_response:
        #     update_list(bot_response, prompt_list)
        #     pos = bot_response.find("\nAssistant: ")
        #     bot_response = bot_response[pos + 11:]
        # else:
        #     bot_response = "Something went wrong..."
        print(f'AI: {bot_response}')

        # # Call OpenAI API
        # headers = {
        #     'Content-Type': 'application/json',
        #     'Authorization': 'Bearer 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',
        # }
        # data = {
        #     'prompt': text,
        #     'max_tokens': 100,
        #     'temperature': 0.7,
        # }
        # response = requests.post('https://api.openai.com/v1/completions', json=data, headers=headers)
        # if response.status_code == 200:
        #     reply = response.json()['choices'][0]['text']
        # else:
        #     reply = "Error processing the request."


        # Combine text and audio
        # combined_text = f"User: {text}\nChatbot: {reply}"
        
        tts(bot_response)

        # Write combined data to files
        # with open(combined_audio_path, 'wb') as combined_file:
        #     combined_file.write(f"{combined_text}\n".encode())
        #     # Append audio data from previous file
        #     with open(audio_path, 'rb') as audio_file:
        #         combined_file.write(audio_file.read())
        # print(output_audio_path)
        # audio_url = request.build_absolute_uri(output_audio_path)

        # output_audio_url = os.path.join(settings.MEDIA_URL, 'output.wav')
        
        # with open('media/output.wav', "rb") as f:
        #     response = FileResponse(f)
        #     response.set_headers(f)
        
        f = open('media/output.wav', "rb")
        response = FileResponse(f)
        response.set_headers(f)
        # output_audio_url = os.path.join(settings.MEDIA_URL, 'news.wav')
        # print(output_audio_url)
        # Return response 'output_audio_path': output_audio_path, 
        # return JsonResponse({'output_audio_url': output_audio_url})
        return response
    else:
        return JsonResponse({'error': 'POST request required'})