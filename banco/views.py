from django import forms
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .models import Cliente, Cuenta, Transacciones


# Create your views here.

class DateInput(forms.DateInput):
    input_type = 'date'

class ClientForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
           'nombre',
           'apellido_paterno',
           'apellido_materno',
           'fecha_registro',
           'email'
        ]
        widgets = {
            'fecha_registro': DateInput()
        }
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
          field.widget.attrs['class'] = 'form-control'

def clients_list(request, template_name='clients_list.html'):
  clients = Cliente.objects.all()
  data = {}
  data['clients'] = clients
  return render(request, template_name, data)

def clients_create(request, template_name='clients_form.html'):
  form = ClientForm(request.POST or None)
  if form.is_valid():
      form.save()
      return redirect('clients_list')
  return render(request, template_name, {'form':form, 'title': 'Crear cliente'})

def clients_update(request, pk, template_name='clients_form.html'):
  client= get_object_or_404(Cliente, pk=pk)
  form = ClientForm(request.POST or None, instance=client)
  if form.is_valid():
      form.save()
      return redirect('clients_list')
  return render(request, template_name, {'form':form, 'title': 'Actualizar cliente'})

def clients_delete(request, pk, template_name='confirm_delete.html'):
  client= get_object_or_404(Cliente, pk=pk)    
  if request.method=='POST':
      client.delete()
      return redirect('clients_list')
  return render(request, template_name, {'object':client, 'title': 'cuenta'})

def accounts_list(request, client, template_name='accounts_list.html'):
  try: 
    accounts = get_list_or_404(Cuenta, cliente=client)
  except Exception as error:
    print("Error al obtener cuentas", error)
    accounts = []
  try:
     client_obj = get_object_or_404(Cliente, id=client)
  except Exception as error:
     print("Error al obtener cliente", error)
     client_obj = {"nombre": "unknown", "apellido_paterno": "user"}
  data = {}
  data['accounts'] = accounts
  data['client_id'] = client
  print("Este es el cliente obj", client_obj)
  data['client_name'] = f'{client_obj.nombre} {client_obj.apellido_paterno}'
  return render(request, template_name, data)


class AccountForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['asesor', 'cliente', 'feha_creacion', 'status', 'tipo_cuenta', 'balance' ]
        widgets = {
            'feha_creacion': DateInput()
        }

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
          field.widget.attrs['class'] = 'form-control'
        


def accounts_create(request, client_id, template_name='clients_form.html'):
  form = AccountForm(request.POST or None, initial={'cliente' : client_id})
  if form.is_valid():
      form.save()
      return redirect('clients_list')
  return render(request, template_name, {'form':form, 'title': "Crear cuenta"})

def account_update(request, pk, template_name='clients_form.html'):
  account= get_object_or_404(Cuenta, pk=pk)
  form = AccountForm(request.POST or None, instance=account)
  if form.is_valid():
      form.save()
      return redirect('clients_list')
  return render(request, template_name, {'form':form, 'title': 'Actualizar cuenta'})

def account_delete(request, pk, template_name='confirm_delete.html'):
  account= get_object_or_404(Cuenta, pk=pk)    
  if request.method=='POST':
      account.delete()
      return redirect('clients_list')
  return render(request, template_name, {'object':account, 'title': 'cuenta'})
  
  
class TransactionsView(View):
  def get(self, request, *args, **kwargs):
    transaction_id = kwargs['transaction']
    try:
      transactions = get_list_or_404(Transacciones, cuenta=transaction_id)
    except Exception as error:
      print("hubo un error", error)
      transactions = []
    return render(request, "transactions_list.html", {"transactions": transactions})

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transacciones
        fields = '__all__'
        widgets = {
            'fecha': DateInput()
        }
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
          field.widget.attrs['class'] = 'form-control'

def transaction_create(request, account, template_name='clients_form.html'):
  form = TransactionForm(request.POST or None, initial={'cuenta' : account})
  cliente_obj = Cuenta.objects.get(id=account)
  print("Este es balance", cliente_obj.balance)
  if form.is_valid():
      print("Este es form", form["cantidad"].value())
      cliente_obj.balance += int(form['cantidad'].value())
      form.save()
      cliente_obj.save()
      return redirect('clients_list')
  return render(request, template_name, {'form':form, 'title': "Nueva Transacción"})