from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(book_dtl)
admin.site.register(room_dtl)