from django.db import models
from django.contrib.auth.models import User 
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "posts")
    liked_users = models.ManyToManyField(User, through = "Like", related_name = "liked_posts")
    created_at = models.DateTimeField(default = timezone.now, editable = False)

    def get_absolute_url(self):
        return reverse("post-detail", kwargs = {"pk": self.pk})


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    

    class Meta:
        unique_together = ("post", "user")


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments")
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments")
    content = models.TextField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post_id}"
