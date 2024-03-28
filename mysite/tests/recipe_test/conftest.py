import pytest
from tests.recipe_test.factories import RecipeFactory, IngredientFactory

@pytest.fixture() 
def basic_recipes():    
    recipe_instances = RecipeFactory.create_batch(10)
    ingredient_instances = IngredientFactory(recipes=recipe_instances)
    return recipe_instances

@pytest.fixture()
def basic_recipe():
    instance = RecipeFactory.create()
    return instance

@pytest.fixture
def basic_recipe_build():    
    instance = RecipeFactory.build() 
    return instance

@pytest.fixture() 
def basic_ingredients():    
    instances = IngredientFactory.create_batch(10)   
    return instances

@pytest.fixture()
def basic_ingredient():
    instance = IngredientFactory.create()
    return instance

@pytest.fixture
def basic_ingredient_build():    
    instance = IngredientFactory.build() 
    return instance