from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Like
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User



def hello(request):
    return render(request,"myapp/home.html", status=200)


# def blog_page(request):
#     context = {"posts":Post.objects.all()}

#     return render(request,"myapp/blog.html",context)

class PostListView(ListView):
    model = Post
    template_name = "myapp/blog.html"
    context_object_name = "posts"
    paginate_by = 3
    ordering = ["id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        user = self.request.user


        if user.is_authenticated:
            context["liked_posts"] = Like.objects.filter(user= user).values_list("post_id", flat= True)

        else:
            context["liked_posts"] = []

        return context

        

class UserPostListView(ListView):
    model = Post
    template_name = "myapp/user_posts.html"
    context_object_name = "posts"
    paginate_by = 3
    ordering = ["-id"]

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get("username"))
        return Post.objects.filter(author = user)




class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        post = self.object
        user = self.request.user

        context["like_count"] = post.liked_users.count()

        if user.is_authenticated:
            context["liked_posts"] = Like.objects.filter(user = user).values_list("post_id", flat = True)


        return context






class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title","content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        return False
    


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog")


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        return False



def toggle_like(request, pk):
    post = get_object_or_404(Post, pk= pk)


    like, created = Like.objects.get_or_create(post= post, user= request.user)

    if not created:
        like.delete()

    return redirect(request.META.get('HTTP_REFERER', "home"))

    