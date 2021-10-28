from enum import unique
from sqlalchemy.orm import backref
from panaderia import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def cargarpersona(id):
    return Personas.query.get(int(id))

# MODELOS


# Modelo para la base de datos Prueba tabla 'Productos'
class Platos(db.Model):
    __tablename__ = 'platos'
    idproducto = db.Column(db.Integer, primary_key=True)
    nombreplato = db.Column(db.String(510), nullable=True)
    precioplato = db.Column(db.Integer, nullable=True)
    descripcionplato = db.Column(db.String(200))
    nombreimagenplato = db.Column(db.String(200), nullable=False)


# Modelo para la base de datos Prueba tabla 'Persona'


class Personas(db.Model, UserMixin):
    __tablename__ = 'personas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=True)
    apellido = db.Column(db.String(200), nullable=True)
    direccion = db.Column(db.String(200))
    celular = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(200), nullable=True)
    fechanacimiento = db.Column(db.String(200))
    idrol = db.Column(db.Integer, db.ForeignKey('roles.idrol'))
    rol = db.relationship('Roles', backref=backref('personas', lazy='dynamic'))

    # Genera un hash de la contraseña
    password_hash = db.Column(db.String(200), nullable=True)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Personas %r>" % self.nombre





# Modelo para la base de datos Panaderia tabla 'Facturas'
class Facturas(db.Model):
    __tablename__ = 'facturas'
    idfactura = db.Column(db.Integer, primary_key=True)
    #fechafactura = db.Column(db.Datetime, nullable=True, default =datetime.utcnow)


# Modelo para la base de datos Panaderia tabla 'Roles'
class Roles(db.Model):
    __tablename__ = 'roles'
    idrol = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(10), unique=True, nullable=True)
