from django.test import TestCase
from django.core import mail 
from .models import Route, CustomUser 
# Create your tests here.

class JobTestCase(TestCase):
    """ This class contains unit test for the Route database model """
    @classmethod 
    def setUpTestData(cls):
        # Sets up data for the whole test case 
        cls.DEFAULT_FROM_EMAIL = 'guerrerj@uvic.ca'
        cls.usr =CustomUser.objects.create_user('admin', 'jose.guerrero10@yahoo.com', 'admin', is_superuser=True, isAdminUser=True, is_staff=True)
        
    def test_send_email(self):
        expectedSubject = 'Your print job from UVIC3D Web app has an associated cost'
        expectedMessage = 'You owe money for your print job. Please make a payment at the library in order to print.'
        expectedRecipient = 'test@gmail.com'
        mail.send_mail(
                    subject=expectedSubject,
                    message= expectedMessage,
                    from_email=self.DEFAULT_FROM_EMAIL,
                    recipient_list=[expectedRecipient],
                    fail_silently=False,
                )
        # Test message has been sent 
        self.assertEqual(len(mail.outbox), 1)
        
        # Verify that the subject of the message is correct 
        self.assertEqual(mail.outbox[0].subject, expectedSubject)
        
    def test_create_job(self):
        projtitle = 'testTitle'
        filenam="test.stl"
        jobdet = "Blue color"
        cst = 5.00
        job = Route.objects.create(projectTitle=projtitle, fileName=filenam, jobDetails=jobdet, cost=cst, user=self.usr)
        self.assertNotEqual(job, None)
   
    def test_job_title(self):
        projtitle = 'testTitle'
        filenam="test.stl"
        jobdet = "Blue color"
        cst = 5.00
        job = Route.objects.create(projectTitle=projtitle, fileName=filenam, jobDetails=jobdet, cost=cst, user=self.usr)       
        self.assertEqual(job.projectTitle, projtitle)
   
    def test_job_file(self):
        projtitle = 'testTitle'
        filenam="test.stl"
        jobdet = "Blue color"
        cst = 5.00
        job = Route.objects.create(projectTitle=projtitle, fileName=filenam, jobDetails=jobdet, cost=cst, user=self.usr)       
        self.assertEqual(job.fileName, filenam)
 
    def test_job_details(self):
        projtitle = 'testTitle'
        filenam="test.stl"
        jobdet = "Blue color"
        cst = 5.00
        job = Route.objects.create(projectTitle=projtitle, fileName=filenam, jobDetails=jobdet, cost=cst, user=self.usr)       
        self.assertEqual(job.jobDetails, jobdet)
       
    def test_job_cost(self):
        projtitle = 'testTitle'
        filenam="test.stl"
        jobdet = "Blue color"
        cst = 5.00
        job = Route.objects.create(projectTitle=projtitle, fileName=filenam, jobDetails=jobdet, cost=cst, user=self.usr)       
        self.assertEqual(job.cost, cst) 
        
    def test_job_user(self):
        projtitle = 'testTitle'
        filenam="test.stl"
        jobdet = "Blue color"
        cst = 5.00
        job = Route.objects.create(projectTitle=projtitle, fileName=filenam, jobDetails=jobdet, cost=cst, user=self.usr)       
        self.assertEqual(job.user, self.usr)
        
    def test_update_price(self):
        projtitle = 'testTitle'
        filenam="test.stl"
        jobdet = "Blue color"
        cst = 5.00
        job = Route.objects.create(projectTitle=projtitle, fileName=filenam, jobDetails=jobdet, cost=cst, user=self.usr)  
        cst = 20.00
        job.cost = cst  
        job.save() 
        job1 = Route.objects.get(pk=job.jobId)
        self.assertEqual(job1.cost, cst) 
        
    def test_update_paycomplete(self):
        projtitle = 'testTitle'
        filenam="test.stl"
        jobdet = "Blue color"
        cst = 5.00
        job = Route.objects.create(projectTitle=projtitle, fileName=filenam, jobDetails=jobdet, cost=cst, user=self.usr)  
        job.paymentCompleted = True 
        job.save() 
        job1 = Route.objects.get(pk=job.jobId)
        self.assertEqual(job1.paymentCompleted, True) 
    
class CustomUserTestCase(TestCase):
    """ This class contains unit test for the custom user database model """
    def test_createAdminUser(self):
        """ Test the creation of a new user """ 
        user = CustomUser.objects.create_user('admin', 'jose.guerrero10@yahoo.com', 'admin', is_superuser=True, isAdminUser=True, is_staff=True)
        self.assertNotEqual(user, None)
        
    def test_admin_hasAdminStatus(self):
        user = CustomUser.objects.create_user('admin', 'jose.guerrero10@yahoo.com', 'admin', is_superuser=True, isAdminUser=True, is_staff=True)
        self.assertEqual(user.isAdminUser, True) 
    
    def test_admin_hasStaffStatus(self):
        user = CustomUser.objects.create_user('admin', 'jose.guerrero10@yahoo.com', 'admin', is_superuser=True, isAdminUser=True, is_staff=True)
        self.assertEqual(user.is_staff, True)
        
    def test_create_normalUser(self):
        user = CustomUser.objects.create_user('normal', 'jose.guerrero10@yahoo.com', 'normal')
        self.assertNotEqual(user, None) 
        
    def test_normal_doesNotHaveAdminStatus(self):
        user = CustomUser.objects.create_user('normal', 'jose.guerrero10@yahoo.com', 'normal')
        self.assertEqual(user.isAdminUser, False)
    
    def test_normal_doesNotHaveStaffStatus(self):
        user = CustomUser.objects.create_user('normal', 'jose.guerrero10@yahoo.com', 'normal')
        self.assertEqual(user.is_staff, False)       
        
