from django.db import models
from django.contrib.auth.models import User 
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "posts")
    liked_users = models.ManyToManyField(User, through = "Like", related_name = "liked_posts")

    def get_absolute_url(self):
        return reverse("post-detail", kwargs = {"pk": self.pk})



class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    

    class Meta:
        unique_together = ("post", "user")
    




