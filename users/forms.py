import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms import BooleanField

from users.models import User


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class AuthenticationForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone',)

    def validate_unique(self):
        pass

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        result = re.sub(
            r'\+(\d{1}) \((\d{3})\) (\d{3})-(\d{2})-(\d{2})',
            r'+\1\2\3\4\5',
            phone
        )
        if phone == result:
            raise ValidationError("Введите корректный номер телефона")
        return result
