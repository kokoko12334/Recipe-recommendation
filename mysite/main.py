# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# django.setup()
# import pickle
import pandas as pd
import numpy as np
import chromadb
from chromadb.utils.batch_utils import create_batches
from tqdm import tqdm
import pickle
from sklearn.preprocessing import normalize
import time
df = pd.read_csv("", index_col= False)

df.head()

client = chromadb.PersistentClient(path="./chroma")
collection = client.get_collection(name="test")

# client.delete_collection('recipes')
client2 = chromadb.PersistentClient(path="D:/chroma")
collection2 = client2.get_or_create_collection(
    name="recipes",
    metadata={
        "hnsw:space": "cosine",
        "hnsw:construction_ef": 50,
        "hnsw:M": 32,
        "hnsw:search_ef": 20, 
              }
    )


#M을 32, efConstruction을 50, efSearch를 17
result = collection.get(include=['embeddings'])


print(len(result['ids']))
print(result['embeddings'][0])


#name,ingre,image_url,ck_mth,ck_knd,serving,url
ids = result['ids']
metadatas = []
embeddings = result['embeddings']

large_array = np.empty((183813, 1536), dtype=np.float64)

for i in range(len(ids)):
    large_array[i] = np.array(embeddings[i],dtype=np.float64)

for i in ids:
    i = int(i)
    dic = {
        'name':df.iloc[i]['name'],
        'ingre':df.iloc[i]['ingre'],
        'image_url':df.iloc[i]['image_url'],
        'url':df.iloc[i]['url']
    }    
    metadatas.append(dic)

print(len(metadatas))
print(metadatas[:5])
print(len(ids))
print(ids[:5])
print(len(large_array))
print(large_array[:5])

# result['embeddings'][2]
# collection.get(ids=['10'], include=['embeddings'])
# large_array[2]


# collection2.add(
#     embeddings=embeddings,
#     metadatas=metadatas,
#     ids=ids,
# )

batches = create_batches(api=client2, ids=ids, embeddings=embeddings, metadatas=metadatas)


for batch in tqdm(batches):
    print(f"Adding batch of size {len(batch[0])}")
    collection2.add(ids=batch[0],
                   embeddings=batch[1],
                   metadatas=batch[2],
)
    

client2 = chromadb.PersistentClient(path="D:/chroma")
collection2 = client2.get_collection('recipes')


collection2.get(ids=['0'], include=['embeddings', 'metadatas'])


with open('data/ingre_vector.pk', 'rb') as f:
    vector = pickle.load(f)

ingre = ['간장', '식초', '고춧가루', '참기름', '깨소금', '대파']
weight = [1, 1, 1, 1, 1, 1, 1]

def cal_vector(ingre, weight):
    n = len(ingre)
    weight_sum = sum(weight)
    weight_adj = [round(w / weight_sum, 4) for w in weight]
    matrix = np.zeros((n,1536))
    for i in range(n):
        v = vector[ingre[i]] * weight_adj[i]
        matrix[i] = v
    
    recipe_vector = matrix.sum(axis=0)/n
    return recipe_vector



embedding = cal_vector(ingre=ingre, weight=weight).reshape(1,1536)
normalized_data = normalize(embedding, norm='l2')


s = time.time()
result = collection.query(
    query_embeddings=normalized_data,
    n_results= 60

)
e = time.time()
print(f"{e-s}초")

s = time.time()
results2 = collection2.query(
    query_embeddings=normalized_data,
    n_results= 60
)
e = time.time()
print(f"{e-s}초")


collection2.metadata

result

results2['metadatas'][0]