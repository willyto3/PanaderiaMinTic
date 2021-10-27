from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
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
    contrasena = None
    form = LoginForm()
    # Validacion de los datos ingresados
    if form.validate_on_submit():
        celular = form.celular.data
        form.celular.data = ''
        contrasena = form.contrasena.data
        form.contrasena.data = ''

    return render_template('/login.html', form=form, celular=celular, contrasena=contrasena)

# Pagina de Registro


@app.route('/Registro')
def registro():
    form=RegistroForm()

    return render_template('registro.html', form=form)

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
    flash('Registro creado exitosamente')
    return render_template('registro.html')


# Funcion Ingresar
@app.route('/ingresar', methods=['POST'])
def ingreso():
    return render_template('index.html')

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
    celular = StringField('Celular', validators=[
                          DataRequired(), Length(min=10, max=10)])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    remember=BooleanField('Recuerdame')
    submit = SubmitField('Ingresar')

# Formulario de Registro


class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    direccion = StringField('Direccion', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    fechanacimiento = StringField(
        'Fecha de Nacimiento', validators=[DataRequired()])
    celular = StringField('Celular', validators=[
                          DataRequired(), Length(min=10, max=10)])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    contrasena2 = PasswordField('Verificar Contraseña', validators=[
                                DataRequired(), EqualTo('contrasena')])
    submit = SubmitField('Registrar')
