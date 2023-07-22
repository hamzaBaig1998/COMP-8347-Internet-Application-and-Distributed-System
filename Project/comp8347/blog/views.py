from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post
from blog.forms import PostForm

class PostListView(ListView):
    # specify the model and template name
    model = Post
    template_name = 'blog/post_list.html'

    # specify the context object name for the list of posts
    context_object_name = 'posts'

    # override the queryset to filter posts by created date and order by descending created date
    def get_queryset(self):
        return Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')

class PostDetailView(DetailView):
    # specify the model and template name
    model = Post
    template_name = 'blog/post_detail.html'

    # specify the context object name for the post
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    # specify the model, form class, and template name
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    # override the success URL to redirect to the newly created post's detail page
    success_url = reverse_lazy('blog:post_list')

    # set the author of the post to the current user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    # specify the model, form class, and template name
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    # override the success URL to redirect to the updated post's detail page
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

    # restrict updating to the author of the post
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect('blog:post_list')
        return super().dispatch(request, *args, **kwargs)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    # specify the model and template name
    model = Post
    template_name = 'blog/post_confirm_delete.html'

    # override the success URL to redirect to the post list
    success_url = reverse_lazy('blog:post_list')

    # restrict deleting to the author of the post
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect('blog:post_list')
        return super().dispatch(request, *args, **kwargs)