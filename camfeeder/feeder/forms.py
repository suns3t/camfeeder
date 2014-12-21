from django import forms
from camfeeder.feeder.models import Feeder, FeederType, Location, Symptom, Transaction, ActionTaken
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

DATE_FORMAT = '%m/%d/%Y'

class TransactionForm(forms.ModelForm):

    barcode = forms.CharField(label="Barcode", required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    list_of_type = FeederType.objects.all()
    list_of_location = Location.objects.all()
    list_of_symptom = Symptom.objects.all()
    list_of_actiontaken = ActionTaken.objects.all()

    feeder_type = forms.ModelChoiceField(label="Type", required=False, queryset=list_of_type)
    location = forms.ModelChoiceField(label="Location", required=True, queryset=list_of_location)
    symptoms = forms.ModelMultipleChoiceField(label="Symptoms", required=False, queryset=list_of_symptom)
    actiontakens = forms.ModelMultipleChoiceField(label="Action Taken", required=False, queryset=list_of_actiontaken)
    comment = forms.CharField(label="Comment", required=False, widget=forms.Textarea(attrs={'class' : 'form-control', 'rows' : '3'}))
    
    
    def __init__(self, request, *args, **kwargs):
        
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.request = request
        
        if kwargs.get('instance'):
            self.fields['barcode'].initial = kwargs['instance'].feeder.barcode
            self.fields['actiontakens'].initial = [f for f in kwargs['instance'].actiontakens.all()] 
            self.fields['symptoms'].intial = [s for s in kwargs['instance'].symptoms.all() ]
            
            self.feeder = kwargs['instance'].feeder.barcode
            self.feeder_type = kwargs['instance'].feeder_type
            
        self.fields['feeder_type'].widget.attrs['class'] = 'form-control select-type'
        self.fields['location'].widget.attrs['class'] = 'form-control select-type'
        self.fields['symptoms'].widget.attrs['class'] = 'form-control select-type'
        self.fields['actiontakens'].widget.attrs['class'] = 'form-control select-type'
            
        if request.user.is_PM:
            self.fields.pop('symptoms')
        elif request.user.is_MT:
            self.fields.pop('actiontakens')
            self.fields.pop('barcode')
            self.fields.pop('feeder_type')
            self.fields['symptoms'].required = True
            self.fields['symptoms'].error_messages = {"required": "You must enter at least a symptom"}
            
    def clean_actiontakens(self):
        actiontakens = self.cleaned_data['actiontakens']
        
        return ActionTaken.objects.filter(id__in=actiontakens)
    
    def clean_symptoms(self):
        symptoms = self.cleaned_data['symptoms']
        
        return Symptom.objects.filter(id__in=symptoms)
    
    def save(self, commit, request):
        form = super(TransactionForm,self).save(commit=False)
        form.user = request.user
        
        # Get data for feeder
        try:
            b = self.cleaned_data['barcode']
            if b:
                try:
                    feeder = Feeder.objects.get(barcode=b)
                except:
                    feeder = Feeder(who_created=request.user, barcode=b, pm_period=30)
        except KeyError:
            feeder = form.feeder
            
        try:
            s = self.cleaned_data['symptoms']
            if s:
                feeder.status = False
            else:
                feeder.status = True
        except KeyError:
            feeder.status = True
        
        try:
            a = self.cleaned_data['actiontakens']
            if a:
                feeder.status = True
        except KeyError:
            pass
        
        feeder.save()
        form.feeder = feeder

        return form


    class Meta:
        model = Transaction
        fields = (
            'barcode',
            'feeder_type',
            'location',
            'symptoms',
            'actiontakens',
            'comment'
        )

class FilterForm(forms.Form):
    list_of_type = FeederType.objects.all()
    list_of_location = Location.objects.all()
    
    start_date = forms.DateField(
        label='From Date', required=True, input_formats=[DATE_FORMAT])
    end_date = forms.DateField(
        label='To Date', required=True, input_formats=[DATE_FORMAT])
    
    location = forms.ModelChoiceField(label="Location", required=True, queryset=list_of_location)
    feeder_type = forms.ModelChoiceField(label="Feeder Type", required=True, queryset=list_of_type)
     
    
        
        
class LocationForm(forms.ModelForm):
    location = forms.CharField(label="Location", required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Location of feeder'}))
    
    class Meta:
        model = Location
        fields = (
            'location',
        )

class FeederTypeForm(forms.ModelForm):
    feeder_type = forms.CharField(label="Feeder Type", required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Type of feeder'}))
    
    class Meta:
        model = FeederType
        fields = (
            'feeder_type',
        )

class SymptomForm(forms.ModelForm):
    symptom = forms.CharField(label="Symptom", required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Symptom of bad feeder'}))
    
    class Meta:
        model = Symptom
        fields = (
            'symptom',
        )

class ActionTakenForm(forms.ModelForm):
    action = forms.CharField(label="Action taken", required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Action taken to fix the feeder'}))
    
    class Meta:
        model = ActionTaken
        fields = (
            'action',
        )
        