from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

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
