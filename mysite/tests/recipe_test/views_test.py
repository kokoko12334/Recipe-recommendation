import pytest
from rest_framework.test import APIClient
from tests.recipe_test.factories import RecipeFactory, IngredientFactory
from django.urls import reverse
from user.serializers import CustomUserRequestSchema
import json

@pytest.mark.django_db()
class TestRecipeView:
    client = APIClient()
    end_point = "/recipes/"
    
    def test_recipe_get(self, basic_recipes):
        recipe_instances = basic_recipes
        url = reverse("recipe-list")
        response = self.client.get(path=url, content_type="application/json")
        n = len(recipe_instances)

        assert response.status_code == 200
        for i in range(n):
            assert response.data[i]['id'] == recipe_instances[i].id
        
    # def test_user_detail(self, basic_user): # 같은 팩토리라도 서로 다른 함수에서 실행되면 다시 생성됨.
    #     user_instance = basic_user
    #     url = reverse("user-detail", kwargs={"pk":user_instance.id})
    #     response = self.client.get(path=url, content_type="application/json")
        
    #     assert response.status_code == 200
    #     assert response.data['id'] == user_instance.id
    #     assert response.data['username'] == user_instance.username

    # def test_user_create(self, basic_user_build):
    #     user_instance = basic_user_build
    #     url = self.end_point
    #     serializer = CustomUserRequestSchema(instance=user_instance)
    #     json_data = json.dumps(serializer.data)
    #     response = self.client.post(path=url, data=json_data, content_type="application/json")

    #     assert response.status_code == 201
    #     assert response.data["id"] == user_instance.id
    #     assert response.data["username"] == user_instance.username
        
    # def test_user_upadte(self, basic_user):
    #     user_instance = basic_user
    #     url = reverse("user-detail", kwargs={"pk":user_instance.id})
    #     user_instance.username = "faker name123123132131"
    #     serializer = CustomUserRequestSchema(instance=user_instance)
    #     json_data = json.dumps(serializer.data)
    #     response = self.client.patch(path=url, data=json_data, content_type="application/json")
        
    #     assert response.status_code == 200
    #     assert response.data['id'] == user_instance.id
    #     assert response.data['username'] == user_instance.username

    # def test_user_delete(self, basic_user):
    #     user_instance = basic_user
    #     url = reverse("user-detail", kwargs={"pk":user_instance.id})
    #     response = self.client.delete(path=url,  content_type="application/json")
        
    #     assert response.status_code == 204