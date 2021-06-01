from django.contrib import admin
from .models import Consumer, Influencer, Niche, Order, Review


admin.site.register([Consumer, Influencer, Niche, Order, Review])
