# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class FormRegistro(FlaskForm):
    nombre = StringField(label="Nombre", validators=[DataRequired()])
    apellido = StringField(label="Apellido", validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    nombre_usuario = StringField(label='Nombre de Usuario', validators=[DataRequired()])
    claustro = SelectField(
        label="Claustro",
        choices=[('Estudiante', 'Estudiante'), ('Docente', 'Docente'), ('PAyS', 'PAyS')],
        validators=[DataRequired()]
    )
    password = PasswordField(
        label='Contraseña',
        validators=[DataRequired(), Length(min=4), EqualTo('confirmacion', message='Las contraseñas deben coincidir')]
    )
    confirmacion = PasswordField(label='Repetir Contraseña', validators=[DataRequired()])
    submit = SubmitField(label='Registrar')


class FormReclamo(FlaskForm):
    usuario = StringField(label='Nombre de Usuario', validators=[DataRequired()])
    contenido = TextAreaField(label='Contenido del Reclamo', validators=[DataRequired(), Length(min=10)])
    departamento = SelectField(
        label="Departamento",
        choices=[('SoporteInformatico', 'Soporte Informático'), ('Mantenimiento', 'Mantenimiento'), ('SecretariaTecnica', 'Secretaría Técnica')],
        validators=[DataRequired()]
    )
    submit = SubmitField(label='Enviar Reclamo')
