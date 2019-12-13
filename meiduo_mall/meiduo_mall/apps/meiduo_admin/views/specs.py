from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from goods.models import SPUSpecification, SpecificationOption
from meiduo_admin.serializers.specs import GoodsSpecsSerializer, SpecsOptionsSerializer, GoodsSpecsSimpleSerializer


# GET /meiduo_admin/goods/specs/
class GoodsSpecsViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = GoodsSpecsSerializer
    queryset = SPUSpecification.objects.all()


# GET /meiduo_admin/specs/options/
class SpecsOptionsViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = SpecsOptionsSerializer
    queryset = SpecificationOption.objects.all()


# GET /meiduo_admin/goods/specs/simple/
class GoodsSpecsSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GoodsSpecsSimpleSerializer
    queryset = SPUSpecification.objects.all()
    pagination_class = None


