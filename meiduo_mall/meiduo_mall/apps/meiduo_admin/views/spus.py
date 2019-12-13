from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from goods.models import SPU, Brand, GoodsCategory, SPUSpecification
from meiduo_admin.serializers.spus import GetSPUSerializer, GetBrandSerializer, GetFirstSerializer, SPUSimpleSerializer, \
    SPUSpecSerializer
from rest_framework.viewsets import ModelViewSet


class SPUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = SPU.objects.all()
    serializer_class = SPUSimpleSerializer
    pagination_class = None


class SPUSpecView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SPUSpecSerializer
    pagination_class = None

    def get_queryset(self):
        pk = self.kwargs['pk']
        specs = SPUSpecification.objects.filter(spu_id=pk)
        return specs


# GET / meiduo_admin / goods /?keyword = < 名称 | 副标题 > & page = < 页码 > & page_size = < 页容量 >
class GetSPUViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = GetSPUSerializer

    lookup_value_regex = '\d+'

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            spus = SPU.objects.get(name__contains=keyword)
        else:
            spus = SPU.objects.all()
        return spus


class GetBrandView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GetBrandSerializer
    queryset = Brand.objects.all()
    pagination_class = None


class GetCategoryView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GetFirstSerializer
    pagination_class = None

    def get_queryset(self):
        categories = GoodsCategory.objects.filter(parent_id__isnull=True)
        return categories


class GetOtherCategoryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        categories = GoodsCategory.objects.filter(parent_id=pk)
        serializer = GetFirstSerializer(categories, many=True)
        return Response(serializer.data)

