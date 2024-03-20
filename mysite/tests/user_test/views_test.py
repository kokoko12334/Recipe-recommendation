import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from tests.user_test.factories import UserFactory

from user.models import CustomUser
from user.serializers import CustomUserRequestSchema
import json

@pytest.fixture
def basic_user():
    instance = baker.make(CustomUser, id=1)
    return instance


@pytest.mark.django_db
class TestUserView:
    client = APIClient()
    end_point = "/users/"

    # def test_user_get(self):
    #     self.client.get()
    
    # def test_user_get_detail(self):
    #     self.client.get()
    
    def test_user_create(self):
        user_instance = UserFactory()
        user_serializer = CustomUserRequestSchema(instance=user_instance).data
        json_data = json.dumps(user_serializer)
        print(json_data)
        response = self.client.post(path=self.end_point, data=json_data,content_type="application/json")
        print(response.data)

        assert response.status_code == 200
        assert response.data["username"] == user_instance.username
        assert response.data["email"] == user_instance.email
        

    # def test_user_upadte(self):
    #     self.client.put()
    
    # def test_user_delete(self):
    #     self.client.delete()

    # def test_user_like(self):
    #     self.client.post()

    # def test_login(self):
    #     self.client.post()

    # def test_logout(self):
    #     self.client.post()
    



