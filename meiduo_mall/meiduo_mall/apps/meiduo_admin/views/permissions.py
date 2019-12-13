from django.contrib.auth.models import Permission
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from meiduo_admin.serializers.permissions import PermissionSerializer, PermissionSimpleSerializer, GroupSimpleSerializer
from django.contrib.contenttypes.models import ContentType
from meiduo_admin.serializers.permissions import ContentTypeSerializer
from django.contrib.auth.models import Group
from meiduo_admin.serializers.permissions import GroupSerializer
from meiduo_admin.serializers.permissions import AdminSerializer
from users.models import User


# GET /meiduo_admin/permission/perms/
class PermissionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    # 指定视图所使用的查询集
    queryset = Permission.objects.all()

    # 指定视图所使用的序列化器类
    serializer_class = PermissionSerializer

    # GET `/meiduo_admin/permission/content_types/`
    def content_types(self, request):
        """
        获取权限内容类型数据：
        1. 获取权限内容类型数据
        2. 将权限内容类型数据序列化并返回
        """
        # 1. 获取权限内容类型数据
        content_types = ContentType.objects.all()

        # 2. 将权限内容类型数据序列化并返回
        serializer = ContentTypeSerializer(content_types, many=True)
        return Response(serializer.data)


# GET  `/meiduo_admin/permission/groups/`
class GroupViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    # 指定视图所使用的查询集
    queryset = Group.objects.all()

    # 指定视图所使用的序列化器类
    serializer_class = GroupSerializer

    # GET `/meiduo_admin/permission/simple/`
    def simple(self, request):
        """
        获取权限数据:
        1. 获取权限数据
        2. 将权限数据序列化并返回
        """
        # 1. 获取权限数据
        permissions = Permission.objects.all()

        # 2. 将权限数据序列化并返回
        serializer = PermissionSimpleSerializer(permissions, many=True)
        return Response(serializer.data)


# GET /meiduo_admin/permission/admins/
class AdminViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    # 指定视图所使用的查询集
    queryset = User.objects.filter(is_staff=True)

    # 指定视图所使用的序列化器类
    serializer_class = AdminSerializer

    # GET /meiduo_admin/permission/groups/simple/
    def simple(self, request):
        """
        获取用户组数据:
        1. 获取用户组数据
        2. 将用户组数据序列化并返回
        """
        # 1. 获取用户组数据
        groups = Group.objects.all()

        # 2. 将用户组数据序列化并返回
        serializer = GroupSimpleSerializer(groups, many=True)
        return Response(serializer.data)
