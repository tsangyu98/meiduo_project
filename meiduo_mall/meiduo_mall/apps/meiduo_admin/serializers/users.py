from django.utils import timezone
from rest_framework import serializers
from users.models import User
from rest_framework_jwt.settings import api_settings


class AdminAuthSerializer(serializers.ModelSerializer):
    """管理员序列化器类"""
    username = serializers.CharField(label='用户名')
    token = serializers.CharField(label='JWT Token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        # 1.获取username和password
        username = attrs['username']
        password = attrs['password']

        # 2.校验用户名和密码
        try:
            user = User.objects.get(username=username, is_staff=True)
        except User.DoesNotExist:
            raise serializers.ValidationError('用户名或密码错误')
        else:
            # 检验密码
            if not user.check_password(password):
                # 未通过验证
                raise serializers.ValidationError('用户名或密码错误')
            # 通过验证后在attrs中添加user属性,保存登录用户
            attrs['user'] = user
        return attrs

    def create(self, validated_data):
        # 1.获取登录用户user
        user = validated_data['user']
        # 2.设置最新登录时间
        user.last_login = timezone.now()
        user.save()
        # 3.服务器生成jwt token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 组织payload的方法
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 生成jwt token数据的方法
        # 4.组织payload数据
        payload = jwt_payload_handler(user)
        # 5.生成token
        token = jwt_encode_handler(payload)
        # 给user对象增加属性，保存jwt token数据
        user.token = token
        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile', 'email')




