import os
import json

pwd = os.getcwd()
data_path = os.path.join(pwd, 'Retail_Sales', 'products.json')
data = {}

with open(data_path) as file:
    data = json.load(file)

print(data.keys())