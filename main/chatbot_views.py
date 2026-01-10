from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from .chatbot import get_chatbot_response

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "")
            language = request.session.get("site_language", "ge")
            response = get_chatbot_response(message, language)
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "POST required"}, status=400)

def chatbot_test(request):
    return render(request, "chatbot_test.html")
