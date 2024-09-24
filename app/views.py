from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .forms import *
from .models import *
from django.utils import timezone
from datetime import timedelta



def home(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.save()
            return redirect('index')

    else:
        form = LeadForm()
    return render(request, 'index.html', {'form': form})

@login_required
def leads(request):
    leads =  Lead.objects.filter()
    context = {'leads': leads}

    return render(request, 'leads.html', context)

@login_required
def users(request):
    users = User.objects.filter()
    context = {'users': users}

    return render(request, 'users.html', context)


@login_required
def leads_dashboard(request):
    total_leads = Lead.objects.count()
    leads_atendidos = Lead.objects.filter(atendido=True, convertido=False).count()
    leads_convertidos = Lead.objects.filter(convertido=True).count()
    leads_nao_atendidos = Lead.objects.filter(atendido=False)
    leads_atendidos_list = Lead.objects.filter(atendido=True, convertido=False)

    context = {
        'total_leads': total_leads,
        'leads_atendidos': leads_atendidos,
        'leads_convertidos': leads_convertidos,
        'leads_nao_atendidos': leads_nao_atendidos,
        'leads_atendidos_list': leads_atendidos_list,
    }

    return render(request, 'leads_dashboard.html', context)

@login_required
def marcar_atendido(request, lead_id):
    lead = Lead.objects.get(id=lead_id)
    lead.atendido = True
    lead.save()
    return redirect('leads_dashboard')

@login_required
def marcar_convertido(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.name = lead.name
            client.save()
            lead.convertido = True
            lead.save()
            return redirect('upload_contract', client_id=client.id)
    else:
        form = ClientForm()
    return render(request, 'preencher_contrato.html', {'form': form, 'lead': lead})

@login_required
@login_required
def dashboard(request):
    total_users = User.objects.count()
    total_leads = Lead.objects.count()
    context = {
        'leads': total_leads,
        'total_users': total_users,
    }
    return render(request, 'dashboard.html', context=context)


@login_required
def gerar_contrato(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        # Processar o formulário de contrato e criar o cliente
        # Suponha que você tenha um formulário ContractForm que lida com os detalhes
        form = ContractForm(request.POST)
        if form.is_valid():
            # Crie o cliente e o contrato
            client = form.save(commit=False)
            client.lead = lead
            client.save()
            # Marcar lead como convertido
            lead.convertido = True
            lead.save()
            return redirect('leads_dashboard')
    else:
        form = ContractForm()
    return render(request, 'preencher_contrato.html', {'form': form, 'lead': lead})

@login_required
def upload_contract(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ContractUploadForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('contratos_ativos')
    else:
        form = ContractUploadForm(instance=client)
    return render(request, 'upload_contract.html', {'form': form, 'client': client})

@login_required
def contratos_ativos(request):
    contratos_inativos = Client.objects.filter(contract_status='inactive')
    contratos_ativos = Client.objects.filter(contract_status='active')

    context = {
        'contratos_inativos': contratos_inativos,
        'contratos_ativos': contratos_ativos,
    }

    return render(request, 'contratos_ativos.html', context)

@login_required
def ativar_servico(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.service_status = 'active'
        client.save()
    return redirect('contratos_ativos')


@login_required
def perfil_cliente(request):
    client = request.user.client
    return render(request, 'perfil_cliente.html', {'client': client})


@login_required
def contratos_ativos_cliente(request):
    client = request.user.client
    contratos_ativos = client.contract_status == 'active'
    
    return render(request, 'contratos_ativos_cliente.html', {
        'client': client,
        'contratos_ativos': contratos_ativos,
    })


@login_required
def pagamento_faturas(request):
    client = request.user.client
    # Supondo que você tenha um modelo "Invoice" que armazena faturas
    faturas_pendentes = client.invoice_set.filter(status='unpaid')
    return render(request, 'pagamento_faturas.html', {'client': client, 'faturas_pendentes': faturas_pendentes})


@login_required
def pagar_fatura(request, fatura_id):
    fatura = get_object_or_404(Invoice, id=fatura_id, client=request.user.client)
    if request.method == 'POST':
        fatura.status = 'paid'
        fatura.save()
        return redirect('pagamento_faturas')


@login_required
def ativar_servico(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        form = AtivarServicoForm(request.POST)
        if form.is_valid():
            client.service_status = 'active'
            client.payment_due_date = form.cleaned_data['payment_due_date']
            client.save()

            # Gerar a primeira fatura
            Invoice.objects.create(
                client=client,
                amount_due=client.monthly_payment,
                due_date=client.payment_due_date
            )

            return redirect('perfil_cliente')
    else:
        form = AtivarServicoForm()

    return render(request, 'ativar_servico.html', {'form': form, 'client': client})

@login_required
def total_leads(request):
    total_leads = Generator.objects.count() 
    return JsonResponse({'total_leads': total_leads})

@login_required
def gerar_faturas_mensais():
    hoje = timezone.now().date()

    for client in Client.objects.filter(service_status='active'):
        if client.payment_due_date and client.payment_due_date <= hoje:
            # Gerar a fatura
            Invoice.objects.create(
                client=client,
                amount_due=client.monthly_payment,
                due_date=client.payment_due_date
            )

            # Atualizar a data de vencimento para o próximo mês
            client.payment_due_date += timedelta(days=30)
            client.save()