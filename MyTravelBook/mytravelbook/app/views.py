from django.shortcuts import render, redirect
from django.views import View
from app.forms import SingupForm
# Create your views here.

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
        return render(request, "login.html")
    
class HomeView(View):
    def get(self, request):
        return render(request, "home.html")   