from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls.static import static
from SBlog.views import ScribbleView, HomeView, BlogListView, PicView, BlogDetailView
from sign.views import LoginView, LogoutView, SignupView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    # url(r'^blog/', include('blog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'home/$', HomeView.as_view(), name='home'),
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'logout/$', LogoutView.as_view(), name='logout'),
    url(r'signup/$', SignupView.as_view(), name='signup'),
    url(r'blogs/$', BlogListView.as_view(), name='blogs'),
    url(r'read_blog/?', BlogDetailView.as_view(), name='read_blog'),
    url(r'scribble/$', ScribbleView.as_view(), name='scribble'),
    url(r'pic/$', PicView.as_view(), name='pic'),
    url(r'home/comments$', 'SBlog.views.get_comments', name='get_comments'),
    url(r'like$', 'SBlog.views.add_like', name='add_like'),
    url(r'home/post_comments$', 'SBlog.views.post_comments', name='post_comments'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

