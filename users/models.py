from django.db import models


# Create your models here.
class UserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    locality = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'UserRegistrations'


class EncryptionModels(models.Model):
    loginid = models.CharField(max_length=100)
    imageName = models.CharField(max_length=100)
    xorShiftKey = models.CharField(max_length=100)
    byteKey = models.IntegerField()
    cdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'EncryptionTable'




class ImageSharingModel(models.Model):
    imgId = models.CharField(max_length=100)
    sharefrom = models.CharField(max_length=100)
    imageName = models.CharField(max_length=100)
    xorShiftKey = models.IntegerField()
    byteKey = models.IntegerField()
    recipientUser = models.CharField(max_length=100)
    cdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'ImageSharingTable'
