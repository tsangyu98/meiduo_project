from rest_framework import serializers
from goods.models import SPU, Brand, GoodsCategory, SpecificationOption, SPUSpecification


class GetSPUSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField(label='品牌名称', read_only=True)
    brand_id = serializers.IntegerField(label='品牌id')
    category1_id = serializers.IntegerField(label='一级分类id')
    category2_id = serializers.IntegerField(label='二级分类id')
    category3_id = serializers.IntegerField(label='三级分类id')

    class Meta:
        model = SPU
        exclude = ('create_time', 'update_time', 'category1', 'category2', 'category3')
        extra_kwargs = {
            'sales': {'read_only': True},
            'comments': {'read_only': True}
        }


class GetBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ('create_time', 'update_time', 'logo', 'first_letter')


class GetFirstSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(label='传递的id', write_only=True)

    class Meta:
        model = GoodsCategory
        exclude = ('create_time', 'update_time', 'parent')
        extra_kwargs = {
            'name': {
                'read_only': True
            },
            'id': {
                'read_only': True
            }
        }


class SPUSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ('id', 'name')


class SpecOptionSerializer(serializers.ModelSerializer):
    """SPU规格序列化器类"""
    class Meta:
        model = SpecificationOption
        fields = ('id', 'value')


class SPUSpecSerializer(serializers.ModelSerializer):
    options = SpecOptionSerializer(label='Opt选项', many=True)

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'options')



