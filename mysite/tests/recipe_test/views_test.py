import pytest
from rest_framework.test import APIClient
from tests.recipe_test.factories import RecipeFactory, IngredientFactory
from django.urls import reverse
from recipe.serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientRelationSerializer
from user.serializers import CustomUserRequestSchema
import json

@pytest.mark.django_db()
class TestRecipeView:
    client = APIClient()
    end_point = "/recipes/"
    
    def test_recipe_get(self, basic_recipes):
        instances = basic_recipes
        url = reverse("recipe-list")
        response = self.client.get(path=url, content_type="application/json")
        n = len(instances)

        assert response.status_code == 200
        for i in range(n):
            assert response.data[i]['id'] == instances[i].id
        
    def test_recipe_detail(self, basic_recipe): # 같은 팩토리라도 서로 다른 함수에서 실행되면 다시 생성됨.
        instance = basic_recipe
        url = reverse("recipe-detail", kwargs={"pk":instance.id})
        response = self.client.get(path=url, content_type="application/json")
        
        assert response.status_code == 200
        assert response.data['id'] == instance.id
        assert response.data['recipe_name'] == instance.recipe_name

    def test_recipe_create(self, basic_recipe_build):
        instance = basic_recipe_build
        url = self.end_point
        serializer = RecipeSerializer(instance=instance)
        json_data = json.dumps(serializer.data)
        response = self.client.post(path=url, data=json_data, content_type="application/json")
        
        assert response.status_code == 201
        assert response.data["id"] == instance.id
        assert response.data["recipe_name"] == instance.recipe_name
        
    def test_recipe_upadte(self, basic_recipe):
        instance = basic_recipe
        url = reverse("recipe-detail", kwargs={"pk":instance.id})
        instance.recipe_name = "recipeeee123"

        serializer = RecipeSerializer(instance=instance)
        json_data = json.dumps(serializer.data)
        response = self.client.put(path=url, data=json_data, content_type="application/json")
        assert response.status_code == 200
        assert response.data['recipe_name'] == instance.recipe_name

    def test_recipe_delete(self, recipe_ingregient_relation):
        recipe_instance, ingredient_instances = recipe_ingregient_relation
        url = reverse("recipe-detail", kwargs={"pk":recipe_instance.id})
        response = self.client.delete(path=url, content_type="application/json")
        
        assert response.status_code == 204
        assert response.data['ingredients'] == len(ingredient_instances)
        assert response.data['recipe'] == 1

    def test_recipe_ingredients_upadte(self, recipe_ingregient_relation):
        recipe_instance, ingredient_instances = recipe_ingregient_relation
        url = reverse("recipe-detail", kwargs={"pk":recipe_instance.id})
        
        recipe_instance.preprocessed_ingredients.remove(ingredient_instances[0]) # => ManytoMany부분 수정
        
        serializer = RecipeSerializer(instance=recipe_instance)
        json_data = json.dumps(serializer.data)
        response = self.client.put(path=url, data=json_data, content_type="application/json")
        
        assert response.status_code == 200
        assert response.data['preprocessed_ingredients'] == recipe_instance.preprocessed_ingredients.count()

@pytest.mark.django_db()
class TestIngredientView:
    client = APIClient()
    end_point = "/ingredients/"
    
    def test_ingredient_get(self, basic_ingredients):
        instances = basic_ingredients
        url = reverse("ingredient-list")
        response = self.client.get(path=url, content_type="application/json")
        n = len(instances)

        assert response.status_code == 200
        for i in range(n):
            assert response.data[i]['id'] == instances[i].id
        
    def test_ingredient_detail(self, basic_ingredient): # 같은 팩토리라도 서로 다른 함수에서 실행되면 다시 생성됨.
        instance = basic_ingredient
        url = reverse("ingredient-detail", kwargs={"pk":instance.id})
        response = self.client.get(path=url, content_type="application/json")
        
        assert response.status_code == 200
        assert response.data['id'] == instance.id
        assert response.data['ingredient'] == instance.ingredient

    def test_ingredient_create(self, basic_ingredient_build):
        instance = basic_ingredient_build
        url = self.end_point
        serializer = IngredientSerializer(instance=instance)
        json_data = json.dumps(serializer.data)
        response = self.client.post(path=url, data=json_data, content_type="application/json")

        assert response.status_code == 201
        assert response.data["id"] == instance.id
        assert response.data["ingredient"] == instance.ingredient

    def test_ingredient_delete(self, basic_ingredient):
        instance = basic_ingredient
        url = reverse("ingredient-detail", kwargs={"pk":instance.id})
        response = self.client.delete(path=url, content_type="application/json")
        
        assert response.status_code == 204