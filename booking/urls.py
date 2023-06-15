from django.urls import path,include
from . import views
from .views import logout_view,revoke_google_oauth
urlpatterns = [
    path('',views.home),
    path('profile/',views.profile),
    path('bookform/',views.bookform),
    path('booklist/',views.booklist),
    path('bookdetail/<int:id>',views.bookdetail),
    path('showlogin/',views.showlogin),
    path('redirected-view/',views.redirected_view),
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('revoke-google-oauth/', views.revoke_google_oauth, name='revoke_google_oauth'),
    path('logout/', logout_view, name='logout'),
]