from django.shortcuts import render
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
import json
import requests
import google.auth.transport.requests
from datetime import datetime, timedelta

def profile(request):
    user_profile = UserProfile.objects.get(infosub=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'profile.html',context)

def booklist(request):
    context = {'book_detail' : book_dtl.objects.all().order_by('-sdate')}
    return render(request,'booklist.html',context)

def bookdetail(request,id):
    fetch_book = book_dtl.objects.get(pk=id)
    return render(request,'bookdetail.html',{'fetch_book': fetch_book})

def home(request):
    return render(request, 'home.html')

def showlogin(request):
    return render(request,"login.html")

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
        print((book_data.room_id_id))
        print(type(book_data.sdate))
        print(type(book_data.stime))
        print(type(book_data.etime))
        if book_data.room_id_id == int(room) and book_data.sdate == c_date and book_data.stime <= c_end_time and book_data.etime >= c_start_time:
            return False
    return True

@login_required(login_url='/showlogin')
def bookform(request):
    context = {'room_get' : room_dtl.objects.all()}
    if request.method == 'POST':
        if request.POST.get('room_name'):
            print(request.POST.get('room_name'))
            print(request.POST.get('purposename'))
            print(request.POST.get('txtonfloor'))
            print(request.POST.get('sdate'))
            room_name = request.POST.get('room_name')
            qry_sdate = datetime.strptime(request.POST.get('sdate'), "%Y-%m-%d")
            minus_stime = datetime.strptime((request.POST.get('stime')), "%H:%M")
            minus_etime = datetime.strptime((request.POST.get('etime')), "%H:%M")
            print((qry_sdate))
            print((minus_stime))
            print((minus_etime))
            print(request.POST.get('txtusername'))
            print(request.POST.get('txttel'))
            print(request.POST.get('other'))
            print("------------------------------------")
            table = book_dtl()
            table.room_id_id = request.POST.get('room_name')
            table.purposename = request.POST.get('purposename')
            table.txtonfloor = request.POST.get('txtonfloor')
            table.sdate = request.POST.get('sdate')
            table.stime = request.POST.get('stime')
            table.etime = request.POST.get('etime')
            table.txtusername = request.POST.get('txtusername')
            table.txttel = request.POST.get('txttel')
            table.other = request.POST.get('other')
            if check_booking(room_name, qry_sdate, minus_stime, minus_etime):
                print("จองได้")
                table.save()
                messages.success(request,'จองสำเร็จ')
            else:
                print("ชน")
                messages.warning(request,'ไม่สำเร็จ วันเวลาที่เลือกถูกลงจองแล้ว')                
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
        'redirect_uri': 'http://127.0.0.1:8000/google/callback',  # Change this to your callback URL
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
        'redirect_uri': 'http://127.0.0.1:8000/google/callback',  # Change this to your callback URL
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
