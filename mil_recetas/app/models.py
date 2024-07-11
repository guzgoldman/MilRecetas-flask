from app import get_db
class Receta:
    def __init__(self, nombre_receta, autor, descripcion, categoria, ruta_imagen, id_receta=None):
        self.id_receta = id_receta
        self.nombre_receta = nombre_receta
        self.autor = autor
        self.descripcion = descripcion
        self.categoria = categoria
        self.ruta_imagen = ruta_imagen

    def guardar(self):
        db = get_db()
        cursor = db.cursor()
        if self.id_receta:
            cursor.execute("""
                UPDATE recetas SET nombre_receta = %s, autor = %s, descripcion = %s, categoria = %s, ruta_imagen = %s
                WHERE id_receta = %s
                """, (self.nombre_receta, self.autor, self.descripcion, self.categoria, self.ruta_imagen, self.id_receta))
            db.commit()
        else:
            cursor.execute("""
                INSERT INTO recetas (nombre_receta, autor, descripcion, categoria, ruta_imagen) VALUES (%s, %s, %s, %s, %s)
                """, (self.nombre_receta, self.autor, self.descripcion, self.categoria, self.ruta_imagen))
            self.id_receta = cursor.lastrowid
            db.commit()
        cursor.close()

    @staticmethod
    def mostrar_todas():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM recetas")
        rows = cursor.fetchall()
        recetas = [Receta(id_receta=row[0], nombre_receta=row[1], autor=row[2], descripcion=row[3], categoria=row[4], ruta_imagen=row[5]) for row in rows]
        cursor.close()
        return recetas
    
    @staticmethod
    def mostrar_por_id(id_receta):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM recetas WHERE id_receta = %s", (id_receta,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return Receta(**result)
        return None
    
    def borrar(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM recetas WHERE id_receta = %s", (self.id_receta,))
        db.commit()
        cursor.close()

    def serializar(self):
        return {
            'id_receta': self.id_receta,
            'nombre_receta': self.nombre_receta,
            'autor': self.autor,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'ruta_imagen': self.ruta_imagen
        }