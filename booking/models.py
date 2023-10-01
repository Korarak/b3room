from django.db import models
from django.contrib.auth.models import User
import requests

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
    book_id = models.AutpipoField(primary_key=True)
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
    
    def save(self, *args, **kwargs):
        # Call the parent class's save method
        super(book_dtl, self).save(*args, **kwargs)

        # Send a Line Notify message when a new record is created
        # FdaOcdTVodq3nDa0pgT5fSANGaamCeJuq0VqYYmZQsG
        access_token = ''
        message = f' {self.room_id.room_name}\n'
        message += f'ใช้เพื่อ: {self.purposename}\n'
        message += f'ข้อความบนเวที: {self.txtonfloor}\n'  # Replace with the actual field names
        message += f'วันที่จอง: {str(self.sdate)}\n'  # Replace with the actual field names
        message += f'เริ่มเวลา: {str(self.stime)}\n'
        message += f'ถึงเวลา: {str(self.etime)}\n'
        message += f'ผู้จอง: {self.txtusername}\n'
        message += f'โทร: {self.txttel}\n'
        # Add more fields as needed

        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        data = {
            'message': message,
        }

        response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data)

        # Check the response for errors (optional)
        if response.status_code != 200:
            print(f'Error sending Line Notify message: {response.status_code} - {response.text}')