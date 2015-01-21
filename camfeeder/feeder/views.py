from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.generic import ListView
from datetime import datetime, timedelta

import json

from .forms import TransactionForm, LocationForm, SymptomForm, FeederTypeForm, ActionTakenForm, FilterForm
from .models import Feeder, FeederType, Location, Symptom, Transaction, ActionTaken
from .reports import ChartData
# Create your views here.

DATE_FORMAT = '%m/%d/%Y'

def list_(request):
    page_title = "List of feeders"
    feeders = Feeder.objects.all()
    has_feeder = feeders.count()

    for feeder in feeders:
        transactions = Transaction.objects.by_feeder(feeder=feeder)

        if transactions:
            latest_transaction = transactions.first()
            feeder.feeder_type = latest_transaction.feeder_type
            feeder.location = latest_transaction.location
            feeder.symptoms = latest_transaction.symptoms
            #import pdb; pdb.set_trace()
            feeder.actiontakens = latest_transaction.actiontakens
            feeder.transactions = transactions

    return render(request, 'home.html', {
        'feeders' : feeders,
        'has_feeder' : has_feeder,
    })
def list_feeder_type(request):
    page_title = "List of feeder types"
    feeder_types = FeederType.objects.all()
    metadata = 'feeder-type'
    has_data = feeder_types.count()
    
    return render(request, 'feeder/list-metadata.html', {
        'feeder_types' : feeder_types,
        'has_data' : has_data,
        'metadata' : metadata,
    })
def list_location(request):
    page_title = "List of all location"
    locations = Location.objects.all()
    metadata = 'location'
    has_data = locations.count()
    
    return render(request, 'feeder/list-metadata.html', {
        'locations' : locations,
        'has_data' : has_data,
        'metadata' : metadata,
    })
def list_symptom(request):
    page_title = "List of all symptom"
    symptoms = Symptom.objects.all()
    metadata = 'symptom'
    has_data = symptoms.count()
    
    return render(request, 'feeder/list-metadata.html', {
        'symptoms' : symptoms,
        'has_data' : has_data,
        'metadata' : metadata,
    })
def list_actiontaken(request):
    page_title = "List of fail code"
    actiontakens = ActionTaken.objects.all()
    metadata = 'actiontaken'
    has_data = actiontakens.count()
    
    return render(request, 'feeder/list-metadata.html', {
        'actiontakens' : actiontakens,
        'has_data' : has_data,
        'metadata' : metadata,
    })

def feeder_dashboard(request):
    no_of_feeder = Feeder.objects.count()

    filter_form = FilterForm()
    
#   Decorate the filter form
    filter_form.fields['start_date'].widget.attrs['class'] = 'form-control'
    filter_form.fields['end_date'].widget.attrs['class'] = 'form-control'
    filter_form.fields['feeder_type'].widget.attrs['class'] = 'form-control select-type'
    filter_form.fields['location'].widget.attrs['class'] = 'form-control select-type'
    
#   Get good & bad number of feeder
    good, bad = ChartData.filter_feeder_status()

    return render(request, 'dashboard.html', {
        'no_of_feeder' : no_of_feeder,
        'good' : good,
        'bad' : bad,
        'filter_form' : filter_form
    })

def top_symptom_json(request):
    data = {}
    
    data['chart_data'] = ChartData.get_count_by_symptom()
    
    return HttpResponse(json.dumps(data), content_type='application/json')

def top_symptom_json_by_feeder(request, feeder_id):
    data = {}
    
    if feeder_id:
        data['chart_data'] = ChartData.get_count_by_symptom_by_feeder(feeder=Feeder.objects.get(id=feeder_id))    
    else:
        data['chart_data'] = None

    return HttpResponse(json.dumps(data), content_type='application/json')

def top_symptom_json_by_location_by_feeder_type(request):    
    params = request.POST
    
#     import pdb; pdb.set_trace();
    
    data = {}
    location = params['location']
    feeder_type = params['feeder_type']
    start_date = params['start_date']
    end_date = params['end_date']
    
    data['chart_data'] = ChartData.get_count_by_location_by_feeder_type(location=location, feeder_type=feeder_type, start_date=start_date, end_date=end_date)
    
    return HttpResponse(json.dumps(data), content_type='application/json')
def add_or_edit_feeder(request, id=None):
    page_title = "Add or Edit a feeder"
    
    transaction = None
    if id:
        last_transaction = Transaction.objects.filter(feeder__id=id).first()
        transaction = last_transaction

    if request.POST:
        transaction_form = TransactionForm(request, request.POST, instance=transaction)
        if transaction_form.is_valid():
            transaction_new = transaction_form.save(commit=False, request=request)
            transaction_new.pk = None
            transaction_new.save()
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
    
def add_or_edit_location(request, id=None):
    form_type = "location"
    
    if id:
        location = get_object_or_404(Location, pk=id)
        title = "Add new location"
    else:
        location = Location(who_created=request.user)
        title = "Edit existing location"
        
    if request.POST:
        location_form = LocationForm(request.POST, instance=location)
        if location_form.is_valid():
            location_form.save()

            return HttpResponseRedirect(reverse('location-list'))
    else:
        location_form = LocationForm(instance=location)

    return render(request, 'feeder/add-location.html', {
        'id' : id,
        'form' : location_form,
        'title' : title,
        'form_type' : form_type,
    })
def add_or_edit_symptom(request, id=None):
    form_type = 'symptom'
    
    if id:
        symptom = get_object_or_404(Symptom, pk=id)
        title = "Add new symptom"
    else:
        symptom = Symptom(who_created=request.user)
        title = "Edit existing symptom"
        
    if request.POST:
        symptom_form = SymptomForm(request.POST, instance=symptom)
        if symptom_form.is_valid():
            symptom_form.save()

            return HttpResponseRedirect(reverse('symptom-list'))
    else:
        symptom_form = SymptomForm(instance=symptom)

    return render(request, 'feeder/add-location.html', {
        'form' : symptom_form,
        'title' : title,
        'form_type' : form_type,
    })
def add_or_edit_feeder_type(request, id=None):
    form_type = 'feeder_type'
    title = 'Add or Edit Feeder Type'
    
    if id:
        feeder_type = get_object_or_404(FeederType, pk=id)
    else:
        feeder_type = FeederType(who_created=request.user)

    if request.POST:
        feeder_type_form = FeederTypeForm(request.POST, instance=feeder_type)
        if feeder_type_form.is_valid():
            feeder_type_form.save()

            return HttpResponseRedirect(reverse('feeder-type-list'))
    else:
        feeder_type_form = FeederTypeForm(instance=feeder_type)

    return render(request, 'feeder/add-location.html', {
        'form' : feeder_type_form,
        'title' : title,
        'form_type' : form_type,
    })
def add_or_edit_actiontaken(request, id=None):
    form_type = "action_taken"
    title = 'Add or Edit Action Taken'
    
    if id:
        action_taken = get_object_or_404(ActionTaken, pk=id)
    else:
        action_taken = ActionTaken(who_created=request.user)
        
    if request.POST:
        action_taken_form = ActionTakenForm(request.POST, instance=action_taken)
        if action_taken_form.is_valid():
            action_taken_form.save()
            
            return HttpResponseRedirect(reverse('actiontaken-list'))
        
    else:
        action_taken_form = ActionTakenForm(instance=action_taken)
        
    return render(request, 'feeder/add-location.html', {
        'form' : action_taken_form,
        'title' : title,
        'form_type' : form_type,    
    })

