from django.urls import path
from . import views
from accounts.views import *


app_name='Main'

urlpatterns = [
    path('orders/', views.MyOrders.as_view(), name='list_my_orders'),
    path('orders/<int:pk>/', views.ModifyMyOrder.as_view(), name='modify_my_order'),
    path('orders/items/', views.MyItems.as_view(), name='list_my_items'),
    path('orders/items/<int:pk>/', views.ModifyMyItems.as_view(), name='modify_my_item'),
    
    
    path('drug/<str:name>', DrugViewDetail.as_view() , name='drug'),
    path('drug/', DrugViewDetail.as_view() , name='drug'),
    path('drug/category/<str:category>', DrugViewDetail.as_view() , name='drug'),
    
    
    path('category/drug/', DrugCategoryData.as_view() , name='drug'),
    path('category/drug/<int:pk>', DrugCategoryData.as_view() , name='drug'),


    path('posts' , views.BlogPostListCreateView.as_view() , name= 'posts'),
    path('posts/<int:pk>' , views.BlogPostRetrieveUpdateDeleteView.as_view() , name= 'posts get by id'),


    path('CommentPostCreateView' , views.BlogPostListCreateView.as_view() , name= 'comments'),
    path('comments/<int:pk>' , views.CommentPostRetrieveUpdateDeleteView.as_view() , name= 'get comments by id '),


    

    

]
