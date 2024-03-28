import pytest
from django.conf import settings
from tests.user_test.factories import UserFactory
# 실제 db에 접근 시
# @pytest.fixture(scope='session')
# def django_db_setup():
#     settings.DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.mysql',
#         "NAME": "drf_test1",
#         "USER":"root",
#         "PASSWORD":"7292",
#         "HOST":"localhost",
#         "PORT":"3306",
#         'ATOMIC_REQUESTS': True,
#     }

# @pytest.fixture
# def basic_user():
#     isinstance = UserFactory.create() # build: 데이터베이스에 영속(저장), create():데이터베이스에 저장, 아무것도 없으면 자동으로 됨
#     # instance = UserFactory()# 자동 create()
#     return isinstance
# 주의사항: 실행할때 마다(즉 함수에서 파라미터로 쓸 때마다 각 각 10개씩 생성, 같은 10개를 쓰는 것이 아님)

@pytest.fixture(scope="function") # scope ="session"=> 하나의 테스트에만 적용 하지만 db접근하려면 무조건 함수단위로 session을 해야한다 함.
def basic_users():    
    instances = UserFactory.create_batch(10)   
    return instances

@pytest.fixture()
def basic_user():
    instance = UserFactory.create()
    return instance

@pytest.fixture
def basic_user_build():    
    instance = UserFactory.build() 
    return instance
