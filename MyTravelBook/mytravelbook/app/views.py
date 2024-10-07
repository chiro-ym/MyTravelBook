from django.shortcuts import render, redirect
from django.views import View
from app.forms import SingupForm, LoginForm
from django.contrib.auth import authenticate, login

class TopView(View):
    def get(self, request):
        return render(request, "top.html")
    
class SignupView(View):
    def get(self, request):
        form = SingupForm()
        return render(request, "signup.html", context={
            "form": form
        })
    def post(self, request):
        print(request.POST)
        form = SingupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')#登録成功後にログインページにリダイレクト
        else:
            print(form.errors)
        return render(request, "signup.html",context={
            "form": form
        })
    
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", context={
            "form": form
        })
    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # ログイン成功後にホームページにリダイレクト
            else:
                form.add_error(None, "メールアドレスまたはパスワードが正しくありません。")
        return render(request, "login.html", context={
            "form": form
            })
    
    
class HomeView(View):
    def get(self, request):
        return render(request, "home.html")