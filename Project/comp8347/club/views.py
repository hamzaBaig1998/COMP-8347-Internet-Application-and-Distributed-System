import datetime
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from club.FxUtil import compute_fx_amount, SYMBOL_MAP, clear_fx_cache
from club.forms import TierForm, FxForm, PaymentForm
from club.models import Club, Fx, Order
from courses.models import Course


# Create your views here.
# def get_user_membership(request):
#     user_membership_qs = UserMembership.objects.filter(user=request.user)
#     if user_membership_qs.exists():
#         return user_membership_qs.first()
#     return None
#
#
# def get_user_subscription(request):
#     user_subscription_qs = Subscription.objects.filter(user_membership=get_user_membership(request))
#     if user_subscription_qs.exists():
#         user_subscription = user_subscription_qs.first()
#         return user_subscription
#     return None
#
#
# def get_selected_membership(request):
#     membership_type = request.session['selected_membership_type']
#     selected_membership_qs = Membership.objects.filter(membership_type=membership_type)
#
#     if selected_membership_qs.exists(): return selected_membership_qs.first()
#     return None
#

def compute_fx_details(price):
    data = {}
    for currency in SYMBOL_MAP.keys():
        data[currency] = compute_fx_amount(currency, price)
    return data


class ClubView(View):

    def get(self, request):
        fx_form = FxForm()
        return render(request, "club/club_details.html", context={'fx_form': fx_form, 'type': 'get'})

    def post(self, request):
        clear_fx_cache()

        fx_choice = Fx.objects.get(id=request.POST['fx_choice'])
        print(fx_choice.fx_code)
        clubs = Club.objects.all()
        # print(f"Club details => {clubs}")
        club_details = {}
        fx_details = {}
        courses = Course.objects.all()
        for club in clubs:
            # print(f"Club data => {club}, club detail => {club.details}")
            tier = club.tier
            details = [course.title.strip() for course in courses.filter(club=club)]
            club_details[tier] = details
            fx_details[club.price] = compute_fx_details(club.price)
        # print(club_details)
        print(fx_details)
        tier_form = TierForm()
        request.session['fx_id'] = fx_choice.id
        request.session['fx_details'] = json.dumps(fx_details)
        print(request.session['fx_details'])
        return render(request, "club/club_details.html", context={'tiers': clubs,
                                                                  'club_details': club_details,
                                                                  'tier_form': tier_form,
                                                                  'fx_details': fx_details,
                                                                  'fx_choice': fx_choice.fx_code,
                                                                  'fx_sign': fx_choice.fx_sign})


def compute_uuid():
    import uuid
    return uuid.uuid4()


def save_order(session_data, card_details, outcome):
    current_dt = datetime.datetime.now()
    fx_amount = session_data['fx_amount']
    fx_choice = session_data['fx_choice']
    amount = session_data['amount']
    order_id = session_data['oid']
    user_id = session_data['uid']
    tier = session_data['tier']
    card_detail = card_details['card_number']
    order = Order.objects.create(order_id=order_id,
                                 user_id=user_id,
                                 tier=tier,
                                 amount_cad=amount,
                                 amount_fx=fx_amount,
                                 fx_choice=fx_choice,
                                 order_time=current_dt,
                                 card_last_6=card_detail,
                                 result=outcome)
    print(f"Saved order {order}")
    return order


@method_decorator(login_required, name='post')  # to enforce login is done before accessing the post method
class PayView(View):
    def get(self, request):
        return redirect('club:club_details')

    def post(self, request):
        if "card_number" not in request.POST:
            print(f"Post data => {request.POST}")
            fx = Fx.objects.get(id=request.session['fx_id'])
            fx_details = dict(json.loads(request.session['fx_details']))
            user_id = request.user.id
            order_id = compute_uuid()
            tier = Club.objects.get(id=request.POST['options'])
            amount = fx_details.get(str(tier.price)).get(fx.fx_code)
            pay_form = PaymentForm()

            # request.session.clear()
            request.session['fx_amount'] = amount
            request.session['fx_choice'] = fx.id
            request.session['amount'] = tier.price
            request.session['oid'] = str(order_id)
            request.session['uid'] = user_id
            request.session['tier'] = tier.tier

            return render(request, "club/payment.html", context={
                "tier": tier,
                "fx_sign": fx.fx_sign,
                "amount": amount,
                "pay_form": pay_form
            })
        else:
            # the user has entered some details and here we need to request the external server for payment status
            import requests
            txn = requests.post("http://127.0.0.1:8083/pay", data=dict(request.POST), timeout=5)
            data = json.loads(txn.content)

            if data['result'] == "Ok":
                print("Payment done!")
                save_order(request.session, request.POST, True)
                return render(request, "club/paymentOk.html")
            else:
                print("Payment failed!")
                save_order(request.session, request.POST, False)
                return render(request, "club/paymentFail.html")

# class MembershipSelectView(ListView):
#     template_name = 'club/club_details.html'
#     context_object_name = 'club'
#     model = Membership
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         current_membership = get_user_membership(self.request)
#         context['current_membership'] = str(current_membership.membership)
#         return context
#
#     def post(self, request, *args, **kwargs):
#         selected_membership_type = request.POST.get('membership_type')
#
#         user_membership = get_user_membership(self.request)
#         user_subscription = get_user_subscription(self.request)
#
#         selected_membership_qs = Membership.objects.filter(membership_type=selected_membership_type)
#         if selected_membership_qs.exists():
#             selected_membership = selected_membership_qs.first()
#
#         """
#         Validation to check if user club == selected_membership
#         """
#         if user_membership.membership == selected_membership:
#             if user_subscription != None:
#                 messages.info(request, 'The selected club is your current Memberships, your next payment would be due by {}'.format('get this value from stripe'))
#                 return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#         # PASS THE SELECTED_MEMBERSHIP INTO THE SESSION TO BE ABLE TO PAS IT INTO THE NEXT VIEWW
#         request.session['selected_membership_type'] = selected_membership.membership_type
#         # the above code is passing the value of enterprise or professional into the next veiw
#         return HttpResponseRedirect(reverse('club:payment'))
#
#
# @login_required
# def PaymentView(request):
#     user_membership = get_user_membership(request)
#     try:
#         selected_membership = get_selected_membership(request)
#     except:
#         return redirect(reverse("club:select_membership"))
#     publishKey = settings.STRIPE_PUBLISHABLE_KEY
#     if request.method == "POST":
#         # try:
#         token = request.POST['stripeToken']
#
#         # UPDATE FOR STRIPE API CHANGE 2018-05-21
#
#         '''
#         First we need to add the source for the customer
#         '''
#
#         customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
#         customer.source = token  # 4242424242424242
#         customer.save()
#
#         '''
#         Now we can create the subscription using only the customer as we don't need to pass their
#         credit card source anymore
#         '''
#
#         subscription = stripe.Subscription.create(
#             customer=user_membership.stripe_customer_id,
#             items=[
#                 {"plan": selected_membership.stripe_plan_id},
#             ]
#         )
#         print(subscription.id)
#
#         return redirect(reverse('club:update_transaction',
#                                 kwargs={
#                                     'subscription_id': subscription.id
#                                 }))
#
#         # except:
#         #     messages.info(request, "An error has occurred, investigate it in the console")
#
#     context = {
#         'publishKey': publishKey,
#         'selected_membership': selected_membership
#     }
#
#     return render(request, "club/payment.html", context)
#
#
# @login_required
# def UpdateTransactionRecords(request, subscription_id):
#     user_membership = get_user_membership(request)
#     selected_membership = get_selected_membership(request)
#     user_membership.membership = selected_membership
#     user_membership.save()
#
#     sub, created = Subscription.objects.get_or_create(user_membership=user_membership)
#     sub.stripe_subscription_id = subscription_id
#     sub.active = True
#     sub.save()
#
#     try:
#         del request.session['selected_membership_type']
#     except:
#         pass
#
#     messages.info(request, 'Successfully created {} club'.format(selected_membership))
#     return redirect(reverse('club:select_membership'))
#
#
# @login_required
# def CancelSubscription(request):
#     user_sub = get_user_subscription(request)
#
#     if user_sub.active is False:
#         messages.info(request, "You dont have an active club")
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#     sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
#     sub.delete()
#
#     user_sub.active = False
#     user_sub.save()
#
#     free_membership = Membership.objects.get(membership_type='Free')
#     user_membership = get_user_membership(request)
#     user_membership.membership = free_membership
#     user_membership.save()
#     user = get_object_or_404(User, username=request.username)
#     user_email = user.email
#
#     messages.info(request, "Successfully cancelled club. We have sent an email")
#     # sending an email here
#     send_mail(
#         'Subscription successfully cancelled',
#         'Successfully cancelled club. We have sent an email',
#         'adebisiayomide68@gmail.com',
#         [user_email],
#         fail_silently=False,
#     )
#
#     return redirect(reverse('club:select'))
