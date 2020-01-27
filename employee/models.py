from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from locations.models import City


class Gender(models.Model):
    GENDER_CHOICES = (
        ('1','Male'),
        ('2','Female')
    )
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,blank=False,null=False)

    def __str__(self):
        return '%s (id:%s)' % (self.gender, self.id)


class Employee(models.Model):
    name = models.CharField(validators=[RegexValidator(regex='^[A-Za-z]+(?: +[A-Za-z]+)*$', message='Invalid name', code='invalid')],max_length=255, blank=False, null=False)
    # pan_number = models.CharField(max_length=10,unique=True, blank=False, null=False)
    pan_number = models.CharField(max_length=10,validators=[RegexValidator(regex='^[A-Z]{5}[0-9]{4}[A-Z]$', message='Invalid PAN', code='invalid')], blank=False, null=False,unique=True)
    age = models.IntegerField(validators=[MaxValueValidator(100),MinValueValidator(1)],null=False,blank=False)
    gender = models.ForeignKey(Gender,null=False,blank=False,on_delete=models.CASCADE)
    email = models.EmailField(blank=False,null=False)
    city = models.ForeignKey(City,null=False,blank=False,on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated_on',)

    def __str__(self):
        return '%s (id:%s)' % (self.name, self.id)
