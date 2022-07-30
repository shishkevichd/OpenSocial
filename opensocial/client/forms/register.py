from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    first_name = StringField(label="Имя", validators=[DataRequired("Введите имя"), Length(min=2, max=56, message="Некорректное имя")])
    last_name = StringField(label="Фамилия", validators=[DataRequired("Введите фамилию"), Length(min=2, max=56, message="Некорректная фамилия")])
    email = EmailField(label="Почта", validators=[DataRequired("Введите почту")])
    password = PasswordField(label="Пароль", validators=[DataRequired("Введите пароль"), Length(min=8, message="Короткий пароль")])
    gender = SelectField(label="Гендер", choices=[(1,'Девочка'),(2,'Мальчик')], validate_choice=True)
    agree_registration = BooleanField(label="Подтверждаю регистрацию", validators=[DataRequired("Подтвердите регистрацию")])
    submit = SubmitField(label="Войти")