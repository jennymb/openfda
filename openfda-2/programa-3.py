import http.client
import json

headers = {'User-Agent': 'http-client'}

fabricantes1=[]
n=0

while True:

    skip=n*100

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", '/drug/label.json?search=active_ingredient:"acetylsalicylic"+substance_name:"ASPIRIN"&limit=100&skip='+str(skip), None, headers)

    r1 = conn.getresponse()

    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()

    r2 = json.loads(repos_raw)

    for i in range (len(r2['results'])):

        if r2['results'][i]['openfda']:

            fabricantes1.append(r2['results'][i]['openfda']['manufacturer_name'][0])

    if (len(r2['results'])<100):
        break
    else:
        print('Obteniendo datos...')

    n=n+1

fabricantes2=set(fabricantes1)

print('Los fabricantes que utilizan la aspirina en sus medicamentos son los siguientes:',fabricantes2)


