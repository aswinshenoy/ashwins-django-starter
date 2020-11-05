from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from chowkidar.graphql import GraphQLView

from django.conf import settings
from framework.views import HealthCheckView
from framework.graphql.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=settings.DEBUG))),
    path('healthz/', HealthCheckView.as_view()),
]

urlpatterns = [url(r'^api/', include(urlpatterns))]
