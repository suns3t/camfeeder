from django.db import models
from camfeeder.users.models import User

# Feeder type table, save name of feeder type, that way we can add/edit/delete 
# new type of feeder later
class FeederType(models.Model):
    id = models.AutoField(primary_key=True)
    feeder_type = models.CharField(max_length=10, blank=False)
    who_created = models.ForeignKey(User)

    class Meta:
        db_table = 'feeder_type'
        ordering = ('id','feeder_type',)

    def __str__(self):
        return "%s" % self.feeder_type

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=10, blank=False)
    who_created = models.ForeignKey(User)

    class Meta:
        db_table = 'feeder_location'
    def __str__(self):
        return "%s" % self.location

class Symptom(models.Model):
    id = models.AutoField(primary_key=True)
    symptom = models.CharField(max_length=400, blank=False)
    who_created = models.ForeignKey(User)
    
    class Meta:
        db_table = 'feeder_symptom'
        
    def __str__(self):
        return "%s" % self.symptom

class Feeder(models.Model):
    id = models.AutoField(primary_key=True)
    barcode = models.CharField(max_length=20, blank=False)
    status = models.BooleanField(default=True)
    pm_period = models.DecimalField(max_digits=2, decimal_places=0) # Period counts by day. i.e. 10 days or 30 days.
    who_created = models.ForeignKey(User)
    
    class Meta:
        db_table = 'feeder'

    def __str__(self):
        return "%s" % self.barcode

class ActionTaken(models.Model):
    id = models.AutoField(primary_key=True)
    action = models.CharField(max_length=100, blank=False)
    who_created = models.ForeignKey(User)
    
    class Meta:
        db_table = 'feeder_action_taken'
        
    def __str__(self):
        return "%s" % self.action
    

class TransactionManager(models.Manager):
    
    def by_feeder(self, feeder, **kwargs):
        """
        Filter transactions by feeder
        """
        return self.select_related().filter(feeder=feeder)
    
    def by_date(self, feeder, start_date, end_date, **kwargs):
        """
        Filter transactions by feeder in a specific time frame
        """
        returnset = self.by_feeder(feeder).filter(
            timestamp__gte=start_date,
            timestamp__lte=end_date
        )
class Transaction(models.Model):
    objects = TransactionManager()
    
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    feeder = models.ForeignKey(Feeder)
    feeder_type = models.ForeignKey(FeederType)
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    symptoms = models.ManyToManyField(Symptom)
    actiontakens = models.ManyToManyField(ActionTaken)
    comment = models.CharField(max_length=200, blank=True)
    
    class Meta:
        db_table = "feeder_transaction"
        ordering = ('-timestamp',)
