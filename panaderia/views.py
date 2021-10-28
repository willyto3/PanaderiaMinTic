from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
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
    form = LoginForm()
    # Validacion de los datos ingresados
    if form.validate_on_submit():
        persona = Personas.query.filter_by(celular=form.celular.data).first()
        if persona and check_password_hash(persona.password_hash, form.contrasena.data):
            login_user(persona)
            flash(f'Ingreso Exitoso', 'success')
            return redirect(url_for('perfil'))
        else:
            flash(f'Ingreso Fallido. Por favor verificar Usuario y Contraseña.', 'danger')
    return render_template('login.html', form=form)

# Pagina de Registro


@app.route('/Registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()

    if form.validate_on_submit():
        try:
            persona = Personas(nombre=form.nombre.data, apellido=form.apellido.data, direccion=form.direccion.data, celular=form.celular.data, email=form.email.data,
                               fechanacimiento=form.fechanacimiento.data, idrol=form.idrol.data, password_hash=generate_password_hash(form.contrasena.data, "sha256"))
            db.session.add(persona)
            db.session.commit()
            flash(f'Registro creado exitosamente', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash("No se realizo el registro del Usuario")
            return render_template('registro.html', form=form)
    return render_template('registro.html', form=form)


# Pagina de Logout
@app.route('/Logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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
    personas = Personas.query.all()
    return render_template('dashboard.html', personas=personas)


@app.route('/Comentarios')
def comentarios():
    return render_template('comentarios.html')


def pagina_no_encontrada(error):
    return redirect(url_for('index'))


def error_de_servidor(error):
    return redirect(url_for('index'))

# FUNCIONES

# Funcion Crear Registro

# Funcion Eliminar Persona


@app.route('/EliminarPersona/<int:id>/delete', methods=['POST'])
def eliminar_persona(id):
    persona = Personas.query.get_or_404(id)
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('dashboard'))

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
    remember = BooleanField('Recuerdame')
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
    idrol = StringField('Rol', validators=[DataRequired()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    contrasena2 = PasswordField('Verificar Contraseña', validators=[
                                DataRequired(), EqualTo('contrasena')])
    submit = SubmitField('Registrar')
