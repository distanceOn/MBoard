from django import forms
from .models import CategoryChoices, CustomUser, Advertisement, Newsletter, Response
from django.contrib.auth.hashers import make_password


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'category', 'attached_file']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']


class VerificationCodeForm(forms.Form):
    code = forms.CharField(label='Код подтверждения', max_length=6)


class ResponseFilterForm(forms.Form):
    category = forms.ChoiceField(
        choices=[('', 'Все категории')] + list(CategoryChoices.choices),
        required=False,  # Делаем поле необязательным
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'}),  # Автоматическая отправка формы при изменении
    )

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'content']