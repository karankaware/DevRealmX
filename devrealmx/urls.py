
from django.contrib import admin
from django.urls import path , include
from basee import urls
# added for image Functionality
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('basee.urls')),
    path('api/',include('basee.api.urls'))
    
]
urlpatterns += static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)