import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
import pandas as pd
from recipe.models import Recipe, Ingredient, RecipeIngredientRelation
from tqdm import tqdm

recipe_df = pd.read_csv("data/recipe_v5.csv", index_col=False)
ingre_df = pd.read_csv("data/ingre_v2.csv", index_col=False)

# ingre_list = []
# ingre_n = len(ingre_df)

# for i in range(ingre_n):
#     obj = Ingredient(
#         ingredient=ingre_df.iloc[i]['ingre'],
#         tfidf_value=ingre_df.iloc[i]['tfidf'],
#     )
#     ingre_list.append(obj)



# recipe_list = []
recipe_n = len(recipe_df)
# for i in tqdm(range(recipe_n)):
#     obj = Recipe(
#         recipe_name=recipe_df.iloc[i]['name'],
#         url=recipe_df.iloc[i]['url'],
#         serving=recipe_df.iloc[i]['serving'],
#         cnt=0,
#         image_url=recipe_df.iloc[i]['image_url'],
#         )
#     recipe_list.append(obj)

# Recipe.objects.bulk_create(recipe_list)
# Ingredient.objects.bulk_create(ingre_list)


fk_list = []

for i in tqdm(range(recipe_n)):
    ingres = eval(recipe_df.iloc[i]['ingre'])
    recipe_obj = Recipe.objects.get(id=i+1)
    for j in range(len(ingres)):
        ingre = ingres[j]
        
        ingre_obj = Ingredient.objects.get(ingredient=ingre)
        
        recipe_obj.preprocessed_ingredients.add(ingre_obj)



# RecipeIngredientRelation.objects.bulk_update(fk_list,['recipe_id','ingredient_id'])
