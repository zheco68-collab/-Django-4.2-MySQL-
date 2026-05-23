from django.urls import path, re_path
from django.contrib import admin
from StaffManage import views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.index_view, name='index'),
    re_path(r'^login$', views.login_view, name='login'),
    re_path(r'^logout$', views.logout_view, name='logout'),

    re_path(r'^employee/list$', views.employee_list, name='employee_list'),
    re_path(r'^employee/create$', views.employee_create, name='employee_create'),
    re_path(r'^employee/update/(\d+)$', views.employee_update, name='employee_update'),
    re_path(r'^employee/delete/(\d+)$', views.employee_delete, name='employee_delete'),
    re_path(r'^employee/export$', views.employee_export, name='employee_export'),
    re_path(r'^employee/import$', views.employee_import, name='employee_import'),

    re_path(r'^premium/query$', views.premium_query, name='premium_query'),
    re_path(r'^premium/export$', views.premium_export, name='premium_export'),

    re_path(r'^company/list$', views.company_list, name='company_list'),
    re_path(r'^company/create$', views.company_create, name='company_create'),
    re_path(r'^company/update/(\d+)$', views.company_update, name='company_update'),
    re_path(r'^company/delete/(\d+)$', views.company_delete, name='company_delete'),

    re_path(r'^supplier/list$', views.supplier_list, name='supplier_list'),
    re_path(r'^supplier/create$', views.supplier_create, name='supplier_create'),
    re_path(r'^supplier/update/(\d+)$', views.supplier_update, name='supplier_update'),
    re_path(r'^supplier/delete/(\d+)$', views.supplier_delete, name='supplier_delete'),
]
