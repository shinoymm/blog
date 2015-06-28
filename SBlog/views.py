# Create your views here.
import json
import re
from datetime import datetime
import bson
from django.http.response import HttpResponse, Http404
from django.template import loader
from django.template.context import RequestContext
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from SBlog.forms import BlogForm, StatusForm, CommentForm, PicForm
from SBlog.models import Blog, StatusChoice, Tag, PostChoice, Comment, Like


class HomeView(ListView):
    template_name = 'home.html'
    model = Blog

    # def get_queryset(self):
    #     return Blog.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['object_list'] = Blog.objects.filter(author=self.request.user.username).order_by('-posted_on')
        context['status_form'] = StatusForm
        return context


class ScribbleView(FormView):
    template_name = 'blog_form.html'
    form_class = BlogForm
    success_url = '/home/'

    def get_context_data(self, **kwargs):
        context = super(ScribbleView, self).get_context_data(**kwargs)
        context['status_form'] = StatusForm
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        post_type = PostChoice.Status
        if data['post_type'] == PostChoice.Pic:
            pass
        elif data['post_type'] == PostChoice.Blog:
            post_type = PostChoice.Blog
        new_blog = Blog(author=self.request.user, title=data['title'], content=data['content'], post_type=post_type,
                        status=StatusChoice.Posted)
        new_blog.save()
        tags = re.findall(r"[\w']+", data['tags'])
        temp_tags = []
        for tag in tags:
            t = Tag.objects.get_or_create(name=tag)
            temp_tags.append(t[0])
        new_blog.tags = temp_tags
        new_blog.save()
        return super(ScribbleView, self).form_valid(form)

    def form_invalid(self, form):
        if form.cleaned_data.get('post_type', 1) == 2:
            self.template_name = 'home.html'
        return super(ScribbleView, self).form_invalid(form)


class CommentView(FormView):
    success_url = '/home/'

    def form_valid(self, form):
        # Comment(commenterer=self.request.user, holder_id=)
        pass


def get_comments(request):
    post_id = request.GET.get('id', '')
    if post_id:
        context = {}
        comments = Comment.objects.filter(holder_id=post_id).order_by('commented_on')
        context['comment_objects'] = comments
        context['comment_form'] = CommentForm
        context['post_id'] = post_id
        t = loader.get_template('comment_list.html')
        c = RequestContext(request, context)
        html = t.render(c)
    else:
        html = ''
    return HttpResponse(json.dumps({'comments': html, 'comment_count': comments.count()}), mimetype='application/json')


def post_comments(request):
    post_id = request.GET.get('id', '')
    content = request.GET.get('content', '')
    if post_id and content:
        post = Blog.objects.filter(id=post_id)[0]
        cmn = Comment(commenter=str(request.user), holder_id=post_id, content=content)
        post.comments.append(cmn)
        post.save()
        cmn.save()
    return HttpResponse(json.dumps({'saved': True}), mimetype='application/json')


def add_like(request):
    post_id = request.GET.get('id', '')
    if post_id:
        already_liked = Like.objects.filter(holder_id=post_id, liker=request.user.username)
        post = Blog.objects.filter(id=post_id)[0]
        obj = Like(liker=request.user.username, holder_id=post_id)
        if already_liked:
            post.likes.remove(obj)
            already_liked.delete()
        else:
            post.likes.append(obj)
            post.save()
            obj.save()
    return HttpResponse(json.dumps({'like_count': len(post.likes)}), mimetype='application/json')


class PicView(FormView):
    form_class = PicForm
    template_name = 'pic_form.html'
    success_url = '/home/'

    def form_valid(self, form):
        new_blog = Blog(author=self.request.user.username, content='Image', posted_on=datetime.now(), post_type=PostChoice.Pic, pic=form.cleaned_data['pic'])
        new_blog.save()
        return super(PicView, self).form_valid(form)

    def form_invalid(self, form):
        form.error = 'Please select a pic !!'
        return self.render_to_response(self.get_context_data(form=form))


class BlogListView(ListView):
    model = Blog
    template_name = 'blogs.html'

    def get_queryset(self):
        post_type = self.request.GET.get('type', PostChoice.Blog)
        try:
            post_type = int(post_type)
        except ValueError:
            post_type = PostChoice.Blog
        if post_type not in [PostChoice.Blog, PostChoice.Pic]:
            raise Http404
        return Blog.objects.filter(post_type=post_type, author=self.request.user.username)


class BlogDetailView(ListView):
    model = Blog
    template_name = 'read_blog.html'

    def get_queryset(self):
        pk = self.request.GET.get('pk', '')
        if bson.objectid.ObjectId.is_valid(pk) and Blog.objects.filter(id=pk).exists():
            return Blog.objects.filter(id=pk)[0]
        else:
            return Http404









