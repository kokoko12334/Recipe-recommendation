import factory
from user.models import CustomUser

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        
    id = 1
    username = factory.Faker("first_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    date_of_birth = factory.Faker("date_of_birth")
    phone = "+821012341234"

