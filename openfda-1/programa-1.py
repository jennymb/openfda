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

repos = json.loads(repos_raw)

info_medicamento=repos['results'][0]

print('El identificador del medicamento es'+info_medicamento['id']+', su propósito es'+info_medicamento['purpose'][0]+', y el nombre del fabricante es' + info_medicamento['openfda']['manufacturer_name'][0])
