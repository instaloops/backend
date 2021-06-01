from rest_framework import serializers
from rest_framework.relations import StringRelatedField
from django.contrib.auth.models import User
from .models import Influencer, Consumer, Niche, Review, Order
from rest_auth.serializers import UserDetailsSerializer


class UserSerializer(UserDetailsSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        if Consumer.objects.filter(user__pk=obj.pk).count() == 1:
            return "consumer"
        if Influencer.objects.filter(user__pk=obj.pk).count() == 1:
            return "influencer"

        return "uncreated"

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ("status",)
        read_only_fields = ("",)


class ConsumerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Consumer
        fields = "__all__"


class ReviewReadSerializer(serializers.ModelSerializer):
    consumer = ConsumerSerializer(many=False, required=False)
    consumer_username = serializers.CharField()

    class Meta:
        model = Review
        fields = "__all__"


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class InfluencerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    niche = serializers.StringRelatedField()
    review_count = serializers.IntegerField(read_only=True)
    reviews = ReviewReadSerializer(many=True, read_only=True)
    username = serializers.CharField()
    email = serializers.CharField()
    insta_posts = StringRelatedField(read_only=True, source="get_insta_posts")
    insta_following = StringRelatedField(read_only=True, source="get_insta_following")
    insta_followers = StringRelatedField(read_only=True, source="get_insta_followers")

    class Meta:
        model = Influencer
        fields = [
            "id",
            "user",
            "username",
            "email",
            "min_budget",
            "max_budget",
            "niche",
            "pic",
            "banner",
            "bio",
            "about",
            "rating",
            "review_count",
            "reviews",
            "insta_username",
            "insta_posts",
            "insta_following",
            "insta_followers",
        ]


class OrderReadSerializer(serializers.ModelSerializer):
    Influencer = InfluencerSerializer()
    consumer = ConsumerSerializer()

    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class NicheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niche
        fields = "__all__"
