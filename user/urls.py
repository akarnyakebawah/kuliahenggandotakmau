from django.conf.urls import url

from user.views import UserListCreateView, UserUpdateDestroyView

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$',
        UserUpdateDestroyView.as_view(),
        name="list-create"),

    url(r'^$', UserListCreateView.as_view(), name="list-create"),
]
