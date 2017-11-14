from django.conf.urls import url

from user.views import UserListCreateView, UserUpdateDestoryView

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$',
        UserUpdateDestoryView.as_view(),
        name="list-create"),

    url(r'^$', UserListCreateView.as_view(), name="list-create"),
]
