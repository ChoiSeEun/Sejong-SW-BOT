import numpy as np
import pandas as pd

meta=pd.read_csv('question.csv')
diff=pd.read_csv('difficulty.csv')

diff.rating=pd.to_numeric(diff.rating) #문자열을 숫자로 변환
diff.user_id=pd.to_numeric(diff.user_id)

data = pd.merge(diff,meta,on='que_id',how='inner')
matrix=data.pivot_table(index='user_id',columns='que_id',values='rating')

GENRE_WEIGHT = 1

def pearsonR(s1, s2):
    s1_c = s1 - s1.mean()
    s2_c = s2 - s2.mean()
    return np.sum(s1_c * s2_c) / np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))

def recommend(input,matrix,n,similar_genre=True):

    input_genres=meta[meta['que_id']==input]['genre'].iloc(0)[0]
    print(input_genres)
    result = []

    for que in matrix.columns:
        if que == input:
            continue
        cor=pearsonR(matrix[input],matrix[que])

        if similar_genre and len(input_genres)>0:
            temp_genres = meta[meta['que_id']==que]['genre'].iloc(0)[0]
            same_count=np.sum(np.isin(input_genres,temp_genres))
            cor+=(GENRE_WEIGHT * same_count)

        if np.isnan(cor):
            continue
        else:
            result.append((que, '{:.2f}'.format(cor), temp_genres))

    result.sort(key=lambda r: r[1], reverse=True)
    return result[:n]


list=[]
list = recommend(7, matrix, 5)
print(list)


