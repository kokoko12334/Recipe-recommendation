from django.shortcuts import render
from rest_framework import viewsets
from user.serializers import CustomUserSchema, CustomUserDetailSchema, CustomUserRequestSchema, LikesSerializer
from user.models import CustomUser, Likes
from rest_framework.response import Response
import time
import json
from rest_framework.decorators import api_view
from django.http import StreamingHttpResponse
def main_page(request):

    return render(request,'index.html')

@api_view(['GET',])
def test(request):
    print("request")
    # time.sleep(100)
    def stream():
        for i in range(1, 101):
            yield str(i) + '\n'  # 각 숫자를 개행 문자와 함께 스트리밍합니다.
            time.sleep(0.1)  # 각 데이터를 보내기 전에 잠시 대기합니다.

    response = StreamingHttpResponse(stream(), content_type='text/plain')
    return response

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSchema
    serializer_classes = {
        "list": CustomUserSchema,
        "retrive": CustomUserDetailSchema,
        "create": CustomUserRequestSchema,
        "update": CustomUserRequestSchema,
        "partial_update": CustomUserRequestSchema,
    }
    
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)        


class LikesViewSet(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    
    serializer_class = LikesSerializer

