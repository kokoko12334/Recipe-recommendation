from rest_framework import serializers
from recipe.models import Recipe, Ingredient, RecipeIngredientRelation
from django.db import transaction
from typing import Any
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"
        

    # @transaction.atomic
    # def create(self, validated_data: dict[str, Any]) -> Recipe:
    #     print(f"data:{validated_data}, type:{type(validated_data)}")
    #     ingredients = validated_data["preprocessed_ingredients"]
    #     validated_data.pop("preprocessed_ingredients", None)
    #     recipe = Recipe()
    #     for k,v in validated_data.items():
    #         setattr(recipe,k,v)
    #     recipe_done: Recipe = Recipe.objects.create(recipe)
        
    #     bulk_list = [[recipe_done, Ingredient.objects.get(ingredient=i)] for i in ingredients]
    #     RecipeIngredientRelation.objects.bulk_create(bulk_list)
        
    #     return recipe_done

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"

class RecipeIngredientRelationSerializer(serializers.ModelSerializer):

    recipe = RecipeSerializer()
    Ingredient = Ingredient()   #n인경우에

    class Meta:
        model = RecipeIngredientRelation
        fields = "__all__"