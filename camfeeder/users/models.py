from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.
class User(AbstractBaseUser):
    """
    A custom user model
    """
    id = models.AutoField(primary_key=True)
    wwid = models.CharField(max_length=10, unique=True, db_index=True)
    email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_staff = models.BooleanField(default=False, blank=True)
    is_MT = models.BooleanField(default=False, blank=True)
    is_PM = models.BooleanField(default=False, blank=True)

    USERNAME_FIELD ='wwid'


    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __unicode__(self):
        if self.first_name:
            return u'%s, %s' % (self.last_name, self.first_name)
        else:
            return u'%s' % (self.wwid)
    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name
    
    def has_module_perms(self, app_label): return True
    def has_perm(self, app_label): return True
