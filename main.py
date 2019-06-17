import random
import datetime
import json
from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])

def index():

    if request.method == "GET":
        nombre = request.cookies.get("nombre")
        apellido = request.cookies.get("apellido")
        intentos = request.cookies.get("intentos") #cogemos nombre, apellidos y número de intentos desde cookies

        return render_template("index.html", nombre=nombre, apellido=apellido, intentos=intentos)

    if request.method == "POST":

        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        oculto = request.cookies.get("oculto")
        intentos = '0' #empieza el juego intentos a cero

        response = make_response(render_template("index.html", nombre=nombre, apellido=apellido, intentos=intentos))
        response.set_cookie("nombre", nombre)
        response.set_cookie("apellido", apellido)
        response.set_cookie("intentos", str(intentos)) #mandamos nombre, apellidos e intentos para recuento y mensajes


        if not oculto:
            nuevo_oculto = random.randint(1, 20)
            response.set_cookie("oculto", str(nuevo_oculto)) # si es la primera vez que llega aquí generamos oculto

        return response


@app.route("/result", methods=["POST"])
def result():
    secreto_usuario = int(request.form.get("secreto_usuario"))
    oculto = int(request.cookies.get("oculto"))
    nombre = request.cookies.get("nombre")
    fecha = datetime.date.today()

    if secreto_usuario == oculto:
        intentos = request.cookies.get("intentos")
        new_intentos = int(intentos) + 1 # generamos nuevo numero de intentos desde la cookie + 1
        mensaje = "Muy bien {0}, acertaste, efectivamente era {1}".format(str(nombre),str(oculto))
        palmares = "Acertaste en {0} intentos".format(str(new_intentos))
        hoy = fecha.strftime('%d-%b-%Y')

        # creamos lista de resultados desde el archivo de texto
        with open("score_list.txt", "r") as score_file:
            score_list = json.loads(score_file.read())


        score_list.append({"Intentos": new_intentos, "Fecha": hoy, "Nombre": nombre})

        with open("score_list.txt", "w") as score_file:
            score_file.write(json.dumps(score_list))

        # ordenamos la lista de resultados por intentos pero solo guardamos los tres mejores resultados
        new_score_list = sorted(score_list, key=lambda k: k['Intentos'])
        del new_score_list[10:]

        for score_dict in new_score_list:
            score_text = "{0} encontro en {1} intentos el {2}.".format(score_dict.get("Nombre"),
                                                                           str(score_dict.get("Intentos")),
                                                                           score_dict.get("Fecha"))


        response = make_response(render_template("result.html", score_text=score_text, mensaje=mensaje, nombre=nombre, new_intentos=new_intentos, intentos=intentos, palmares=palmares, new_score_list=new_score_list))
        response.set_cookie("oculto", str(random.randint(1, 20)))
        response.set_cookie("intentos", str(0))

        return response


    elif secreto_usuario > oculto:
        intentos = request.cookies.get("intentos")
        new_intentos = int(intentos) + 1 # añadimos un intento
        mensaje = "No {0}, el numero secreto es más pequeño".format(str(nombre))
        response = make_response(render_template("result.html", mensaje=mensaje, nombre=nombre, new_intentos=new_intentos))
        response.set_cookie("intentos", str(new_intentos)) #actualizamos cookie de intentos

        return response

    elif secreto_usuario < oculto:
        intentos = request.cookies.get("intentos")
        new_intentos = int(intentos) + 1
        mensaje = "No {0}, el número secreto es más grande".format(str(nombre))
        response = make_response(render_template("result.html", mensaje=mensaje, nombre=nombre, new_intentos=new_intentos))
        response.set_cookie("intentos", str(new_intentos))

        return response

if __name__ == '__main__':
    app.run(debug=True)