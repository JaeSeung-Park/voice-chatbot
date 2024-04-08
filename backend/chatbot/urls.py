# from .views import chatbot_controller
from django.urls import path
from . import views

urlpatterns = [
    # todo routes
    # path('talk/', chatbot_controller, name='chatbot-talk'),
    path('chatbot/', views.chatbot, name='chatbot-talk'),
]