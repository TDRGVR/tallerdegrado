from flask import Flask
from flask import request
import psycopg2
from psycopg2.extras import RealDictCursor
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

## Conectividad a la base de datos
def Conexion():
  return psycopg2.connect(host="ec2-23-21-4-7.compute-1.amazonaws.com",database="d788louhdpbuak", user="sbnbneejrneocn", password="01d52cb0709999b659de360be58f509abbb4539b0270ad612af8af6af0116c42")

## Conectividad a la base de datos local, para pruebas
##  return psycopg2.connect(host="",database="", user="", password="")

@app.route('/')
def inicio():
  return "Hola mundo 2"


##Login



##Fin login


##Inicio CU2: Materias

@app.route('/getListaMaterias', methods=["POST"])
def getListaMaterias():
  conn = Conexion()
  cursor1=conn.cursor(cursor_factory=RealDictCursor)

  sql="select *from materia where idprofesor=%s"
  datos=(request.form['id'],)

  cursor1.execute(sql,datos)
  conn.commit()
  resultado = cursor1.fetchall()
  conn.close()
  cursor1.close()
  return json.dumps(resultado)

##Fin CU2: Materias


@app.route('/getPadreFamilia', methods=["GET"])
def getPadreFamilia():
  conn = Conexion()
  cursor1=conn.cursor(cursor_factory=RealDictCursor)
  cursor1.execute("select *from padrefamilia")
  resultado = cursor1.fetchall()
  conn.close()
  cursor1.close()
  return json.dumps(resultado)

##Inicio CU7: Vincular cuenta
@app.route('/setDatosEstudiante', methods=["POST"])
def setDatosEstudiante():
  conn = Conexion()
  cursor1=conn.cursor()
  sql="insert into alumno(id,nombre,apellido,direccion,idpadre1,idpadre2) values(%s,%s,%s,%s,%s,null)"
  datos=(request.form['id'], request.form['nombre'],request.form['apellido'],request.form['dir'],request.form['idpadre1'])
  try:
    cursor1.execute(sql, datos)
    conn.commit()
    conn.close()
    cursor1.close()
    return "1"
  except Exception as err:
    return "0"

@app.route('/setDatosProfesor', methods=["POST"])
def setDatosProfesor():
  conn = Conexion()
  cursor1=conn.cursor()
  sql="insert into profesor(id,nombre,apellido,especialidad,telefono) values (%s,%s,%s,%s,%s)"
  datos=(request.form['id'], request.form['nombre'],request.form['apellido'],request.form['especialidad'],request.form['telefono'])
  try:
    cursor1.execute(sql, datos)
    conn.commit()
    conn.close()
    cursor1.close()
    return "1"
  except Exception as err:
    return "0"

##Fin CU7: Vincular cuenta


## Aplicacion del PNL
@app.route('/api', methods=["POST"])
def funcion():
  Content = request.form['texto']
  sid = SentimentIntensityAnalyzer()
  txt2 = TextBlob( Content )
  txt3 = txt2.translate()
  resultado = sid.polarity_scores(str(txt3))
  return json.dumps(resultado)

if __name__ == "__main__":
  app.run(debug=True)