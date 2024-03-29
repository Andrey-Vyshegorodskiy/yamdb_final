from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from api_yamdb.schema import schema

urlpatterns = [
    path('', schema),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
