from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course, Lesson, Category, Request, Contact
from club.models import Order, User, Club
from courses.form import RequestForm
from django.db.models import Prefetch

from django.shortcuts import render, redirect
from django.views import View
from .models import Request
from django.views.generic import ListView
from django.db.models import Q
from .models import Course
from django.contrib import messages

class RequestTeacherView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('e-mail')
        phone = request.POST.get('phone')
        request_obj = Request(name=name, email=email, phone=phone)
        request_obj.save()
        messages.success(request, 'Your request was submitted successfully.')
        return render(request, 'index.html')                                       
    
# View for the home page
class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # Retrieve all categories with count of courses and add them to the context
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        categories_with_count = []
        for category in categories:
            # print(category)
            course_count = Course.objects.filter(category=category).count()
            categories_with_count.append((category, course_count))
        context['categories'] = categories_with_count
        print(context['categories'])
        return context


# View for the about page
class AboutView(TemplateView):
    template_name = 'about.html'


# View for the contact page
# class ContactView(TemplateView):
#     template_name = 'contact.html'


# View for the course list page
class CourseListView(ListView):
    model = Course  # Use the Course model
    context_object_name = 'courses'  # Use 'courses' as the context variable name
    template_name = 'courses/course_list.html'
    def get_queryset(self):
        return Course.objects.select_related('creator').prefetch_related(
            Prefetch('club', queryset=Club.objects.all())
        )


# View for the course detail page
class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = self.object.lessons.all().order_by('position')
        return context


# View for the lesson detail page
class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    context_object_name = 'lesson'
    template_name = 'courses/lesson_detail.html'

    def get_object(self, queryset=None):
        course_slug = self.kwargs.get('course_slug')
        lesson_slug = self.kwargs.get('lesson_slug')
        return get_object_or_404(Lesson, course__slug=course_slug, slug=lesson_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = context['lesson']
        orders = Order.objects.filter(user_id=self.request.user.id, result=True)
        tier = None
        if orders.exists():
            tier = orders.last().tier
        if not lesson.course.club.has_tier(tier):
            context['membership_required'] = True
        return context
    
class CourseSearchView(ListView):
    model = Course
    template_name = 'courses/course_search.html'
    context_object_name = 'courses'

    def get_queryset(self):
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        queryset = super().get_queryset()

        if query and category:
            queryset = queryset.filter(
                Q(title__icontains=query) &
                Q(category__category__icontains=category)
            )
        elif query:
            queryset = queryset.filter(title__icontains=query)
        elif category:
            queryset = queryset.filter(category__category__icontains=category)

        return queryset
    

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()
        return render(request, 'contact.html', {'success': True})
    

# def get(self,request,course_slug,lesson_slug,*args,**kwargs):
#
#     course_qs = Course.objects.filter(slug=course_slug)
#     if course_qs.exists():
#         course = course_qs.first()
#     lesson_qs = course.lessons.filter(slug=lesson_slug)
#     if lesson_qs.exists():
#         lesson = lesson_qs.first()
#     user_membership = UserMembership.objects.filter(user=request.user).first()
#     user_membership_type = user_membership.membership.membership_type
#
#     course_allowed_membership_type = course.allowed_memberships.all()
#     context = {'lessons':None}
#
#     if course_allowed_membership_type.filter(membership_type=user_membership_type).exists():
#         context = {'lesson':lesson}
#
#     return render(request,'courses/lesson_detail.html',context)
