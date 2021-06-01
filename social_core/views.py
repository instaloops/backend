from social_core.permissions import IsAdminOrReadOnly
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Influencer, Consumer, Niche, Review, Order, Token
from math import ceil
from .serializers import (
    InfluencerSerializer,
    ConsumerSerializer,
    ReviewCreateSerializer,
    ReviewReadSerializer,
    OrderCreateSerializer,
    OrderReadSerializer,
    NicheSerializer,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_consumer(request):
    try:
        data = ConsumerSerializer(instance=Consumer.objects.get(user=request.user))
        return Response(data=data)
    except Consumer.DoesNotExist:
        return Response(data="DoesNotExist", status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_influencer(request):
    try:
        data = InfluencerSerializer(instance=Influencer.objects.get(user=request.user))
        return Response(data=data)
    except Influencer.DoesNotExist:
        return Response(data="DoesNotExist", status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def get_influencer_list(request):
    params = request.query_params
    queryset = Influencer.objects.all()
    per_page = 15

    if "search" in params:
        search = params["search"]
        # NEEDS TO BE MADE BETTER
        queryset = queryset.filter(user__username__contains=search)

    if "niche" in params:
        niche = params["niche"]
        queryset = queryset.filter(niche__name=niche)

    page_count = ceil(queryset.count() / per_page)
    if "page" in params:
        page = int(params["page"][0])
        queryset = queryset[(page - 1) * per_page: page * per_page]

    serializer = InfluencerSerializer(queryset, many=True)
    # if serializer.is_valid():
    return Response(data={"influencers": serializer.data, "page_count": page_count})
    # return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAdminOrReadOnly])
def get_influencer_detail(request, id):
    try:
        queryset = Influencer.objects.get(id=id)
        serializer = InfluencerSerializer(queryset)

        # if serializer.is_valid():
        return Response(data=serializer.data)

    except Influencer.DoesNotExist:
        return Response({"detail": "Not found."}, status=HTTP_400_BAD_REQUEST)
    # return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


# class InfluencerViewSet(ModelViewSet):
#     permission_classes = [IsAdminOrReadOnly]
#     serializer_class =

#     def get_queryset(self):


#         return


class NicheViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = NicheSerializer
    queryset = Niche.objects.all()


class ReviewViewSet(ModelViewSet):
    permission_classes = []

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReviewReadSerializer
        return ReviewCreateSerializer

    def get_queryset(self):
        return Review.objects.filter(influencer__user=self.request.user)


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderReadSerializer
        return OrderCreateSerializer

    def get_queryset(self):
        return Order.objects.filter(influencer__user=self.request.user)


@api_view(["POST"])
def resetPassword(request):
    email = request.data["email"]
    try:
        user = User.objects.get(email=email)
        token = Token()
        token.user = user
        token.save()
        subject = "Reset Password"
        msg = f"""
    Hey {user}! here is your password reset link for your InstaLoops user account http://localhost:3000/reset/password/confirm/{token.token}

    If you don't recognise this request then kindly ignore this.

    Thank You,
    Regards, Team InstaLoops.
    """
        recipient_list = [token.user.email]
        send_mail(subject, msg, "insta.loops.service@gmail.com", recipient_list)
        return Response({"msg": "Successful"})
    except User.DoesNotExist:
        return Response({"msg": "User with given Email does not exist"},
                        status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def check_reset_token(request):
    token = request.GET["token"]
    try:
        token_obj = Token.objects.get(token=token)
        if token_obj.is_valid():
            return Response(status=HTTP_200_OK, data="Token is Valid")
        token_obj.delete()
    except Token.DoesNotExist:
        pass
    return Response(status=HTTP_400_BAD_REQUEST, data="Token is Invalid")


@api_view(["POST"])
def reset_password_confirm(request):
    token = request.data["token"]
    pass1 = request.data["pass1"]
    pass2 = request.data["pass2"]
    msg = "Success"
    try:
        token_object = Token.objects.get(token=token)
        if pass1 == pass2:
            user = User.objects.get(pk=token_object.user.pk)
            user.password = make_password(pass1)
            user.save()
            token_object.delete()
            return Response(status=HTTP_200_OK, data=msg)
        msg = "Passwords didn't match"
    except Token.DoesNotExist:
        msg = "Token is invalid"
    return Response(data=msg, status=HTTP_400_BAD_REQUEST)
