from django.conf.urls import include, url #User 목록을 불러움
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from blog import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls')),
    url(r'^blog/(?P<pk>[0-9]+)$',views.post_detail, name='post_detail'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
