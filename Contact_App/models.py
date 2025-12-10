from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=12,blank=True)
    address = models.TextField()
    image = models.ImageField(upload_to='uploads/',null=True, blank=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey('Registration', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name
    
class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=12,blank=True)
    password = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
    
    
    