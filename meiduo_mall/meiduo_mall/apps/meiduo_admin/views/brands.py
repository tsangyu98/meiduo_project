from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAdminUser
from goods.models import Brand
from meiduo_admin.serializers.brands import GoodsBrandsSerializer


# GET /meiduo_admin
class GoodsBrandsViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = GoodsBrandsSerializer
    queryset = Brand.objects.all()
    lookup_value_regex = '\d+'

