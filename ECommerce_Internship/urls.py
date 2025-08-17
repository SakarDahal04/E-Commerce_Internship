"""
URL configuration for ECommerce_Internship project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin 
from django.urls import path , include
from debug_toolbar.toolbar import debug_toolbar_urls
from rest_framework_simplejwt.views import(
    TokenObtainPairView, TokenRefreshView,
)
from oauth2_provider import urls as oauth2_urls

from django.urls import include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
#from rest_framework.authtoken.views import obtain_auth_token
 
   
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user_orders', include('user_orders.urls')),
    path('api/product/', include('product.api.urls')),
    path('cart/', include('cart.urls')),
    #path('api/login/', LoginView.as_view(), name='api-login'),  

    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   # path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   # path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('o/', include(oauth2_urls)), # oauth access token
    path('api-auth/', include('rest_framework.urls')),
]+ debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)