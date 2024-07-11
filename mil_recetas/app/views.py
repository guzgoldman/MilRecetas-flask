from flask import render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
from app import app
from app.models import Receta
from werkzeug.utils import secure_filename
import os
from app import get_db

EXTENSIONES_PERMITIDAS = {'png', 'jpg', 'jpeg'}
CARPETA_STATIC = os.path.join(os.path.dirname(app.root_path), 'app', 'static')
CARPETA_SUBIDA = os.path.join(CARPETA_STATIC, 'uploads', 'recetas')
app.config['UPLOAD_FOLDER'] = CARPETA_SUBIDA

CORS(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def archivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS

def crear_receta():
    if 'ruta_imagen' not in request.files:
        return jsonify({'error': 'No se proporcionó ningún archivo'}), 400

    file = request.files['ruta_imagen']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400

    if file and archivo_permitido(file.filename):
        filename = secure_filename(file.filename)
        ruta_absoluta_carpeta = app.config['UPLOAD_FOLDER']
        os.makedirs(ruta_absoluta_carpeta, exist_ok=True)
        file.save(os.path.join(ruta_absoluta_carpeta, filename))

    nueva_receta = Receta(
        nombre_receta=request.form['nombre_receta'],
        autor=request.form['autor'],
        descripcion=request.form['descripcion'],
        categoria=request.form['categoria'],
        ruta_imagen=filename
    )
    nueva_receta.guardar()

    return jsonify({'message': 'Receta creada correctamente'}), 201

@app.route('/api/recetas/', methods=['GET'])
def mostrar_recetas():
    recetas = Receta.mostrar_todas()
    return jsonify([receta.serializar() for receta in recetas])

@app.route('/eliminar-receta')
def eliminar_receta():
    return render_template('eliminar-receta.html')

@app.route('/borrar/<int:id_receta>', methods=['POST'])
def eliminar_receta_por_id(id_receta):
    receta = Receta.mostrar_por_id(id_receta)
    if receta:
        receta.borrar()
        return jsonify({'message': 'Receta eliminada correctamente'}), 200
    else:
        return jsonify({'message': 'Receta no encontrada'}), 404
    
@app.route('/editar/<int:id_receta>', methods=['GET', 'POST'])
def editar_receta(id_receta):
    receta = Receta.mostrar_por_id(id_receta)
    if not receta:
        return jsonify({'message': 'Receta no encontrada'}), 404
    if request.method == 'POST':
        print("Método POST recibido en editar_receta")
        print(f"Datos del formulario: {request.form}")
        receta.nombre_receta = request.form['nombre_receta']
        receta.autor = request.form['autor']
        receta.descripcion = request.form['descripcion']
        receta.categoria = request.form['categoria']
        if 'ruta_imagen' in request.files:
            imagen = request.files['ruta_imagen']
            if imagen.filename != '':
                pass
        receta.guardar()
        return redirect(url_for('get_receta', id_receta=id_receta))
    return render_template('editar-receta.html', receta=receta)

@app.route('/api/recetas/<int:id_receta>', methods=['GET', 'PUT'])
def get_receta(id_receta):
    if request.method == 'PUT':
        receta = Receta.mostrar_por_id(id_receta)
        if not receta:
            return jsonify({'message':'Receta no encontrada'}), 404
        data = request.form
        receta.nombre_receta = data['nombre_receta']
        receta.autor = data['autor']
        receta.descripcion = data['descripcion']
        receta.categoria = data['categoria']
        if 'ruta_imagen' in request.files:
            imagen = request.files['ruta_imagen']
            if imagen.filename != '':
                pass 
        receta.guardar()
        return jsonify({'message':'Receta modificada correctamente'})
    else:
        receta = Receta.mostrar_por_id(id_receta)
        if receta:
            return jsonify(receta.serializar())
        else:
            return jsonify({'message': 'Receta no encontrada'}), 404

app.route('/api/recetas/', methods=['POST']) (crear_receta)

@app.route('/crear-receta')
def mostrar_formulario():
    return render_template('crear-receta.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingresar')
def login():
    return render_template('login.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/preguntas-frecuentes')
def faq():
    return render_template('faq.html')

@app.route('/sobre-nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/registro')
def registro():
    return render_template('register.html')