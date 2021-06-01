from django.contrib import admin
from .models import Banner


class BannerAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'image']


admin.site.register(Banner, BannerAdmin)
