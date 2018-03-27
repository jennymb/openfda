#basandonos en el ejemplo del ejercici 10 de L7,
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()

print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

response = json.loads(repos_raw)

info=response['results'][0]

print('El identificador del medicamento es'+info['id']+', su propósito es'+info['purpose'][0]+', y el nombre del fabricante es' + info['openfda']['manufacturer_name'][0])
