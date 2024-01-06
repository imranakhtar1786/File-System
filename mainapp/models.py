from django.db import models
class userDetail(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=30)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    staff=models.BooleanField(default=False)
class Files(models.Model):
    id=models.AutoField(primary_key=True)
    file=models.FileField(upload_to=("uploads"))

