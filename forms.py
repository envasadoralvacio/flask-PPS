from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PersonaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellidos = StringField('Apellidos')
    email = StringField('Email', validators=[DataRequired()])
    enviar = SubmitField('Enviar')