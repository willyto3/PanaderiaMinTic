from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from panaderia.models import Personas

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
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=50)])
    direccion = StringField('Direccion', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    fechanacimiento = StringField(
        'Fecha de Nacimiento', validators=[DataRequired()])
    celular = StringField('Celular', validators=[
                          DataRequired(), Length(min=10, max=10)])
    idrol = StringField('Rol', validators=[DataRequired()])
    contrasena = PasswordField('Contraseña', validators=[DataRequired()])
    contrasena2 = PasswordField('Verificar Contraseña', validators=[
                                DataRequired(), EqualTo('contrasena')])
    submit = SubmitField('Registrar')

    def validar_celular(self, celular):
        persona = Personas.query.filter_by(nombre=celular.data).first()
        if persona:
            raise ValidationError('Este numero de Celular ya esta usado. Por favor ingrese a su cuenta.')

    def validate_email(self, email):
        persona = Personas.query.filter_by(email=email.data).first()
        if persona:
            raise ValidationError('Este numero de Celular ya esta usado. Por favor ingrese a su cuenta.')

# Formulario de Actualizacion de Datos


class ActualizacionForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=50)])
    fotopersona = FileField('Actualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    direccion = StringField('Direccion', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    fechanacimiento = StringField(
        'Fecha de Nacimiento', validators=[DataRequired()])
    celular = StringField('Celular', validators=[
                          DataRequired(), Length(min=10, max=10)])
    idrol = StringField('Rol', validators=[DataRequired()])
    submit = SubmitField('Actualizar')

    def validar_celular(self, celular):
        if celular.data != current_user.celular:
            persona = Personas.query.filter_by(nombre=celular.data).first()
            if persona:
                raise ValidationError('Este numero de Celular ya esta usado. Por favor ingrese a su cuenta.')

    def validate_email(self, email):
        if email.data != current_user.email:
            persona = Personas.query.filter_by(email=email.data).first()
            if persona:
                raise ValidationError('Este Correo Electronico ya esta usado. Por favor ingrese a su cuenta.')
