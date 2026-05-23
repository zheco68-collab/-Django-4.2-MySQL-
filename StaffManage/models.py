from django.db import models
from django.utils import timezone


class Department(models.Model):
    """部门表"""
    name = models.CharField(max_length=100, unique=True, verbose_name='部门名称')
    code = models.CharField(max_length=20, unique=True, verbose_name='部门编码')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'department'
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.name


class InsuranceCompany(models.Model):
    """投保公司表"""
    name = models.CharField(max_length=100, unique=True, verbose_name='投保公司名称')
    code = models.CharField(max_length=20, unique=True, verbose_name='公司编码')
    contact = models.CharField(max_length=50, blank=True, verbose_name='联系人')
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'insurance_company'
        verbose_name = '投保公司'
        verbose_name_plural = '投保公司'

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """供应商表"""
    name = models.CharField(max_length=100, unique=True, verbose_name='供应商名称')
    code = models.CharField(max_length=20, unique=True, verbose_name='供应商编码')
    contact = models.CharField(max_length=50, blank=True, verbose_name='联系人')
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'supplier'
        verbose_name = '供应商'
        verbose_name_plural = '供应商'

    def __str__(self):
        return self.name


class Employee(models.Model):
    """员工表"""
    WORK_TYPE_CHOICES = [
        ('TYPE1', '一类'),
        ('TYPE2', '二类'),
        ('TYPE3', '三类'),
    ]
    STATUS_CHOICES = [
        ('ON', '在职'),
        ('OFF', '离职'),
    ]

    name = models.CharField(max_length=50, verbose_name='姓名')
    work_type = models.CharField(max_length=10, choices=WORK_TYPE_CHOICES, verbose_name='工种')
    insurance_company = models.ForeignKey(InsuranceCompany, on_delete=models.PROTECT, related_name='employees', verbose_name='投保公司')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='employees', verbose_name='供应商')
    premium_standard = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='保费标准(每天)')
    real_time_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='实时保费')
    hire_date = models.DateField(verbose_name='入职时间')
    leave_date = models.DateField(null=True, blank=True, verbose_name='离职时间')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ON', verbose_name='在职状态')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees', verbose_name='所属部门')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'employee'
        verbose_name = '员工'
        verbose_name_plural = '员工'

    def __str__(self):
        return self.name


class Premium(models.Model):
    """保费信息表"""
    start_date = models.DateField(verbose_name='开始时间')
    end_date = models.DateField(verbose_name='截止时间')
    insurance_company = models.ForeignKey(InsuranceCompany, on_delete=models.PROTECT, related_name='premiums', verbose_name='投保公司')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='保费总额(元)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'premium'
        verbose_name = '保费信息'
        verbose_name_plural = '保费信息'

    def __str__(self):
        return f"{self.insurance_company.name} - {self.start_date} to {self.end_date}"


class AdminUser(models.Model):
    """管理员表"""
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    real_name = models.CharField(max_length=50, blank=True, verbose_name='真实姓名')
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='最后登录时间')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        db_table = 'admin_user'
        verbose_name = '管理员'
        verbose_name_plural = '管理员'

    def __str__(self):
        return self.username
