
import http.client
import json

headers = {'User-Agent': 'http-client'}

# Para este ejercicio, en el cual tenemos que conseguir todos los fabricantes que utilizan aspirinas
# en sus medicamentos, nos encontramos con el principal problema que es, que la página web sólo
# es capaz de devolvernos 100 medicamentos, pues si el límite sobrepasara de 100, la página web
# tardaría mucho en responder, incluso podría bloquearse el navegador.

n=0 # inicializamos un parámetro n, el cual irá aumentando en el número de vueltas,
    # que nos será necesario para ir cambiando el número del skip, y poder ir avanzando por toda la información total.

while True:

    skip=n*100 # definimos el número skip que le pasaremos a la URL.

    conn = http.client.HTTPSConnection("api.fda.gov")

    try:
        conn.request("GET", '/drug/label.json?search=active_ingredient:"acetylsalicylic"&limit=100&skip='+str(skip), None, headers)
    except:
        print('Ha ocurrido un error. No se a podido solicitar el recurso.')

# Necesitamos convertir el número skip en un string ya que la URL lo es, y para convertir skip de tipo int a string, utilizamos str. De esta forma
# lo puede leer.
# Buscamos en el complejo activo.

    r1 = conn.getresponse()

    print(r1.status, r1.reason)

    if r1.status == 404:
        print('Ha ocurrido un error. Recurso no encontrado')
        exit(1)

    repos_raw = r1.read().decode("utf-8")
    conn.close()

    r2 = json.loads(repos_raw)

    print('Los fabricantes que utilizan aspirinas son los siguientes:')

    for i in range (len(r2['results'])): # Realizamos un bucle for para ir iterando por la información de cada medicamento.

        info=r2['results'][i]

        if info['openfda']: # No todos ellos van a tener definido el campo openfda. Por ello, debemos asegurarnos
                            # de que lo tiene para poder añadir el nombre del fabricante a la lista. Sin este paso
                            # de aseguración, nos saldría un KeyError para aquellos en los que no exista openfda
                            # o no tenga ninguún valor.

            print('El medicamento con id', info['id'], 'fue fabricado por', info['openfda']['manufacturer_name'][0])

        else:
            print('El medicamento con id',info['id'], ', no tiene especificado el fabricante.' )

    if (len(r2['results'])<100): # Si el número de valores que da results es menor que 100, significa ya ha llegado a la parte final del documento,
                                 # ya que estamos imponiendo como límite 100.
                                 # Por tanto, ya hemos recorrido el dococumento entero y
                                 # realizamos un break para salir del bucle while.
        break

    n=n+1 # Para ir aumentando el skip, aumentamos en una unidad el parámetro n, que hará que se pasen n*100 medicamentos (ya anteriormente leídos). Este paso
          # podría identarse dentro del else, ya que si se cumple el if, al hacer un break, no llegaría a realizarse este paso.


# OBSERVACIÓN: Anteriormnete, tenía este ejercicio buscando también ASPIRIN en substance_name. Si lo pongo como parámetro
# a buscar, me salen muchos más fabricantes que utilizan la aspirina, aunque no esté figurado como complejo activo del medicamento.
# La estructura de este programa es eficaz si se utiliza el parámetro substance_name. Utilizando solo el parámetro
# active ingredient, solo refieren 2 medicamentos en el documenton total, por tanto no es necesario utilizar el skip
# ni ir aumentando el número del skip.

