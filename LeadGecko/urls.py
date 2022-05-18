from django.contrib import admin
from django.urls import path , include
from django.contrib.auth.views import LogoutView
from rest_framework_swagger.views import get_swagger_view
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="LeadGecko API",
        default_version='v1',
        description="under development",
        terms_of_service="",
        license=openapi.License(name="Lead Gecko"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

schema_view_x = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('authenticate.api.urls')),
    path('auth/',include('rest_framework.urls')),
    path('',include('authenticate.urls')),
    path('logout/',LogoutView.as_view()),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
