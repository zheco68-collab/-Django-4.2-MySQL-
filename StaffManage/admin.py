from django.contrib import admin
from StaffManage.models import (
    Department, InsuranceCompany, Supplier, Employee, Premium, AdminUser
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']


@admin.register(InsuranceCompany)
class InsuranceCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'contact', 'phone', 'created_at']
    search_fields = ['name', 'code']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'contact', 'phone', 'created_at']
    search_fields = ['name', 'code']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'work_type', 'insurance_company', 'supplier', 'department', 'status', 'hire_date']
    search_fields = ['name', 'id_card', 'phone']
    list_filter = ['status', 'work_type', 'department']


@admin.register(Premium)
class PremiumAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'insurance_company', 'total_amount', 'created_at']
    search_fields = ['insurance_company__name']
    list_filter = ['start_date', 'end_date']


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'real_name', 'is_active', 'last_login', 'created_at']
    search_fields = ['username', 'real_name']
    list_filter = ['is_active']
