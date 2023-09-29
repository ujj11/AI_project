from selectorlib import Extractor
import requests 
import json 
from time import sleep
import csv
import argparse
import os

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('search_results.yml')

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

    # Downloading page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Checking if page blocked (Usually 503)
    if r.status_code > 500:
        print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Passing HTML of the page and creating 
    return e.extract(r.text)


def run(keyword, pages):
    with open("search_results_urls.txt",'w') as urllist:
        for page in range(1, pages+1):
            urllist.write("https://www.amazon.in/s?k="+keyword+"&page="+str(page)+"\n")
 
    df=[]
    with open("search_results_urls.txt",'r') as urllist, open('search_results_output.jsonl','w') as outfile:
        for url in urllist.read().splitlines():
            data = scrape(url) 
            if data:
                for product in data['products']:
                    product['output'] = keyword
                    product['Product_name'] = (product['Product_name'].replace('"', ''))
                    if(product['Product_Price']):
                        product['Product_Price'] = product['Product_Price'].split(" .")[0]
                    if(product['Product_Price']):
                        product['Product_Price'] = (product['Product_Price'].replace('"', ''))
                        product['Product_Price'] = int(product['Product_Price'].replace(',', ''))
                    if(product['Product_Reviews']=='Another way to buy'):
                        product['Product_Reviews']=''
                    elif(product['Product_Reviews']):
                        product['Product_Reviews'] = (product['Product_Reviews'].replace('(', ''))
                        product['Product_Reviews'] = (product['Product_Reviews'].replace(')', ''))
                        product['Product_Reviews'] = int(product['Product_Reviews'].replace(',', ''))
                    if(product['Product_Rating']):
                        product['Product_Rating'] = product['Product_Rating'].split(" o")[0]
                    if((product['Product_Rating']=='No reviews') or (product['Product_Rating']=='New to Amazon')):
                        product['Product_Rating']=''
                    print("Saving Product: %s"%product['Product_name'])
                    df.append([product['Product_name'], product['Product_Brand'], product['Product_Image'], product['Product_Price'], product['Product_Reviews'], product['Product_Rating'], product['output']])
                    json.dump(product, outfile)
                    outfile.write("\n")

    # Saving data to a CSV file
    with open('db_duplicate.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product_name', 'Product_Brand', 'Product_Image', 'Product_Price', 'Product_Reviews', 'Product_Rating', 'output'])
        writer.writerows(df)
    
    # Remove duplicate rows
    from more_itertools import unique_everseen
    with open('db_duplicate.csv', 'r') as f, open('db.csv', 'w') as out_file:
        out_file.writelines(unique_everseen(f))


if __name__ == "__main__":
    run("shoe", 10)