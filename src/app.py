from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder=template_dir)

# RUTAS DE LA APLICACION 
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM ETU")
    myresult = cursor.fetchall()
    # Convertir los datos a diccionario  
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()

    return render_template('index.html', data=insertObject)

# RUTA PARA GUARDAR USUARIOS EN LA BD
@app.route('/ETU', methods=['POST'])
def adduser():
    correo = request.form['Correo']
    nombre = request.form['Nombre']
    calificacion = request.form['Calificaciones']

    if correo and nombre and calificacion:
        cursor = db.database.cursor()
        sql = "INSERT INTO ETU (correo, nombre, calificacion) VALUES (%s, %s, %s)"
        data = (correo, nombre, calificacion)
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()
    return redirect(url_for('home'))

# RUTA PARA BORRAR UN REGISTRO
@app.route('/Borrar/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM ETU WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    cursor.close()
    return redirect(url_for('home'))

# RUTA PARA EDITAR UN REGISTRO
@app.route('/Editar/<string:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        correo = request.form['Correo']
        nombre = request.form['Nombre']
        calificacion = request.form['Calificaciones']

        if correo and nombre and calificacion:
            cursor = db.database.cursor()
            sql = "UPDATE ETU SET correo=%s, nombre=%s, calificacion=%s WHERE id=%s"
            data = (correo, nombre, calificacion, id)
            cursor.execute(sql, data)
            db.database.commit()
            cursor.close()
        return redirect(url_for('home'))
    else:
        cursor = db.database.cursor()
        sql = "SELECT * FROM ETU WHERE id=%s"
        cursor.execute(sql, (id,))
        data = cursor.fetchone()
        cursor.close()
        return render_template('edit.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, port=4000)