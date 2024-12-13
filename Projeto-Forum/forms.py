from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField
from flask_login import current_user
from flask_wtf import FlaskForm
from models import User

class TopicoForm(FlaskForm):

    titulo = StringField(validators=[DataRequired(), Length(max=50)])
    categoria = SelectField(validators=[DataRequired()])
    etiqueta = SelectField(validators=[DataRequired()])
    texto = CKEditorField('Texto', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class CadastroForm(FlaskForm):
    nome = StringField(validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(validators=[DataRequired(), Email()])
    senha = PasswordField(validators=[DataRequired(), Length(min=8)])
    confirmar_senha = PasswordField(validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Cadastrar')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Esse emai, já esta cadastrado nosso sistema')
    
class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    senha = PasswordField(validators=[DataRequired()])
    lembrar = BooleanField('Lembrar de mim')
    submit = SubmitField('Login')

class UpdateForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    foto = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Atualizar')

    def validarEmail(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Esse email já está em uso. Por favor escolha outro')

class RespostaForm(FlaskForm):
    texto = CKEditorField('Texto', validators=[DataRequired()])
    submit = SubmitField('Enviar')