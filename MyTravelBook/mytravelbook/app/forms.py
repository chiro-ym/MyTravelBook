from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app.models import User

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