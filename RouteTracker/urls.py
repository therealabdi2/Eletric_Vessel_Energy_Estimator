from django.urls import path 
from .views import AboutView, RouteListView, RouteCreateView, view_routes
from django.contrib.auth.decorators import login_required

from django.conf.urls import url
from RouteTracker import views

urlpatterns = [
    path('about/', login_required(AboutView.as_view()), name="about"),
    path('view/', login_required(view_routes), name="view"),     
]