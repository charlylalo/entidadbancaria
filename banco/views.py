from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente

# Create your views here.


class BankView(View):
  def get(self, request, *args, **kwargs):
    clients = Cliente.objects.all()    
    return render(request, 'clients_list.html', {'clients': clients})