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
from users.models import Profile, User


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
    card_detail = card_details.get('card_number', '0000000000000000')
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
    club = Club.objects.filter(tier=tier).first()
    profile = Profile.objects.filter(user=User.objects.get(id=user_id)).first()
    profile.set_club(club)
    profile.save()
    print(f"Profile of {profile} updated with club being {profile.club}")
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

            if tier.tier == "Free":
                save_order(request.session, request.POST, True)
                return render(request, "club/paymentOk.html")

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
