import factory
import random
from user.models import CustomUser, Likes
from recipe.models import Recipe, RecipeIngredientRelation, Ingredient

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        
    id = factory.Sequence(lambda n: n + 1)  # create_batch나 create 시 충돌 방지
    username = factory.Sequence(lambda n: 'fake name{0}'.format(n))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    date_of_birth = factory.Faker("date_of_birth")
    phone =  factory.LazyAttribute(lambda x: f"+8210{random.randint(1000, 9999)}{random.randint(1000, 9999)}")

    @factory.post_generation
    def like(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for recipe in extracted:
                self.like.add(recipe)

    @factory.post_generation
    def hash_password(self, create, extracted, **kwargs):
        # 패스워드를 해시 처리
        self.set_password(self.password)
        
    #post_generation 실행 후 변경사항 저장
    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if create and results:
            instance.save()



