import pickle
import json
import numpy as np
import boto3
from pinecone import Pinecone
from typing import List

BUCKET_NAME = 'bucket-name'
FILE_NAME = 'filename'
PINECONE_APIKEY = 'apikey'
INDEX_NAME = 'recipe-index'

# Pinecone 벡터DB연결 및 인덱스 불러오기
pc = Pinecone(api_key=PINECONE_APIKEY)
index = pc.Index(INDEX_NAME)

# s3에서 (재료-벡터)로 매핑된 데이터 불러오기
s3 = boto3.resource('s3')
ingre_vector = pickle.loads(s3.Bucket(BUCKET_NAME).Object(FILE_NAME).get()['Body'].read())

# 입력한 재료(ingre), 가중치(weight)를 벡터로 변환시키는 함수
def cal_recipe_vector(ingre: List[str], weight: List[float]) -> List[float]:
    n = len(ingre)
    weight_sum = sum(weight)
    weight_adj = [round(w/weight_sum, 4) for w in weight]
    matrix = np.zeros((n, 1536))
    for i in range(n):
        v = ingre_vector[ingre[i]] * weight_adj[i]
        matrix[i] = v
    
    recipe_vector = matrix.sum(axis=0)/n
    return list(recipe_vector)

# AWS lambda 함수
def lambda_handler(event, context):
    req = event['input']
    ingre = []
    weight = []
    for data in req:
        ingre.append(data['values'])
        weight.append(data['range'])
    
    query_vector = cal_recipe_vector(ingre=ingre, weight=weight)

    # 쿼리벡터와 코사인유사도가 가장 높은 레시피 벡터 조회(top_k만큼)
    top_k = 20
    result = index.query(
        vector=query_vector,
        top_k=top_k,
        include_values=False,
        include_metadata=True
    )

    # 조회된 결과 전처리
    matches = result['matches']
    recipe_rec_list = []
    for i in range(len(matches)):
        metadata = matches[i]['metadata']
        name = metadata['name'] if 'name' in metadata.keys() else '요리'
        ingredients = metadata['ingre'] if 'ingre' in metadata.keys() else '재료'
        url = metadata['url'] if 'url' in metadata.keys() else '링크없음'
        image_url = metadata['image_url'] if 'image_url' in metadata.keys() else '이미지없음'

        recipe = {
            'name': name,
            'ingredients': ingredients,
            'url': url,
            'image_url': image_url
        }
        recipe_rec_list.append(recipe)

    output = {'output': recipe_rec_list}
    
    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }