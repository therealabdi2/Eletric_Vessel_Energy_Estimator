from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from django.views.generic.base import TemplateView
from django.http.response import JsonResponse, HttpResponse
from JobTracker.models import Job
import stripe 
import os 

# Create your views here.
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': os.getenv('STRIPE_PUBLISHABLE_KEY')}
        return JsonResponse(stripe_config, safe=False)
    
    
@csrf_exempt
def create_checkout_session(request, jobId):
    if request.method == 'GET':
        domain_url = os.getenv('DOMAIN_URL')
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        try:
            printRequest = Job.objects.get(pk=jobId)            
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.userId if request.user.is_authenticated else None,
                success_url=domain_url + 'payments/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'payments/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': printRequest.projectTitle,
                        'quantity': 1,
                        'currency': 'cad',
                        'amount': int(printRequest.cost*100), # must be in the smallest currency which is cents 
                    }
                ],
                metadata = {
                    "jobId": printRequest.jobId
                }
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})
        
        

class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'
    
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None   
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        jobId = event['data']['object']['metadata']['jobId']
        printRequest =Job.objects.get(pk=jobId)        
        printRequest.paymentCompleted = True 
        printRequest.save()

    return HttpResponse(status=200)