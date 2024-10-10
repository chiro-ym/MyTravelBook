from django.contrib import admin
from django.urls import path
from app.views import TopView, SignupView, LoginView, LogoutView, HomeView, MypageView, CustomPasswordChangeView, CustomPasswordChangeDoneView
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TopView.as_view(), name="top"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('user_edit/', views.user_edit, name="user_edit"),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('home/', HomeView.as_view(), name="home"),
    path('mypage/', MypageView.as_view(), name="mypage"),
    path('travel_list/', views.travel_list, name='travel_list'), 
    path('create/', views.create_travel_record, name='create_travel_record'),
]
