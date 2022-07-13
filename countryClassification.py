import pandas
import os
import json
from google.cloud import bigquery
from pprintpp import pprint as pp
from scipy.spatial import KDTree
from webcolors import (
    css3_hex_to_names,
    hex_to_rgb,
)


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jiya/Downloads/package-classification-353918-420f00ac7c33.json"
client = bigquery.Client()
sql = """SELECT int64_field_0, Market, Primary_Image_Thumbnail, Dominant_Color FROM `package-classification-353918.ProductPackaging.PackagingColorsUniqueRID`"""
productDict = client.query(sql).to_dataframe()
countryDict = {}


def convert_rgb_to_names(rgb_tuple):
    # a dictionary of all the hex and their respective names in css3
    css3_db = css3_hex_to_names
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return f'{names[index]}'


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def bubble_sort(array):
    n = len(array)
    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False
        if already_sorted:
            break
    return array


index = 0
for x in productDict['Primary_Image_Thumbnail']:
    if (productDict['Dominant_Color'][index] != None):
        country = productDict['Market'][index]
        dominantColor = convert_rgb_to_names(
            (hex_to_rgb(productDict['Dominant_Color'][index])))
        if not country in countryDict:
            countryDict[(country)] = {'colors': {}, 'total': 1}
            countryDict[(country)]['colors'][dominantColor] = 1
        else:
            if not dominantColor in ((countryDict[country])['colors']):
                (countryDict[country])['colors'][dominantColor] = 1
                (countryDict[country])['total'] += 1
            else:
                (countryDict[country])['colors'][dominantColor] += 1
                (countryDict[country])['total'] += 1
        index = index+1

totalNum = 0
for x in countryDict:
    totalNum += countryDict[x]['total']
    for y in countryDict[x]['colors']:
        countryDict[x]['colors'][y] = round(
            (countryDict[x]['colors'][y]/(countryDict[x]['total'])), 5)

for x in countryDict:
    countryDict[x]['colors'] = sorted(
        countryDict[x]['colors'].items(), key=lambda x: x[1], reverse=True)

j = json.dumps(countryDict, indent=4)
f = open('country-color.json', 'w')
print(j, file=f)
f.close()
#json_object = json.dumps(countryDict, indent=1)
#print("This is the total: " + str(totalNum))
# pp(json_object)
