from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
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
    ordering = ["-created_at", "-id"]

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
    ordering = ["-created_at", "-id"]

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get("username"))
        return Post.objects.filter(author = user).order_by("-created_at", "-id")




class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object
        user = self.request.user

        context["like_count"] = post.liked_users.count()
        context["comments"] = post.comments.select_related("author")
        context["comment_form"] = kwargs.get("comment_form") or CommentForm()

        if user.is_authenticated:
            context["liked_posts"] = Like.objects.filter(user = user).values_list("post_id", flat = True)
        else:
            context["liked_posts"] = []

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            messages.info(request, "Please log in to comment on posts.")
            return redirect(f"{reverse_lazy('login')}?next={request.path}")

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, "Your comment was posted.")
            return redirect(f"{self.object.get_absolute_url()}#comments")

        messages.error(request, "Please enter a comment before posting.")
        context = self.get_context_data(comment_form = form)
        return self.render_to_response(context)






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

    
