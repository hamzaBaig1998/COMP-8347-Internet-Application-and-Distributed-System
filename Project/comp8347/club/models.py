from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    tier = models.CharField(max_length=51)
    price = models.IntegerField(default=35)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"Tier: {self.tier}, pricing: ${self.price}"

    def create_tier(self, name, price, details=""):
        club = Club()
        club.name, club.price, club.details = name, price, details
        Club.objects.create(club)
        print(f"Club objects: {Club.objects.all()}")

    class Meta:
        ordering = ['price']


class Fx(models.Model):
    fx_name = models.CharField(max_length=25, default="Canadian Dollar")
    fx_sign = models.CharField(max_length=5, default="C$")
    fx_code = models.CharField(max_length=5, default="CAD")

    def __str__(self):
        return f"{self.fx_name}, {self.fx_code}, {self.fx_sign}"

    class Meta:
        ordering = ['fx_name']


class Order(models.Model):
    order_id = models.CharField(max_length=100)
    user_id = models.IntegerField()
    tier = models.CharField(max_length=10)
    amount_cad = models.IntegerField()
    amount_fx = models.DecimalField(max_digits=10, decimal_places=2)
    fx_choice = models.IntegerField()
    order_time = models.DateTimeField()
    card_last_6 = models.IntegerField(max_length=6)
    result = models.BooleanField()

    def __str__(self):
        user = User.objects.get(id=self.user_id)
        return f"{self.order_id}, {user}, {self.tier}, {self.amount_cad}, {self.result}"

# class Membership(models.Model):
#     slug = models.SlugField()
#     membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default='Free', max_length=30)
#     price = models.IntegerField(default=15)
#     stripe_plan_id = models.CharField(max_length=40)
#
#     def __str__(self):
#         return self.membership_type
#
#
# class UserMembership(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     stripe_customer_id = models.CharField(max_length=40)
#     membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, blank=True)
#
#     def __str__(self):
#         return self.user.username
#
#
# def post_save_create_user_membership(sender, instance, created, *args, **kwargs):
#     if created:
#         UserMembership.objects.get_or_create(user=instance)
#     user_membership, created = UserMembership.objects.get_or_create(user=instance)
#     if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
#         new_customer_id = stripe.Customer.create(email=instance.email)
#         user_membership.stripe_customer_id = new_customer_id['id']
#         user_membership.save()
#
#
# post_save.connect(post_save_create_user_membership, User)
#
