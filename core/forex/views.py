from django.shortcuts import render
from django.http import JsonResponse
from forex.services import chatbot_response

def chat(request):
    msg = request.GET.get("msg", "")
    response = chatbot_response(msg)
    return JsonResponse({"response": response})