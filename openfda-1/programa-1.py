# basándonos en el ejemplo del ejercici 10 de L7,
import http.client
import json

# los módulos que vamos a utilizar para establecer la conexión y acceder a la información (http.client)
# y para decodificar la información y obtenerla finalmente en un formato python, el módulo json.

headers = {'User-Agent': 'http-client'} # Indicamos qué navegador somos, no es un paso necesario para el funcionamiento
                                        # del programa.

conn = http.client.HTTPSConnection("api.fda.gov")   # establecemos la conexión con el servidor

try:

    conn.request("GET", "/drug/label.json", None, headers)  # Al no indicar 'limit', por defecto nos devuelve
                                                        # La información de un medicamento (es como poner limit=1)
                                                        # Obtenemos la información pedida con el método request GET.
except:
    print('Ha ocurrido un error. No se a podido solicitar el recurso.')

r1 = conn.getresponse() # guardamos la respuesta obtenida por la función conn.get.response() en la variable r1.

print(r1.status, r1.reason) # Imprimimos por pantalla el estado y la razón, que será 200 OK si se ha establecido
                            # bien la conexión.
if r1.status==404:
    print('Ha ocurrido un error. Recurso no encontrado')
    exit(1) # si el recurso no es encontrado, el programa avisa al usuario y cierra el programa.

repos_raw = r1.read().decode("utf-8") # decodificamos la respuesta con utf-8 (Formato de Transformación Unicode)
conn.close()

r2 = json.loads(repos_raw)       # convierte el objeto json a un formato python (diccionarios, listas...)
                                 # una vez que tenemos la información en su estado más legible, obtenemos la
                                 # parte que queremos, guardándolo en la variable info.
info=r2['results'][0]

print('El identificador del medicamento es ',info['id']+'.')
print('Su propósito es su utilización en caso de '+info['purpose'][0]+'.')
print('El nombre del fabricante es' , info['openfda']['manufacturer_name'][0]+'.')
