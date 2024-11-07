from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from app.models import User, TravelRecord, Prefecture, Photo, Category, TravelMemo

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "email", "password1", "password2"]
        error_messages = {
            'email': {
                'unique': "このメールアドレスは既に登録されています。",
                'required': "メールアドレスは必須です。",
            },
            'password1': {
                'required': "パスワードは必須です。",
            },
            'password2': {
                'required': "確認用パスワードを入力してください。",
            }
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if not password2:
            raise forms.ValidationError("確認用パスワードを入力してください。")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("確認用パスワードが一致しません。")
        
        return password2 
    
class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="メールアドレス",
        error_messages={'required': "メールアドレスを入力してください。"}
    )  # メールアドレスをusernameとして使用
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label="パスワード",
        error_messages={'required': "パスワードを入力してください。"}
    )
    
    error_messages = {
        'invalid_login': ("メールアドレスまたはパスワードが正しくありません。"),
        'inactive': ("このアカウントは無効です。"),
    }
    
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
        
class UserEditForm(forms.ModelForm):
    name = forms.CharField(label='名前', max_length=64)
    email = forms.EmailField(label='メールアドレス')
    
    class Meta:
        model = User
        fields = ('name', 'email')
        
class CustomPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        'password_in_common': '',  
        'password_too_similar': '',
        'password_too_short': '',
        'password_entirely_numeric': '',
        'password_incorrect': ("現在のパスワードが正しくありません。"),
        'password_mismatch': ("新しいパスワードが一致しません。"),
    }

    old_password = forms.CharField(
        label=("現在のパスワード"),
        strip=False,
        widget=forms.PasswordInput,
        error_messages={'required': ("現在のパスワードを入力してください。")},
    )
    new_password1 = forms.CharField(
        label=("新しいパスワード"),
        strip=False,
        widget=forms.PasswordInput,
        error_messages={'required': ("新しいパスワードを入力してください。")},
    )
    new_password2 = forms.CharField(
        label=("新しいパスワード（確認用）"),
        strip=False,
        widget=forms.PasswordInput,
        error_messages={'required': ("確認用パスワードを入力してください。")},
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(("新しいパスワードが一致しません。"))

        return password2

class TravelRecordForm(forms.ModelForm):
    title = forms.CharField(required=True, max_length=100, label="タイトル")
    prefecture = forms.ModelChoiceField(
        queryset=Prefecture.objects.all(),
        required=False,
        label="旅行場所",
        empty_label="選択しない")
    city = forms.CharField(required=False, max_length=100, label="都市名")
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="出発日")
    end_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="帰宅日")
    main_photo_url = forms.ImageField(required=False, label="メイン写真")
    comment = forms.CharField(required=False, widget=forms.Textarea, label="コメント")
    accommodation_info = forms.CharField(required=False, widget=forms.Textarea, label="宿泊情報")
    meal_info = forms.CharField(required=False, widget=forms.Textarea, label="食事情報")
    transport_info = forms.CharField(required=False, widget=forms.Textarea, label="交通情報")
    cost_info = forms.CharField(required=False, widget=forms.Textarea, label="旅行費用")    
    
    class Meta:
        model = TravelRecord
        fields = ['title', 'start_date', 'end_date', 'prefecture', 'city', 'main_photo_url', 'comment',
                  'accommodation_info','meal_info', 'transport_info', 'cost_info']
    
    def save(self, commit=True):
        travel_record = super().save(commit=False)
        if not travel_record.main_photo_url:
            travel_record.main_photo_url = 'photos/default.jpg'
        if commit:
            travel_record.save()
        return travel_record
# Prefectureのデータを作成
prefectures = [
    '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
    '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
    '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県',
    '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
    '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
    '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県',
    '大分県', '宮崎県', '鹿児島県', '沖縄県', 'その他'
]

for pref_name in prefectures:
    if not Prefecture.objects.filter(name=pref_name).exists():
        Prefecture.objects.create(name=pref_name)
    else:
        print(f"{pref_name}はすでに存在しています。")
        
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['photo_url']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_comment']
        
class TravelMemoForm(forms.ModelForm):
    audio_data = forms.CharField(widget=forms.HiddenInput(), required=False)  # 音声データのためのhiddenフィールド
    
    class Meta:
        model = TravelMemo
        fields = ['memo_text', 'memo_photo_path', 'audio_path', 'memo_location']
        widgets = {
            'memo_text': forms.Textarea(attrs={'placeholder': 'ここにメモを入力してください'}),
            'memo_photo_path': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'audio_path': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
class TravelSearchForm(forms.Form):
    keyword = forms.CharField(label="検索キーワード", required=False)
    date_from = forms.DateField(label="開始日", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(label="終了日", required=False, widget=forms.DateInput(attrs={'type': 'date'}))