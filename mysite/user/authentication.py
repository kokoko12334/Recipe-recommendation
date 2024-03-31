from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(email=email)
            
            if user.check_password(password):
                
                return user
        except UserModel.DoesNotExist:
            # 사용자가 존재하지 않는 경우
            print("nononono")
            return None
        except MultipleObjectsReturned:
            # 이메일 주소가 중복되어 여러 사용자가 반환된 경우
            return UserModel.objects.filter(email=email).order_by('id').first()
        return None