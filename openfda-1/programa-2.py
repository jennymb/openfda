import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
try:
    conn.request("GET", "/drug/label.json?limit=10", None, headers) #en este caso,como queremos la información de
                                                                # 10 pacientes, ponemos limit=10.
except:
    print('Ha ocurrido un error. No se a podido solicitar el recurso.')

r1 = conn.getresponse()

print(r1.status, r1.reason)

if r1.status==404:
    print('Ha ocurrido un error. Recurso no encontrado')

repos_raw = r1.read().decode("utf-8")
conn.close()

r2 = json.loads(repos_raw)

for medicamento in range (len (r2['results'])):

    info=r2['results'][medicamento]

    print ('El identificador del medicamento',medicamento+1,'es'+info['id'])

# el único cambio frente al programa 1, es que realizamos un bucle for iterando por cada posición de los elementos
# (en este caso iterando sobre la información de cada medicamento) y obteniendo e imprimiendo por pantalla
# para cada medicamento (i + 1 porque el iterador i comienza en 0, por tanto el número del medicamento corresponde a
# un número más) el identificador del mismo.
# comprobamos que para los 10 primeros está definido su identificador, por lo que para este documento no
# hace falta el uso de excepciones en cuanto al diccionario, ya que no nos dará un KeyError.
