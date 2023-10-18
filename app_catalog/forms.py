from django import forms
from .models import Review


class CreateReview(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ФИО'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-textarea', 'placeholder': 'Отзыв'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))

    class Meta:
        model = Review
        fields = ('full_name', 'description', 'email')


    def clean_full_name(self):
        cd = self.cleaned_data
        result = cd['full_name'].split(' ')
        if not ''.join(result).isalpha():
            raise forms.ValidationError("В имени присутствует число")
        elif len(result) != 3:
            raise forms.ValidationError("Формат имени пользователя Фамилия Имя Отчество")
        return cd['full_name']
