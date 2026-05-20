from django.urls import path, re_path
from django.contrib import admin
from StaffManage import views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.index, name='index'),
    re_path(r'^login$', views.login_view, name='login'),
    re_path(r'^logout$', views.logout_view, name='logout'),

    re_path(r'^department/list$', views.department_list, name='department_list'),
    re_path(r'^department/create$', views.department_create, name='department_create'),
    re_path(r'^department/delete$', views.department_delete, name='department_delete'),

    re_path(r'^position/list$', views.position_list, name='position_list'),
    re_path(r'^position/create$', views.position_create, name='position_create'),
    re_path(r'^position/delete$', views.position_delete, name='position_delete'),

    re_path(r'^employee/list$', views.employee_list, name='employee_list'),
    re_path(r'^employee/api/list$', views.employee_list_api, name='employee_list_api'),
    re_path(r'^employee/create$', views.employee_create, name='employee_create'),
    re_path(r'^employee/update/(\d+)$', views.employee_update, name='employee_update'),
    re_path(r'^employee/detail/(\d+)$', views.employee_detail, name='employee_detail'),
    re_path(r'^employee/delete$', views.employee_delete, name='employee_delete'),
    re_path(r'^employee/export$', views.employee_export, name='employee_export'),

    re_path(r'^education/create$', views.education_create, name='education_create'),
    re_path(r'^emergency-contact/create$', views.emergency_contact_create, name='emergency_contact_create'),
    re_path(r'^contract/create$', views.contract_create, name='contract_create'),
    re_path(r'^contract/list$', views.contract_list, name='contract_list'),

    re_path(r'^salary/list$', views.salary_list, name='salary_list'),
    re_path(r'^salary/create$', views.salary_create, name='salary_create'),
    re_path(r'^salary/export$', views.salary_export, name='salary_export'),

    re_path(r'^api/departments$', views.get_departments_api, name='get_departments_api'),
    re_path(r'^api/positions$', views.get_positions_api, name='get_positions_api'),
]
