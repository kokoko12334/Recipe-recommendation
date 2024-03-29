from django.shortcuts import render
from rest_framework import viewsets
from user.serializers import CustomUserSchema, CustomUserDetailSchema, CustomUserRequestSchema, LikesSerializer
from user.models import CustomUser, Likes
from recipe.serializers import RecipeSerializer
from rest_framework.response import Response
from recipe.models import Recipe
import time
import json
from rest_framework.decorators import api_view, action
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
        "destroy": CustomUserRequestSchema,
    }
    
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)        

    @action(detail=True, methods=['POST', 'DELETE'], url_path='like') # 같은url에 메소드만 다르면 이렇게도 가능 근데 이렇게 않하면 now allowed 에러남.
    def like_create(self, request, **kwargs):
        user_id = kwargs.get('pk')
        user_instance = CustomUser.objects.get(id=user_id)
        recipe_instance = Recipe.objects.get(id=request.data['recipe_id'])
        
        if request.method == 'POST':
            user_instance.like.add(recipe_instance)
        elif request.method == 'DELETE':
            user_instance.like.remove(recipe_instance)

        user_instance.save()

        data = {"recipe_id":recipe_instance.id}
        json_data = json.dumps(data)
        
        if self.request.method == 'POST':
            return Response(status=201, data=json_data, content_type="application/json")
        elif self.request.method == 'DELETE':
            return Response(status=204, data=json_data, content_type="application/json")


    # 이와 같이 detail=False로 두고 pk를 파라미터로 지정안하는 방식으로도 가능하기는 함. 만약에 함수를 post, delete 두개로 정의하려면
    # @action(detail=False, methods=['DELETE'], url_path='like') # delete는 detail False로 해야함
    # def like_delete(self, request, *kwargs):
    #     user_instance = CustomUser.objects.get(id=request.data['user_id'])
    #     recipe_instance = Recipe.objects.get(id=request.data['recipe_id'])
    #     user_instance.like.remove(recipe_instance)
    #     user_instance.save()

    #     data = {"recipe_id":recipe_instance.id}
    #     json_data = json.dumps(data)

    #     return Response(status=204, data=json_data, content_type="application/json")

# class LikesViewSet(viewsets.ModelViewSet):
#     queryset = Likes.objects.all()
    
#     serializer_class = LikesSerializer

