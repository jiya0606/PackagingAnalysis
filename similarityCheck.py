from numpy import e
import pandas
import pandas as pd
from pprintpp import pprint as pp
from datetime import datetime
from collections import OrderedDict
import random
import requests


def similarityAPI(x, y):
    if type(x) == str and type(y) == str:
        r = requests.post(
            "https://api.deepai.org/api/image-similarity",
            data={
                'image1': x,
                'image2': y,
            },
            headers={'api-key': 'ddf90f83-e2c5-46e8-8b93-181169ca9973'}
        )
        a = r.json()['output']['distance']
        print("Found the Similarity Index for " + str(i) + "as " + str(a))
        return(a)
    else:
        return ('')


def isNaN(num):
    return num != num


productDict = pandas.read_csv(
    'Mintel_Matched_Similarity.csv', encoding='latin-1')
print(len(productDict))

for i in range(1, len(productDict)):
    if isNaN(productDict['Similarity.Index'][i]):
        productDict["Similarity.Index"][i] = similarityAPI(
            productDict['Primary.Image.Thumbnail'][i], productDict['Compare.URL'][i])
    else:
        print("Similarity Index already set for " + str(i))
    if (i % 500 == 0):
        productDict.to_csv('Mintel_Matched_Similarity.csv')
        print('saved to csv. Index is ' + str(i))

print("Succesfully Finished. Hurray!")
