from django.urls import path 

from .import views 

urlpatterns = [
    path('config/', views.stripe_config, name='config'),  
    path('create-checkout-session/<int:jobId>/', views.create_checkout_session),
    path('success/', views.SuccessView.as_view()), 
    path('cancelled/', views.CancelledView.as_view()),
    path('webhook/', views.stripe_webhook),
]