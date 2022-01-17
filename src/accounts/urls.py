from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordChangeView, PasswordResetView, PasswordResetDoneView)
from django.urls import path

from . import views

urlpatterns = [
    path('delete', views.delete_view, name='delete'),
    path('register', views.register_view, name='register'),
    path('update', views.update_view, name='update'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('password_reset/done', PasswordResetDoneView.as_view(
        template_name='accounts/email_sent.html'),
        name='password_reset_done'
        ),
    path('password_reset', PasswordResetView.as_view(
        template_name='accounts/reset_password.html',
        subject_template_name='accounts/reset_subject.txt',
        email_template_name='accounts/reset_email.txt'),
        name='password_reset'
        ),
    path('password_change', PasswordChangeView.as_view(
        template_name='accounts/change_password.html'),
        name='change_password'
        ),
    path('password_change/done', PasswordChangeDoneView.as_view(
        template_name='accounts/password_changed.html'),
        name='password_change_done'
        )
]
