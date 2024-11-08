from django.contrib import admin
from django.urls import path
from app.views import (TopView, SignupView, LoginView, LogoutView, HomeView,
                       MypageView, CustomPasswordChangeView, CustomPasswordChangeDoneView,
                       TravelDetailView, CategoryDetailView, CategoryAddView, TravelEditView,
                       TravelDeleteView, TravelMemoListView, CustomCategoryDetailView
                       )
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TopView.as_view(), name="top"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('user_edit/', views.user_edit, name="user_edit"),
    path('password_change/', CustomPasswordChangeView.as_view(), name="password_change"),
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name="password_change_done"),
    path('home/', HomeView.as_view(), name="home"),
    path('mypage/', MypageView.as_view(), name="mypage"),
    path('travel_list/', views.travel_list, name="travel_list"), 
    path('create_travel_record/', views.create_travel_record, name="create_travel_record"),
    path('travel_record_edit/<int:travel_id>/', TravelEditView.as_view(), name="travel_record_edit"),
    path('travel_record_delete/<int:travel_id>/', TravelDeleteView.as_view(), name="travel_record_delete"),
    path('travel_detail/<int:travel_id>/', TravelDetailView.as_view(), name="travel_detail"),
    path('travel/<int:travel_id>/category/<int:category_id>/', CategoryDetailView.as_view(), name='category_detail'),
    path('travel/<int:travel_id>/add_category/', CategoryAddView.as_view(), name='add_category'),
    path('travel/<int:travel_id>/category/<int:category_id>/custom/', CustomCategoryDetailView.as_view(), name='custom_category_detail'),
    path('category/<int:category_id>/add_photo/', views.add_photo, name='add_photo'),
    path('category/<int:travel_id>/category/<int:category_id>/photo/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
    path('travel/<int:travel_id>/category/<int:category_id>/edit_comment/', views.edit_comment, name='edit_comment'),
    path('travel_record/<int:travel_record_id>/memo/', TravelMemoListView.as_view(), name='travelmemo_list'),
    path('memo/delete/<int:memo_id>/', views.delete_memo, name='delete_memo'),
    path('travel_record/<int:travel_record_id>/delete_all_memos/', views.delete_all_memos, name= 'delete_all_memos'),
    path('search/', views.search_travel_records, name='travel_search'), 
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('roulette/', views.roulette_view, name='roulette'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)