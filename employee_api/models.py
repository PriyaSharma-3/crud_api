# employee_api/models.py
from django.db import models

class Employee(models.Model):
    id                = models.AutoField(primary_key = True)
    name              = models.CharField(max_length=255,null=True)
    email             = models.CharField(max_length=255,unique=True,null=True)
    age               = models.IntegerField(null=True)
    gender            = models.CharField(max_length=10,null=True)
    phone_no          = models.CharField(max_length=10,null=True)
    address_details   = models.JSONField(null=True)
    work_experience   = models.JSONField(null=True)
    qualifications    = models.JSONField(null=True)
    projects          = models.JSONField(null=True)
    # photo           = models.ImageField(upload_to="",null=False, blank=True)

    class Meta:  
        db_table = "employee"
    


    
