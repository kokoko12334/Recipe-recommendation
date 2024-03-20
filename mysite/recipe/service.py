
from django.db import transaction
from recipe.models import Recipe, Ingredient, RecipeIngredientRelation
from recipe.serializers import RecipeSerializer
from typing import List
class RecipeAppService():

    
    @transaction.atomic
    @staticmethod
    def recipe_create_with_ingredients(recipe: RecipeSerializer, ingredients: List[str]):

        if recipe.is_valid():
            instance = recipe.save()
            # print(Recipe.objects.get(id=103))
            # print(Ingredient.objects.get(id=1))
            # bulk_list = [[instance, Ingredient.objects.get(ingredient=i)] for i in ingredients]
            # RecipeIngredientRelation.objects.bulk_create(bulk_list)
            
            return instance

        
