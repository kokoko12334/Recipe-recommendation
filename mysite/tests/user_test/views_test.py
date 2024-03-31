import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from tests.user_test.factories import UserFactory
from django.urls import reverse
from user.models import CustomUser
from user.serializers import CustomUserRequestSchema
import json
from django.forms.models import model_to_dict
from user.models import CustomUser
from recipe.serializers import RecipeSerializer


"""
- `build` 전략은 데이터베이스에 저장되지 않는 실제 모델 인스턴스를 생성합니다. 이를 통해 모델의 메서드와 속성을 자유롭게 사용할 수 있지만, 데이터베이스에 영구적으로 저장되지는 않습니다.
- `stub` 전략은 모델의 구조를 가진 `StubObject`를 생성합니다. 이 객체는 데이터베이스 상호작용이나 모델 메서드 호출 없이 필드 값에 대한 접근만 가능합니다.
"""


@pytest.mark.django_db()
class TestUserView:
    client = APIClient()
    end_point = "/users/"
    
    def test_user_get(self, basic_users):
        user_instances = basic_users
        url = reverse("user-list")
        response = self.client.get(path=url, content_type="application/json")
        n = len(user_instances)

        assert response.status_code == 200
        for i in range(n):
            assert response.data[i]['id'] == user_instances[i].id
        
    def test_user_detail(self, basic_user): # 같은 팩토리라도 서로 다른 함수에서 실행되면 다시 생성됨.
        user_instance = basic_user
        url = reverse("user-detail", kwargs={"pk":user_instance.id})
        response = self.client.get(path=url, content_type="application/json")
        
        assert response.status_code == 200
        assert response.data['id'] == user_instance.id
        assert response.data['username'] == user_instance.username

    def test_user_create(self, basic_user_build):
        user_instance = basic_user_build
        url = self.end_point
        serializer = CustomUserRequestSchema(instance=user_instance)
        json_data = json.dumps(serializer.data)
        response = self.client.post(path=url, data=json_data, content_type="application/json")
        print(response.data)
        assert response.status_code == 201
        assert response.data["id"] == user_instance.id
        assert response.data["username"] == user_instance.username
        
    def test_user_upadte(self, basic_user):
        user_instance = basic_user
        url = reverse("user-detail", kwargs={"pk":user_instance.id})
        user_instance.username = "faker name123123132131"
        serializer = CustomUserRequestSchema(instance=user_instance)
        json_data = json.dumps(serializer.data)
        response = self.client.patch(path=url, data=json_data, content_type="application/json")
        # print(response.data)
        assert response.status_code == 200
        assert response.data['id'] == user_instance.id
        assert response.data['username'] == user_instance.username

    def test_user_delete(self, basic_user):
        user_instance = basic_user
        url = reverse("user-detail", kwargs={"pk":user_instance.id})
        response = self.client.delete(path=url,  content_type="application/json")
        
        assert response.status_code == 204
        
    def test_like_create(self, like_create_testcase):
        recipe_instance, user_instance = like_create_testcase
        url = reverse("user-like-create", kwargs={"pk": user_instance.id})
        data = {"recipe_id":recipe_instance.id}
        json_data = json.dumps(data)

        response = self.client.post(path=url, data=json_data, content_type = "application/json")
        response_data = json.loads(response.data)

        assert response.status_code == 201
        assert response_data['recipe_id'] == data['recipe_id']

    def test_like_delete(self, like_delete_testcase):
        recipe_instance, user_instance = like_delete_testcase
        url = reverse("user-like-create", kwargs={"pk": user_instance.id})
        data = {"recipe_id":recipe_instance.id}
        json_data = json.dumps(data)

        response = self.client.delete(path=url, data=json_data, content_type="application/json")
        response_data = json.loads(response.data)
        
        assert response.status_code == 204
        assert response_data['recipe_id'] == data['recipe_id']
     
    def test_login(self, basic_user_with_raw_password):
        user_instance, raw_password = basic_user_with_raw_password
        url = reverse('user-login')
        data = {
            'email': user_instance.email,
            'password': raw_password,
        }
  
        json_data = json.dumps(data,)
        response = self.client.post(path=url, data=json_data, content_type="application/json")
        # print(response.data)
        assert response.status_code == 200

        session_id = response.cookies.get('sessionid') # 없으면 None
        assert session_id != None


    # def test_logout(self, basic_user_with_raw_password):

    #     self.client.post()
    



