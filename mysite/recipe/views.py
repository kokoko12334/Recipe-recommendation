
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.request import Request
from recipe.serializers import RecipeSerializer
from recipe.models import Recipe
from typing import Dict, Any, List
from rest_framework import viewsets
from recipe.models import Recipe, Ingredient, RecipeIngredientRelation
from recipe.serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientRelationSerializer
from django.db import transaction
from drf_spectacular.utils import extend_schema,OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.pagination import PageNumberPagination
from recipe.service import RecipeAppService
from rest_framework import filters
# Create your views here.


class RecipeViewSet(viewsets.ModelViewSet):
    
    queryset = Recipe.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    serializer_class = RecipeSerializer
    #,커스텀 엔드포인트 작성 함수이름이 자동으로 엔드포인트가 됨 detail=True면 id키 받고 아니면 전체리스트(list)
    # @action(detail=False, methods=["post"],url_path="create_with_prepared_ingredients/(?P<ingre>\d+)")  #커스텀action에 인자 넣고싶을때
    # 이때 d는 숫자형인듯
    # @extend_schema(summary="레시피 넣으면서 재료도 manytomany필드 넣기",parameters=[
    #     OpenApiParameter(
    #         name="recipe_name",
    #         type=OpenApiTypes.ANY,
    #         required=True
    #     ),
    # ]
    #     )
    # @action(detail=False, methods=["post"])  #커스텀action에 인자 넣고싶을때
    #page380에 create,list,retriece,update particail_update 내용이 있음.
    def list(self, request):
        queryset = Recipe.objects.all()
        serializer = RecipeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        book = Recipe.objects.get(pk=pk)
        serializer = RecipeSerializer(book)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = RecipeSerializer(data=request.data)
        print(Recipe.objects.all())
        print(Ingredient.objects.get(ingredient="사과"))
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    
    def update(self, request, pk=None):
        
        serializer = RecipeSerializer(data=request.data, partial=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        return Response(serializer.data)
    
    def partial_update(self, request,pk=None):
        
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    def destroy(self, request,pk=None):
        
        queryset = Recipe.objects.get(pk=pk)
        
        return Response(queryset.delete())
    
    @action(detail=False,methods=["post"])
    def custom_create(self, request, *args, **kwargs):
        
        
        recipe = RecipeSerializer(data=request.data)
        ingredients = request.data["preprocessed_ingredients"]
        
        result = RecipeAppService.recipe_create_with_ingredients(recipe=recipe, ingredients=ingredients) 
        # result = 0
        
        b = RecipeSerializer(instance=result)
        
        return Response(status=200, data=b.data, content_type="application/json")
        

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    
    serializer_class = IngredientSerializer


class RecipeIngredientRelationViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredientRelation.objects.all()

    serializer_class = RecipeIngredientRelationSerializer
