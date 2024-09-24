from django.contrib.auth.forms import UserCreationForm

from .models import User, Lead, Services, Client
from django import forms

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control my-2', 'placeholder': 'Confirm Password'}))
    class Meta:
        model = User
        fields= ['username', 'email', 'password1', 'password2']

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'telephone', 'service']

        # Definindo os widgets com classes CSS para o design
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Seu Nome Completo',
            'email': 'Seu Email',
            'telephone': 'Seu Telefone',
            'service': 'Selecione o Serviço',
        }
    
    
    # Definindo o queryset ordenado
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Services.objects.all().order_by('name')

class ContractUploadForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['contract_file']

    def save(self, commit=True):
        client = super().save(commit=False)
        client.contract_status = 'active'
        if commit:
            client.save()
        return client
    
        

class ClientForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ['username', 'password', 'name', 'email', 'telephone', 'address', 'plan', 'monthly_payment']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']
        )
        client = super().save(commit=False)
        client.user = user
        if commit:
            client.save()
        return client
    
