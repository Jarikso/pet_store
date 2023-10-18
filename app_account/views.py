from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy

from .forms import CreationUserForm, ChangeUserForm
from django.contrib.auth import get_user_model

from app_orders.models import Order

User = get_user_model()


def sign_up_view(request):
    if request.method == 'POST':
        user_form = CreationUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()  # zaq12wsx33 - password
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    else:
        user_form = CreationUserForm()
    return render(request, 'app_account/account_register.html', {'signup': user_form})


class ModalLoginView(View):
    def post(self, request):
        page_redirect = request.GET.get('next')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Вы вошли')
                return redirect('/') if page_redirect == '/account/sign-up/' else redirect(page_redirect)
            messages.error(request, 'Ошибка ввода e-mail или пароля. Проверьте e-mail или пароль, и повторите вход.')
            return redirect('account:sign_up') if page_redirect == '/account/sign-up/' else redirect(page_redirect)
        messages.error(request, 'Введите e-mail и пароль.')
        return redirect('account:sign_up')


class LogoutUserView(LoginRequiredMixin, LogoutView):
    """Представление выхода в аккаунт пользователем"""
    pass


class ProfileUserView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'app_account/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.request.user.pk
        try:
            context['order'] = Order.objects.filter(user=pk)[0]
        except:
            context['error'] = 'История заказов пуста'
        return context


class ChangeUserView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ChangeUserForm
    context_object_name = 'user'
    template_name = 'app_account/account_update.html'
    # success_url = reverse_lazy('catalog:main_page')

    def form_valid(self, form):
        print(self.request.user.id)
        data = self.request.POST
        if data['new_password1'] != '' and data['new_password1'] == data['new_password2']:
            user = self.object
            user.set_password(form.cleaned_data.get("new_password1"))
            user.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        super().form_valid(form)
        return redirect('account:profile', pk=self.request.user.id)

    def get_object(self):
        return self.request.user
