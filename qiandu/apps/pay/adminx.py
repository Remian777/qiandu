import xadmin
# Register your models here.

from . import models
# 自定义xadmin主题
from xadmin import views
class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "小说网站"  # 设置站点标题
    site_footer = "阿姆斯特朗回旋加速喷气式阿姆斯特朗炮小说网站"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠
xadmin.site.register(views.CommAdminView, GlobalSettings)

xadmin.site.register(models.Order)
xadmin.site.register(models.payment)