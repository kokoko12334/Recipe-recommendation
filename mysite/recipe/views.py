from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.models import Recipe, Ingredient, RecipeIngredientRelation
from recipe.serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientRelationSerializer
from recipe.service import RecipeAppService

class RecipeViewSet(viewsets.ModelViewSet):
    
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

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

        # print(RecipeIngredientRelation.objects.all())
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

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class RecipeIngredientRelationViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredientRelation.objects.all()
    serializer_class = RecipeIngredientRelationSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
