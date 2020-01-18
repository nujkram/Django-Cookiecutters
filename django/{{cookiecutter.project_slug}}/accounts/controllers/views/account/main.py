from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from accounts.models.account.constants import USER_DASHBOARD_ROOTS
from .forms.account_forms import LoginForm


class AccountLoginView(View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return HttpResponseRedirect(f'/{USER_DASHBOARD_ROOTS[request.user.user_type]}')

        form = LoginForm

        context = {
            "page_title": f"Login",
            "form": form,
            "location": "login"
        }

        return render(request, "accounts/login.html", context)

    def post(self, request, *args, **kwargs):

        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if not user.is_active:
                    messages.error(
                        request, "User account is not active", extra_tags="danger"
                    )
                else:
                    login(request, user)
                    messages.success(request, f"Welcome, {user}!", extra_tags="success")

                    next = request.GET.get('next', None)
                    if next:
                        return HttpResponseRedirect(next)
                    return HttpResponseRedirect(f'/{USER_DASHBOARD_ROOTS[user.user_type]}')
            else:
                messages.error(request, "Invalid credentials", extra_tags="danger")
        else:
            messages.error(request, form.errors, extra_tags="danger")

        context = {
            "page_title": f"Login",
            "form": form,
            "location": "login"
        }
        return render(request, "accounts/login.html", context)


class AccountLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("accounts_login"))

