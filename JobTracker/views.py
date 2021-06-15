from django.views.generic import TemplateView 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect 
from django.shortcuts import render 
from django.shortcuts import redirect 
from django.views import View 
from django.views.generic import ListView, CreateView

from .models import Job, CustomUser
from .forms import JobForm, UpdateJobForm
"""
from .models import Author
"""

class AboutView(TemplateView):
    template_name = "about.html"

class JobsListView(ListView):
    template_name = "viewjobs.html"
    context_object_name = "jobs"      
    model = Job 
    
    # return only the user's requests if they don't have admin privilege 
    def get_queryset(self):
        user = list(CustomUser.objects.filter(username=self.request.user))[0] 
        # If the user has isAdminUser then return all the requests for viewing 
        if user.isAdminUser:
            return  Job.objects.all().order_by('-dateRequested')
        else:
           return Job.objects.filter(user=self.request.user).order_by('-dateRequested')
    
    
class JobsCreateView(CreateView):
    form_class = JobForm
    template_name = "createjob.html"
    context_object_name = "jobs"


def add_job(request):
    projtitle = request.POST["projectTitle"]
    filnam = request.POST["fileName"]
    jobdet = request.POST["jobDetails"]
    created_obj = Job.objects.create(projectTitle=projtitle, fileName=filnam, jobDetails=jobdet, cost=0.00, user=request.user)
 
    return(redirect('/jobs/view'))

def update_job(request):
    """ Meant to update a job with price and payment details """
    if request.method == "POST":
        form = UpdateJobForm(request.POST)
        if form.is_valid():
            jobId = form.cleaned_data['jobId']
            price = form.cleaned_data['price']
            paymentCompleted = form.cleaned_data['paymentCompleted']
            jobCompleted = form.cleaned_data['jobCompleted']
            try:
                rec = Job.objects.get(pk=jobId)   
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
                return render(request, 'updateJob.html', context)
           
      
    else:
        form = UpdateJobForm() 
        context = {
            'form': form
        }
        return render(request, 'updateJob.html', context)


   
            