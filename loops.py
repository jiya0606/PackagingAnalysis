import requests
startId = 0
incr = 75
total = 74000
#incr = 100
#total = 148317
while startId < total:
    endId = startId + incr - 1
    data = '{{"startId": {}, "endId": {}}}'.format(startId, endId)
    print(data)
    headers = {'Content-type': 'application/json', }
    try:
        response = requests.post(
            'http://us-west2-package-classification-353918.cloudfunctions.net/analyze-packaging-color-1', headers=headers, data=data)  # timeout=0.5
    except requests.exceptions.ReadTimeout:
        print("Initiated the program for entries " +
              str(startId) + " to " + str(endId))
    startId += incr
