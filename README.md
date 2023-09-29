# E-Commerce Website Product Recommendation System

The aim of the project is to make recommendations based on images, title and brand information of Amazon products. The project works in real-time, providing recommendations for the user based upon a product of their choice. The user simply enters the product url in a text file (product_urls.txt), and runs the program, specifying the method of recommendation and the number of Amazon pages to search for similar products.

The first part of the project trains and tests an image classification model (in Product_Recommendation.ipynb) on various Amazon products listed in a static csv dataset. The lightweight CNN model achieves 92.96% training accuracy and 92.88% test accuracy. For recommendation, a much more powerful model, VGG-16 is used as a feature extractor to achieve even greater accuracy.

The second part of the project contains three recommendation engines -
1. The first recommendation engine takes in images from the user and recommends products solely based on image similarity (in Product_Recommendation.ipynb),
2. The second recommendation engines takes the product's title and recommends products that has a high similarity score based on the title (recommendation_title.py), 
3. The final recommendation engine takes into account the title and brand information and recommends products that have a high similarity score based on the title and brand name (recommendation_brand.py).

As image-based recommendation is extremely time-consuming for real-time data, and as such, not feasible for deployment, it has been restricted to a static scenario. The images in the static scenario represent a fashion dataset (one of the top categories on Amazon) and are based on 5 categories/types of apparel scraped from Amazon. The categories are hats, watches, shirts, shoes and trousers.

To run the program, install the dependencies and then run

```
python3 product.py --recommend 1 --pages 10
```

where recommend=1 signifies a product title-based recommendation, and 2 signifies a product title and brand-based recommendation.
Argument pages signifies the number of search result pages to crawl Amazon for.
