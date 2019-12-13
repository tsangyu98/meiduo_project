from django.conf.urls import url

from meiduo_admin.views import orders, permissions
from .views import users, statistical, skus, goods, channels, spus, specs, brands
from rest_framework.routers import DefaultRouter, SimpleRouter


urlpatterns = [
    # 进行url配置
    url(r'^authorizations/$', users.AdminAuthorizeView.as_view()),
    url(r'^statistical/day_active/$', statistical.UserDayActiveView.as_view()),
    url(r'^statistical/day_orders/$', statistical.UserDayOrdersView.as_view()),
    url(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    url(r'^users/$', users.UserInfoView.as_view()),
    url(r'^skus/simple/$', skus.SKUSimpleView.as_view()),
    url(r'^statistical/total_count/$', users.UserCountView.as_view()),
    url(r'^statistical/day_increment/$', users.UserDayCreateNum.as_view()),
    url(r'^statistical/goods_day_views/$', goods.DayCategoryGoodsView.as_view()),
    url(r'^goods/channel_types/$', channels.ChannelTypesView.as_view()),
    url(r'^goods/categories/$', channels.GetFirstCategoryView.as_view()),
    url(r'^goods/brands/simple/$', spus.GetBrandView.as_view()),
    url(r'^goods/channel/categories/$', spus.GetCategoryView.as_view()),
    url(r'^goods/channel/categories/(?P<pk>\d+)/$', spus.GetOtherCategoryView.as_view()),
    url(r'^goods/simple/$', spus.SPUSimpleView.as_view()),
    url(r'^goods/(?P<pk>\d+)/specs/$', spus.SPUSpecView.as_view()),
    url(r'^goods/specs/simple/$', specs.GoodsSpecsSimpleView.as_view()),
    url(r'^orders/(?P<pk>\d+)/status/$', orders.ChangeStatusView.as_view()),
    url(r'^permission/content_types/$', permissions.PermissionViewSet.as_view({'get': 'content_types'})),
    url(r'^permission/simple/$', permissions.GroupViewSet.as_view({'get': 'simple'})),
    url(r'^permission/groups/simple/$', permissions.AdminViewSet.as_view({'get': 'simple'}))
]

# 创建route对象
route = SimpleRouter()
# 注册
route.register(r'skus/images', skus.SKUImageViewSet, base_name='images')
route.register(r'skus', skus.SKUViewSet, base_name='skus')
route.register(r'goods/channels', channels.ChannelsViewSet, base_name='channels')
route.register(r'goods', spus.GetSPUViewSet, base_name='goods')
route.register(r'goods/specs', specs.GoodsSpecsViewSet, base_name='goodsspecs')
route.register(r'specs/options', specs.SpecsOptionsViewSet, base_name='specsoptions')
route.register(r'goods/brands', brands.GoodsBrandsViewSet, base_name='goodsbrands')
route.register(r'orders', orders.OrdersViewSet, base_name='orders')
route.register('permission/perms', permissions.PermissionViewSet, base_name='perms')
route.register('permission/groups', permissions.GroupViewSet, base_name='groups')
route.register('permission/admins', permissions.AdminViewSet, base_name='admins')
# 添加到路由列表中
urlpatterns += route.urls
