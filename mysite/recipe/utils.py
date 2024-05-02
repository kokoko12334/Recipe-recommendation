import numpy as np
import pickle
import pandas as pd

df_ingre = pd.read_csv("data/ingre_v2.csv", index_col=False)
df = pd.read_csv("data/recipe_v5.csv")
with open('data/ingre_vector.pk', 'rb') as f:
    vector = pickle.load(f)

def cal_weight(ingre):
    arr = np.array([])
    for i in ingre:
        r = df_ingre.loc[df_ingre['ingre'] == i,'tfidf'].iloc[0]
        arr = np.append(arr, r)    
    mean = arr.mean()
    arr = arr * mean
    
    return arr

def cal_vector(ingre, portion):
    n = len(ingre)
    matrix = np.zeros((n,3072))
    for i in range(n):
        v = vector[ingre[i]] * portion[i]
        matrix[i] = v
    
    recipe_vector = matrix.sum(axis=0)/n

    return recipe_vector

def get_detailed_recipe(ids):
    recipe = []
    for id in ids:
        recipe.append(df.iloc[int(id)].to_dict())

    return recipe