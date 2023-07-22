from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course, Lesson, Category
from club.models import Order, User, Club


# View for the home page
class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # Retrieve all categories and add them to the context
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
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
        context = {'lesson': None}
        orders = Order.objects.filter(user_id=request.user.id, result=True)
        tier = None
        if orders.exists():
            tier = orders.last().tier
        user = User.objects.get(id=request.user.id)
        if user:
            context['lesson'] = Club.objects.filter(tier=tier).first().details

        return render(request, "courses/lesson_detail.html", context)
