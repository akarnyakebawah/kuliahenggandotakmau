from django.conf.urls import url

from helper_app.views import (
    TemporaryImageListCreateView,
    TemporaryImageRetrieveDestroyView,
)

urlpatterns = [
    url(r'^images/$',
        TemporaryImageListCreateView.as_view(),
        name="tmp-image-list-create"),

    url(r'^images/(?P<tmp_image_id>\d+)/$',
        TemporaryImageRetrieveDestroyView.as_view(),
        name="tmp-image-retrieve-destroy"),
]
