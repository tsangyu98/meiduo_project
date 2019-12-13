from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from meiduo_admin.serializers.users import AdminAuthSerializer, UserSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework import mixins


# POST /meiduo_admin/authorizations/
class AdminAuthorizeView(CreateAPIView):
    """
    管理员登录
    1.获取参数并进行校验
    2.服务器签发jwt token数据
    3.返回响应
    """
    serializer_class = AdminAuthSerializer


# GET /meiduo_admin/users/?keyword=<搜索内容>&page=<页码>&pagesize=<页容量>
class UserInfoView(ListAPIView, CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    """
    获取普通用户数据
    1.获取keyword关键字
    2.查询普通用户数据
    3.将用户数据序列化后返回响应
    """

    def get_queryset(self):
        # 1.获取keyword关键字
        keyword = self.request.query_params.get('keyword')
        # 2.查询用户数据
        if keyword:
            users = User.objects.filter(is_staff=False, username__contains=keyword)
        else:
            users = User.objects.filter(is_staff=False).all()
        # 返回users
        return users


# GET /meiduo_admin/statistical/total_count/
class UserCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        获取网站用户总数
        1.获取网站用户的人数
        2.返回响应
        """
        # 获取当前时间
        now_date = timezone.now()
        # 获取用户个数
        count = User.objects.filter(is_staff=False).count()
        # 返回响应
        return Response({
            "date": now_date.date(),
            "count": count
        })


# GET /meiduo_admin/statistical/day_increment/
class UserDayCreateNum(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        获取网站日增用户数
        1.获取今天创建账号的用户
        2.返回响应
        """
        # 获取今天的日期
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # 获取今天创建账号的数量
        count = User.objects.filter(date_joined__gte=today, is_staff=False).count()
        return Response({
            "date": today.date(),
            "count": count
        })
