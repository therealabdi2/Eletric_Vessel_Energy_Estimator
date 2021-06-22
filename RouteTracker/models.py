from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import User
from EVEESystem.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail 
from .validators import validateFileExtension


class CustomUser(AbstractUser):    
    userId        = models.AutoField(primary_key=True)
    createdDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    lastAccessDate  = models.DateTimeField(auto_now=True, auto_now_add=False)
    isAdminUser = models.BooleanField(default=False)
    studentId = models.CharField(max_length=10)
    
    class Meta:
        ordering =["-username"]
        verbose_name = 'User'
"""    
class Author(models.CustomUser):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
"""
    # def __str__(self):
    #     """ Allows admin to view username as objects  """
    #     return self.username
# To sync db -> python manage.py migrate --run-syncdb
#Manually delete migrations folder, delete sqlite3 then run makemigrations then migrate 

class Route(models.Model):
    routeId            = models.AutoField(primary_key=True)
    user               = models.ForeignKey(CustomUser, verbose_name="User", on_delete=models.CASCADE)
    # cost             = models.DecimalField(max_digits=6, decimal_places=2)
    dateAdded          = models.DateTimeField(auto_now=False, auto_now_add=True)
    # jobCompleted     = models.BooleanField(default=False)
    # paymentCompleted = models.BooleanField(default=False)
    routeTitle     = models.CharField(max_length=50, verbose_name="Project Title", default="")
    fileName         = models.FileField(upload_to='uploads/%Y/%m/%d/', max_length=100, verbose_name="STL File", validators=[validateFileExtension])
    # jobDetails       = models.TextField(verbose_name="Route Details", default="", blank=True)
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.pk is not None:
            orig = Route.objects.get(pk=self.pk)
            if orig.cost!= self.cost:
                user = list(CustomUser.objects.filter(username=orig.user))[0]
                send_mail(
                    subject='Your print job from UVIC3D Web app has an associated cost',
                    message='You owe money for your print job. Please make a payment at the library in order to print.',
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
        super(Route, self).save()           
    
    class Meta:
        """ Allows to define metadata for the database """
        ordering = ["dateAdded"]
        db_table = 'Route'
        verbose_name = "Route List"
    
    def __str__(self):
        """ Lets us name instances of each record(row) """
        return str(self.jobId)
    
    def get_absolute_url(self):
        return reverse("jobs/view", kwargs={})
