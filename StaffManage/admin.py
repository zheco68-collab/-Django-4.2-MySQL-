from django.contrib import admin
from StaffManage.models import (
    Department, Position, Employee, Education,
    EmergencyContact, Contract, Salary, AdminUser
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'parent', 'leader', 'phone', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['created_at']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'level', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['department', 'level']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['emp_no', 'name', 'gender', 'department', 'position', 'status', 'hire_date']
    search_fields = ['emp_no', 'name', 'id_card', 'phone']
    list_filter = ['status', 'gender', 'department', 'hire_date']
    date_hierarchy = 'hire_date'


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'school', 'major', 'degree', 'end_date']
    search_fields = ['employee__name', 'school', 'major']


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ['employee', 'name', 'relation', 'phone']
    search_fields = ['employee__name', 'name', 'phone']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['contract_no', 'employee', 'contract_type', 'salary', 'start_date', 'end_date', 'status']
    search_fields = ['contract_no', 'employee__name']
    list_filter = ['contract_type', 'status']


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['employee', 'pay_month', 'base_salary', 'net_salary', 'pay_date']
    search_fields = ['employee__name', 'pay_month']
    list_filter = ['pay_month']


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'real_name', 'is_active', 'last_login', 'created_at']
    search_fields = ['username', 'real_name']
    list_filter = ['is_active']
