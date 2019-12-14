from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from goods.models import SKUImage, SKU
from meiduo_admin.serializers.skus import SKUImageSerializer, SKUSimpleSerializer, SKUSerializer
from rest_framework.generics import ListAPIView


# GET  /meiduo_admin/skus/images/?page=<页码>&page_size=<页容量>
class SKUImageViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    # 指定视图使用的查询集
    queryset = SKUImage.objects.all()
    # 指定序列化器类
    serializer_class = SKUImageSerializer

    def perform_destroy(self, instance):
        # 删除FDFS中的图片
        instance.image.delete(save=False)
        # 删除数据表中的记录
        instance.delete()


# GET /meiduo_admin/skus/simple/
class SKUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    # 指定视图所用的序列化器类
    serializer_class = SKUSimpleSerializer
    # 指定视图使用的查询集
    queryset = SKU.objects.all()
    # 关闭分页
    pagination_class = None


class SKUViewSet(ModelViewSet):
    """SKU视图集"""
    permission_classes = [IsAdminUser]

    # 指定router动态生成路由时，提取参数的正则表达式
    lookup_value_regex = '\d+'

    def get_queryset(self):
        # 提取关键字
        keyword = self.request.query_params.get('keyword')
        if keyword:
            skus = SKU.objects.filter(Q(name__contains=keyword) | Q(caption__contains=keyword))
        else:
            skus = SKU.objects.all()
        return skus

    # 指定序列化器类
    serializer_class = SKUSerializer
