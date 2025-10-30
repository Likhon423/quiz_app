from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('home/', include('home.urls')),
    path('quiz/', include('quiz.urls')),
    path('attempt/', include('attempts.urls')),
]
