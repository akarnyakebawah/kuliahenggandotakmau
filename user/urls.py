from django.conf.urls import url

from user.views import UserListCreateView, UserRetrieveUpdateDestroyView

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$',
        UserRetrieveUpdateDestroyView.as_view(),
        name="user-retrieve-update-destroy"),

    url(r'^$', UserListCreateView.as_view(), name="user-list-create"),
]
