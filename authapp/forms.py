from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from authapp.models import HabrUser


class HabrUserRegisterForm(UserCreationForm):
    """
    Переопределённая форма для регистрации нового пользователя.
    Задан Bootstrap стиль при инициализации.
    """

    class Meta:
        model = HabrUser
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''
