#este servidor está basado en el server3 del ejercicio 6 L7.
import http.server
import socketserver

# -- Puerto donde lanzar el servidor
PORT = 8005

def lista_medicamentos():
    #necesitamos un cliente que acceda a la página web para bajar los medicamentos. Con ello,
    #crearemos un fichero html que se lo pasaremos a nuestro servidor web, que lo mandará en respuesta a cualquier
    #petición de un cliente

    import http.client
    import json

    medicamentos=[]

    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=100", None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()

    r2 = json.loads(repos_raw)

    for i in range (len(r2['results'])):

        if r2['results'][i]['openfda']:
            medicamentos.append(r2['results'][i]['openfda']['generic_name'][0])
            if len(medicamentos)==10:
                break

    return(medicamentos)

# Clase con nuestro manejador. Es una clase derivada de BaseHTTPRequestHandler
# Esto significa que "hereda" todos los metodos de esta clase. Y los que
# nosotros consideremos los podemos reemplazar por los nuestros
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET. Este metodo se invoca automaticamente cada vez que hay una
    # peticion GET por HTTP. El recurso que nos solicitan se encuentra
    # en self.path
    def do_GET(self):

        # La primera linea del mensaje de respuesta es el
        # status. Indicamos que OK
        self.send_response(200)

        # En las siguientes lineas de la respuesta colocamos las
        # cabeceras necesarias para que el cliente entienda el
        # contenido que le enviamos (que sera HTML)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Este es el mensaje que enviamos al cliente: un texto y
        # el recurso solicitado

        contenido="""
        <!doctype html>
        <html>
             <h1>Hola!</h2>
             <p>Listado de medicamentos:</p>
             <p>"""
        for i in lista_medicamentos():
            contenido=contenido+"<p>"+i+"</p>"
        """</p>
        </html>
        """



        # Enviar el mensaje completo
        self.wfile.write(bytes(contenido, "utf8"))
        print("File served!")
        return


# ----------------------------------
# El servidor comienza a aqui
# ----------------------------------
# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

# -- Configurar el socket del servidor, para esperar conexiones de clientes
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

# Entrar en el bucle principal
# Las peticiones se atienden desde nuestro manejador
# Cada vez que se ocurra un "GET" se invoca al metodo do_GET de
# nuestro manejador
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
httpd.close()


