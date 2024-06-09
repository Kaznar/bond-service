from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import UserDetailsView, LogoutView
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Admin URL patterns
admin_urlpatterns = [
    path('admin/', admin.site.urls),
]

# Authentication URL patterns
auth_urlpatterns = [
    path('api/registration/', RegisterView.as_view(), name='rest_register'),
    path('api/user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('api/logout/', LogoutView.as_view(), name='rest_logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# API URL patterns
api_urlpatterns = [
    path('api/bond/', include('bond.urls')),
]

# Documentation URL patterns
docs_urlpatterns = [
    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Combine all URL patterns
urlpatterns = (
        admin_urlpatterns
        + auth_urlpatterns
        + api_urlpatterns
        + docs_urlpatterns
)
