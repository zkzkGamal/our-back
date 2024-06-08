
from django.urls import path, include
from .views import RegisterUserView
from rest_framework.routers import DefaultRouter

from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'register' , RegisterUserView , basename='register')
app_name = 'accounts' 

urlpatterns = [
    path('' , include(router.urls)),
    path('login/' , views.LoginUser.as_view() , name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    path('profile/',views.ProfileData.as_view() , name = 'profile'  ),
    path('profile/<int:pk>',views.ProfileData.as_view() , name = 'profile'  ),
    
    
    path('updatepassword/<int:pk>' , views.UpdatePassword.as_view() , name='update'),
    path('doctors/', views.DoctorData.as_view() , name ='doctors'),
    path('doctors/<slug:slug>', views.DoctorData.as_view() , name ='doctors'),
    path('doctors/account/<int:pk>', views.DoctorData.as_view() , name ='doctors')
    
    
    

]
