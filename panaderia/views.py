from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
import secrets
from PIL import Image
from panaderia.models import *
from panaderia.forms import *
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
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Pagina de Creacion de Platos


@app.route('/CrearPlatos')
@login_required
def crearplatos():
    return render_template('crearplatos.html')


@app.route('/Busqueda')
def busqueda():
    return render_template('busqueda.html')


@app.route('/Menu')
def menu():
    platos = Platos.query.all()
    return render_template('menu.html', platos=platos)

def save_picture(fotopersona):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(fotopersona.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/fotosperfil', picture_fn)

    output_size = (125, 125)
    i = Image.open(fotopersona)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/Perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    form = ActualizacionForm()
    if form.validate_on_submit():
        if form.fotopersona.data:
            picture_file = save_picture(form.fotopersona.data)
            current_user.fotopersona = picture_file
        current_user.nombre = form.nombre.data
        current_user.apellido = form.apellido.data
        current_user.direccion = form.direccion.data
        current_user.celular = form.celular.data
        current_user.email = form.email.data
        current_user.fechanacimiento = form.fechanacimiento.data
        db.session.commit()
        flash('Tu Perfil ha sido Actualizado', 'success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.nombre.data = current_user.nombre
        form.apellido.data = current_user.apellido
        form.direccion.data = current_user.direccion
        form.email.data = current_user.email
        form.celular.data = current_user.celular
        form.fechanacimiento.data = current_user.fechanacimiento
    fotopersona = url_for('static', filename='fotosperfil/' + current_user.fotopersona)
    return render_template('perfil.html', image_file=fotopersona, form = form)


@app.route('/Carrito')
def carrito():
    return render_template('carrito.html')


@app.route('/Dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    personas = Personas.query.all()
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
    return render_template('dashboard.html', form=form, personas=personas)


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
    flash(f'Plato creado exitosamente', 'success')
    return render_template('crearplatos.html')




