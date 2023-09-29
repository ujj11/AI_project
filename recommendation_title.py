from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

# Accepts PID, Number of most similar products to recommend
def text_recommend_1(pid, num_recommend):
    data = pd.read_csv('db.csv')
    data=data.reset_index()
    data=data.rename(columns={"index":"PID"})
    count_vectorize = CountVectorizer(stop_words = 'english')
    title_vectorized = count_vectorize.fit_transform(data['Product_name'])
    cosine_sim = cosine_similarity(title_vectorized, title_vectorized)

    recommended_prod = []
    score=[]
    
    # Displaying query product - PID, Name, Brand
    print("-----------------------------------------------------------------------")
    print("Original product:")
    print("-----------------------------------------------------------------------")
    print("Product ID : " , pid)
    print("Title : ", data['Product_name'][data['PID']==pid].item())
    print("Brand : ", data['Product_Brand'][data['PID']==pid].item())
    print("Price : ",data['Product_Price'][data['PID']==pid].item())
    print("Reviews : ",data['Product_Reviews'][data['PID']==pid].item())
    print("Rating : ",data['Product_Rating'][data['PID']==pid].item())
    
    # Getting indexes, scores of N most similar products
    score_series = pd.Series(cosine_sim[pid]).sort_values(ascending = False)
    top_10_indexes = list(score_series.iloc[1:(num_recommend+1)].index)
    top_10_score=list(score_series.iloc[1:(num_recommend+1)])
    
    # Displaying recommended products - Image, PID, Name, Brand, Similarity Score
    print("\n")
    print("-----------------------------------------------------------------------")
    print("Most similar products:")
    print("-----------------------------------------------------------------------")
    
    for i in range(0,len(top_10_score)):
        recommended_prod.append(list(data['Product_name'])[i])
        print("\nProduct ID : " , top_10_indexes[i])
        print("Title : ", data['Product_name'][data['PID']==top_10_indexes[i]].item())
        print("Brand : ", data['Product_Brand'][data['PID']==top_10_indexes[i]].item())
        print("Price : ",data['Product_Price'][data['PID']==top_10_indexes[i]].item())
        print("Reviews : ",data['Product_Reviews'][data['PID']==top_10_indexes[i]].item())
        print("Rating : ",data['Product_Rating'][data['PID']==top_10_indexes[i]].item())
        print("Similarity score : ",top_10_score[i])

def run():
    data = pd.read_csv('db.csv')
    text_recommend_1((data.shape[0]-1), 5)

if __name__=="__main__":
    data = pd.read_csv('db.csv')
    text_recommend_1((data.shape[0]-1), 5)