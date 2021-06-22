from django.forms import ModelForm
from allauth.account.forms import SignupForm
from django import forms
from .models import Route, CustomUser

class RouteForm(ModelForm):    
    class Meta:
        model = Route
        verbose_name = "Route List"
        fields = ["routeTitle"]


class CustomSignupForm(SignupForm):
    studentId = forms.CharField(max_length=10, required=True)
    def save(self, request):
        user = super(CustomSignupForm, self).save(request) 
        user.studentId = self.cleaned_data['studentId']
        user.save()
        return user 
    
class UpdateJobForm(forms.Form):    
    routeId = forms.IntegerField(label="Route ID", min_value=0, required=True)
    price = forms.DecimalField(label="Estimated Route Cost", min_value=0,decimal_places=2, required=False)
    paymentCompleted = forms.BooleanField(label="Payment Completed", required=False)
    