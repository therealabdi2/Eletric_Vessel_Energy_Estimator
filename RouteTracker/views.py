from django.views.generic import TemplateView 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect 
from django.shortcuts import render 
from django.shortcuts import redirect 
from django.views import View 
from django.views.generic import ListView, CreateView

from .models import Route, CustomUser
from .forms import RouteForm, UpdateJobForm
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
    context_object_name = "routess"


def add_route(request):
    projtitle = request.POST["projectTitle"]
    filnam = request.POST["fileName"]
    jobdet = request.POST["jobDetails"]
    created_obj = Route.objects.create(projectTitle=projtitle, fileName=filnam, jobDetails=jobdet, cost=0.00, user=request.user)
 
    return(redirect('/routes/view'))

def update_route(request):
    """ Meant to update a job with price and payment details """
    if request.method == "POST":
        form = UpdateJobForm(request.POST)
        if form.is_valid():
            jobId = form.cleaned_data['jobId']
            price = form.cleaned_data['price']
            paymentCompleted = form.cleaned_data['paymentCompleted']
            jobCompleted = form.cleaned_data['jobCompleted']
            try:
                rec = Route.objects.get(pk=jobId)   
                if rec:  
                    if price:       
                        rec.cost = float(price)
                    rec.paymentCompleted = paymentCompleted
                    rec.jobCompleted = jobCompleted 
                    rec.save() 
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            except:
                context = {
                    'form': form
                }
                return render(request, 'updateRoute.html', context)
           
      
    else:
        form = UpdateJobForm() 
        context = {
            'form': form
        }
        return render(request, 'updateRoute.html', context)


   
            