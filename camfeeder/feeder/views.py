from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from .forms import TransactionForm, LocationForm, StatusForm, FeederTypeForm
from .models import Feeder, FeederType, Location, Status, Transaction
# Create your views here.

def list_(request):
    page_title = "List of feeders"
    feeders = Feeder.objects.all()
    has_feeder = feeders.count()

    return render(request, 'home.html', {
        'feeders' : feeders,
        'has_feeder' : has_feeder,
    })

def list_feeder_type(request):
    page_title = "List of feeder types"
    feeder_types = FeederType.objects.all()
    has_feeder_type = feeder_types.count()

    return render(request, 'feeder/list-feeder-type.html', {
        'feeder_types' : feeder_types,
        'has_feeder_type' : has_feeder_type,
    })

def add_feeder(request, id=None):
    page_title = "Add or Edit a feeder"
    
    if id:
        transaction = Transaction.objects.filter(feeder__id=id).first()
    else:
        transaction = Transaction()

    if request.POST:
        transaction_form = TransactionForm(request, request.POST, instance=transaction)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False, request=request)
            transaction.save()
            transaction_form.save_m2m()
            if id:
                messages.success(request, "Feeder is edited")
            else:
                messages.success(request, "New feeder added!")

            return HttpResponseRedirect(reverse('feeder-list'))
    else:
        transaction_form = TransactionForm(request, instance=transaction)

    return render(request, 'feeder/create.html', {
        'transaction_form' :  transaction_form,
        'title' : page_title,
    })
    
def add_location(request):
    title = "Add new location"
    form_type = "location"
    
    if request.POST:
        location_form = LocationForm(request.POST)
        if location_form.is_valid():
            location = location_form.save(commit=False)
            location.who_created = request.user
            location.save()

            return HttpResponseRedirect(reverse('feeder-list'))
    else:
        location_form = LocationForm()

    return render(request, 'feeder/add-location.html', {
        'form' : location_form,
        'title' : title,
        'form_type' : form_type,
    })

def add_status(request):
    title = "Add new status"
    form_type = 'status'

    if request.POST:
        status_form = StatusForm(request.POST)
        if status_form.is_valid():
            status = status_form.save(commit=False)
            status.who_created = request.user
            status.save()

            return HttpResponseRedirect(reverse('feeder-list'))
    else:
        status_form = StatusForm()

    return render(request, 'feeder/add-location.html', {
        'form' : status_form,
        'title' : title,
        'form_type' : form_type,
    })

def edit_feeder_type(request, id=None):
    title = "Add new feeder type"
    form_type = 'feeder_type'
    
    if id:
        feeder_type = get_object_or_404(FeederType, pk=id)
    else:
        feeder_type = FeederType(who_created=request.user)

    if request.POST:
        feeder_type_form = FeederTypeForm(request.POST, instance=feeder_type)
        if feeder_type_form.is_valid():
            feeder_type_form.save()

            return HttpResponseRedirect(reverse('feeder-list'))
    else:
        feeder_type_form = FeederTypeForm(instance=feeder_type)

    return render(request, 'feeder/add-location.html', {
        'form' : feeder_type_form,
        'title' : title,
        'form_type' : form_type,
    })
