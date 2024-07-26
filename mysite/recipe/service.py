from recipe.utils import cal_vector
from recipe.models import Recipe
import chromadb
import numpy as np

client = chromadb.PersistentClient(path="./chroma")
collection = client.get_collection(name="test")
collection.query(query_embeddings=np.zeros((1, 1536)) ,n_results=1)

def get_recipe_recommands(ingre, weight, count):
    recipe_vector = cal_vector(ingre, weight)
    result=collection.query(
        query_embeddings=recipe_vector,
        n_results=count,
    )
    ids = [int(i)+1 for i in result['ids'][0]]
    recipes = Recipe.objects.filter(pk__in=ids).prefetch_related('preprocessed_ingredients')

    return recipes

# python manage.py dbshell
# EXPLAIN QUERY PLAN SELECT * FROM ingredient WHERE id IN (SELECT ingredient_id FROM recipe_ingredient_set WHERE recipe_id = 1);
# QUERY PLAN
# |--SEARCH ingredient USING INTEGER PRIMARY KEY (rowid=?)
# `--LIST SUBQUERY 1
#    `--SEARCH recipe_ingredient_set USING INDEX recipe_ingredient_set_recipe_id_0ddb9c0a (recipe_id=?)