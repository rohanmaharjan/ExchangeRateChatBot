# Output as JSON response
'''
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
'''

# Output in Django restframework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import chatbot_response


class ChatBotAPIView(APIView):

    def post(self, request):
        message = request.data.get("message", "")

        if not message:
            return Response(
                {"error": "Message is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = chatbot_response(message)

        return Response({
            "message": message,
            "response": response
        })