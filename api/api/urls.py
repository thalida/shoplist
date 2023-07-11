"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from authentication.views import UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

from graphene_django.views import GraphQLView
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication

# class DOTAuthenticatedGraphQLView(GraphQLView):
#     def parse_body(self, request):
#         if isinstance(request, Request):
#             return request.data
#         return super(DOTAuthenticatedGraphQLView, self).parse_body(request)

#     @classmethod
#     def as_view(cls, *args, **kwargs):
#         view = super(DOTAuthenticatedGraphQLView, cls).as_view(*args, **kwargs)
#         view = permission_classes((IsAuthenticated, TokenHasReadWriteScope, ))(view)  # add permissions to the view
#         view = authentication_classes((OAuth2Authentication,))(view)
#         view = api_view(['POST'])(view)
#         return view

# class DRFAuthenticatedGraphQLView(GraphQLView):
#     # custom view for using DRF TokenAuthentication with graphene GraphQL.as_view()
#     # all requests to Graphql endpoint will require token for auth, obtained from DRF endpoint
#     # https://github.com/graphql-python/graphene/issues/249
#     @classmethod
#     def as_view(cls, *args, **kwargs):
#         view = super(DRFAuthenticatedGraphQLView, cls).as_view(*args, **kwargs)
#         view = permission_classes((IsAuthenticated,))(view)
#         view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)(view)
#         view = api_view(['GET', 'POST'])(view)
#         return view

class DRFAuthenticateGraphQLView(GraphQLView):
    pass
    # def parse_body(self, request):
    #     if isinstance(request, Request):
    #         return request.data
    #     return super(DRFAuthenticateGraphQLView, self).parse_body(request)

    # @classmethod
    # def as_view(cls, *args, **kwargs):
    #     view = super(DRFAuthenticateGraphQLView, cls).as_view(*args, **kwargs)
    #     view = permission_classes((IsAuthenticated, TokenHasReadWriteScope, ))(view)
    #     view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)(view)
    #     view = api_view(['POST'])(view)
    #     return view

urlpatterns = [
    path("api/", include(router.urls)),
    re_path(r'^api/auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("graphql", csrf_exempt(DRFAuthenticateGraphQLView.as_view(graphiql=True))),
    path("admin/", admin.site.urls),
]
