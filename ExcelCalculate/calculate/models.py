from django.db import models

# Create your models here.
class Document(models.Model):
    user_upload_file = models.FileField(upload_to='user_upload_files/ %Y%m%d/')

class Old(models.Model):
    age = models.IntegerField(null=True)


class Gender(models.Model):
    STATUS = (('남자','남자'), ('여자','여자'))
    gender = models.CharField(max_length=5 ,choices=STATUS , null=True)