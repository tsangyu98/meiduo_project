from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory
from meiduo_admin.serializers.channels import ChannelsSerializer, ChannelTypesSerializer, GetFirstCategorySerializer
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework import mixins


# GET /meiduo_admin/goods/channels/?page=<页码>&pagesize=<页容量>
class ChannelsViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    serializer_class = ChannelsSerializer
    queryset = GoodsChannel.objects.all()


# GET /meiduo_admin/channel_types/
class ChannelTypesView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ChannelTypesSerializer
    queryset = GoodsChannelGroup.objects.all()
    pagination_class = None


# GET /meiduo_admin/goods/categories/
class GetFirstCategoryView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GetFirstCategorySerializer
    queryset = GoodsCategory.objects.all()
    pagination_class = None


# class ChannelViewSet()
