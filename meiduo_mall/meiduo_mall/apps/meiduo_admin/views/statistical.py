from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView


# GET /meiduo_admin/statistical/day_active/
from users.models import User


class UserDayActiveView(APIView):
    permission_classes = [IsAdminUser]
    """
    获取用户日活跃量
    1.获取用户日活跃量
    2.返回响应
    """
    def get(self, request):
        # 1.获取用户日活跃量
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(last_login__gte=now_date).count()
        # 2.返回响应
        response_data = {
            "count": count,
            "date": now_date.date()
        }
        return Response(response_data)


# GET /meiduo_admin/statistical/day_active/
class UserDayOrdersView(APIView):
    permission_classes = [IsAdminUser]
    """
    获取用户日下单量
    1.获取用户日下单量
    2.返回响应
    """
    def get(self, request):
        # 1.获取用户日下单量
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(orders__create_time__gte=now_date).distinct().count()
        # 2.返回数据
        response_data = {
            "count": count,
            "date": now_date.date()
        }
        return Response(response_data)


class UserMonthCountView(APIView):
    permission_classes = [IsAdminUser]
    """
    获取当月每日新增用户数据:
    1.获取当月每日新增用户数据
    2.返回响应
    """
    def get(self, request):
        # 1.获取结束的时间
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # 2.获取起始时间
        begin_date = now_date - timezone.timedelta(days=29)
        # 3.当天时间
        current_date = begin_date
        # 4.新增用户量
        month_li = []
        while current_date <= now_date:
            # 获取下一天
            next_date = current_date + timezone.timedelta(days=1)
            # 获取当天加入的用户数量
            count = User.objects.filter(date_joined__gte=current_date, date_joined__lte=next_date).count()
            # 把数量添加到列表中
            month_li.append({
                "count": count,
                "date": current_date.date()
            })
            # 将当天时间+1天
            current_date += timezone.timedelta(days=1)
        # 5.返回响应
        return Response(month_li)


