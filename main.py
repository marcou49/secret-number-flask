import random
from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])

def index():

    if request.method == "GET":
        nombre = request.cookies.get("nombre")
        apellido = request.cookies.get("apellido")

        return render_template("index.html", nombre=nombre, apellido=apellido)

    if request.method == "POST":

        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        oculto = request.cookies.get("oculto")

        response = make_response(render_template("index.html", nombre=nombre, apellido=apellido))
        response.set_cookie("nombre", nombre)
        response.set_cookie("apellido", apellido)

        if not oculto:  # if not, create a new cookie
            nuevo_oculto = random.randint(1, 20)
            response.set_cookie("oculto", str(nuevo_oculto))


        return response


@app.route("/result", methods=["POST"])
def result():
    secreto_usuario = int(request.form.get("secreto_usuario"))
    oculto = int(request.cookies.get("oculto"))
    nombre = request.cookies.get("nombre")

    if secreto_usuario == oculto:
        mensaje = "Muy bien {0}, acertaste".format(str(nombre))
        response = make_response(render_template("result.html", mensaje=mensaje, nombre=nombre))
        response.set_cookie("oculto", str(random.randint(1, 20)))

        return response

    elif secreto_usuario > oculto:
        mensaje = "Espabila {0} es más chico".format(str(nombre))
        return render_template("result.html", mensaje=mensaje, nombre=nombre)
    elif secreto_usuario < oculto:
        mensaje = "Espabila {0} es más tocho".format(str(nombre))
        return render_template("result.html", mensaje=mensaje, nombre=nombre)


if __name__ == '__main__':
    app.run()