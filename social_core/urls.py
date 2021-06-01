from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    NicheViewSet,
    OrderViewSet,
    ReviewViewSet,
    get_consumer,
    get_influencer_detail,
    get_influencer_list,
)

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"reviews", ReviewViewSet, basename="reviews")
router.register(r"niche", NicheViewSet, basename="niche")

urlpatterns = [
    path("consumer/", get_consumer),
    path("influencer/", get_consumer),
    path("influencers/", get_influencer_list),
    path("influencers/<int:id>/", get_influencer_detail),
] + router.urls
