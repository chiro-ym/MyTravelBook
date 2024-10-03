from django.shortcuts import render
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
    
class LoginView(View):
    def get(self, request):
        return render(request, "login.html")
    
class HomeView(View):
    def get(self, request):
        return render(request, "home.html")   