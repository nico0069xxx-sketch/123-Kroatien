from django.urls import path
from main import chatbot_views

urlpatterns = [
    path('chatbot/', chatbot_views.chatbot_api, name='chatbot_api'),
    path('test/', chatbot_views.chatbot_test, name='chatbot_test'),
]
