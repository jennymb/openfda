#basandonos en el ejemplo del ejercici 10 de L7,
import http.client
import json

# los módulos que vamos a utilizar para establecer la conexión y acceder a la información (http.client)
# y para

headers = {'User-Agent': 'http-client'} # Indicamos qué navegador somos, no es un paso necesario para el funcionamiento
                                        # del programa.

conn = http.client.HTTPSConnection("api.fda.gov")   # establecemos la conexión con el servidor

conn.request("GET", "/drug/label.json", None, headers)  # Al no indicar 'limit', por defecto nos devuelve
                                                        # La información de un medicamento (es como poner limit=1)
                                                        # Obtenemos la información pedida con el método request GET.

r1 = conn.getresponse() # guardamos la respuesta obtenida por la función conn.get.response() en la variable r1.

print(r1.status, r1.reason) # Imprimimos por pantalla el estado y la razón, que será 200 OK si se ha establecido
                            # bien la conexión.

repos_raw = r1.read().decode("utf-8") # decodificamos la respuesta con utf-8 (Formato de Transformación Unicode)
conn.close()

r2 = json.loads(repos_raw)       # convierte el objeto json a un formato python (diccionarios, listas...)
                                 # una vez que tenemos la información en su estado más legible, obtenemos la
                                 # parte que queremos, guardándolo en la variable info.
info=r2['results'][0]

print('El identificador del medicamento es ',info['id']+', su propósito es su utilización en caso de '+info['purpose'][0]+'; y el nombre del fabricante es' , info['openfda']['manufacturer_name'][0]+'.')
