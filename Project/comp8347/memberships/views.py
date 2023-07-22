from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from memberships.models import Membership, UserMembership, Subscription

import stripe

User = get_user_model()

# helper function to get the user's membership
@login_required
def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    return user_membership_qs.first() if user_membership_qs.exists() else None

# helper function to get the user's subscription
@login_required
def get_user_subscription(request):
    user_membership = get_user_membership(request)
    user_subscription_qs = Subscription.objects.filter(user_membership=user_membership)
    return user_subscription_qs.first() if user_subscription_qs.exists() else None

# helper function to get the selected membership
@login_required
def get_selected_membership(request):
    membership_type = request.session.get('selected_membership_type')
    selected_membership_qs = Membership.objects.filter(membership_type=membership_type)
    return selected_membership_qs.first() if selected_membership_qs.exists() else None

class MembershipSelectView(ListView):
    template_name = 'memberships/membership_list.html'
    context_object_name = 'memberships'
    model = Membership

    # add the current membership to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership) if current_membership else None
        return context

    # handle the form submission to select a membership
    def post(self, request, *args, **kwargs):
        selected_membership_type = request.POST.get('membership_type')

        # get the user's current membership and subscription
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)

        # get the selected membership
        selected_membership = get_selected_membership(request)
        if not selected_membership:
            messages.error(request, 'Invalid membership type selected')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # check if the user is already subscribed to the selected membership
        if user_membership and user_membership.membership == selected_membership:
            if user_subscription and user_subscription.active:
                messages.info(request, 'You are already subscribed to this membership plan.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # store the selected membership type in the session and redirect to the payment page
        request.session['selected_membership_type'] = selected_membership.membership_type
        return HttpResponseRedirect(reverse('memberships:payment'))

@login_required
def PaymentView(request):
    # get the user's current membership, selected membership, and subscription
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)

    if not selected_membership:
        messages.error(request, 'Invalid membership type selected')
        return redirect(reverse('memberships:select_membership'))

    # set up Stripe
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == "POST":
        # process the payment
        token = request.POST['stripeToken']

        try:
            customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
            customer.source = token
            customer.save()

            subscription = stripe.Subscription.create(
                customer=user_membership.stripe_customer_id,
                items=[
                    {"plan": selected_membership.stripe_plan_id},
                ]
            )

            # redirect to the transaction update page
            return redirect(reverse('memberships:update_transaction',
                                     kwargs={
                                         'subscription_id': subscription.id
                                     }))
        except stripe.error.StripeError as e:
            # handle any Stripe errors
            messages.error(request, f"An error has occurred: {e}")

    # render the payment page
    context = {
        'publishKey': publishKey,
        'selected_membership': selected_membership
    }
    return render(request, "memberships/membership_payment.html", context)

@login_required
def UpdateTransactionRecords(request, subscription_id):
    # get the user's current membership and selected membership
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)

    if not selected_membership:
        messages.error(request, 'Invalid membership type selected')
        return redirect(reverse('memberships:select_membership'))

    # update the user's membership and subscription records
    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.objects.get_or_create(user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    # remove the selected membership type from the session
    try:
        del request.session['selected_membership_type']
    except KeyError:
        pass    # display a success message and redirect to the membership selection page
    messages.success(request, f'Successfully created {selected_membership} membership')
    return redirect(reverse('memberships:select_membership'))

@login_required
def CancelSubscription(request):
    # get the user's current membership and subscription
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)

    if not user_membership or not user_subscription or not user_subscription.active:
        messages.error(request, "You don't have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # cancel the subscription in Stripe and update the user's membership and subscription records
    sub = stripe.Subscription.retrieve(user_subscription.stripe_subscription_id)
    sub.delete()

    user_subscription.active = False
    user_subscription.save()

    free_membership = Membership.objects.get(membership_type='Free')
    user_membership.membership = free_membership
    user_membership.save()

    # send an email to the user to confirm the cancellation
    user_email = user_membership.user.email
    messages.success(request, "Successfully cancelled membership. An email has beensent to you.")
    send_mail(
        'Subscription successfully cancelled',
        'Successfully cancelled membership. An email has been sent to you.',
        'adebisiayomide68@gmail.com',
        [user_email],
        fail_silently=False,
    )

    # redirect to the membership selection page
    return redirect(reverse('memberships:select_membership'))