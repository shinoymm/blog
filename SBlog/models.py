from django.contrib.auth.models import User
from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField


class StatusChoice(object):
    Draft = 1
    Posted = 2
    NotApproved = 1
    Approved = 2


class PostChoice(object):
    Blog = 1
    Status = 2
    Pic = 3

PostStatusChoices = (
    (StatusChoice.Draft, 'Draft'),
    (StatusChoice.Posted, 'Posted'),
)
CommentStatusChoices = (
    (StatusChoice.NotApproved, 'Not Approved'),
    (StatusChoice.Approved, 'Approved'),
)
PostChoices = (
    (PostChoice.Blog, 'Blog'),
    (PostChoice.Status, 'Status'),
    (PostChoice.Pic, 'Pic'),
)


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Comment(models.Model):
    # holder = models.ForeignKey(Blog)
    commenter = models.CharField(max_length=500)
    holder_id = models.CharField(max_length=50)
    content = models.TextField()
    commented_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=CommentStatusChoices, default=StatusChoice.NotApproved)
    is_edited = models.BooleanField(default=False)


class Like(models.Model):
    liker = models.CharField(max_length=500)
    holder_id = models.CharField(max_length=50)


class Blog(models.Model):
    author = models.CharField(max_length=100)
    content = models.TextField()
    title = models.CharField(max_length=300, blank=True, null=True)
    status = models.IntegerField(choices=PostStatusChoices, default=StatusChoice.Draft)
    pic = models.ImageField(upload_to='Media/')
    tags = ListField(EmbeddedModelField(Tag))
    comments = ListField(EmbeddedModelField(Comment))
    likes = ListField(EmbeddedModelField(Like))
    created_on = models.DateTimeField(auto_now_add=True)
    posted_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    post_type = models.IntegerField(choices=PostChoices)


class Status(models.Model):
    author = models.CharField(max_length=100)
    content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)









