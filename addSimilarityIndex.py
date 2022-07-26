from numpy import e
import pandas
import pandas as pd
from pprintpp import pprint as pp
from datetime import datetime
from collections import OrderedDict
import random
import requests

cpd = pandas.read_csv('Mintel_Matched_Compare_URL.csv', encoding='latin-1')
cpd['Similarity.Index'] = ""
cpd.to_csv('Mintel_Matched_Similarity.csv')
