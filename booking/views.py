from django.shortcuts import render ,get_object_or_404,redirect
# Create your views here.from django.shortcuts import redirect
from django.shortcuts import redirect
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib  import messages
from .models import *
#import environ
import os
import json
import requests
import google.auth.transport.requests
from datetime import datetime, timedelta
from .forms import RoomForm,BookForm

def edit_book(request, book_id):
    book = get_object_or_404(book_dtl, book_id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('/managebook')  # แก้ไปที่หน้าที่คุณต้องการ
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form, 'book': book})

def restict_user(request,id):
    table = User.objects.get(pk=id)
    if table.is_active is True :
        table.is_active = False
        table.save()
    else:
        table.is_active = True
        table.save()
    return redirect('/manageuser')

def mng_user(request):
    table = User.objects.filter(is_superuser=False).order_by('-date_joined')
    return render(request,'mnguser.html',{'users':table})

def mng_book(request):
    table = book_dtl.objects.all().order_by('-sdate')
    return render(request,'mngbook.html',{'book_detail':table})

def create_or_update_room(request, room_id=None):
    go_room = room_dtl.objects.all()
    instance = None
    if room_id:
        instance = get_object_or_404(room_dtl, pk=room_id)
    form = RoomForm(request.POST or None, instance=instance)
    if form.is_valid():
        room = form.save(commit=False)
        # กรณีที่ต้องการจัดเก็บข้อมูลหลังจากการปรับเปลี่ยน
        # room.additional_field = 'additional_value'
        room.save()
        return redirect('/room')  # เปลี่ยนเป็นชื่อหน้าที่ต้องการไปหลังจากบันทึก
    return render(request, 'room_form.html', {'form': form,'room':go_room})

def delete_room(request, room_id):
    room = get_object_or_404(room_dtl, pk=room_id)
    room.delete()
    return redirect('/room')

def delete_user(request , id):
    del_id = get_object_or_404(User,pk=id)
    if del_id.delete():
        messages.success(request,'ลบข้อมูลสำเร็จ')
    else:
        messages.warning(request,'ล้มเหลว')
    return redirect('/manageuser')

def go_config(request):
    return render(request,'config.html')

def dashboard(request):
    x = None
    context = {'xxx':x}
    if 7>6:
        x = '1'
        zzz = {'xxx':x}
        return render(request,'dashboard.html',zzz)
    return render(request,'dashboard.html',context)

def mybooking(request):
    email_book = request.user.email
    """ print(email_book) """
    table = book_dtl.objects.filter(book_email=email_book)
    context = {"book_detail":table}
    return render(request,'mybooking.html',context)

def search(request):
    if request.method == "POST":
        if request.POST.get("search_date"):
            search_key = request.POST.get("search_date")
            qry_book = book_dtl.objects.filter(sdate=search_key).order_by('-sdate')
            print(qry_book)
            if not qry_book:
                print(qry_book)
                messages.warning(request,'ไม่พบรายการจองในวันดังกล่าว')
                return render(request,'booksearch.html')
            else:
                context = {'book_detail' : qry_book}
            return render(request,'booksearch.html',context)

def profile(request):
    user_profile = UserProfile.objects.get(infosub=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'profile.html',context)

def booklist(request):
    if request.method == "POST":
        if request.POST.get("search_date"):
            context = {'book_detail' : book_dtl.objects.all().order_by('-sdate')[:20]}
    context = {'book_detail' : book_dtl.objects.all().order_by('-sdate')[:20]}
    return render(request,'booklist.html',context)

def booktable(request):
    if request.method == "POST":
        if request.POST.get("search_date"):
            context = {'book_detail' : book_dtl.objects.all().order_by('-sdate')}
    context = {'book_detail' : book_dtl.objects.all().order_by('-sdate')}
    return render(request,'booktable.html',context)

def bookdetail(request,id):
    fetch_book = book_dtl.objects.get(pk=id)
    return render(request,'bookdetail.html',{'fetch_book': fetch_book})

def home(request):
    return render(request, 'home.html')

def showlogin(request):
    return render(request,"login.html")

def booksearch(request):
    return render(request,"booksearch.html")

def check_booking(room ,date, start_time, end_time):
    c_date = date.date()
    c_start_time = start_time.time()
    c_end_time = end_time.time()
    print(type(room))
    print(type(c_date))
    print(type(c_start_time))
    print(type(c_end_time))
    print("+++++++++++++++++++")
    book_fetch = book_dtl.objects.all()
    for book_data in book_fetch:
        """ 
        print((book_data.room_id_id))
        print(type(book_data.sdate))
        print(type(book_data.stime))
        print(type(book_data.etime)) """
        if book_data.room_id_id == int(room) and book_data.sdate == c_date and book_data.stime <= c_end_time and book_data.etime > c_start_time:
            return False
    return True

def convert_minutes_to_hms(minutes):
    hours = minutes // 60
    remaining_minutes = minutes % 60
    #seconds = remaining_minutes * 60
    return f"{hours:02}:{remaining_minutes:02}"

@login_required(login_url='/showlogin')
def bookform(request):
    context = {'room_get' : room_dtl.objects.all()}
    if request.method == 'POST':
        if request.POST.get('room_name'):
            room_name = request.POST.get('room_name')
            qry_sdate = datetime.strptime(request.POST.get('sdate'), "%Y-%m-%d")
            formatted_stime = convert_minutes_to_hms(int(request.POST.get('stime')))
            minus_stime = datetime.strptime(formatted_stime, "%H:%M")
            formatted_etime = convert_minutes_to_hms(int(request.POST.get('etime')))
            minus_etime = datetime.strptime(formatted_etime, "%H:%M")
            table = book_dtl()
            table.room_id_id = request.POST.get('room_name')
            table.book_email = request.POST.get('email')
            table.purposename = request.POST.get('purposename')
            table.txtonfloor = request.POST.get('txtonfloor')
            table.sdate = request.POST.get('sdate')
            table.stime = minus_stime
            table.etime = minus_etime
            table.txtusername = request.POST.get('txtusername')
            table.txttel = request.POST.get('txttel')
            table.other = request.POST.get('other')
            print(minus_stime)
            print(minus_etime)
            if float(request.POST.get('stime')) - float(request.POST.get('etime')) > 0 :
                print('error')
                state = 'fail'
                book_result = {'state':state}
                messages.warning(request,'ไม่สำเร็จ เวลาไม่ถูกต้อง กด "กลับ" เพื่อแก้ไข')
                return render(request,"bookform.html",book_result)
            else:
                if check_booking(room_name, qry_sdate, minus_stime, minus_etime):
                    print("จองได้")
                    table.save()
                    state = 'success'
                    book_result = {'state':state}
                    messages.success(request,'จองสำเร็จ ตรวจสอบข้อมูลที่หน้ารายการจอง')
                    return render(request,"bookform.html",book_result)
                else:
                    print("ชน")
                    state = 'fail'
                    book_result = {'state':state}
                    messages.warning(request,'ไม่สำเร็จ วันเวลาดังกล่าวถูกจองไปแล้ว กด "กลับ" เพื่อแก้ไข')
                    return render(request,"bookform.html",book_result) 
        else:
            messages.warning(request,'ไม่สำเร็จ กรุณาตรวจสอบข้อมูล')
        return render(request,"bookform.html",context)
    return render(request,"bookform.html",context)

def logout_view(request):
    if request.user.is_authenticated:
        # Revoke the access token
        # Logout the user
        logout(request)
    return redirect('/')  # Redirect to your desired page after logout

def revoke_google_oauth(request):
    # Get the access token from the user session or wherever you stored it
    access_token = request.session.get('access_token')
    # Send a request to Google's token revocation endpoint
    revoke_url = 'https://oauth2.googleapis.com/revoke'
    params = {'token': access_token}
    response = requests.post(revoke_url, params=params)
    # Perform any additional actions required after revoking the token
    # ...
    return redirect('/')

def google_login(request):
    # Build the authorization URL
    authorization_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': os.environ.get('GOOGLE_URI_CALLBACK'),  # Change this to your callback URL
        'response_type': 'code',
        'scope': 'openid email profile',
        'prompt': 'select_account',
    }
    authorization_url += '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
    
    # Redirect the user to the authorization URL
    return redirect(authorization_url)

def google_callback(request):
    # Handle the callback after the user authorizes the application
    code = request.GET.get('code')
    # Exchange the authorization code for an access token
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': os.environ.get('GOOGLE_URI_CALLBACK'),  # Change this to your callback URL
        'grant_type': 'authorization_code',
    }
    response = requests.post(token_url, data=data)
    token_data = json.loads(response.text)
    request = google.auth.transport.requests.Request()
    # Verify the ID token
    id_token.verify_oauth2_token(token_data['id_token'], request, settings.GOOGLE_CLIENT_ID)
    profile_data = id_token.verify_oauth2_token(token_data['id_token'], request, settings.GOOGLE_CLIENT_ID)
    #id_token.verify_oauth2_token(token_data['id_token'], request, settings.GOOGLE_CLIENT_ID)
    # Save the access token and other relevant user data to your user model or session
    access_token = token_data['access_token']
    # Retrieve the user profile information from Google API
    userinfo_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(userinfo_url, headers=headers)
    userinfo = json.loads(response.text)
    # Save the user profile to the UserProfile model
    print(userinfo)
    user, created = User.objects.get_or_create(username=userinfo['sub'],email=userinfo['email'],first_name=userinfo['given_name'],last_name=userinfo['family_name'])
    user_profile, profile_created = UserProfile.objects.get_or_create(infosub=user)
    user_profile.name = userinfo['name']
    user_profile.fname = userinfo['given_name']
    user_profile.lname = userinfo['family_name']
    user_profile.email = userinfo['email']
    user_profile.profile_picture = userinfo['picture']
    user_profile.save()
    auth_user = User.objects.filter(username=userinfo['sub']).get()
    if auth_user is not None:
        value=userinfo['sub']
        return redirect('/redirected-view/?value={}'.format(value))
    else:
        #message
        return redirect('/')
    
def redirected_view(request):
    value = request.GET.get('value', None)
    if request.method == 'GET':
        user = User.objects.filter(username=value).get()
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            message = "Invalid username or password."
            return render(request, 'login.html', {'message': message})
    else:
        return render(request, 'login.html')
