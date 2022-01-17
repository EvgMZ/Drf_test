from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from scrapping.models import Language, City
from django.forms import fields

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()
        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('User is not found')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Password wrong')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Accounts is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistraionForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Write password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Password again:)',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('email', )

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Password not equals')
        return data['password2']


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Город'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        to_field_name='slug',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Специальность'
    )
    send_email = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput,
        label='Получение рассылки'
        )

    class Meta:
        model = User
        fields = ('city', 'language', 'send_email')
