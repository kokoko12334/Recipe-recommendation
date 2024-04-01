import pytest
from tests.recipe_test.factories import RecipeFactory, IngredientFactory


@pytest.fixture() 
def basic_recipes():
    ingredient_instances = IngredientFactory.create_batch(5)
    recipe_instances = RecipeFactory.create_batch(10, preprocessed_ingredients=ingredient_instances)
    
    return recipe_instances

@pytest.fixture()
def basic_recipe():
    ingredient_instances = IngredientFactory.create_batch(5)
    instance = RecipeFactory.create(preprocessed_ingredients=ingredient_instances)
    # relation테이블에도 자동으로 생성
    return instance

@pytest.fixture
def basic_recipe_build():
    instance = RecipeFactory.build() 
    return instance

@pytest.fixture() 
def basic_ingredients():    
    instances = IngredientFactory.create_batch(5)   
    return instances

@pytest.fixture()
def basic_ingredient():
    instance = IngredientFactory.create()
    return instance

@pytest.fixture
def basic_ingredient_build():    
    instance = IngredientFactory.build() 
    return instance

@pytest.fixture
def recipe_ingregient_relation():
    ingredients = IngredientFactory.create_batch(5)
    recipe_instance = RecipeFactory.create(preprocessed_ingredients=ingredients)  #

    return recipe_instance, ingredients
