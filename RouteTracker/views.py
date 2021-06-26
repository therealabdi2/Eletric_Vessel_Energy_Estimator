from django.views.generic import TemplateView 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect 
from django.shortcuts import render 
from django.shortcuts import redirect 
from django.views import View 
from django.views.generic import ListView, CreateView

from .models import Route, CustomUser
from .forms import RouteForm
from django.http import JsonResponse

"""
from .models import Author
"""

class AboutView(TemplateView):
    template_name = "about.html"

class RouteListView(ListView):
    template_name = "viewRoutes.html"
    context_object_name = "routes"      
    model = Route 
    
    # return only the user's requests if they don't have admin privilege 
    def get_queryset(self):
        user = list(CustomUser.objects.filter(username=self.request.user))[0] 
        # If the user has isAdminUser then return all the requests for viewing 
        if user.isAdminUser:
            return  Route.objects.all().order_by('-dateAdded')
        else:
           return Route.objects.filter(user=self.request.user).order_by('-dateAdded')
    
    
class RouteCreateView(CreateView):
    form_class = RouteForm
    template_name = "createRoute.html"
    context_object_name = "routes"




def view_routes(request):
    """ Meant to gather route details and display SOC levels """
    user = request.user
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
           route = form.save(commit=False) # get the new route without saving to database
           route.user = user # Add the current user to the record 
           route.save() # Save route information to the database
           # Calculate soc here 
           return JsonResponse({'data_SOC':[1,2]})

    else:
        form = RouteForm() 
        context = {
            'form': form
        }
        return render(request, 'viewRoutes.html', context)


   

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
