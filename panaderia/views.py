from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.utils import secure_filename
from panaderia.models import *
from panaderia import app
import os

# Creacion de las Paginas

# Pagina Principal


@app.route('/')
def index():
    platos = Platos.query.all()
    return render_template('/index.html', platos=platos)

# Pagina de Inicio de Sesion


@app.route('/Login', methods=['GET', 'POST'])
def login():
    celular = None
    form = LoginForm()
    # Validacion de los datos ingresados
    if form.validate_on_submit():
        celular = form.celular.data
        form.celular.data = ''
        contrasena = form.contrasena.data
    
    return render_template('login.html', celular=celular, form=form)

# Pagina de Registro


@app.route('/Registro')
def registro():
    return render_template('registro.html')

# Pagina de Creacion de Platos


@app.route('/CrearPlatos')
def crearplatos():
    return render_template('crearplatos.html')


@app.route('/Busqueda')
def busqueda():
    return render_template('busqueda.html')


@app.route('/Menu')
def menu():
    platos = Platos.query.all()
    return render_template('menu.html', platos=platos)


@app.route('/Perfil')
def perfil():
    return render_template('perfil.html')


@app.route('/Carrito')
def carrito():
    return render_template('carrito.html')


@app.route('/Dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/Comentarios')
def comentarios():
    return render_template('comentarios.html')


@app.route('/Usuarios')
def usuarios():
    return render_template('usuarios.html')


def pagina_no_encontrada(error):
    return redirect(url_for('index'))


def error_de_servidor(error):
    return redirect(url_for('index'))

# FUNCIONES

# Funcion Crear Registro


@app.route('/crearregistro', methods=['POST'])
def create():

    if request.form['password_hash'] == request.form['password_hash2']:
        try:
            pw_hash = generate_password_hash(
                request.form['password_hash'], "sha256")
            persona = Personas(nombre=request.form['nombre'], apellido=request.form['apellido'],
                               direccion=request.form['direccion'], celular=request.form['celular'],
                               email=request.form['email'], fechanacimiento=request.form['fechanacimiento'],
                               password_hash=pw_hash)
            db.session.add(persona)
            db.session.commit()
            flash('Registro creado exitosamente')
            return render_template('registro.html')

        except Exception as e:
            flash("No se realizo el registro del Usuario")
            return render_template('registro.html')
    else:
        flash("Las Contraseñas deben ser iguales")
        return render_template('registro.html')


# Funcion Ingresar
@app.route('/ingresar', methods=['POST'])
def ingreso():

    try:
        persona = Personas.query.filter_by(
            celular=request.form['celular']).first()
        if persona and check_password_hash(persona.password_hash, request.form['contrasena']):
            return render_template('perfil.html')
        else:
            flash('Usuario o Contraseña incorrectos')
            return render_template('login.html')
    except Exception as e:
        flash('Usuario o Contraseña incorrectos')
        return render_template('login.html')

    # Funcion Crear Plato


@app.route('/crearplatos', methods=['POST'])
def crearplato():

    imagen = request.files['imagenplato']

    filename = secure_filename(imagen.filename)
    imagen.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    plato = Platos(nombreplato=request.form['nombreplato'], precioplato=request.form['precioplato'],
                   descripcionplato=request.form['descripcionplato'], nombreimagenplato=filename)
    db.session.add(plato)
    db.session.commit()
    flash('Registro creado exitosamente')
    return render_template('crearplatos.html')

# CLASES DE FORMULARIO

# Formulario de Login


class LoginForm(FlaskForm):
    celular = StringField('Celular', validators=[DataRequired()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')
