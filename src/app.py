from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config

app=Flask(__name__)
CORS(app)

con=MySQL(app)

#Metodo para registrar usuarios
@app.route('/user_registration',methods=['POST'])
def registrar_usuario():
    try:
        datos = request.get_json()
        user=leer_usuarios_db(datos.get('email'), datos.get('password'))
        print("parametro1:", datos.get('email'))
        print("parametro2:", datos.get('password'))
        
        if user != None:
            return jsonify({'mensaje':'El correo ya esta registrado', 'exito':False})
        else: 
            cursor=con.connection.cursor()
            sql="""INSERT INTO usuarios(email,password)
            VALUES('{0}','{1}')""".format(datos.get('email'),datos.get('password'))
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':'Usuario registrado', 'exito':True})
                                                        
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':False})

#Metodo para detectar usuarios
def leer_usuarios_db(email_user, password):
    try:
        cursor = con.connection.cursor()
        sql = 'select * from usuarios where email = "{0}" and password = "{1}"'.format(email_user, password)
        cursor.execute(sql)
        datos = cursor.fetchone()

        if datos != None:
            usuario = {'id_user':datos[0],'nickname':datos[1],'email':datos[2],'password':datos[3],'number_phone':datos[4]}
            return usuario
        else: 
            return None
    

    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':True})

#Metodo para obtener el usuario para su validacion
@app.route('/user',methods=['GET'])
def leer_alumno():
    try:
        email_user = request.args.get('email')
        password = request.args.get('password')
        user=leer_usuarios_db(email_user, password)

        if user != None:
            return jsonify({'mensaje':'Usuario encontrado', 'exito':True})
        else:
            return jsonify({'mensaje':'Usuario no encontrado', 'exito':False})  
              
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':False})
    
#Metodo para obtener las peliculas
@app.route('/movies',methods=['GET'])
def obtener_peliculas():
    try:
        cursor = con.connection.cursor()
        sql = 'select * from movies'
        cursor.execute(sql)
        datos=cursor.fetchall()
        peliculas=[]
        for fila in datos:
            pelicula={'id':fila[0],'titulo':fila[1],'fecha':fila[2],'genero':fila[3],'sinopsis':fila[4],'estudio':fila[5], 'banner':fila[6]}
            peliculas.append(pelicula)
            print(pelicula)
        return jsonify({'peliculas':peliculas, 'mensaje':'lista de Peliculas', 'exito':True})
              
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':False})

#Metodo para registrar una pelicula
@app.route('/movie_registration',methods=['POST'])
def registrar_pelicula():
    try:
        datosPelicula = request.get_json()
        cursor=con.connection.cursor()
        sql="""INSERT INTO movies(title,date,genre,description,studio,banner)
        VALUES('{0}','{1}','{2}','{3}','{4}','{5}')""".format(datosPelicula.get('titulo'),datosPelicula.get('fecha'),datosPelicula.get('genero'),datosPelicula.get('sinopsis'),datosPelicula.get('estudio'),datosPelicula.get('imagen'))
        cursor.execute(sql)
        con.connection.commit()
        return jsonify({'mensaje':'Pelicula registrada', 'exito':True})
                                                        
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':False})
    
#Metodo para borrar una Pelicula
@app.route('/movie_delete',methods=['POST'])
def eliminar_pelicula():
    try:
        datosPelicula = request.get_json()
        cursor=con.connection.cursor()
        sql="""DELETE FROM movies WHERE id_movie = {0}""".format(datosPelicula.get('id'))
        cursor.execute(sql)
        con.connection.commit()
        return jsonify({'mensaje':'Pelicula eliminada', 'exito':True})
                                                        
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':False})
    
#Metodo para modificar una Pelicula
@app.route('/movie_edit',methods=['POST'])
def modificar_pelicula():
    try:
        datosPelicula = request.get_json()
        cursor=con.connection.cursor()
        sql="""UPDATE movies SET title='{0}', date={1}, genre='{2}', description='{3}', studio='{4}', banner='{5}' WHERE id_movie = {6}
        """.format(datosPelicula.get('titulo'),datosPelicula.get('fecha'),datosPelicula.get('genero'),datosPelicula.get('sinopsis'),datosPelicula.get('estudio'),datosPelicula.get('imagen'),datosPelicula.get('id'),)
        cursor.execute(sql)
        con.connection.commit()
        return jsonify({'mensaje':'Pelicula eliminada', 'exito':True})
                                                        
    except Exception as ex:
        return jsonify({'mensaje':'error {}'.format(ex), 'exito':False})

@app.route('/subir-archivo',methods=['POST'])
def guardar_imagen():

    return jsonify({'error': 'No se proporcionó ningún archivo'}), 400

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>"

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()