from board.urls import router
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', include_docs_urls(title='My api docs')),
    path('api/token/', obtain_auth_token, name='api-token'),
    path('api/', include(router.urls)),
]
