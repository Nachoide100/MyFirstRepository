#Líneas de código para levantar un servidor en nuestro ordenador web con Flask
from flask import Flask, render_template, request, redirect, url_for
import db
from models import Tarea

app = Flask(__name__)

#Definición de rutas
@app.route("/") #ruta principal solo con la raíz
def home(): #obligatorio una función debajo
    todas_las_tareas = db.session.query(Tarea).all()
    print(todas_las_tareas)
    return render_template("index.html", lista_de_tareas=todas_las_tareas)

@app.route("/crear-tarea", methods=["POST"])
def crear():
    contenido = request.form["contenido_tarea"]
    print(contenido)
    tarea = Tarea(contenido=contenido, hecha=False)
    db.session.add(tarea)
    db.session.commit()
    return  redirect(url_for("home")) #nos redirige a la página principal, función home

@app.route("/eliminar-tarea/<id>")
def eliminar(id):
    db.session.query(Tarea).filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/tarea-hecha/<id>")
def hecha(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    tarea.hecha = not(tarea.hecha)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    db.Base.metadata.create_all(bind=db.engine)
    app.run(debug=True)


