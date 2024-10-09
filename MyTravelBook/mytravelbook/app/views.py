from django.shortcuts import render, redirect
from django.views import View
from app.forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

class TopView(View):
    def get(self, request):
        return render(request, "top.html")
    
class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", context={
            "form": form
        })
    def post(self, request):
        print(request.POST)
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')#登録成功後にログインページにリダイレクト
        else:
            error_messages = []
            for field in form:
                for error in field.errors:
                    error_messages.append(error)
            print(error_messages)  # デバッグ用
        return render(request, "signup.html", context={
            "form": form,
            "error_messages": error_messages,  
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
            username = form.cleaned_data.get('username')#メールアドレス  
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # ログイン成功後にホームページにリダイレクト
            else:
                form.add_error(None, "メールアドレスまたはパスワードが正しくありません。")
        return render(request, "login.html", context={
            "form": form
            })
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('top')
       
@method_decorator([login_required, never_cache], name='dispatch')
class HomeView(View):
    def get(self, request):
        return render(request, "home.html")
    
@method_decorator([login_required, never_cache], name='dispatch')
class MypageView(View):
    def get(self, request):
        user = request.user
        return render(request, 'mypage.html',context={
            'user': user
        })
