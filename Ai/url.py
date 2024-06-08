from django.urls import path
from . import views

app_name = 'Ai'

urlpatterns = [
    path('check/comment', views.check_comment.as_view(), name='check comment'),
    path('mysessions',views.get_sessions,name='messages'),
    path('mymessages/<str:sessions>',views.my_ai_messages.as_view(),name='messages'),

]