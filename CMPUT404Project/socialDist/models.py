from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
# https://docs.djangoproject.com/en/4.1/topics/db/examples/many_to_one/
# https://www.crunchydata.com/blog/composite-primary-keys-postgresql-and-django
# https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.URLField()
    github = models.URLField()
    profileImg = models.URLField()
    host = models.URLField()

# https://stackoverflow.com/questions/58794639/how-to-make-follower-following-system-with-django-model
# https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user_id', 'following_user_id')

class Post(models.Model):
    postURL = models.URLField()
    source = models.URLField()
    origin = models.URLField()
    description = models.TextField()
    title = models.CharField(max_length=50)
    content = models.BinaryField()
    contentType = models.TextField()
    posterID = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField()
    visibility = models.CharField(max_length=30)
    unlisted = models.BooleanField()

class Comment(models.Model):
    content = models.TextField()
    contentType = models.TextField()
    parentPostID = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class Like(models.Model):
    likeType = models.CharField(max_length=20)
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    parentComment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)