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
from django.http import FileResponse
from django.contrib.staticfiles.storage import staticfiles_storage


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
@api_view(['POST'])
def chatbot(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        print(text)
        # audio = request.FILES.get('audio')

        # Check if previous audio and text files exist
        # audio_path = os.path.join(settings.MEDIA_ROOT, 'audio.mp3')
        text_path = os.path.join(settings.MEDIA_ROOT, 'text.txt')
        output_audio_path = os.path.join(settings.MEDIA_ROOT, 'output.wav')
        
        
        # if not os.path.exists(audio_path):
        #     open(audio_path, 'wb').close()
        if not os.path.exists(text_path):
            open(text_path, 'w').close()

        # Append new audio data
        # if audio:
        #     with open(audio_path, 'ab') as f:
        #         for chunk in audio.chunks():
        #             f.write(chunk)

        # Append new text data
        with open(text_path, 'a') as f:
            f.write(text + '\n')
            
        user_input = text
        prompt = create_prompt(user_input, prompt_list)
        response = client.chat.completions.create(
        model="gpt-4",
        messages = [
        {
            "role": "system",
            "content": prompt
        },
        ],
        max_tokens=50,
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
        if bot_response:
            update_list(bot_response, prompt_list)
            pos = bot_response.find("\nAI: ")
            bot_response = bot_response[pos + 4:]
        else:
            bot_response = "Something went wrong..."
        print(f'AI {bot_response}')

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
        print(output_audio_path)
        # audio_url = request.build_absolute_uri(output_audio_path)
        output_audio_url = os.path.join(settings.MEDIA_URL, 'output.wav')
        print(output_audio_url)
        # Return response 'output_audio_path': output_audio_path, 
        return JsonResponse({'reply': bot_response, 'output_audio_url': output_audio_url})
    else:
        return JsonResponse({'error': 'POST request required'})