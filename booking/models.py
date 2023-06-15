from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    infosub = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True)
    fname = models.CharField(max_length=255,null=True)
    lname = models.CharField(max_length=255,null=True)
    email = models.EmailField()
    profile_picture = models.URLField()

    def __str__(self):
        return self.name

class room_dtl(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.room_name

class book_dtl(models.Model):
    book_id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(room_dtl,null=True,on_delete=models.CASCADE)
    purposename = models.CharField(max_length=200,null=True)
    txtonfloor = models.CharField(max_length=200,null=True)
    sdate = models.DateField(auto_now=False, auto_now_add=False)
    stime = models.TimeField(auto_now=False, auto_now_add=False)
    etime = models.TimeField(auto_now=False, auto_now_add=False)
    txtusername = models.CharField(max_length=200,null=True)
    txttel = models.IntegerField(null=True)
    other = models.CharField(max_length=200,null=True)

    def __str__(self):
        ssdate = str(self.sdate)
        sstime = str(self.stime)
        eetime = str(self.etime)
        return self.room_id.room_name +" "+ self.txtusername +" "+ ssdate +" "+ sstime +" "+ eetime