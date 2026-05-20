import uuid
from django.db import models
from django.utils import timezone


def make_uuid():
    return str(uuid.uuid4()).replace('-', '')


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='部门名称')
    code = models.CharField(max_length=20, unique=True, verbose_name='部门编码')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name='上级部门')
    leader = models.CharField(max_length=50, blank=True, verbose_name='部门负责人')
    phone = models.CharField(max_length=20, blank=True, verbose_name='部门电话')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'department'
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return self.name


class Position(models.Model):
    LEVEL_CHOICES = [
        ('L1', 'L1-基层员工'),
        ('L2', 'L2-骨干员工'),
        ('L3', 'L3-主管级'),
        ('L4', 'L4-经理级'),
        ('L5', 'L5-总监级'),
        ('L6', 'L6-副总经理级'),
        ('L7', 'L7-总经理级'),
    ]
    name = models.CharField(max_length=100, unique=True, verbose_name='职位名称')
    code = models.CharField(max_length=20, unique=True, verbose_name='职位编码')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions', verbose_name='所属部门')
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='L1', verbose_name='职级')
    remark = models.TextField(blank=True, verbose_name='职位说明')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'position'
        verbose_name = '职位'
        verbose_name_plural = '职位'

    def __str__(self):
        return f"{self.department.name} - {self.name}"


class Employee(models.Model):
    GENDER_CHOICES = [('M', '男'), ('F', '女')]
    MARITAL_CHOICES = [('S', '未婚'), ('M', '已婚'), ('D', '离异'), ('W', '丧偶')]
    STATUS_CHOICES = [
        ('ONBOARD', '在职'),
        ('PROBATION', '试用期'),
        ('LEAVE', '离职'),
        ('RETIRED', '退休'),
    ]
    BLOOD_TYPE_CHOICES = [
        ('A', 'A型'), ('B', 'B型'), ('O', 'O型'), ('AB', 'AB型'),
    ]

    emp_no = models.CharField(max_length=20, unique=True, verbose_name='工号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性别')
    id_card = models.CharField(max_length=18, unique=True, verbose_name='身份证号')
    birth_date = models.DateField(verbose_name='出生日期')
    marital_status = models.CharField(max_length=1, choices=MARITAL_CHOICES, default='S', verbose_name='婚姻状况')
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True, verbose_name='血型')
    phone = models.CharField(max_length=20, verbose_name='手机号码')
    email = models.EmailField(verbose_name='电子邮箱')
    native_place = models.CharField(max_length=200, blank=True, verbose_name='籍贯')
    address = models.CharField(max_length=255, blank=True, verbose_name='现住地址')
    emergency_contact = models.CharField(max_length=50, blank=True, verbose_name='紧急联系人')
    emergency_phone = models.CharField(max_length=20, blank=True, verbose_name='紧急联系电话')

    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees', verbose_name='所属部门')
    position = models.ForeignKey(Position, on_delete=models.PROTECT, related_name='employees', verbose_name='职位')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROBATION', verbose_name='员工状态')
    hire_date = models.DateField(verbose_name='入职日期')
    contract_start = models.DateField(verbose_name='合同起始日期')
    contract_end = models.DateField(verbose_name='合同结束日期')

    social_security_no = models.CharField(max_length=30, blank=True, verbose_name='社保账号')
    bank_card_no = models.CharField(max_length=30, blank=True, verbose_name='工资卡号')
    bank_name = models.CharField(max_length=100, blank=True, verbose_name='开户银行')
    photo = models.ImageField(upload_to='photos/', blank=True, verbose_name='照片')

    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'employee'
        verbose_name = '员工'
        verbose_name_plural = '员工'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.emp_no} - {self.name}"


class Education(models.Model):
    DEGREE_CHOICES = [
        ('HS', '高中/中专'),
        ('CJ', '大专'),
        ('BK', '本科'),
        ('SS', '硕士'),
        ('BS', '博士'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='educations', verbose_name='员工')
    school = models.CharField(max_length=200, verbose_name='毕业学校')
    major = models.CharField(max_length=100, verbose_name='专业')
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES, verbose_name='学历')
    start_date = models.DateField(verbose_name='入学日期')
    end_date = models.DateField(verbose_name='毕业日期')
    diploma_no = models.CharField(max_length=50, blank=True, verbose_name='毕业证号')

    class Meta:
        db_table = 'education'
        verbose_name = '学历信息'
        verbose_name_plural = '学历信息'

    def __str__(self):
        return f"{self.employee.name} - {self.school}"


class EmergencyContact(models.Model):
    RELATION_CHOICES = [
        ('SPOUSE', '配偶'), ('CHILD', '子女'), ('PARENT', '父母'),
        ('SIBLING', '兄弟姐妹'), ('OTHER', '其他'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='emergency_contacts', verbose_name='员工')
    name = models.CharField(max_length=50, verbose_name='联系人姓名')
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES, verbose_name='关系')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    address = models.CharField(max_length=255, blank=True, verbose_name='住址')

    class Meta:
        db_table = 'emergency_contact'
        verbose_name = '紧急联系人'
        verbose_name_plural = '紧急联系人'

    def __str__(self):
        return f"{self.employee.name} - {self.name}"


class Contract(models.Model):
    TYPE_CHOICES = [
        ('FIXED', '固定期限劳动合同'),
        ('OPEN', '无固定期限劳动合同'),
        ('PART_TIME', '非全日制用工合同'),
        ('OUTSOURCE', '劳务派遣合同'),
    ]
    STATUS_CHOICES = [
        ('DRAFT', '草稿'),
        ('ACTIVE', '生效中'),
        ('EXPIRED', '已过期'),
        ('TERMINATED', '已终止'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contracts', verbose_name='员工')
    contract_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='合同类型')
    contract_no = models.CharField(max_length=50, unique=True, verbose_name='合同编号')
    start_date = models.DateField(verbose_name='合同起始日')
    end_date = models.DateField(verbose_name='合同终止日')
    salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='合同月薪')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name='合同状态')
    file_path = models.CharField(max_length=255, blank=True, verbose_name='合同文件路径')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'contract'
        verbose_name = '劳动合同'
        verbose_name_plural = '劳动合同'

    def __str__(self):
        return f"{self.employee.name} - {self.contract_no}"


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries', verbose_name='员工')
    pay_month = models.CharField(max_length=7, verbose_name='发放月份')
    base_salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='基本工资')
    post_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='岗位工资')
    traffic_subsidy = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='交通补贴')
    communication_subsidy = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='通讯补贴')
    meal_subsidy = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='餐补')
    overtime_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='加班费')
    performance_bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='绩效奖金')
    social_security = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='社保扣款')
    housing_fund = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='公积金扣款')
    income_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='个人所得税')
    other_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='其他扣款')
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='实发工资')
    pay_date = models.DateField(null=True, blank=True, verbose_name='发放日期')
    remark = models.CharField(max_length=255, blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'salary'
        verbose_name = '薪资记录'
        verbose_name_plural = '薪资记录'
        unique_together = ['employee', 'pay_month']

    def __str__(self):
        return f"{self.employee.name} - {self.pay_month}"


class AdminUser(models.Model):
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
