from django.urls import path 
from .views import AboutView, RouteListView, RouteCreateView 
from django.contrib.auth.decorators import login_required

from django.conf.urls import url
from RouteTracker import views

urlpatterns = [
    path('about/', login_required(AboutView.as_view()), name="about"),
    path('view/', login_required(RouteListView.as_view()), name="view"),
    path('create/', login_required(RouteCreateView.as_view()), name="create"),
    url(r'add_route/', login_required(views.add_route)),
    url(r'update_route/', login_required(views.update_route), name="update"),
   
]