from django.contrib import admin
from django.urls import path, include
from auth_app.views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth_app/user/register/', RegisterView.as_view(), name='register'),
    path('', TemplateView.as_view(template_name='register.html')),
    path('api/token/', TokenObtainPairView.as_view(), name='get_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api-auth/', include('rest_framework.urls')),
]
