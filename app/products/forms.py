from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Назва товару', validators=[
        DataRequired(message="Обов'язкове поле"),
        Length(min=3, message="Назва має містити щонайменше 3 символи")
    ])
    content = TextAreaField('Опис товару', validators=[
        DataRequired(message="Обов'язкове поле")
    ])
    price = DecimalField('Ціна ($)', places=2, validators=[
        DataRequired(message="Обов'язкове поле"),
        NumberRange(min=0.01, message="Ціна має бути додатним числом")
    ])
    category = SelectField('Категорія', choices=[
        ('Electronics', 'Електроніка'),
        ('Computers', 'Компʼютери'),
        ('Gadgets', 'Гаджети'),
        ('Accessories', 'Аксесуари')
    ], validators=[DataRequired()])
    quantity = IntegerField('Кількість одиниць', validators=[
        DataRequired(message="Обов'язкове поле"),
        NumberRange(min=0, message="Кількість не може бути від'ємною")
    ])
    image = FileField('Зображення товару', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Дозволено тільки формати JPG, JPEG та PNG!')
    ])
    submit = SubmitField('Зберегти товар')