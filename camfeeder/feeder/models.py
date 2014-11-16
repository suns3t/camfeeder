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

    def __str__(self):
        return "%s" % self.location

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=400, blank=False)
    who_created = models.ForeignKey(User)
    
    def __str__(self):
        return "%s" % self.status

class Feeder(models.Model):
    id = models.AutoField(primary_key=True)
    barcode = models.CharField(max_length=20, blank=False)
    who_created = models.ForeignKey(User)
    
    class Meta:
        db_table = 'feeder'

    def __str__(self):
        return "%s" % self.barcode

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    feeder = models.ForeignKey(Feeder)
    status = models.ForeignKey(Status)
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location)

    class Meta:
        db_table = "feeder_transaction"
        ordering = ('timestamp',)
