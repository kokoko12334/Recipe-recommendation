import factory
from recipe.models import Recipe, RecipeIngredientRelation, Ingredient
from faker.providers import DynamicProvider
from faker import Faker
#https://medium.com/peter-kilczuk-software-engineer/factory-boy-post-generation-demystified-dc348c67e03c
# @post_generation은 외래키 관련
#The @post_generation decorator guarantees that the decorated method will run after the object has been built.


ingredient_provider = DynamicProvider(
    provider_name="ingredient",
    elements=["Apple","Banana","Blueberry", "Almond","Beaf"]
)
ran_nums_provider = DynamicProvider(
    provider_name="number",
    elements=list(range(1,11))
)

faker = Faker()
faker.add_provider(ingredient_provider)
faker.add_provider(ran_nums_provider)

class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe
        # skip_postgeneration_save = True # post generation 저장 안할거면

    id = factory.Sequence(lambda n: n + 1)
    recipe_name = factory.Sequence(lambda n: "recipe{0}".format(n))
    ingredients_with_quantity = factory.Sequence(lambda n: "ingredient_with_quantity{0}".format(n))
    url = faker.url()
    serving = faker.number()
    cnt = faker.number()
    cluster = faker.number()
    image_url = faker.url()
    tag = faker.number()
    
    @factory.post_generation
    def preprocessed_ingredients(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for ingredient in extracted:
                self.preprocessed_ingredients.add(ingredient)

    """Save again the instance if creating and at least one hook ran."""
    @classmethod 
    def _after_postgeneration(cls, instance, create, results=None):
        if create and results:
            instance.save()

class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    id = factory.Sequence(lambda n: n + 1) 
    ingredient = faker.ingredient()

class RecipeIngredientRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeIngredientRelation

    @factory.post_generation
    def recipe_id(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for ingredient in extracted:
                self.recipe_id.add(ingredient)

    @factory.post_generation
    def ingredient_id(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for ingredient in extracted:
                self.ingredient_id.add(ingredient)

    """Save again the instance if creating and at least one hook ran."""
    @classmethod 
    def _after_postgeneration(cls, instance, create, results=None):
        if create and results:
            instance.save()