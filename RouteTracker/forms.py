from django.forms import ModelForm
from allauth.account.forms import SignupForm
from django import forms
from django.forms import widgets
from .models import Route, CustomUser


PROPULSION_METHODS = (
    ('full electric', 'FULL ELECTRIC'),
    ('diesel electric', 'DIESEL ELECTRIC')
)

class RouteForm(ModelForm):    
    class Meta:
        model = Route
        verbose_name = "Route List"
        fields = [
            'initialSOC',
            'batteryCapacity',
            'routeTitle',
            'batteryRating',
            'propulsionMethod',
            'minDeparturePow',
            'maxDeparturePow',
            'minTransitPow',
            'maxTransitPow',
            'minArrivalPow',
            'maxArrivalPow',
            'minStayingPow',
            'maxStayingPow',
            'departure',
            'transit',
            'arrival',
            'stay',
        ]
        widgets = {
            'propulsionMethod': forms.RadioSelect(choices=PROPULSION_METHODS),
            'departure': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'transit': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'stay': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    
        }
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['propulsion_method'] = forms.ChoiceField(widget=forms.RadioSelect(choices=PROPULSION_METHODS))



