from rest_framework import serializers

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory


class ChannelsSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(label='一级分类名', read_only=True)
    category_id = serializers.IntegerField(label='一级分类id')

    group = serializers.StringRelatedField(label='频道组名', read_only=True)
    group_id = serializers.IntegerField(label='频道组id')

    class Meta:
        model = GoodsChannel
        exclude = ('create_time', 'update_time')


class ChannelTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsChannelGroup
        fields = ('id', 'name')


class GetFirstCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')



