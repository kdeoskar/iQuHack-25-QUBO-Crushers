from django.db import models 

# Create your models here.
class fileUpload(models.Model):
    file = models.FileField(upload_to="files/")