from django import forms
from .models import room_dtl,book_dtl

class RoomForm(forms.ModelForm):
    class Meta:
        model = room_dtl
        fields = ['room_name']  # ระบุฟิลด์ที่ต้องการให้แสดงในฟอร์ม

class BookForm(forms.ModelForm):
    class Meta:
        model = book_dtl
        fields = '__all__'
        labels = {
            'room_id': 'Room ID',  # กำหนดชื่อเฉพาะสำหรับ room_id
            'book_email': 'Email Address',
            'purposename': 'Purpose Name',
            'txtonfloor': 'Text on Floor',
            'sdate': 'Start Date',
            'stime': 'Start Time',
            'etime': 'End Time',
            'txtusername': 'Username',
            'txttel': 'Telephone',
            'other': 'Other',
        }