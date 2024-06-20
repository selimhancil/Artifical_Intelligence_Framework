
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# http://127.0.0.1:8000                 ===> homepage
# http://127.0.0.1:8000/index           ===> homepage
# http://127.0.0.1:8000/blogs           ===> blogs
# http://127.0.0.1:8000/blogs/3         ===> blog-details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('account/', include('account.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


