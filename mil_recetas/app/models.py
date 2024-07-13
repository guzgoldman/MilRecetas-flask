from app import get_db
from config import bcrypt
from flask_login import UserMixin
import mysql.connector

class Receta:
    def __init__(self, nombre_receta, descripcion, categoria, ruta_imagen, autor=None, id_receta=None):
        self.id_receta = id_receta
        self.nombre_receta = nombre_receta
        self.autor = autor
        self.descripcion = descripcion
        self.categoria = categoria
        self.ruta_imagen = ruta_imagen

    def guardar(self):
        db = get_db()
        with db.cursor() as cursor:
            if self.id_receta:
                query = """
                UPDATE recetas SET nombre_receta = %s, autor = %s, descripcion = %s, categoria = %s, ruta_imagen = %s
                WHERE id_receta = %s
                """
                valores = (self.nombre_receta, self.autor, self.descripcion, self.categoria, self.ruta_imagen, self.id_receta)
            else:
                query = """
                INSERT INTO recetas (nombre_receta, autor, descripcion, categoria, ruta_imagen) 
                VALUES (%s, %s, %s, %s, %s)
                """
                valores = (self.nombre_receta, self.autor, self.descripcion, self.categoria, self.ruta_imagen)
            cursor.execute(query, valores)
            self.id_receta = cursor.lastrowid
            db.commit()

    @staticmethod
    def mostrar_todas():
        db = get_db()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id_receta, nombre_receta, autor, descripcion, categoria, ruta_imagen FROM recetas")
            resultados = cursor.fetchall()
            return resultados
    
    @staticmethod
    def mostrar_por_id(id_receta):
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id_receta, nombre_receta, autor, descripcion, categoria, ruta_imagen FROM recetas WHERE id_receta = %s", (id_receta,))
            result = cursor.fetchone()
            if result:
                return Receta(**result)
            return None
        
    @staticmethod
    def mostrar_por_autor(autor):
        db = get_db()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id_receta, nombre_receta, descripcion, categoria FROM recetas WHERE autor = %s", (autor,))
            resultados = cursor.fetchall()
            return resultados
    
    def borrar(self):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM recetas WHERE id_receta = %s", (self.id_receta,))
            db.commit()

    def serializar(self):
        return {
            'id_receta': self.id_receta,
            'nombre_receta': self.nombre_receta,
            'autor': self.autor,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'ruta_imagen': self.ruta_imagen
        }
    
class Usuario(UserMixin):
    def __init__(self, nombre_usuario, email, password, id_usuario=None):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def guardar(self):
        db = get_db()
        with db.cursor() as cursor:
            if self.id_usuario:
                query = """
                UPDATE usuarios SET nombre_usuario = %s, email = %s, password = %s
                WHERE id_usuario = %s
                """
                valores = (self.nombre_usuario, self.email, self.password, self.id_usuario)
            else:
                query = """
                INSERT INTO usuarios (nombre_usuario, email, password) VALUES (%s, %s, %s)
                """
                valores = (self.nombre_usuario, self.email, self.password)
            cursor.execute(query, valores)
            self.id_usuario = cursor.lastrowid
            db.commit()

    def get_id(self):
        return self.id_usuario

    @staticmethod
    def mostrar_usuarios():
        with get_db().cursor() as cursor:
            cursor.execute("SELECT id_usuario, nombre_usuario, email FROM usuarios")
            rows = cursor.fetchall()
            return [Usuario(*row) for row in rows]
    
    @staticmethod
    def mostrar_usuario(id_usuario):
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id_usuario, nombre_usuario, email FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            result = cursor.fetchone()
            if result:
                return Usuario(**result)
            return None
    
    @staticmethod
    def mostrar_usuario_con_password(id_usuario):
        with get_db().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id_usuario, nombre_usuario, email, password FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            result = cursor.fetchone()
            if result:
                return Usuario(**result)
            return None
        
    @staticmethod
    def obtener_por_nombre_usuario(nombre_usuario):
        db = get_db()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id_usuario, nombre_usuario, email, password FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
            result = cursor.fetchone()

            if result:
                return result

        return None
    
    def borrar(self):
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (self.id_usuario,))
            db.commit()

    def serializar(self):
        return {
            'ID': self.id_usuario,
            'Nombre de usuario': self.nombre_usuario,
            'Email': self.email,
        }