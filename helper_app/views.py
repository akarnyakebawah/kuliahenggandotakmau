from rest_framework import generics
from user.permissions import IsAdminOrReadOnly
from helper_app.models import TemporaryImage
from helper_app.serializers import TemporaryImageSerializer


class TemporaryImageListCreateView(generics.ListCreateAPIView):
    queryset = TemporaryImage.objects.all()
    serializer_class = TemporaryImageSerializer


class TemporaryImageRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = TemporaryImage.objects.all()
    serializer_class = TemporaryImageSerializer
    lookup_url_kwarg = 'tmp_image_id'
