from django.urls import path

from courses.views import HomeView,AboutView,ContactView,CourseListView, CourseDetailView,LessonDetailView, RequestTeacherView, CourseSearchView

app_name = 'courses'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/<course_slug>/<lesson_slug>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('request_teacher/', RequestTeacherView.as_view(), name='request_teacher'),
    path('search/', CourseSearchView.as_view(), name='course_search')
]
