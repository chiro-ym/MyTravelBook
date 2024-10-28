from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.forms import SignupForm, LoginForm, UserEditForm, CustomPasswordChangeForm, TravelRecordForm, PhotoForm, CommentForm, TravelMemoForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy
from .models import TravelRecord, Prefecture, Category, Photo, TravelMemo


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
            return redirect('login')
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
                return redirect('home') 
            else:
                form.add_error(None, "メールアドレスまたはパスワードが正しくありません。")
        return render(request, "login.html", context={
            "form": form
            })
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
            
@login_required
def user_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mypage')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'user_edit.html',context={
            'form':form
            })
    
class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'password_change.html'
    success_url = reverse_lazy('password_change_done')
    
    def form_valid(self, form):
        
        messages.success(self.request, "パスワードが正常に変更されました。")
        return super().form_valid(form)
    
class CustomPasswordChangeDoneView(View):
    def get(self, request):
        return render(request, 'password_change_done.html')
     
@method_decorator([login_required, never_cache], name='dispatch')
class MypageView(View):
    def get(self, request):
        user = request.user
        return render(request, 'mypage.html',context={
            'user': user
        })

@method_decorator([login_required, never_cache], name='dispatch')
class HomeView(View):
    def get(self, request):
        return render(request, "home.html")
    
@login_required
def create_travel_record(request):
    if request.method == 'POST':
        form = TravelRecordForm(request.POST, request.FILES)
        if form.is_valid():
            travel_record = form.save(commit=False)
            travel_record.user = request.user
            
            if not travel_record.main_photo_url:
                travel_record.main_photo_url = 'photos/default.jpg'
            
            travel_record.save()
            messages.success(request, '旅行記録が正常に追加されました。') 
            return redirect('travel_detail',travel_record.id)
        else:
            messages.error(request, 'フォームにエラーがあります。再度お試しください。')
            print(form.errors)
    else:
        form = TravelRecordForm()
        
    prefectures = Prefecture.objects.all() 
    return render(request, 'create_travel_record.html', context={
        'form': form,
        'messages': messages.get_messages(request),
        'prefectures': prefectures
        
        })
    
@method_decorator([login_required, never_cache], name='dispatch')
class TravelDetailView(View):
    def get(self, request, travel_id):
        travel_record = get_object_or_404(TravelRecord, id=travel_id)
        
        fixed_categories = ['観光', '食べる', '宿泊']
        
        existing_categories = travel_record.category_set.values_list('category_name', flat=True)
        
        for category_name in fixed_categories:
            if category_name not in existing_categories:
                Category.objects.get_or_create(
                travel_record=travel_record,
                category_name=category_name
            )
            
        categories = travel_record.category_set.all()
        print("カテゴリ数:", categories.count())#デバッグ
        
        photos = []
        for category in categories:
            photos.extend(category.photo_set.all())
        
        return render(request, 'travel_detail.html', context={
            'travel_record': travel_record,
            'categories': categories,
            'photos': photos,
            'custom_categories_count': categories.exclude(category_name__in=fixed_categories).count(),
        })
            
@method_decorator([login_required, never_cache], name='dispatch')
class TravelEditView(View):
    def get(self, request, travel_id):
        travel_record = get_object_or_404(TravelRecord, id=travel_id)
        form = TravelRecordForm(instance=travel_record)
        return render(request, 'travel_record_edit.html', context={
            'form':form,
            'travel_record': travel_record,
            'travel_id': travel_id
        })
        
    def post(self, request, travel_id):
        travel_record = get_object_or_404(TravelRecord, id=travel_id)
        form = TravelRecordForm(request.POST, request.FILES, instance=travel_record)
        if form.is_valid():
            form.save()
            return redirect('travel_detail', travel_id=travel_record.id)
        return render(request, 'travel_record_edit.html',context={
            'form':form,
            'travel_record': travel_record,
            'travel_id': travel_id
        })
        
@method_decorator([login_required, never_cache], name='dispatch')
class TravelDeleteView(View):
    def post(self, request, travel_id):
        travel_record = get_object_or_404(TravelRecord, id=travel_id)
        travel_record.delete()
        return redirect('travel_list')
    
@method_decorator([login_required, never_cache], name='dispatch')
class CategoryDetailView(View):
    def get(self, request, travel_id, category_id):
        travel_record = get_object_or_404(TravelRecord, id=travel_id)
        category = get_object_or_404(Category, id=category_id)
        
        photos = category.photo_set.all()
        categories = travel_record.category_set.all()
        
        return render(request, 'category_detail.html', context={
            'travel_record': travel_record,
            'category':category,
            'photos': photos,
            'categories': categories, 
        })
        
@method_decorator(login_required, name='dispatch')
class CategoryAddView(View):
    def get(self, request, travel_id):
        travel_record = get_object_or_404(TravelRecord, id=travel_id)
        return render(request, 'add_category.html', {'travel_record':travel_record})
    
    def post(self, request, travel_id):
        travel_record = get_object_or_404(TravelRecord, id=travel_id)
        category_name = request.POST.get('category_name')
        
        user_added_categories = travel_record.category_set.exclude(category_name__in=['観光', '食べる', '宿泊'])
        
        if travel_record.category_set.count() >= 2:
            error_message = "カテゴリは2つまでしか追加できません"
            return render(request, 'add_category.html',context={
                'travel_record': travel_record,
                'error_message': error_message
            })
        
        if category_name:
            Category.objects.create(travel_record=travel_record, category_name=category_name)
            return redirect('travel_detail', travel_id=travel_id)
        
        error_message = "カテゴリ名を入力してください"
        return render(request, 'add_category.html', context={
            'travel_record':travel_record,
            'error_message':error_message
        })
    
@login_required
def travel_list(request):
    travel_records = TravelRecord.objects.filter(user=request.user)
    return render(request, 'travel_list.html',context= {
        'travel_records': travel_records
        })
    
@login_required
def add_photo(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    travel_record = category.travel_record
    
    if request.method == 'POST':
        print(request.FILES)
        form = PhotoForm(request.POST, request.FILES)
        
        if form.is_valid():
            photo = form.save(commit=False)
            photo.category = category
            photo.save()
            print(photo.photo_url)
            return redirect('category_detail',travel_id=category.travel_record.id, category_id=category.id)
        print(form.errors)
        
    else:
        form = PhotoForm()
            
    return render(request, 'add_photo.html',context={
        'form': form,
        'category': category
    })
    
@login_required
def delete_photo(request, travel_id, category_id, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, category_id=category_id)
    
    if request.method == "POST":
        photo.delete()
        return redirect('category_detail',travel_id=travel_id, category_id=category_id)
    
    return redirect('category_detail',travel_id=travel_id, category_id=category_id)
        
@login_required
def edit_comment(request, travel_id, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        category.category_comment = request.POST.get('category_comment', '')
        category.save()
        return redirect('category_detail', travel_id=travel_id, category_id=category_id)

    return render(request, 'edit_comment.html', context={
        'category': category
        })
    
@method_decorator([login_required, never_cache], name='dispatch')
class TravelMemoListView(View):
    def get(self, request, travel_record_id):
        travel_record = get_object_or_404(TravelRecord, id=travel_record_id)
        memos = TravelMemo.objects.filter(travel_record_id=travel_record_id).order_by('created_at')
        form = TravelMemoForm()
        
        return render(request, 'travelmemo_list.html', context={
            'travel_record': travel_record,
            'memos': memos,
            'form': form
        })
        
    def post(self, request, travel_record_id):
        travel_record = get_object_or_404(TravelRecord, id=travel_record_id)
        form = TravelMemoForm(request.POST, request.FILES)

        if form.is_valid():
            travel_memo = form.save(commit=False)
            travel_memo.travel_record = travel_record
            travel_memo.save()
            return redirect('travelmemo_list', travel_record_id=travel_record.id)
        
        memos = TravelMemo.objects.filter(travel_record=travel_record).order_by('created_at')
        return render(request, 'travelmemo_list.html', context={
            'travel_record': travel_record,
            'memos': memos,
            'form': form
            })

@login_required        
def delete_memo(request, memo_id):
    memo = get_object_or_404(TravelMemo, id=memo_id)
    travel_record_id = memo.travel_record.id
    memo.delete()
    return redirect('travelmemo_list', travel_record_id=travel_record_id)