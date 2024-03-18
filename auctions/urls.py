from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('creat_new_list', views.creat_new_list, name="creatnewlist"),
    path('item/<int:pk>', views.view_item, name='viewitem'),
    path('addToWatchList', views.addToWatchList, name='addToWatchList'),
    path('removeFromWatchList', views.removeFromWatchList, name='removethelist'),
    path('addBid', views.addBid , name="add_bid"),
]
