from django.contrib import admin
from courses.models import Course,Lesson,Category,Request,Contact
# Register your models here.

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Category)
admin.site.register(Request)
admin.site.register(Contact)