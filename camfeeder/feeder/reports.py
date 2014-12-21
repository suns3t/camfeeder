from datetime import datetime, timedelta

from .models import Transaction, Feeder, Symptom
DATE_FORMAT = '%m/%d/%Y'

class ChartData(object):
    @classmethod
    def get_data(cls, symptoms, transactions):
        data = {'symptom': [], 'data': []}
        
        for symptom in symptoms:
            # Create a temp list to store array of date and number of error on that day
            temp_data = []
            symptom.count = 0
            
            # Start with the latest data
            symptom.date = datetime.date(Transaction.objects.filter(symptoms=symptom).first().timestamp)
            for transaction in transactions:
                temp_date = datetime.date(transaction.timestamp)
                if symptom in transaction.symptoms.all():
                    symptom.count += 1
                if temp_date < symptom.date and symptom.count > 0:
                    # Convert date to milisecond to present in Highchart
                    temp_data.append([int(symptom.date.strftime('%s'))*1000, symptom.count])   
                    symptom.date = temp_date
                    symptom.count = 0
            
            # Get last data point
            if temp_date == symptom.date and symptom.count > 0:
                temp_data.append([int(symptom.date.strftime('%s'))*1000, symptom.count])   
                symptom.date = temp_date
                symptom.count = 0
            
            # Output
            if temp_data:
                data['symptom'].append(symptom.symptom)
                data['data'].append(temp_data)
        
        return data
    
    @classmethod
    def get_count_by_symptom(cls, start_date=None, end_date=None):
        # Get all symptom
        symptoms = Symptom.objects.all()
        if start_date and end_date:
            transactions = Transaction.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date)
        else:
            transactions = Transaction.objects.all()
        
        return ChartData.get_data(symptoms, transactions)
    
    @classmethod
    def get_count_by_symptom_by_feeder(cls, feeder, start_date=None, end_date=None):
        # Get all symptoms
        if start_date and end_date:
            transactions = Transaction.objects.filter(feeder=feeder,timestamp__gte=start_date, timestamp__lte=end_date)
        else:
            transactions = Transaction.objects.by_feeder(feeder)
        
        symptoms = Symptom.objects.all()
        
        return ChartData.get_data(symptoms, transactions)
    
    
    @classmethod
    def filter_feeder_status(cls):
        good = 0
        bad = 0
        for feeder in Feeder.objects.all():
            if feeder.status:
                good +=1
            else:
                bad +=1
                
        return good, bad
    
    @classmethod
    def get_count_by_location_by_feeder_type(cls, location=None, feeder_type=None, start_date=None, end_date=None):
        
        # Setup defaul value for parameters if they are not provided.
#         import pdb; pdb.set_trace()
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).date()
        else:
            start_date = datetime.strptime(start_date, DATE_FORMAT)
        if not end_date:
            end_date = (datetime.now()).date()
        else:
            end_date = datetime.strptime(end_date, DATE_FORMAT)
        if not location:
            location = 0
        if not feeder_type:
            feeder_type = 0
        
        # Load data
        symptoms = Symptom.objects.all()

        if location == 0:
            if feeder_type == 0:
                transactions = Transaction.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date)
                
            else:
                transactions = Transaction.objects.filter(feeder_type=feeder_type,timestamp__gte=start_date, timestamp__lte=end_date)
        else:
            if feeder_type == 0:
                transactions = Transaction.objects.filter(location=location, timestamp__gte=start_date, timestamp__lte=end_date)
            else:
                transactions = Transaction.objects.filter(location=location, feeder_type=feeder_type, timestamp__gte=start_date, timestamp__lte=end_date)
                
        return ChartData.get_data(symptoms, transactions)
            
            