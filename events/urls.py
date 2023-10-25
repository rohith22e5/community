from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('register',views.register,name='register'),
    path('event/<int:event_id>',views.event,name='event'),
    path("wishlist",views.wishlist,name="wishlist"),
    path('orders',views.orders,name='orders'),
    path('get_events', views.get_events, name='get_events'),
    path('create',views.create,name='create'),
    path('categories',views.categories,name='categories'),
    path('help',views.help,name='help'),
     path("account",views.account,name="Account"),
     path('search',views.search,name='search'),
]