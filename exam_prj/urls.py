from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from account.views import AuthorRegisterApiView

schema_view = get_schema_view(
   openapi.Info(
      title="Ecommerce API",
      default_version='v0.1',
      description="API для интернет магазинов",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="No License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth', include('rest_framework.urls')),
    path('api/account/register/',AuthorRegisterApiView.as_view()),
    path('api/account/token/', obtain_auth_token),

    path('api/', include('news.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_ui'),
    path('redoc/',schema_view.with_ui('redoc', cache_timeout=0), name='redoc_ui'),


]
