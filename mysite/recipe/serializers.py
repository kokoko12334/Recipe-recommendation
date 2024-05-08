from rest_framework import serializers
from recipe.models import Recipe, Ingredient, RecipeIngredientRelation

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"
        depth = 1

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