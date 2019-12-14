from django.db import transaction
from rest_framework import serializers
from goods.models import SKUImage, SKU, SKUSpecification, SPU, SpecificationOption


class SKUImageSerializer(serializers.ModelSerializer):
    """SKU图片序列化器类"""
    # 关联对象嵌套序列化
    sku = serializers.StringRelatedField(label='SKU商品名称')
    sku_id = serializers.IntegerField(label='SKU商品ID')

    class Meta:
        model = SKUImage
        exclude = ('create_time', 'update_time')

    # 数据校验
    def validate_sku_id(self, value):
        # 判断sku商品是否存在
        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        return value

    # 重写create方法
    def create(self, validated_data):
        """sku商品上传图片保存"""
        # 调用ModelSerializer的create方法
        sku_image = SKUImage.objects.create(**validated_data)
        # 保存上传记录
        sku = SKU.objects.get(id=validated_data['sku_id'])
        # 如果sku商品没有默认图片，则设置其默认图片
        if not sku.default_image:
            sku.default_image = sku_image.image
            sku.save()
        return sku_image

    def update(self, instance, validated_data):
        # 删除FDFS中原有的图片
        instance.image.delete(save=False)
        # 获取传递的数据
        image = validated_data['image']
        sku_id = validated_data['sku_id']
        # 保存更新的图片
        instance.image = image
        instance.sku_id = sku_id
        instance.save()
        return instance


class SKUSimpleSerializer(serializers.ModelSerializer):
    """SKU商品序列化器类"""

    class Meta:
        model = SKU
        fields = ('id', 'name')


class SKUSpecSerializer(serializers.Serializer):
    """商品规格信息序列化器类"""
    spec_id = serializers.IntegerField(label='规格id')
    option_id = serializers.IntegerField(label='选项id')

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSerializer(serializers.ModelSerializer):
    # 关联对象嵌套序列化
    category = serializers.StringRelatedField(label='三级分类名称')
    spu_id = serializers.IntegerField(label='SPU编号')
    # 关联对象嵌套序列化
    specs = SKUSpecSerializer(label='商品规格信息', many=True)

    class Meta:
        model = SKU
        exclude = ('create_time', 'update_time', 'default_image', 'spu', 'comments')

        extra_kwargs = {
            'sales': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        # 获取spu_id
        spu_id = attrs['spu_id']
        # 检查spu商品是否存在
        try:
            spu = SPU.objects.get(id=spu_id)
        except SPU.DoesNotExist:
            raise serializers.ValidationError('SPU商品不存在')
        # attrs中添加第三级分类
        attrs['category_id'] = spu.category3.id
        # 检查sku规格数据是否有效
        specs = attrs['specs']
        spu_specs = spu.specs.all()
        spec_count = spu_specs.count()
        # SKU商品的规格数据是否完整
        if spec_count != len(specs):
            raise serializers.ValidationError('SKU规格数据不完整')

        # SKU商品的规格数据是否一致
        specs_ids = [spec.get('spec_id') for spec in specs]
        spu_specs_ids = [spec.id for spec in spu_specs]

        # 排序
        specs_ids.sort()
        spu_specs_ids.sort()

        # 对比规格数据是否一致
        if spu_specs_ids != specs_ids:
            raise serializers.ValidationError('商品规格数据有误')

        for spec in specs:
            spec_id = spec.get('spec_id')
            option_id = spec.get('option_id')

            # 检查spec_id对应的规格是否包含option_id对应的选项
            options = SpecificationOption.objects.filter(spec_id=spec_id)
            options_ids = [option.id for option in options]

            if option_id not in options_ids:
                raise serializers.ValidationError('规格选项数据有误')

        return attrs

    def create(self, validated_data):
        """保存sku商品数据"""
        specs = validated_data.pop('specs')

        with transaction.atomic():
            # 新增sku商品
            sku = SKU.objects.create(**validated_data)
            # 保存商品规格信息
            for spec in specs:
                SKUSpecification.objects.create(
                    sku=sku,
                    spec_id=spec.get('spec_id'),
                    option_id=spec.get('option_id')
                )

        return sku

    def update(self, instance, validated_data):
        """修改sku商品数据"""
        specs = validated_data.pop('specs')

        with transaction.atomic():
            # 调用父类方法更新sku商品
            sku = super().update(instance, validated_data)

            # 清除sku原有的规格信息
            instance.specs.all().delete()

            # 保存商品规格信息
            for spec in specs:
                SKUSpecification.objects.create(
                    sku=instance,
                    spec_id=spec.get('spec_id'),
                    option_id=spec.get('option_id')
                )

        return sku
