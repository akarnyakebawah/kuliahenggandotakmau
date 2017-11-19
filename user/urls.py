from django.conf.urls import url

from user.views import UserListCreateView, UserRetrieveUpdateDestroyView
from user.views import UserRequestPasswordResetView, UserConfirmPasswordResetView

urlpatterns = [
    url(r'^(?P<user_id>\d+)/$',
        UserRetrieveUpdateDestroyView.as_view(),
        name="user-retrieve-update-destroy"),

    url(r'^$', UserListCreateView.as_view(), name="user-list-create"),

    # Password Reset URL
    url(r'^reset-password/$', UserRequestPasswordResetView.as_view(), name="request-password-reset"),
    url(r'^reset-password/confirm/$', UserConfirmPasswordResetView.as_view(), name="confirm-password-reset"),
]
