from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Modelo
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(70), unique=True)
    descripcion = db.Column(db.String(100))
    
    def __init__(self, titulo, descripcion):
        self.titulo = titulo
        self.descripcion = descripcion

db.create_all()

class TareaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'titulo', 'descripcion')

tarea_schema = TareaSchema()
tareas_schema = TareaSchema(many=True)

# Rutas
@app.route('/', methods=['GET'])
def index():
    return jsonify('mensagge': 'Welcome')

@app.route('/tarea', methods=['POST'])
def create_tarea():
    titulo = request.json['titulo']
    descripcion = request.json['descripcion']
    new_task = Tarea(titulo, descripcion)
    db.session.add(new_task)
    db.session.commit()
    return tarea_schema.jsonify(new_task)

@app.route('/tareas', methods=['GET'])
def get_tareas():
    all_tareas = Tarea.query.all()
    res = tareas_schema.dump(all_tareas)
    return jsonify(res)

@app.route('/tarea/<id>', methods=['GET'])
def get_tarea(id):
    tarea = Tarea.query.get(id)
    res = tarea_schema.dump(tarea)
    return jsonify(res)

@app.route('/tarea/<id>', methods=['PUT'])
def update_tarea(id):
    tarea = Tarea.query.get(id)

    titulo = request.json['titulo']
    descripcion = request.json['descripcion']

    tarea.titulo = titulo
    tarea.descripcion = descripcion

    db.session.commit()
    return tarea_schema.jsonify(tarea)

@app.route('/tarea/<id>', methods=['DELETE'])
def delete_tarea(id):
    tarea = Tarea.query.get(id)
    db.session.delete(tarea)
    db.session.commit()
    return tarea_schema.jsonify(tarea)

if __name__ == '__main__':
    app.run(debug=True, port=5000) #debug=True -> reinicio

 