from numpy import e
import pandas
import pandas as pd
from pprintpp import pprint as pp
from datetime import datetime
from collections import OrderedDict
import random
import requests
import warnings
warnings.filterwarnings("ignore")

blankurl = 0
goodurl = 0
def isNaN(num):
    return num != num

def addCompareURL(rid, url):
    # print("Setting the compare URL of " + str(rid) + " to " + str(url))
    r = productDict.loc[productDict['Record.ID'] == rid]
    productDict['Compare.URL'][r.index[0]] = url

def getPrimaryURL(rid):
    r = productDict.loc[productDict['Record.ID'] == rid]
    return(r['Primary.Image.Thumbnail'][r.index[0]])

productDict = pandas.read_csv('Mintel_Matched_Clean.csv', encoding='latin-1')
print(len(productDict))

newpackaging = {}
productDict['Compare.URL'] = ""

newp = 0 
newpkg = 0
newv = 0
for x in range(1, len(productDict)):
    key = str(productDict['Product'][x]) + ":" + str(productDict['Brand'][x])
    if productDict['Launch.Type'][x] == "New Product": newp += 1
    if productDict['Launch.Type'][x] == "New Packaging": newpkg += 1
    if productDict['Launch.Type'][x] == "New Product" or productDict['Launch.Type'][x] == "New Packaging":
        if not key in newpackaging:
            # Add the first product or the new packaging
            newpackaging[key] = {productDict['Date.Published'][x]:productDict['Record.ID'][x]}
        else:
            newpackaging[key][(productDict['Date.Published'][x])] = productDict['Record.ID'][x]
            newv += 1
#print(newpackaging)
print(str(len(newpackaging)) + ": Total")
print(str(newp) + ": New Products")
print(str(newpkg) + ": New Packages")
print(str(newv) + ": Multiple Variants")

# Sort the variants by the launch date
for x in newpackaging.keys():
    newpackaging[x] = OrderedDict(
        sorted(newpackaging[x].items(), key=lambda x: datetime.strptime(x[0], '%Y-%m-%d')))

#pp(newpackaging)
potentials = 0
for y in newpackaging:
    p = []
    l = []
    if (len(newpackaging[y]) > 1):
        potentials += len(newpackaging[y]) - 1 
        for x in newpackaging[y]:
            p.append(newpackaging[y][x])
            l.append(getPrimaryURL(newpackaging[y][x]))
        for i in range(len(p)-1):
            addCompareURL(p[i+1], l[i])
            if type(l[i]) != str: blankurl += 1
            else: goodurl += 1

print(str(blankurl) + ": Blank URLs")
print(str(goodurl) + ": Good URLs")
print(str(potentials) + ": Potentials")
productDict.to_csv('Mintel_Matched_Compare_URL.csv')
