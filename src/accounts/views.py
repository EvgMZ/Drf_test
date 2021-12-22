from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout


from .forms import UserLoginForm, UserRegistraionForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home_page')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home_page')


def register_view(request):
    form = UserRegistraionForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return render(
            request,
            'accounts/register_done.html',
            {'new_user': new_user}
        )
    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )
