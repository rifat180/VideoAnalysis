from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from feature.public.forms import SignInForm


class SignInView(View):
    @staticmethod
    def get(request):
        return render(request, "public/sign_in.html")

    @staticmethod
    def post(request):
        form = SignInForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, "Successfully signed in.")
                return redirect(request.GET.get("next", "/dashboard"))
            else:
                messages.warning(request, "User is not authenticated")
        else:
            for _, errors in form.errors.get_json_data().items():
                for error in errors:
                    messages.info(request, error.get("message"))
        return redirect("public:sign-in")


class DashboardView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        return render(request, "public/dashboard.html")


def sign_out(request):
    logout(request)
    messages.success(request, "Successfully signed out.")
    return redirect("public:sign-in")
