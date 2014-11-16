from django import forms
from camfeeder.feeder.models import Feeder, FeederType, Location, Status, Transaction
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

class TransactionForm(forms.ModelForm):

    barcode = forms.CharField(label="Barcode", required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    list_of_type = FeederType.objects.all()
    list_of_location = Location.objects.all()
    list_of_status = Status.objects.filter(id__gt=1)

    type = forms.ModelChoiceField(label="Type", required=True, queryset=list_of_type)
    location = forms.ModelChoiceField(label="Location", required=True, queryset=list_of_location)
    status = forms.ModelChoiceField(label="Status", required=True, queryset=list_of_status)
    
    def __init__(self, request, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['type'].widget.attrs['class'] = 'form-control'
        self.fields['location'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control'

    def clean_type(self):
        type = self.cleaned_data.get('type')

        return FeederType.objects.get(id=type.id)

    def clean_location(self):
        location = self.cleaned_data.get('location')

        return Location.objects.get(id=location.id)

    def clean_status(self):
        status = self.cleaned_data.get('status')
        return Status.objects.get(id=status.id)

    def save(self, commit, request):
        import pdb; pdb.set_trace()
        form = super(TransactionForm,self).save(commit=False)
        form.user = request.user
        
        # Get data for feeder
        barcode = self.cleaned_data['barcode']

        try:
            feeder = Feeder.objects.get(barcode=barcode)
        except:
            feeder = Feeder(who_created=request.user, barcode=self.cleaned_data['barcode'])
            feeder.save()
            form.feeder = feeder
        else:
            form.feeder = feeder

        if commit:
            form.save()
        return form


    class Meta:
        model = Transaction
        fields = (
            'barcode',
            'type',
            'location',
            'status'
        )

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

class StatusForm(forms.ModelForm):
    status = forms.CharField(label="Status", required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Status of feeder'}))
    
    class Meta:
        model = Status
        fields = (
            'status',
        )
