from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course, Lesson, Category, Request
from memberships.models import UserMembership
from courses.form import RequestForm


class RequestView(View):
    def get(self, request):
        form = RequestForm()
        return render(request, 'request.html', {'form': form})
    
    def post(self, request):
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'request_success.html')
        else:
            return render(request, 'request.html', {'form': form})
    
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
class ContactView(TemplateView):
    template_name = 'contact.html'


# View for the course list page
class CourseListView(ListView):
    model = Course  # Use the Course model
    context_object_name = 'courses'  # Use 'courses' as the context variable name
    template_name = 'courses/course_list.html'


# View for the course detail page
class CourseDetailView(DetailView):
    model = Course  # Use the Course model
    context_object_name = 'course'  # Use 'course' as the context variable name
    template_name = 'courses/course_detail.html'


# View for the lesson detail page
class LessonDetailView(LoginRequiredMixin, View):
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        # Retrieve the course and lesson objects
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)

        # Retrieve the user's membership and its type
        user_membership = get_object_or_404(UserMembership, user=request.user)
        user_membership_type = user_membership.membership.membership_type

        # Retrieve the membership types allowed for the course
        course_allowed_membership_type = course.allowed_memberships.all()

        # If the user's membership type is allowed for the course, show the lesson
        if course_allowed_membership_type.filter(membership_type=user_membership_type).exists():
            context = {'lesson': lesson}
        # Otherwise, do not show the lesson
        else:
            context = {'lesson': None}

        return render(request, "courses/lesson_detail.html", context)
    
from django.views.generic import ListView
from django.db.models import Q
from .models import Course

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
