from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_api.urls')),
    path('api/users/', include('users_api.urls')),
    path('api/', include('foodgram_api.urls'))
]
