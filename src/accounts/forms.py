from django import forms
from django.contrib.auth import authenticate, get_user_model


User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('User is not find')
            
            user = authenticate(email=email, password=password)
            

