from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = EmailField(label="Почта", validators=[DataRequired("Введите почту")])
    password = PasswordField(label="Пароль", validators=[DataRequired("Введите пароль"), Length(min=8, message="Короткий пароль")])
    save_me = BooleanField(label="Запомнить меня.")
    submit = SubmitField(label="Войти")