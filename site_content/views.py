from rest_framework.viewsets import ModelViewSet
from .models import Banner
from .serialziers import BannerSerializer


class BannerViewSet(ModelViewSet):
    serializer_class = BannerSerializer

    def get_queryset(self):
        return Banner.objects.all().order_by("order_no")
