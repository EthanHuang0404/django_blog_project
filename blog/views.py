from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, 
    UpdateView, DeleteView
)
from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all() #get data from the 'Post' class in blog/models.py
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted'] # '-' means descending order

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']    

    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author of the post to the current logged in user
        return super().form_valid(form) # Run the form_valid method on the parent class
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']    

    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author of the post to the current logged in user
        return super().form_valid(form) # Run the form_valid method on the parent class
    
    def test_func(self):
        post = self.get_object() # Get the post we are trying to update
        if self.request.user == post.author: # If the current user is the author of the post
            return True                      # Then allow the user to update the post
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # Redirect to the home page after deleting a post

    def test_func(self):
        post = self.get_object() # Get the post we are trying to delete
        if self.request.user == post.author: # If the current user is the author of the post
            return True                      # Then allow the user to delete the post
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})