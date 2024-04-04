from ast import Global
from django.shortcuts import render
from rest_framework.decorators import api_view
from .chatbotService.chartBotService import get_bot_response, tts, audio_play, record_voice, speech_recognition
from rest_framework.response import Response

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

@api_view(['POST'])
def chatbot_controller(request):
        # print(request.data, 'request.data::')
        global prompt_list
        # global name, age, interest, diasease
        f = open("chatbot\conversation.html", 'w')
        f.close()
        while True:
            try:
                # user_input = request.data['prompt']
                user_input = speech_recognition()
                # if(user_input == 'exit'):
                #     prompt_list = [
                #         '너는 혼자계신 시니어분의 말동무 역할을 수행하게 될거야. 사용자의 정보를 알려줄게',
                #         f'시니어 분의 성별은 {sex}이고 나이는 {age}세 이시며 관심사로는 {interest}등이 있고 {diasease}와 같은 질병을 앓고 계셔',
                #         '위 정보를 참고해서 이 분이 심심하지 않으시게 일상생활의 간단한 질문이나 대답을 해주면 되',
                #         '너무 자세하게 질문과 대답을 하기보단 호응해주고 맞춰주는 식으로 대화를 해줘',
                #         '무조건 존댓말로 대답해줘',
                #     ]
                response = get_bot_response(user_input, prompt_list)
                tts(response)
                # audio_play()
                print(f'AI {response}')
                # return Response(response, status=200)
            except Exception as e:
                print('err:', e)
                # return Response('error', status=500)
            