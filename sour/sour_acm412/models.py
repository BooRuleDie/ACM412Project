from django.db import models
from django.utils import timezone
import uuid

class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    summary =  models.CharField(max_length=255, default="Hi, I'm [username], and I'm excited to be part of the conversation here on Sour! I enjoy sharing my thoughts and engaging with others on various topics such as [list your interests].")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Topics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=50, unique=True)
    origin_comment = models.CharField(max_length=1000)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Comments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    comment = models.CharField(max_length=1000)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    # if it's a origin_comment topic_id column's value will be the same with id column
    topic_id = models.ForeignKey(Topics, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment

class Upvotes(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    # related_name="upvotes" thanks to this reverse relationship we are able to fetch all upvotes for each comment by using this syntax
    # comment.upvotes.all()
    comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='upvotes')

    class Meta:
        unique_together = ('user_id', 'comment_id')

    def __str__(self):
        return f'{self.user_id.username} upvoted {self.comment_id}'

class Downvotes(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='downvotes')

    class Meta:
        unique_together = ('user_id', 'comment_id')

    def __str__(self):
        return f'{self.user_id.username} downvoted {self.comment_id}'
