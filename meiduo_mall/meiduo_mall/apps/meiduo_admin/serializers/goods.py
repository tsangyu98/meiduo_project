from rest_framework import serializers

from goods.models import GoodsVisitCount


class DayCategoryGoodsSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField(label='分类名称')

    class Meta:
        model = GoodsVisitCount
        fields = ('category', 'count')
        extra_kwargs = {
            'category': {
                'read_only': True
            },
            'count': {
                'read_only': True
            }
        }
