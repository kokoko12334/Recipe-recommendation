import numpy as np
import pickle
from sklearn.preprocessing import normalize

with open('data/ingre_vector2.pk', 'rb') as f:
    vector = pickle.load(f)

def cal_vector(ingre, weight):
    n = len(ingre)
    weight_sum = sum(weight)
    weight_adj = [round(w / weight_sum, 4) for w in weight]
    matrix = np.zeros((n,1536))
    for i in range(n):
        v = vector[ingre[i]] * weight_adj[i]
        matrix[i] = v
    
    recipe_vector = (matrix.sum(axis=0)/n)
    
    return normalize(recipe_vector.reshape(1,1536), norm='l2')
