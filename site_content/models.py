from django.db import models


def getIncreasingBannerOrder():
    return Banner.objects.all().count()


class Banner(models.Model):
    image = models.ImageField(upload_to="Site/Banners/")
    link = models.URLField(blank=True, null=True)
    order_no = models.PositiveIntegerField(default=getIncreasingBannerOrder)

    def __str__(self):
        return self.order_no
