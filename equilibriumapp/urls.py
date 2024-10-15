from django.urls import path
from .views import *
from django.contrib.auth import views

urlpatterns = [
    path('', homepage, name='homepage'),
    path('fazer_login/', fazer_login, name='fazer_login'),
    path('criar_conta/', criar_conta, name='criar_conta'),
    path('consulta/', consulta, name='consulta'),
    path('dashboard/', dashboard, name='dashboard'),
    path('medicos/', medicos, name='medicos'),

    # Configuração padrão pra mudança de senha
    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]