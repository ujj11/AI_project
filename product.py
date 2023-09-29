from selectorlib import Extractor
import requests
from time import sleep
import csv
import argparse
import pandas as pd
from io import BytesIO
from PIL import Image

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('product.yml')

def scrape(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.in/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)

def write_csvs():
    with open('product.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product_name', 'Product_Brand', 'Product_Image', 'Product_Price', 'Product_Reviews', 'Product_Rating', 'output'])

    df = []
    with open("product_urls.txt",'r') as urllist, open('db.csv', 'a', newline='', encoding='utf-8') as file, open('product.csv', 'w', newline='', encoding='utf-8') as product:
        writer = csv.writer(file)
        product_writer = csv.writer(product)
        for url in urllist.read().splitlines():
            data = scrape(url) 
            if data:
                if(data['Product_name']):
                    data['Product_Brand']=data['Product_name'].split(" ")[0]
                    data['Product_name']=data['Product_name'].split((data['Product_Brand']+" "))[1]
                    data['Product_name'] = (data['Product_name'].replace('"', ''))
                if(data['Product_Price']):
                    data['Product_Price'] = data['Product_Price'].split(" .")[0]
                if(data['Product_Price']):
                    data['Product_Price'] = (data['Product_Price'].replace('"', ''))
                    data['Product_Price'] = int(data['Product_Price'].replace(',', ''))
                if(data['Product_Reviews']=='Another way to buy'):
                    data['Product_Reviews']=''
                elif(data['Product_Reviews']):
                    data['Product_Reviews'] = data['Product_Reviews'].split(" ")[0]
                    data['Product_Reviews'] = int(data['Product_Reviews'].replace(',', ''))
                if(data['Product_Rating']):
                    data['Product_Rating'] = data['Product_Rating'].split(" o")[0]
                if((data['Product_Rating']=='No reviews') or (data['Product_Rating']=='New to Amazon')):
                    data['Product_Rating']=''
                df.append([data['Product_name'], data['Product_Brand'], data['Product_Image'], data['Product_Price'], data['Product_Reviews'], data['Product_Rating']])
        writer.writerows(df)
        product_writer.writerow(['Product_name', 'Product_Brand', 'Product_Image', 'Product_Price', 'Product_Reviews', 'Product_Rating', 'output'])
        product_writer.writerows(df)

def download_img():
    imgs_path = "images/"
    data = pd.read_csv("db.csv")
    data=data.reset_index()
    data=data.rename(columns={"index":"PID"})
    url = data['Product_Image'][data['PID']==(data.shape[0]-1)].item()
    if(url!='nan' and url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.save(imgs_path + str((data.shape[0]-1)) + '.jpeg')  

def delete_from_db():
    df = pd.read_csv("db.csv")
    df = df.drop(df.tail(1).index)
    df.to_csv("db.csv", sep=',', index=False)
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Scrape and Recommend')
    parser.add_argument('--recommend', default=1, type=int, required=True, help='Recommendation Type: 1 - Title, 2 - Title and Brand')
    parser.add_argument('--pages', default=10, type=int, required=True, help='Number of pages to search products')

    args = parser.parse_args()
    with open("product_urls.txt",'r') as urllist:
        url = urllist.read().splitlines()[0]
    url = url.split("keywords=")[1]
    url = url.split("&")[0]
    import search_results
    search_results.run(url, args.pages)
    write_csvs()
    if(args.recommend==1):
        import recommendation_title
        recommendation_title.run()
    elif(args.recommend==2):
        import recommendation_brand
        recommendation_brand.run()

    delete_from_db()

    # usage: python3 product.py --recommend 2 --pages 10