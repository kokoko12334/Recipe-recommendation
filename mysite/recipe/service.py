from recipe.utils import cal_vector, cal_weight, get_detailed_recipe
from sklearn.preprocessing import normalize
import chromadb

client = chromadb.PersistentClient(path="./chroma")
collection = client.get_collection(name="test")

def get_recipe_recommand(ingre,n):

    portion = cal_weight(ingre)
    v = cal_vector(ingre, portion).reshape(1,3072)
    normalized_data = normalize(v, norm='l2')

    result=collection.query(
        query_embeddings=normalized_data,
        n_results=n,

    )
    ids = result['ids'][0]
    result = get_detailed_recipe(ids)

    return result
