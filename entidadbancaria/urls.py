"""entidadbancaria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from banco.views import accounts_list, transaction_create, account_update, accounts_create, account_delete, clients_list, clients_create, clients_update, clients_delete, TransactionsView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', clients_list, name='clients_list'),
    path('clients/create/', clients_create, name='client_new'),
    path('clients/edit/<int:pk>/', clients_update, name='client_edit'),
    path('clients/delete/<int:pk>/', clients_delete, name='client_delete'),
    path('accounts/<int:client>/', accounts_list, name='account_list'),
    path('accounts/create/<int:client_id>/', accounts_create, name='account_create'),
    path('accounts/update/<str:pk>/', account_update, name= 'account_update'),
    path('account/delete/<str:pk>', account_delete, name='account_delete'),
    path('transactions/<str:transaction>/', TransactionsView.as_view(), name='transactions_list'),
    path('transactoins/create/<str:account>/', transaction_create, name='transaction_create')
]
