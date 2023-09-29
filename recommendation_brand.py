from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

# Accepts PID, Number of most similar products to recommend, weights for the word-2-vec features: product name and brand
def text_recommend_2(pid, num_recommend, w1, w2):
    data = pd.read_csv('db.csv')
    data=data.reset_index()
    data=data.rename(columns={"index":"PID"})
    brand_vectors = CountVectorizer(stop_words = 'english')
    brand_vectorized = brand_vectors.fit_transform(data['Product_Brand'])
    title_vectorized = brand_vectors.fit_transform(data['Product_name'])
    title_sim  = cosine_similarity(title_vectorized, title_vectorized)
    brand_sim = cosine_similarity(brand_vectorized, brand_vectorized)
    total_sim   = (w1 * title_sim +  w2 * brand_sim)/float(w1 + w2)

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
    score_series = pd.Series(total_sim[pid]).sort_values(ascending = False)
    top_indexes = list(score_series.iloc[1:(num_recommend+1)].index)
    top_score=list(score_series.iloc[1:(num_recommend+1)])
            
    # Displaying recommended products - Image, PID, Name, Brand, Similarity Score
    print("\n")
    print("-----------------------------------------------------------------------")
    print("Most similar products:")
    print("-----------------------------------------------------------------------")
    
    for i in range(0,len(top_score)):
        recommended_prod.append(list(data['Product_name'])[i])
        print("\nProduct ID : " , top_indexes[i])
        print("Title : ", data['Product_name'][data['PID']==top_indexes[i]].item())
        print("Brand : ", data['Product_Brand'][data['PID']==top_indexes[i]].item())
        print("Price : ",data['Product_Price'][data['PID']==top_indexes[i]].item())
        print("Reviews : ",data['Product_Reviews'][data['PID']==top_indexes[i]].item())
        print("Rating : ",data['Product_Rating'][data['PID']==top_indexes[i]].item())
        print("Similarity score : ",top_score[i])

def run():
    data = pd.read_csv('db.csv')
    text_recommend_2((data.shape[0]-1), 5, 0.75, 0.25)

if __name__=="__main__":
    data = pd.read_csv('db.csv')
    text_recommend_2((data.shape[0]-1), 5, 0.75, 0.25)