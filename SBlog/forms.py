from SBlog.models import PostChoice

__author__ = 'shinoymm'
from django import forms


class BlogForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'id': 'blog_title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'id': 'blog_content', 'class': 'materialize-textarea'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'id': 'blog_tags'}), required=False)
    post_type = forms.IntegerField(widget=forms.HiddenInput(), initial=PostChoice.Blog)


class StatusForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'id': 'status_input', 'class': 'materialize-textarea'}))
    title = forms.CharField(widget=forms.HiddenInput(), initial='Status')
    post_type = forms.IntegerField(widget=forms.HiddenInput(), initial=PostChoice.Status)

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'id': 'comment_content', 'class': 'materialize-textarea'}))


class PicForm(forms.Form):
    pic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'file-path validate', 'accept':'image/x-png, image/jpeg'}))
