from django.urls import path
from main import chatbot_views
from main.views import send_professional_inquiry

urlpatterns = [
    path('chatbot/', chatbot_views.chatbot_api, name='chatbot_api'),
    path('test/', chatbot_views.chatbot_test, name='chatbot_test'),
    path('professional-inquiry/', send_professional_inquiry, name='professional_inquiry'),
]
