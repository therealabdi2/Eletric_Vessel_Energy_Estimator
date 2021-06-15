from django.urls import path 
from .views import AboutView, JobsListView, JobsCreateView 
from django.contrib.auth.decorators import login_required

from django.conf.urls import url
from JobTracker import views

urlpatterns = [
    path('about/', login_required(AboutView.as_view()), name="about"),
    path('view/', login_required(JobsListView.as_view()), name="view"),
    path('create/', login_required(JobsCreateView.as_view()), name="create"),
    url(r'add_job/', login_required(views.add_job)),
    url(r'update_job/', login_required(views.update_job), name="update"),
   
]