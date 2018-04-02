import http.client
import json

headers = {'User-Agent': 'http-client'}

# Para este ejercicio, en el cual tenemos que conseguir todos los fabricantes que utilizan aspirinas
# en sus medicamentos, nos encontramos con el principal problema que es, que la página web sólo
# es capaz de devolvernos 100 medicamentos, pues si el límite sobrepasara de 100, la página web
# tardaría mucho en responder, incluso podría bloquearse el navegador.

fabricantes1=[] # creamos una lista donde vamos a ir añadiendo todos los fabricantes.
n=0 # inicializamos un parámetro n, el cual irá aumentando en el número de vueltas,
    # que nos será necesario para ir cambiando el número del skip, y poder ir avanzando por toda la información total.

while True:

    skip=n*100 # definimos el número skip que le pasaremos a la URL.

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", '/drug/label.json?search=active_ingredient:"acetylsalicylic"+substance_name:"ASPIRIN"&limit=100&skip='+str(skip), None, headers)

# Necesitamos convertir el número skip en un string ya que la URL lo es, y para convertir skip de tipo int a string, utilizamos str. De esta forma
# lo puede leer.
#Buscamos en el nombre de la sustancia y en el complejo activo.

    r1 = conn.getresponse()

    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()

    r2 = json.loads(repos_raw)

    for i in range (len(r2['results'])): # Realizamos un bucle for para ir iterando por la información de cada medicamento.

        if r2['results'][i]['openfda']: # No todos ellos van a tener definido el campo openfda. Por ello, debemos asegurarnos
                                        # de que lo tiene para poder añadir el nombre del fabricante a la lista. Sin este paso
                                        # de aseguración, nos saldría un KeyError para aquellos en los que no exista openfda
                                        # o no tenga ninguún valor.

            fabricantes1.append(r2['results'][i]['openfda']['manufacturer_name'][0]) # para los que sí tienen el campo requerido,
                                                                                     # añadimos el fabricante del medicamento a la
                                                                                     # lista fabricantes1.

    if (len(r2['results'])<100): # Si el número de valores que da results es menor que 100, significa que el documento se ha acabado, ya que va de
                                 # 100 en 100 y no puede sacar otros 100 medicamentos. Por tanto, ya hemos recorrido el dococumento entero y
                                 # realizamos un break para salir del bucle while.
        break
    else:                        # En caso de que sí consigamos 100 medicamentos, seguimos dando una vuelta más al documento,
        print('Obteniendo datos...')

    n=n+1 # Para ello, aumentamos en una unidad el parámetro n, que hará que se pasen n*100 medicamentos (ya anteriormente leídos). Este paso
          # podría identarse dentro del else, ya que si se cumple el if, al hacer un break, no llegaría a realizarse este paso

fabricantes2=set(fabricantes1) # Una vez que salimos del bucle while y obtengamos toda la información, obtendremos fabricantes repetidos
                               # ya que es posible que un mismo fabricante sea el autor de distintos medicamentos.
                               # Para asegurarnos de no repetir ninguno, utilizamos set() con lo que nos quedará un conjunto
                               # de elementos únicos y no repetidos.

print('Los fabricantes que utilizan la aspirina en sus medicamentos son los siguientes:',fabricantes2)

