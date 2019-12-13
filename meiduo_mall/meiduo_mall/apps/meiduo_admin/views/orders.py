from django.db.models import Q
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet
from orders.models import OrderInfo
from meiduo_admin.serializers.orders import OrderListSerializer, OrderDetailSerializer, ChangeStatusSerializer
from rest_framework.generics import UpdateAPIView


# GET /meiduo_admin/orders/?keyword=<搜索内容>&page=<页码>&pagesize=<页容量>
class OrdersViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]

    # 指定序列化器类
    # serializer_class = OrderListSerializer
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        else:
            return OrderDetailSerializer

    def get_queryset(self):
        # 获取搜寻关键字
        keyword = self.request.query_params.get('keyword')

        if not keyword:
            orders = OrderInfo.objects.all()
        else:
            orders = OrderInfo.objects.filter(Q(order_id=keyword) | Q(skus__sku__name__contains=keyword))
        return orders


class ChangeStatusView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ChangeStatusSerializer
    queryset = OrderInfo.objects.all()
    lookup_value_regex = '\d+'
