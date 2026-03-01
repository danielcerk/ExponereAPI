import os
import stripe
from dateutil.relativedelta import relativedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import ( 
    IsAuthenticated,
    BasePermission, 
    SAFE_METHODS
)

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

from .models import CheckoutSessionRecord, Plan
from .serializers import ( 
    CheckoutSessionResponseSerializer, 
    CheckoutSessionSerializer,
    PlanSerializer
)

from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN = settings.DOMAIN

class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:

            return True
        
        return request.user and (request.user.is_staff or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True
        
        return request.user.is_staff or request.user.is_superuser

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return False
        
        return obj.user == request.user

@method_decorator(ratelimit(key='ip', rate='30/m', method='POST', block=True), name='dispatch')
class PlanModelViewSet(ModelViewSet):

    permission_classes = [IsAdminOrReadOnly]
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='dispatch')
class CancelAPIView(APIView):

    permission_classes = [IsOwner]

    def post(self, request):

        checkout_record = CheckoutSessionRecord.objects.filter(user=request.user).last()

        if not checkout_record or not checkout_record.stripe_customer_id:

            return Response(

                {"error": "Nenhuma assinatura ativa encontrada"},
                status=status.HTTP_404_NOT_FOUND

            )

        subscriptions = stripe.Subscription.list(customer=checkout_record.stripe_customer_id, limit=1)

        if not subscriptions.data:

            return Response(

                {"error": "Nenhuma assinatura ativa para este cliente"},
                status=status.HTTP_404_NOT_FOUND

            )

        subscription = subscriptions.data[0]

        canceled = stripe.Subscription.delete(subscription.id)

        checkout_record.plan_end_date = checkout_record.plan_start_date + relativedelta(months=1)
        checkout_record.status = CheckoutSessionRecord.PaymentStatus.CANCELED

        checkout_record.save()

        return Response(

            {"detail": "Assinatura cancelada com sucesso", "subscription_id": canceled.id},
            status=status.HTTP_200_OK

        )
@method_decorator(ratelimit(key='ip', rate='20/m', method='POST', block=True), name='dispatch')
class SuccessAPIView(APIView):

    def get(self, request):

        session_id = request.query_params.get('session_id')

        if not session_id:

            return Response({'error': 'session_id ausente'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': 'Pagamento realizado com sucesso', 'session_id': session_id})

# Esse aqui, deve fazer toda a questão de pagamento e processamento aqui
'''@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='dispatch')
class CreateCheckoutSessionAPIView(APIView):

    permission_classes = [IsOwner]

    def post(self, request):

        pass'''

# Esse aqui, redireciona para a página de pagamento da stripe

@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='dispatch')
class CreateCheckoutSessionAPIView(APIView):

    permission_classes = [IsOwner]

    def post(self, request):

        serializer = CheckoutSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        price_lookup_key = serializer.validated_data['price_lookup_key']

        try:

            prices = stripe.Price.list(lookup_keys=[price_lookup_key], expand=['data.product'])

            if not prices.data:

                return Response({'error': 'Preço não encontrado'}, status=404)

            price_item = prices.data[0]
            product = price_item.product

            checkout_record = CheckoutSessionRecord.objects.filter(user=request.user).last()

            if not checkout_record.stripe_customer_id:

                customer = stripe.Customer.create(
                    email=request.user.email,
                    name=request.user.name,
                    metadata={'user_id': str(request.user.id)}
                )

                checkout_record.stripe_customer_id = customer.id

            checkout_session = stripe.checkout.Session.create(
                line_items=[{'price': price_item.id, 'quantity': 1}],
                mode='subscription',
                success_url=DOMAIN + '/api/v1/subscription/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=DOMAIN + '/api/v1/subscription/cancel',
                subscription_data={
                    'metadata': {
                        'trial_period_days': 7,
                        'product_id': str(product.id),
                        'product_name': str(product.name),
                        'product_price': str(price_item.unit_amount / 100),
                        'user_id': str(request.user.id),
                    }
                }
            )

            if price_lookup_key == settings.STRIPE_LOCAL_PLAN_PREMIUM: # <- Esses aqui são as chaves de pesquisa dos planos, onde posso mudar de outros planos

                checkout_record.plan = get_object_or_404(Plan, lookup_key_plan=price_lookup_key)

            elif price_lookup_key == settings.STRIPE_LOCAL_PLAN_PREMIUM_2:

                checkout_record.plan = get_object_or_404(Plan, lookup_key_plan=price_lookup_key)

            checkout_record.stripe_checkout_session_id = checkout_session.id
            checkout_record.stripe_price_id = price_item.id
            checkout_record.plan_start_date = timezone.now()

            checkout_record.stripe_subscription_id = checkout_session.subscription
            checkout_record.stripe_payment_intent_id = getattr(checkout_session, 'payment_intent', None)
            
            checkout_record.save()

            response_data = {
                'checkout_url': checkout_session.url,
                'session_id': checkout_session.id,
                'customer_id': checkout_record.stripe_customer_id,
                'subscription_id': checkout_session.subscription,
                'payment_intent_id': getattr(checkout_session, 'payment_intent', None),
            }

            response_serializer = CheckoutSessionResponseSerializer(response_data)

            return Response(response_serializer.data, status=201)

        except Exception as e:

            return Response({'error': str(e)}, status=500)

@method_decorator(ratelimit(key='ip', rate='3/m', method='POST', block=True), name='dispatch')    
class UpgradeDowngradeSessionAPIView(APIView):

    permission_classes = [IsOwner]

    def post(self, request):

        serializer = CheckoutSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_price_lookup_key = serializer.validated_data['price_lookup_key']
        checkout_record = CheckoutSessionRecord.objects.filter(user=request.user).last()

        if not checkout_record or not checkout_record.stripe_subscription_id:

            return Response({'error': 'Nenhuma assinatura ativa encontrada'}, status=404)

        try:

            prices = stripe.Price.list(lookup_keys=[new_price_lookup_key], expand=['data.product'])

            if not prices.data:

                return Response({'error': 'Preço não encontrado'}, status=404)

            new_price_item = prices.data[0]

            subscription = stripe.Subscription.retrieve(checkout_record.stripe_subscription_id)

            stripe.Subscription.modify(

                subscription.id,
                cancel_at_period_end=False,
                items=[{
                    'id': subscription['items']['data'][0].id,
                    'price': new_price_item.id,
                }]

            )

            plan = get_object_or_404(Plan, lookup_key_plan=new_price_lookup_key)

            checkout_record.plan = plan
            checkout_record.plan_end_date = None
            checkout_record.status = CheckoutSessionRecord.PaymentStatus.COMPLETED
            checkout_record.has_access = True
            checkout_record.is_completed = True
            checkout_record.stripe_price_id = new_price_item.id

            checkout_record.save()

            return Response({'detail': f'Assinatura alterada para {plan.name} com sucesso'}, status=200)

        except Exception as e:

            return Response({'error': str(e)}, status=500)



@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        webhook_secret = settings.STRIPE_WEBHOOK_SECRET
        signature = request.META.get('HTTP_STRIPE_SIGNATURE')
        payload = request.body

        try:

            event = stripe.Webhook.construct_event(

                payload=payload, sig_header=signature, secret=webhook_secret

            )

        except ValueError as e:

            return Response({'error': 'Payload inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
        except stripe.error.SignatureVerificationError:

            return Response({'error': 'Assinatura inválida'}, status=status.HTTP_400_BAD_REQUEST)

        self._update_record(event)

        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    def _update_record(self, webhook_event):

        data_object = webhook_event['data']['object']
        event_type = webhook_event['type']

        if event_type == 'checkout.session.completed':

            try:

                checkout_record = CheckoutSessionRecord.objects.get(

                    stripe_checkout_session_id=data_object['id']

                )

            except CheckoutSessionRecord.DoesNotExist:

                return

            metadata = data_object.get('metadata', {})

            checkout_record.stripe_customer_id = data_object['customer']
            checkout_record.stripe_subscription_id = data_object.get('subscription')

            checkout_record.currency = data_object.get('currency', 'BRL')

            checkout_record.mark_as_completed()

            checkout_record.save()

        elif event_type == 'customer.subscription.updated':

            try:

                checkout_record = CheckoutSessionRecord.objects.get(

                    stripe_subscription_id=data_object['id']

                )

            except CheckoutSessionRecord.DoesNotExist:

                return

            price_lookup_key = data_object['items']['data'][0]['price']['lookup_key']

            if price_lookup_key == settings.STRIPE_LOCAL_PLAN_PREMIUM:

                plan = Plan.objects.get(lookup_key_plan=price_lookup_key)

            elif price_lookup_key == settings.STRIPE_LOCAL_PLAN_PREMIUM_2:

                plan = Plan.objects.get(lookup_key_plan=price_lookup_key)

            else:

                plan = None

            if plan:

                checkout_record.plan = plan

                checkout_record.save()

        elif event_type == 'customer.subscription.deleted':

            try:

                checkout_record = CheckoutSessionRecord.objects.get(

                    stripe_subscription_id=data_object['id']

                )

            except CheckoutSessionRecord.DoesNotExist:

                return

            checkout_record.status = CheckoutSessionRecord.PaymentStatus.CANCELED

            checkout_record.save()

@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='dispatch')
class RemoveAccess4CanceledPlan(APIView):

    def get(self, request):

        today = timezone.localdate()
        
        expired_checkouts = CheckoutSessionRecord.objects.filter(
            plan_end_date__lte=today,
            has_access=True
        )

        free_plan = Plan.objects.filter(name='Grátis').first()
        count = 0

        for checkout in expired_checkouts:

            checkout.has_access = False
            checkout.is_completed = False
            
            checkout.plan = free_plan
            checkout.plan_end_date = None

            checkout.save()

            count += 1

        return Response(
            {"detail": f"OK"},
            status=status.HTTP_200_OK
        )