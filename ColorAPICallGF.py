from google.cloud import bigquery
from colormap import rgb2hex


def detect_properties_uri(uri):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.image_properties(image=image)
    if response.error.message:
        print("Failed to fetch dominant color for "+uri)
        return(None)
    props = response.image_properties_annotation
    # print('Properties:')
    if(len(props.dominant_colors.colors)):
        dcHex = rgb2hex(int(props.dominant_colors.colors[0].color.red),
                        int(props.dominant_colors.colors[0].color.green),
                        int(props.dominant_colors.colors[0].color.blue))
        return(dcHex)
    else:
        print("Failed to fetch dominant color for "+uri)
        return(None)


def analyze_colors(request):
    request_json = request.get_json()
    startId = 1
    endId = 100
    if request_json and 'startId' in request_json:
        startId = request_json['startId']
    if request_json and 'endId' in request_json:
        endId = request_json['endId']

    client = bigquery.Client()
    # Download query results.
    query_string = "SELECT int64_field_0, Primary_Image_Thumbnail, Dominant_Color FROM `package-classification-353918.ProductPackaging.PackagingTableAll` where Dominant_Color is NULL and Primary_Image_Thumbnail != '' and int64_field_0 BETWEEN " + \
        str(startId) + " and " + str(endId)

    productDict = (
        client.query(query_string)
        .result()
        .to_dataframe(
            # Optionally, explicitly request to use the BigQuery Storage API. As of
            # google-cloud-bigquery version 1.26.0 and above, the BigQuery Storage
            # API is used by default.
            create_bqstorage_client=True,
        )
    )
    index = 0
    for x in productDict['Primary_Image_Thumbnail']:
        #print("the dominant color for " + x + " is " + productDict['Dominant_Color'][index])
        if (productDict['Dominant_Color'][index] is None):
            print('Trying to find color for ' + x)
            dcolor = detect_properties_uri(x)
            i = 0
            while (dcolor is None and i < 3):
                print("Failed to find the color. Trying again. i =" + str(i))
                dcolor = detect_properties_uri(x)
                i += 1
            productDict['Dominant_Color'][index] = dcolor
            if (productDict['Dominant_Color'][index] != None):
                print('Trying to set color for ' + x)
                sql = "UPDATE package-classification-353918.ProductPackaging.PackagingTableAll SET Dominant_Color = '" + \
                    str(productDict['Dominant_Color'][index]) + \
                    "' WHERE int64_field_0 = " + \
                    str(productDict['int64_field_0'][index]) + ";"
                query_job = client.query(sql)
                query_job.result()
        index = index+1

    print(productDict)
    return("Success")
