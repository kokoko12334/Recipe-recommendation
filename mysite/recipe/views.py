from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from recipe.models import Recipe, Ingredient, RecipeIngredientRelation
from recipe.serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientRelationSerializer
from recipe.service import get_recipe_recommands
from django.shortcuts import render
import json
import pandas as pd
from django.http import JsonResponse
import time

df = pd.read_csv("data/ingre_v2.csv", index_col=False)
ingre_data = df['ingre'].to_list()
# import json


# a = {'ingre_data':ingre_data}

# with open("ingres.json", "w", encoding='utf-8') as f:
#     json.dump(a, f)

def recipe_page(request):
    global ingre_data
    # if 'access_allowed' not in request.session:
    #     return redirect('/')
      
    return render(request, 'recipe_page.html',{'ingre_data': json.dumps(ingre_data)})

class RecipePagination(PageNumberPagination): # PageNumberPagination 상속
    page_size = 20

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination

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
        if serializer.is_valid():
            serializer.save()

        return Response(status=201, data=serializer.data)
    
    def update(self, request, pk=None): #put
        serializer = RecipeSerializer(data=request.data, partial=False)
        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
            result_serializer = RecipeSerializer(instance=result) #serializer는 읽기전용, 수정불가능
            data = dict(result_serializer.data)
            n = len(RecipeIngredientRelation.objects.filter(recipe_id=request.data['id']))
            data['preprocessed_ingredients'] = n
            
        return Response(data=data)

    def destroy(self, request,pk=None):
        queryset = Recipe.objects.get(pk=pk)
        result = queryset.delete()
        data = {"ingredients": result[1]['recipe.RecipeIngredientRelation'], "recipe":result[1]['recipe.Recipe']}
        
        return Response(status=204, data=data)
    
    @action(detail=False, methods=['POST'])
    def recipe_rec(self, request):
        try:
            parsed_data = json.loads(request.body)  # JSON 데이터 파싱
            print(request)
            print(parsed_data)
            ingre = []
            weight = []
            for data in parsed_data:
                ingre.append(data['values'])
                weight.append(data['range'])

            recommand_cnt = 60
            recipes_queryset = get_recipe_recommands(ingre=ingre, weight=weight, count=recommand_cnt)
            serializer = RecipeSerializer(recipes_queryset, many=True)
            return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class RecipeIngredientRelationViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredientRelation.objects.all()
    serializer_class = RecipeIngredientRelationSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
