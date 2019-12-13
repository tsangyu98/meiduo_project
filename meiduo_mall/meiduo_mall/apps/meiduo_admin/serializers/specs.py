from rest_framework import serializers
from goods.models import SPUSpecification, SpecificationOption


class GoodsSpecsSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField(label='SPU商品名称', read_only=True)
    spu_id = serializers.IntegerField(label='SPU商品id')

    class Meta:
        model = SPUSpecification
        exclude = ('create_time', 'update_time')


class SpecsOptionsSerializer(serializers.ModelSerializer):
    spec = serializers.StringRelatedField(label='规格名称')
    spec_id = serializers.IntegerField(label='规格id')

    class Meta:
        model = SpecificationOption
        exclude = ('create_time', 'update_time')


class GoodsSpecsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPUSpecification
        exclude = ('create_time', 'update_time', 'spu')

