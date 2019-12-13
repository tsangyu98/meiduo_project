from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from goods.models import GoodsVisitCount
from meiduo_admin.serializers.goods import DayCategoryGoodsSerializer


# GET /meiduo_admin/statistical/goods_day_views/
class DayCategoryGoodsView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = DayCategoryGoodsSerializer
    pagination_class = None

    def get_queryset(self):
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # 获取当天被访问的商品
        goods = GoodsVisitCount.objects.filter(date__gte=now_date)
        # 返回数据
        return goods

