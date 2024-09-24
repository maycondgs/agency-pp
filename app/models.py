from django.db import models
from django.contrib.auth.models import User
import datetime
import os

# Create your models here.
def get_file_path(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/', filename)


class Services(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name 
    
    
class Lead(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    email = models.CharField(max_length=150, null=False, blank=False)
    telephone = models.CharField(max_length=150, null=False, blank=False)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    atendido = models.BooleanField(default=False)  # Novo campo para indicar se foi atendido
    convertido = models.BooleanField(default=False)  # Novo campo para diferenciar leads convertidos

    def __str__(self):
        return f"{self.name} - {self.telephone}"

    

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    address = models.TextField()
    plan = models.CharField(max_length=255)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    contract_file = models.FileField(upload_to='contracts/')
    contract_status = models.CharField(max_length=10, choices=[('inactive', 'Inativo'), ('active', 'Ativo')], default='inactive')
    service_status = models.CharField(max_length=10, choices=[('inactive', 'Inativo'), ('active', 'Ativo')], default='inactive')
    payment_due_date = models.DateField(null=True, blank=True)  # Data de vencimento da fatura
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=[('unpaid', 'Não Pago'), ('paid', 'Pago')], default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fatura #{self.id} - {self.client.name}"
    