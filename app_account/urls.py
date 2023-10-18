from django.urls import path

from .views import sign_up_view, ModalLoginView, LogoutUserView, ProfileUserView, ChangeUserView

urlpatterns = [
    path('sign-up/', sign_up_view, name='sign_up'),
    path('login_passim/', ModalLoginView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('<int:pk>/', ProfileUserView.as_view(), name='profile'),
    path('<int:pk>/change/', ChangeUserView.as_view(), name='change'),
]