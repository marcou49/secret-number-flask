import random
from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])

def index():

    if request.method == "GET":
        nombre = request.cookies.get("nombre")
        apellido = request.cookies.get("apellido")
        intentos = request.cookies.get("intentos")

        return render_template("index.html", nombre=nombre, apellido=apellido, intentos=intentos)

    if request.method == "POST":

        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        oculto = request.cookies.get("oculto")
        intentos = '0'

        response = make_response(render_template("index.html", nombre=nombre, apellido=apellido, intentos=intentos))
        response.set_cookie("nombre", nombre)
        response.set_cookie("apellido", apellido)
        response.set_cookie("intentos", str(intentos))


        if not oculto:
            nuevo_oculto = random.randint(1, 5)
            response.set_cookie("oculto", str(nuevo_oculto))

        return response


@app.route("/result", methods=["POST"])
def result():
    secreto_usuario = int(request.form.get("secreto_usuario"))
    oculto = int(request.cookies.get("oculto"))
    nombre = request.cookies.get("nombre")

    if secreto_usuario == oculto:
        intentos = request.cookies.get("intentos")
        new_intentos = int(intentos) + 1
        mensaje = "Muy bien {0}, acertaste".format(str(nombre))
        palmares = "Acertaste en {0} intentos".format(str(new_intentos))
        response = make_response(render_template("result.html", mensaje=mensaje, nombre=nombre, new_intentos=new_intentos, intentos=intentos, palmares=palmares))
        response.set_cookie("oculto", str(random.randint(1, 5)))
        response.set_cookie("intentos", str(0))

        return response


    elif secreto_usuario > oculto:
        intentos = request.cookies.get("intentos")
        new_intentos = int(intentos) + 1
        mensaje = "Espabila {0} es más chico".format(str(nombre))
        response = make_response(render_template("result.html", mensaje=mensaje, nombre=nombre, new_intentos=new_intentos))
        response.set_cookie("intentos", str(new_intentos))

        return response

    elif secreto_usuario < oculto:
        intentos = request.cookies.get("intentos")
        new_intentos = int(intentos) + 1
        mensaje = "Espabila {0} es más tocho".format(str(nombre))
        response = make_response(render_template("result.html", mensaje=mensaje, nombre=nombre, new_intentos=new_intentos))
        response.set_cookie("intentos", str(new_intentos))

        return response

if __name__ == '__main__':
    app.run(debug=True)