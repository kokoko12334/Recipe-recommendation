# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# django.setup()
# import pandas as pd
# from recipe.models import Recipe, Ingredient, RecipeIngredientRelation
# from tqdm import tqdm

# recipe_df = pd.read_csv("data/recipe_v11.csv", index_col=False)
# ingre_df = pd.read_csv("data/ingre_v2.csv", index_col=False)


# ingre_set = set()

# for i in tqdm(range(len(recipe_df))):
#     ingres = eval(recipe_df.iloc[i]['ingre'])
#     for ingre in ingres:
#         ingre_set.add(ingre)

# print(len(ingre_set))


# ingre_list = list(ingre_set)
# ingre_n = len(ingre_list)
# ingre_lst = []
# for i in range(ingre_n):
#     obj = Ingredient(ingredient=ingre_list[i])
#     ingre_lst.append(obj)

# Ingredient.objects.bulk_create(ingre_lst)


# recipe_list = []
# recipe_n = len(recipe_df)
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

# objs = Ingredient.objects.all()
# dic = dict()

# for i in objs:
#     dic[i.ingredient] = i.pk
    
# fk_list = []
# # len(recipe_df)
# for i in tqdm(range(len(recipe_df))):
#     ingres = eval(recipe_df.iloc[i]['ingre'])
#     recipe_obj = Recipe.objects.get(id=i+1)
    
#     for j in range(len(ingres)):
#         ingre = ingres[j]
#         ingre_obj = Ingredient.objects.get(id=dic[ingre])
        
#         relation = RecipeIngredientRelation(recipe=recipe_obj, ingredient=ingre_obj)
        
#         fk_list.append(relation)
# print(len(fk_list))

# RecipeIngredientRelation.objects.bulk_create(fk_list)


# RecipeIngredientRelation.objects.all().delete()