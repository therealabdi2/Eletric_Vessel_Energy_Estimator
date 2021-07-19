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
import statistics
from pprint import pprint
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
        pprint(request.POST)
        form = RouteForm(request.POST)
        if form.is_valid():
           route = form.save(commit=False) # get the new route without saving to database
           route.user = user # Add the current user to the record 
           route.save() # Save route information to the database
           print("Calculating soc ")
           # Calculate soc here 
           return JsonResponse({'data_SOC':[1,2]})
        else:
           return render(request, 'viewRoutes.html', {'form': form})

    else:
        form = RouteForm() 
        context = {
            'form': form
        }
        return render(request, 'viewRoutes.html', context)


def getOutputData(request):
    labels = []
    data = []
    print("This is request", request.GET) 
    if request.method == "POST":
        routeName = request.POST.get('routeName', None) 
        routeInfo = None
        try:
            routeInfo = Route.objects.get(routeTitle=routeName)
        except:
            return JsonResponse({})
        avgDepartPow = statistics.mean([routeInfo.minDeparturePow, routeInfo.maxDeparturePow])
        avgArrivalPow = statistics.mean([routeInfo.minArrivalPow, routeInfo.maxArrivalPow])
        data.append(routeInfo.initialSOC)
        labels.append(routeInfo.departure[0])
        soc = None
        for i, depart in enumerate(routeInfo.departure):
            if i > 0: 
                # Stay sections 
                timeDelta = depart - routeInfo.stay[i-1] 
                soc = soc - routeInfo.stayingPow/routeInfo.batteryCapacity * timeDelta.total_seconds()/3600 * 100 # change seconds to hours 
                data.append(soc) 
                labels.append(depart)
                
                 # Departures 
                timeDelta = routeInfo.transit[i] - depart           
                soc = soc - avgDepartPow/routeInfo.batteryCapacity * timeDelta.total_seconds()/3600 * 100 # change seconds to hours            
                data.append(soc)
                labels.append(routeInfo.transit[i])
            else:
                # Departures 
                timeDelta = routeInfo.transit[i] - depart           
                soc = routeInfo.initialSOC - avgDepartPow/routeInfo.batteryCapacity * timeDelta.total_seconds()/3600 * 100 # change seconds to hours            
                data.append(soc)
                labels.append(routeInfo.transit[i])
                
            # Transits 
            timeDelta = routeInfo.arrival[i] - routeInfo.transit[i] 
            print(timeDelta)
            soc = soc - routeInfo.transitPow/routeInfo.batteryCapacity * timeDelta.total_seconds()/3600 * 100 # change seconds to hours 
            data.append(soc)
            labels.append(routeInfo.arrival[i])
            # Arrivals 
            timeDelta = routeInfo.stay[i] - routeInfo.arrival[i] 
            chargingVal = (100/routeInfo.chargingTime) * (timeDelta.total_seconds()/60)  
            print("charging val", chargingVal)         
            soc = soc - avgArrivalPow/routeInfo.batteryCapacity * timeDelta.total_seconds()/3600 * 100 + chargingVal # change seconds to hours 
            data.append(min(soc, 90))  
            labels.append(routeInfo.stay[i])          
            
        print('data', data)
        return JsonResponse({'labels': labels, 'data': data}) 
    else:
        return redirect('/')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
