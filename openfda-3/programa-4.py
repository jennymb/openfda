#este servidor está basado en el server3 del ejercicio 6 L7.
import http.server
import socketserver

#Puerto donde lanzar el servidor
PORT = 8000

def lista_medicamentos():
    #necesitamos un cliente que acceda a la página web para bajar los medicamentos. Con ello,
    #crearemos un fichero html que se lo pasaremos a nuestro servidor web, que lo mandará en respuesta a cualquier
    #petición de un cliente.

    import http.client
    import json

    medicamentos=[] # Creamos una lista donde iremos añadiendo el nombre del medicamento, que es lo que nos interesa.

    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    try:
        conn.request("GET", "/drug/label.json?limit=100", None, headers)
    except:
        print('Ha ocurrido un error. No se a podido solicitar el recurso.')

    r1 = conn.getresponse()
    print(r1.status, r1.reason)

    if r1.status == 404:
        print('Ha ocurrido un error. Recurso no encontrado')
        exit(1)

    repos_raw = r1.read().decode("utf-8")
    conn.close()

    r2 = json.loads(repos_raw)

    for i in range (len(r2['results'])):

        info=r2['results'][i]

        if info['openfda']: # Nos aseguramos de que exista el campo openfda para el medicamento
                            # que vamos a añadir a la lista de medicamentos, ya que si no, nos daría KeyError

            medicamentos.append(info['openfda']['generic_name'][0])

            if len(medicamentos)==10: # Una vez que la lista que hemos creado tenga 10 medicamentos, salimos del bucle for
                                      # con un break. Este paso se realiza por el anterior if, ya que no tenemos asegurado
                                      # que según vayamos iterando, los 10 primeros vayan a tener el campo requerido para
                                      # poder añadirlos a la lista. (Es más, comprobándolo, solo obtenemos 9 medicamentos,
                                      # por eso es necesario poner como límite 100 (un número cualquiera pero mayor a 10)
                                      # para poder seguir iterando y especificar que el programa sólo debe parar
                                      # una vez que la lista 'medicamentos' tenga 10 elementos).
                                      # Este 'if' podría ponerse al mismo nivel que el otro if, pero como sólo aumentamos la
                                      # lista cuando se añaden medicamentos, me parece mejor comprobar la longitud de la lista sólo
                                      # si esta aumenta. Pero funcionalmente, no es necesario que este if esté identado dentro del otro.

                break

    return(medicamentos) # Por último, la función nos devuelve la lista medicamentos.


# La clase testHTTPRequestHandler hereda todos los métodos de la clase http.server.BaseHTTPRequestHandler.
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):


        self.send_response(200) #Primero enviamos el estado de la respuesta, que será OK.

        self.send_header('Content-type', 'text/html') # Después enviamos las cabeceras necesarias para que el cliente entienda el
                                                      # contenido que le enviamos (que sera HTML)
        self.end_headers() # Indicamos que las cabeceras ya han terminamos.

        # Procedemos al contenido html.

        contenido="""
        <!doctype html>
        <html>
             <h1>El listado de medicamentos obtenido es el siguiente:</h2>
             <ol>"""
        for i in lista_medicamentos():
            contenido=contenido+"<li>"+i+"</li>"
        """</ol>
        </html>
        """
        #con un bucle for, vamos iterando por cada elemento de la lista, colocando cada medicamento en un párrafo consecutivamente.

        # Enviamos el contenido html.
        self.wfile.write(bytes(contenido, "utf8"))
        print("File served!")
        return

# El servidor comienza a aquí

# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

# Creamos el socket que esperará las peticiones de los clientes.
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)


try:
    httpd.serve_forever() # el servidor recibirá y establecerá conexión con todos los clientes
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario.") # Solo parará en caso de que el usuario lo decida.

print("Servidor parado")
httpd.close()


#OBSERVACIÓN: Si ponemos limit 10, nunca podríamos obtener una lista con el nombre de 10 medicamentos, ya que el
# programa coge los 10 primeros medicamentos y el medicamento número 2 no tiene información sobre su nombre.