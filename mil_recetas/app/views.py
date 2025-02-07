from flask import render_template, jsonify, request, redirect, url_for, flash
from flask_cors import CORS
from app import app
from app.models import Receta, Usuario, RecetaGuardada
from werkzeug.utils import secure_filename
import os
from config import bcrypt
from flask_login import login_user, logout_user, login_required, current_user

EXTENSIONES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'webp', 'jfif'}
CARPETA_STATIC = os.path.join(os.path.dirname(app.root_path), 'app', 'static')
CARPETA_SUBIDA = os.path.join(CARPETA_STATIC, 'uploads', 'recetas')
app.config['UPLOAD_FOLDER'] = CARPETA_SUBIDA

CORS(app)

def archivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS

@app.route('/crear-receta', methods=['POST', 'GET'])
def crear_receta():
    if not current_user.is_authenticated:
        flash('Debe iniciar sesión para crear una receta', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            if 'ruta_imagen' not in request.files or request.files['ruta_imagen'].filename == '':
                return jsonify({'error': 'No se seleccionó ningún archivo o el archivo está vacío'}), 400
            
            file = request.files['ruta_imagen']
            if file and archivo_permitido(file.filename):
                filename = secure_filename(file.filename)
                img_folder = app.config['UPLOAD_FOLDER']
                os.makedirs(img_folder, exist_ok=True)
                file.save(os.path.join(img_folder, filename))

                nueva_receta = Receta(
                    nombre_receta=request.form['nombre_receta'],
                    autor=current_user.nombre_usuario,
                    descripcion=request.form['descripcion'],
                    categoria=request.form['categoria'],
                    ruta_imagen=filename
                )
                nueva_receta.guardar()
                return jsonify({'redirect': url_for('ver_receta', id_receta=nueva_receta.id_receta)})
            else:
                return jsonify({'error': 'El archivo adjunto no es válido'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return render_template('crear-receta.html', title='Crear receta | MilRecetas')

@app.route('/recetas/<int:id_receta>')
def ver_receta(id_receta):
    receta = Receta.mostrar_por_id(id_receta)
    if receta:
        es_autor = current_user.is_authenticated and current_user.nombre_usuario == receta.autor
        receta_guardada = current_user.is_authenticated and RecetaGuardada.esta_guardada(current_user.id_usuario, id_receta)
        title = f"{receta.nombre_receta} | MilRecetas"
        return render_template('recetas/receta.html', receta=receta, es_autor=es_autor, receta_guardada=receta_guardada, title=title)
    else:
        return redirect(url_for('not_found'))

@app.route('/recetas/')
def mostrar_recetas():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    offset = (page - 1) * per_page
    recetas = Receta.mostrar_todas(offset=offset, limit=per_page)
    total_recetas = Receta.contar_todas()
    
    recetas_obj = [Receta(**receta_dict) for receta_dict in recetas]
    
    pagination_info = {
        'page': page,
        'per_page': per_page,
        'total': total_recetas,
        'total_pages': (total_recetas + per_page - 1) // per_page,
    }
    
    return render_template('recetas/lista-receta.html', recetas=recetas_obj, pagination=pagination_info, title='Todas las recetas | MilRecetas')

@app.route('/eliminar-receta/<int:id_receta>', methods=['GET', 'POST'])
def eliminar_receta(id_receta):
    receta = Receta.mostrar_por_id(id_receta)

    if not receta:
        return redirect(url_for('not_found'))
    
    if request.method == 'POST':
        receta.borrar()
        return redirect(url_for('profile'))
    
    return render_template('confirmar-eliminacion.html', receta=receta, title='Eliminar receta | MilRecetas')

@app.route('/editar/<int:id_receta>', methods=['GET', 'POST'])
def editar_receta(id_receta):
    receta = Receta.mostrar_por_id(id_receta)
    if not receta:
        return redirect(url_for('not_found'))
    if request.method == 'POST':
        receta.nombre_receta = request.form['nombre_receta']
        receta.descripcion = request.form['descripcion']
        receta.categoria = request.form['categoria']
        if 'ruta_imagen' in request.files:
            imagen = request.files['ruta_imagen']
            if imagen.filename != '':
                pass
        receta.guardar()
        return redirect(url_for('ver_receta', id_receta=id_receta))
    return render_template('editar-receta.html', receta=receta, title='Editar receta | MilRecetas')

@app.route('/api/recetas/<int:id_receta>', methods=['GET', 'PUT'])
def get_receta(id_receta):
    if request.method == 'PUT':
        receta = Receta.mostrar_por_id(id_receta)
        if not receta:
            return redirect(url_for('not_found'))
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
    else:
        receta = Receta.mostrar_por_id(id_receta)
        if receta:
            return jsonify(receta.serializar())
        else:
            return redirect(url_for('not_found'))

@app.route('/registro', methods=['POST'])
def crear_usuario():
    datos_usuario = request.form 

    nombre_usuario = datos_usuario.get('nombre_usuario')
    email = datos_usuario.get('email')
    password = datos_usuario.get('password')
    confirmar = datos_usuario.get('confirm')

    if not nombre_usuario or not email or not password or not confirmar:
        flash('Todos los campos deben ser completados', 'warning')
    
    if password != confirmar:
        flash('La contraseña y la confirmación no coinciden', 'warning')

    nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, email=email, password=password)

    try:
        Usuario.guardar(nuevo_usuario)
        return redirect(url_for('index'))
    except Exception as e:
        flash('Error al crear el usuario', 'error')
    
@app.route('/ingresar', methods=['POST'])
def ingresar_cuenta():
    datos_usuario = request.form

    nombre_usuario = datos_usuario.get('nombre_usuario')
    password = datos_usuario.get('password')

    if not nombre_usuario or not password:
        flash('Debe ingresar nombre de usuario y contraseña', 'warning')

    usuario = Usuario.obtener_por_nombre_usuario(nombre_usuario)
    if usuario and bcrypt.check_password_hash(usuario['password'], password):
        user_instance = Usuario(id_usuario=usuario['id_usuario'], nombre_usuario=usuario['nombre_usuario'], email=usuario['email'], password=usuario['password'])
        login_user(user_instance)
        return redirect(url_for('index'))
    else:
        flash('Nombre de usuario o contraseña incorrectos', 'danger')
        return redirect(url_for('login'))
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', title='MilRecetas | Guarda y comparte recetas')

@app.route('/ingresar')
def login():
    return render_template('ingresar.html', title='Ingresa a tu cuenta | MilRecetas')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html', title='Contacto | MilRecetas')

@app.route('/preguntas-frecuentes')
def faq():
    return render_template('faq.html', title='Preguntas frecuentes | MilRecetas')

@app.route('/sobre-nosotros')
def nosotros():
    return render_template('nosotros.html', title='Sobre nosotros | MilRecetas')

@app.route('/registro')
def registro():
    return render_template('registro.html', title='Registrate | MilRecetas')

@app.route('/mi-perfil')
@login_required
def profile():
    recetas_usuario = Receta.mostrar_por_autor(current_user.nombre_usuario)
    recetas_guardadas = RecetaGuardada.mostrar_por_usuario(current_user.id_usuario)
    return render_template('perfil.html', recetas=recetas_usuario,
                            recetas_guardadas=recetas_guardadas,  
                            nombre_usuario=current_user.nombre_usuario,
                            email=current_user.email,
                            title='Mi perfil | MilRecetas')

@app.route('/guardar_receta/<int:id_receta>', methods=['POST'])
@login_required
def guardar_receta(id_receta):
    if RecetaGuardada.esta_guardada(current_user.id_usuario, id_receta):
        RecetaGuardada.eliminar(current_user.id_usuario, id_receta)
        return jsonify({'guardada': False})
    else:
        receta_guardada = RecetaGuardada(current_user.id_usuario, id_receta)
        receta_guardada.guardar()
        return jsonify({'guardada': True})

@app.route('/receta_guardada/<int:id_receta>', methods=['GET'])
@login_required
def receta_guardada(id_receta):
    return jsonify({
        'guardada': RecetaGuardada.esta_guardada(current_user.id_usuario, id_receta)
    })

@app.route('/404/')
def not_found():
    return render_template('error.html', title='Error 404 | MilRecetas')