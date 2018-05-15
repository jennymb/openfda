
import http.client
import json
import socketserver
import http.server

# Este programa está basado en las anteriores prácticas openfda.


class OpenFDAClient():
    # definimos tres clientes diferentes, ya que cada uno se conectará al recurso con prarámetros diferentes.
    # definimos las cabeceras, que le indica a la página web qué navegador somos.
    headers = {'User-Agent': 'http-client'}

    def get_drugs(self, limit):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")  # establecemos la conexión con el servidor
        conn.request("GET", '/drug/label.json?limit=' + limit, None,
                     headers)  # la petición es de tipo GET, es decir, queremos obtener una información
        r1 = conn.getresponse()  # guardamos la respuesta obtenida por la función conn.get.response() en la variable r1.
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode(
            "utf-8")  # decodificamos la respuesta con utf-8 (Formato de Transformación Unicode)
        conn.close()
        drogas = json.loads(repos_raw)  # convierte el objeto json a un formato python (diccionarios, listas...)

        return drogas

    # las demás funciones realizan la misma tarea, pero con otros parámetros.

    def get_active_ingredient(self, active_ingredient):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection('api.fda.gov')
        conn.request('GET', '/drug/label.json?search=active_ingredient:' + active_ingredient + '&limit=10', None,
                     headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()
        drogas = json.loads(repos_raw)

        return drogas

    def get_companies(self, company):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection('api.fda.gov')
        conn.request('GET', '/drug/label.json?search=manufacturer_name:' + company + '&limit=10', None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        conn.close()
        drogas = json.loads(repos_raw)

        return drogas


class OpenFDAParser():

    # después definimos la clase OpenfdaPARSER, en el que se incluye la lógica para obtener los datos de los medicamentos.
    # como queremos obtener diferente información según lo que nos pida el cliente, debemos crear diferentes funciones.

    def get_list_drugs(self, drogas):  # para obtener la lista de medicamentos
        list_drugs = []

        for i in range(len(
                drogas['results'])):  # realizamos un bucle que itere por todos los elementos del diccionario 'drogas'.
            info = drogas['results'][i]

            if info['openfda']:  # Nos aseguramos de que exista el campo openfda para el medicamento
                # que vamos a añadir a la lista de medicamentos, ya que si no, nos daría KeyError
                nombre = info['openfda']['generic_name'][0]
            else:
                id = info['id']
                nombre = 'El medicamento con ID ' + id + ', no tiene nombre genérico.'

            list_drugs.append(nombre)  # añadimos el valor de la variable nombre a nuestra lista.

        return list_drugs

    # Las demás funciones realizan la misma tarea.

    def get_list_companies(self, drogas):  # para obtener el nombre de los fabricantes.
        list_companies = []

        for i in range(len(drogas['results'])):
            info = drogas['results'][i]

            if info['openfda']:
                company = info['openfda']['manufacturer_name'][0]
            else:
                id = info['id']
                company = 'El medicamento con ID ' + id + ', no tiene especificado el fabricante.'

            list_companies.append(company)

        return list_companies

    def get_warnings(self, drogas):  # para obtener las advertencias acerca de los medicamentos.
        list_warnings = []

        for i in range(len(drogas['results'])):
            info = drogas['results'][i]
            id = info['id']

            if 'warnings' in info:
                advertencia = '(ID: ' + id + ')' + info['warnings'][0]
            else:
                advertencia = 'No se especifican advertencias sobre el medicamento con ID ' + id

            list_warnings.append(advertencia)

        return list_warnings

    def get_search(self,
                   drogas):  # para obtener el nombre del medicamento al que su campo 'active_ingredient' o 'manufacturer_name' coincida con lo pedido por el cliente.

        drugs = []
        for i in range(len(drogas['results'])):
            info = drogas['results'][i]
            if info['openfda']:
                nombre = info['openfda']['generic_name'][0]
            else:
                id = info['id']
                nombre = 'El medicamento con ID ' + id + ', no tiene nombre genérico.'

            drugs.append(nombre)

        return drugs


class OpenFDAHTML():

    # creamos la clase OpenfdaHTML en el que crearemos las páginas html que el servidor enviará como respuesta a nuestro cliente.

    def menu_page(self):
        html = """
        <!DOCTYPE html>
        <html>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 

        <head>
        <title> Menú OpenFDA </title>
        </head>

        <body>
        <h1>Menú OpenFDA</h1>

        <form method="get" action ="searchDrug">
        Buscar medicamentos según su principio activo: <input name="active_ingredient" type="text"> <input type="submit">
        </form>

        <form method="get" action = "searchCompany">
        Buscar medicamentos según su fabricante: <input name="company" type="text"> <input type = "submit">
        </form>

        <form method="get" action = "listDrugs">
        Para una lista de medicamentos, escoga el límite: <input name="limit" type="text"> <input type = "submit">
        </form>

        <form method="get" action = "listCompanies">
        Para una lista de fabricantes, escoga el límite: <input name="limit" type="text"> <input type = "submit">
        </form>

        <form method="get" action = "listWarnings">
        Para una lista de advertencias sobre medicamentos, escoga el límite: <input name="limit" type="text"> <input type = "submit">
        </form>

        </body>

        </html>
        """
        return html

    # La línea de código <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    # es necesaria para que el programa pueda escribir las tildes, entre otros elementos.
    # 'action' nos indica la ruta del recurso pedido por el cliente.
    # 'input' relaciona la variable de nuestro código para obtener el parámetro de la API con la url a la que se enviará la información.
    # El valor de esta variable será designado por el cliente,
    # finalmente, 'submit' envía la información.

    def drug_page(self, medicamentos):
        html = """
        <!DOCTYPE html>
        <html>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 
        <head>
        <title> OpenFDA Data </title>
        </head>
        <h1>Los datos obtenidos se muestran a continuación: </h1>
        <ul>"""
        for i in medicamentos:
            html = html + "<li>" + i + "</li>"
        """</ul>
        </html>
        """
        return html

    # en este html, realizamos un bucle for para iterar por la lista de elementos e ir escribiéndolos en forma de lista con las etiquetas <ul>,
    #  y <li> para colocar cada elemento en un punto.


class testHTTPRequestHandler(
    http.server.BaseHTTPRequestHandler):  # La clase testHTTPRequestHandler hereda todos los métodos de la clase http.server.BaseHTTPRequestHandler.

    def do_GET(self):

        response = 200
        header1 = 'Content-type'
        header2 = 'text/html'

        # estos son los valores que por defecto van a adquirir el estado de la respuesta y las cabeceras.
        # las cabeceras indican el tipo de contenido que el cliente va a recibir como respuesta.

        print('RECURSO SOLICITADO: ', self.path)

        try:

            if self.path == "/":
                html = OpenFDAHTML.menu_page(self)  # en este caso simplemente creamos la página web inicial.

            elif "/listDrugs" in self.path:
                limite = self.path.split("=")[1]  # especificamos qué es 'limit' en la ruta /listDrugs,
                # que corresponde al parámetro limit que hay que pasarle a nuestra función cliente
                # para que obtenga la información de la API OPENFDA.
                pagina = OpenFDAClient.get_drugs(self,
                                                 limite)  # obtenemos el diccionario del recurso solicitado y lo guaramos en la variable 'pagina'.
                medicamentos = OpenFDAParser.get_list_drugs(self,
                                                            pagina)  # obtenemos y guardamos la información que queremos sobre el diccionario que hemos obtenido previamente, y
                # guardamos esta información en la variable medicamentos.
                html = OpenFDAHTML.drug_page(self,
                                             medicamentos)  # finalmente, creamos una estructura html para mostrar la información al cliente, pasándole la información
                # de 'medicamentos', para que se implemente en nuestra página html.

            elif "/listCompanies" in self.path:
                limite = self.path.split("=")[1]
                pagina = OpenFDAClient.get_drugs(self, limite)
                medicamentos = OpenFDAParser.get_list_companies(self, pagina)
                html = OpenFDAHTML.drug_page(self, medicamentos)

            elif "/listWarnings" in self.path:
                limite = self.path.split("=")[1]
                pagina = OpenFDAClient.get_drugs(self, limite)
                medicamentos = OpenFDAParser.get_warnings(self, pagina)
                html = OpenFDAHTML.drug_page(self, medicamentos)

            elif "/searchCompany" in self.path:
                fabricante = self.path.split("?")[1].split("=")[1].split("&")[0]
                pagina = OpenFDAClient.get_companies(self, fabricante)
                fabricantes = OpenFDAParser.get_search(self, pagina)
                html = OpenFDAHTML.drug_page(self, fabricantes)

            elif "/searchDrug" in self.path:
                ppio_activo = self.path.split("?")[1].split("=")[1].split("&")[0]
                pagina = OpenFDAClient.get_active_ingredient(self, ppio_activo)
                medicamentos = OpenFDAParser.get_search(self, pagina)
                html = OpenFDAHTML.drug_page(self, medicamentos)

            elif "/redirect" in self.path:
                response = 302        # este código significa un redireccionamiento temporal.
                header1 = 'Location'  # nos redirige a la localización que nosotros insertemos en el header 2.
                header2 = 'http://localhost:8000' # en nuestro caso, nos redirige a la página principal.

            elif "/secret" in self.path:
                response = 401               # envía un error con el código 401, que significa no autorizado a acceder a la página.
                header1 = 'WWW-Authenticate' # para poder acceder a la página, es necesario una autentificación.
                header2 = 'Basic realm = "openfda"' # en este caso, la autentificación será "openfda"
                self.send_error(401)     # se manda una página error al cliente, explicando el motivo (error 401)

            else:
                response = 404       # en el caso de que la ruta no coincida con ninguno de los recursos, se enviará un
                                     # error 404 not found (send_error), indicando que es porque el recurso pedido no existe.
                self.send_error(404)

        except:
            response = 404
            self.send_error(404)

        # la estructura try/except es para manejar también los errores que se puedan dar en los parámetros, como que se
        # mande un ingrediente activo que no exista, o un string como valor de límite.

        self.send_response(response)  # cabecera que envía el estado de la respuesta
        self.send_header(header1, header2)  # Después enviamos las cabeceras necesarias para que el cliente entienda el
        # contenido que le enviamos (que sera HTML)
        self.end_headers()
        if response == 200:
            self.wfile.write(bytes(html,
                                   "utf8"))  # Como solo tenemos contenido html en caso de que la respuesta sea 200 OK, creamos un if.

        # self. send_error envía una respuesta de error al cliente, donde el número (404,401...) especifica el código de error http.


# servidor:

PORT = 8000
Handler = testHTTPRequestHandler

# Creamos el socket que esperará las peticiones de los clientes.
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

try:
    httpd.serve_forever()  # el servidor recibirá y establecerá conexión con todos los clientes
except KeyboardInterrupt:
    print("Interrumpido por el usuario.")  # Solo parará en caso de que el usuario lo decida.

print("Servidor parado")
httpd.close()

# bibliografia
# función self.send_error y self.send_response: https://docs.python.org/2/library/basehttpserver.html#BaseHTTPServer.BaseHTTPRequestHandler
# esctructura html: https://www.w3schools.com/tags/att_form_action.asp, https://www.w3schools.com/tags/tag_form.asp,
# estructura html: https://www.w3schools.com/tags/tag_ol.asp, https://www.w3schools.com/tags/tag_title.asp, https://www.w3schools.com/tags/tag_li.asp
# información redirect: https://www.inboundcycle.com/blog-de-inbound-marketing/que-son-las-redirecciones-301-y-302-y-como-configurarlas
# información error 401 https://es.wikipedia.org/wiki/Autenticaci%C3%B3n_de_acceso_b%C3%A1sica