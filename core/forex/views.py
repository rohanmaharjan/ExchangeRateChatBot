from django.shortcuts import render
from django.http import JsonResponse
from forex.services import chatbot_response

def chat(request):
    user_input = request.GET.get("q", "")  # ?q=USD rate

    if not user_input:
        return JsonResponse({"error": "Please provide query using ?q="})

    response = chatbot_response(user_input)

    return JsonResponse({
        "input": user_input,
        "response": response
    })