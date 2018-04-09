from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('service.urls')),
    url(r'^docs/', include('rest_framework_docs.urls')),
]
