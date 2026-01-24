from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from .chatbot import get_chatbot_response, is_professional_search, KI_MATCHING_AVAILABLE
if KI_MATCHING_AVAILABLE:
    from .ki_matching import get_professional_matches

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "")
            language = request.session.get("site_language", "ge")
            
            # Prüfen ob es eine Professional-Suche ist
            professionals = []
            if KI_MATCHING_AVAILABLE and is_professional_search(message):
                result = get_professional_matches(message, language)
                if result.get('success') and result.get('professionals'):
                    professionals = result['professionals'][:3]
            
            response = get_chatbot_response(message, language)
            return JsonResponse({
                "response": response,
                "professionals": professionals
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "POST required"}, status=400)

def chatbot_test(request):
    return render(request, "chatbot_test.html")
