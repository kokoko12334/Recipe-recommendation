import factory
import random
from user.models import CustomUser, Likes
from recipe.models import Recipe, RecipeIngredientRelation, Ingredient

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        
    id = factory.Sequence(lambda n: n + 1)  # create_batch나 create 시 충돌 방지
    username = factory.Sequence(lambda n: 'fake name{0}'.format(n)) #=> unique는 이런식으로 유니크값 보장하기
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    date_of_birth = factory.Faker("date_of_birth")
    phone =  factory.LazyAttribute(lambda x: f"+8210{random.randint(1000, 9999)}{random.randint(1000, 9999)}")

class LikesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

