from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from authapp.models import HabrUser
from mainapp.models import Article


class FormControlForm(forms.ModelForm):
    """Базовый шаблон Bootstrap класса form-control"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''


class HabrUserRegisterForm(UserCreationForm, FormControlForm):
    """
    Переопределённая форма для регистрации нового пользователя.
    Задан Bootstrap стиль при инициализации.
    """

    class Meta:
        model = HabrUser
        fields = ('username', 'email')


class HabrUserUpdateForm(UserChangeForm, FormControlForm):
    class Meta:
        model = HabrUser
        fields = ('email', 'first_name', 'last_name', 'age', 'avatar', 'bio')


class UserCreateArticleForm(FormControlForm):
    """Форма создания новой статьи"""
    class Meta:
        model = Article
        fields = ('category', 'title', 'body', 'image', 'status')


class UserUpdateArticleForm(FormControlForm):
    """Форма редактирования статьи"""
    class Meta:
        model = Article
        fields = ('title', 'body', 'image', 'status')
