import pytest
from django.conf import settings
from tests.user_test.factories import UserFactory
from tests.recipe_test.factories import RecipeFactory, IngredientFactory
from faker import Faker
# 실제 db에 접근 시 데이터 다사라짐
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
    ingredients_instances = IngredientFactory.create_batch(5)
    recipe_instances = RecipeFactory.create_batch(5,preprocessed_ingredients=ingredients_instances)
    instances = UserFactory.create_batch(10, like=recipe_instances)   
    return instances

@pytest.fixture()
def basic_user():
    ingredients_instances = IngredientFactory.create_batch(5)
    recipe_instances = RecipeFactory.create_batch(5,preprocessed_ingredients=ingredients_instances)
    instance = UserFactory.create(like=recipe_instances)
    return instance

@pytest.fixture
def basic_user_build():    
    instance = UserFactory.build() 
    return instance

@pytest.fixture
def basic_user_with_raw_password():
    raw_password = Faker().password()  # 평문 패스워드 생성
    # UserFactory 호출 시 password 인자에 평문 패스워드를 전달
    user_instance = UserFactory.create(password=raw_password)
    # 생성된 객체에 평문 패스워드를 별도로 저장하지 않고, 필요한 경우 반환
    return user_instance, raw_password

@pytest.fixture
def like_create_testcase():
    ingredients_instances = IngredientFactory.create_batch(5)
    recipe_instance = RecipeFactory.create(preprocessed_ingredients=ingredients_instances)
    user_instance = UserFactory.create()
    return recipe_instance, user_instance

@pytest.fixture
def like_delete_testcase():
    ingredients_instances = IngredientFactory.create_batch(5)
    recipe_instance = RecipeFactory.create(preprocessed_ingredients=ingredients_instances)
    user_instance = UserFactory.create(like=[recipe_instance])
    return recipe_instance, user_instance

