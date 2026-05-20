import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from functools import wraps
from StaffManage.models import (
    Department, Position, Employee, Education,
    EmergencyContact, Contract, Salary, AdminUser
)


def admin_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_view(request):
    if request.method == 'GET':
        return render(request, 'StaffManage/login.html')

    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()

    if not username or not password:
        return render(request, 'StaffManage/login.html', {'error': '用户名和密码不能为空'})

    try:
        admin = AdminUser.objects.get(username=username)
        if not admin.is_active:
            return render(request, 'StaffManage/login.html', {'error': '账号已被禁用'})
        if check_password(password, admin.password):
            admin.last_login = timezone.now()
            admin.save(update_fields=['last_login'])
            request.session['admin_id'] = admin.id
            request.session['admin_username'] = admin.username
            request.session['admin_real_name'] = admin.real_name
            return redirect('index')
    except AdminUser.DoesNotExist:
        pass

    return render(request, 'StaffManage/login.html', {'error': '用户名或密码错误'})


def logout_view(request):
    request.session.flush()
    return redirect('login')


@admin_login_required
def index(request):
    stats = {
        'total_employees': Employee.objects.count(),
        'onboard_count': Employee.objects.filter(status='ONBOARD').count(),
        'probation_count': Employee.objects.filter(status='PROBATION').count(),
        'leave_count': Employee.objects.filter(status='LEAVE').count(),
        'departments_count': Department.objects.count(),
        'contracts_expiring': Contract.objects.filter(
            status='ACTIVE',
            end_date__lte=timezone.now().date() + timezone.timedelta(days=30)
        ).count(),
    }
    return render(request, 'StaffManage/index.html', {'stats': stats})


@admin_login_required
def department_list(request):
    departments = Department.objects.all().order_by('code')
    return render(request, 'StaffManage/department_list.html', {'departments': departments})


@admin_login_required
@csrf_exempt
def department_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dept = Department.objects.create(
            name=data['name'],
            code=data['code'],
            leader=data.get('leader', ''),
            phone=data.get('phone', ''),
            remark=data.get('remark', ''),
        )
        if data.get('parent_id'):
            dept.parent_id = data['parent_id']
            dept.save()
        return JsonResponse(model_to_dict(dept, exclude=['created_at', 'updated_at']))
    return JsonResponse({'error': 'invalid method'}, status=405)


@admin_login_required
@csrf_exempt
def department_delete(request):
    if request.method == 'POST':
        dept_id = request.POST.get('id')
        dept = get_object_or_404(Department, id=dept_id)
        if dept.employees.exists():
            return JsonResponse({'error': '该部门下有员工，无法删除'}, status=400)
        dept.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'invalid method'}, status=405)


@admin_login_required
def position_list(request):
    positions = Position.objects.select_related('department').all().order_by('department__code', 'code')
    return render(request, 'StaffManage/position_list.html', {'positions': positions})


@admin_login_required
@csrf_exempt
def position_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pos = Position.objects.create(
            name=data['name'],
            code=data['code'],
            department_id=data['department_id'],
            level=data.get('level', 'L1'),
            remark=data.get('remark', ''),
        )
        return JsonResponse({
            'id': pos.id, 'name': pos.name, 'code': pos.code,
            'department': pos.department.name, 'level': pos.level, 'remark': pos.remark
        })
    return JsonResponse({'error': 'invalid method'}, status=405)


@admin_login_required
@csrf_exempt
def position_delete(request):
    if request.method == 'POST':
        pos_id = request.POST.get('id')
        pos = get_object_or_404(Position, id=pos_id)
        if pos.employees.exists():
            return JsonResponse({'error': '该职位下有员工，无法删除'}, status=400)
        pos.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'invalid method'}, status=405)


@admin_login_required
def employee_list(request):
    employees = Employee.objects.select_related('department', 'position').all()
    departments = Department.objects.all()
    positions = Position.objects.select_related('department').all()
    return render(request, 'StaffManage/employee_list.html', {
        'employees': employees,
        'departments': departments,
        'positions': positions,
    })


@admin_login_required
@csrf_exempt
def employee_list_api(request):
    filters = {}
    if request.POST.get('name'):
        filters['name__icontains'] = request.POST['name']
    if request.POST.get('emp_no'):
        filters['emp_no__icontains'] = request.POST['emp_no']
    if request.POST.get('department_id'):
        filters['department_id'] = request.POST['department_id']
    if request.POST.get('status'):
        filters['status'] = request.POST['status']
    if request.POST.get('gender'):
        filters['gender'] = request.POST['gender']

    employees = Employee.objects.select_related('department', 'position').filter(**filters)
    data = [{
        'id': e.id, 'emp_no': e.emp_no, 'name': e.name,
        'gender': e.get_gender_display(), 'phone': e.phone,
        'department': e.department.name, 'position': e.position.name,
        'status': e.get_status_display(), 'hire_date': str(e.hire_date),
    } for e in employees]
    return JsonResponse({'data': data})


@admin_login_required
@csrf_exempt
def employee_create(request):
    if request.method == 'POST':
        from django.db import IntegrityError
        try:
            data = json.loads(request.body)
            emp_data = {
                'emp_no': data['emp_no'], 'name': data['name'], 'gender': data['gender'],
                'id_card': data['id_card'], 'birth_date': data['birth_date'],
                'marital_status': data.get('marital_status', 'S'),
                'blood_type': data.get('blood_type', ''),
                'phone': data['phone'], 'email': data['email'],
                'native_place': data.get('native_place', ''),
                'address': data.get('address', ''),
                'emergency_contact': data.get('emergency_contact', ''),
                'emergency_phone': data.get('emergency_phone', ''),
                'department_id': data['department_id'],
                'position_id': data['position_id'],
                'status': data.get('status', 'PROBATION'),
                'hire_date': data['hire_date'],
                'contract_start': data.get('contract_start', data['hire_date']),
                'social_security_no': data.get('social_security_no', ''),
                'bank_card_no': data.get('bank_card_no', ''),
                'bank_name': data.get('bank_name', ''),
                'remark': data.get('remark', ''),
            }
            if data.get('contract_end'):
                emp_data['contract_end'] = data['contract_end']
            emp = Employee.objects.create(**emp_data)
            return JsonResponse({
                'id': emp.id, 'emp_no': emp.emp_no, 'name': emp.name,
                'gender': emp.get_gender_display(),
                'phone': emp.phone, 'department': emp.department.name,
                'position': emp.position.name, 'status': emp.get_status_display(),
                'hire_date': str(emp.hire_date),
            })
        except IntegrityError as e:
            return JsonResponse({'error': '数据重复: 工号或身份证号已存在'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'invalid method'}, status=405)


@admin_login_required
@csrf_exempt
def employee_detail(request, emp_id):
    emp = get_object_or_404(Employee.objects.select_related('department', 'position'), id=emp_id)
    educations = list(emp.educations.all().values())
    contacts = list(emp.emergency_contacts.all().values())
    contracts = list(emp.contracts.all().values())
    salaries = list(emp.salaries.all().order_by('-pay_month').values())
    emp_data = model_to_dict(emp, exclude=['photo', 'created_at', 'updated_at'])
    emp_data['gender_display'] = emp.get_gender_display()
    emp_data['status_display'] = emp.get_status_display()
    emp_data['department_name'] = emp.department.name
    emp_data['position_name'] = emp.position.name
    return JsonResponse({
        'employee': emp_data,
        'educations': educations,
        'contacts': contacts,
        'contracts': contracts,
        'salaries': salaries,
    })


@admin_login_required
@csrf_exempt
def employee_update(request, emp_id):
    if request.method == 'POST':
        emp = get_object_or_404(Employee, id=emp_id)
        data = json.loads(request.body)
        for field in ['name', 'gender', 'id_card', 'birth_date', 'marital_status',
                       'blood_type', 'phone', 'email', 'native_place', 'address',
                       'emergency_contact', 'emergency_phone', 'department_id',
                       'position_id', 'status', 'hire_date', 'contract_start',
                       'social_security_no', 'bank_card_no',
                       'bank_name', 'remark']:
            if field in data:
                setattr(emp, field, data[field])
        if data.get('contract_end'):
            emp.contract_end = data['contract_end']
        elif 'contract_end' in data and not data['contract_end']:
            emp.contract_end = None
        emp.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'invalid method'}, status=405)


@admin_login_required
def employee_export(request):
    import csv
    from django.http import HttpResponse
    from urllib.parse import quote
    
    employees = Employee.objects.select_related('department', 'position').all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{quote("员工档案.csv")}"'
    
    response.write('\ufeff')
    
    writer = csv.writer(response)
    writer.writerow([
        '工号', '姓名', '性别', '身份证号', '出生日期', '婚姻状况',
        '血型', '手机', '邮箱', '籍贯', '现住地址',
        '紧急联系人', '紧急联系电话', '部门', '职位', '员工状态',
        '入职日期', '合同起始日期', '合同结束日期',
        '社保账号', '工资卡号', '开户银行', '备注'
    ])
    
    for emp in employees:
        writer.writerow([
            emp.emp_no, emp.name, emp.get_gender_display(), emp.id_card, emp.birth_date,
            emp.get_marital_status_display(), emp.get_blood_type_display() if emp.blood_type else '',
            emp.phone, emp.email, emp.native_place, emp.address,
            emp.emergency_contact, emp.emergency_phone, emp.department.name,
            emp.position.name, emp.get_status_display(), emp.hire_date,
            emp.contract_start, emp.contract_end if emp.contract_end else '',
            emp.social_security_no, emp.bank_card_no, emp.bank_name, emp.remark
        ])
    
    return response


@admin_login_required
@csrf_exempt
def employee_delete(request):
    if request.method == 'POST':
        emp_id = request.POST.get('id')
        get_object_or_404(Employee, id=emp_id).delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'invalid method'}, status=405)


@admin_login_required
@csrf_exempt
def education_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        edu = Education.objects.create(
            employee_id=data['employee_id'],
            school=data['school'], major=data['major'],
            degree=data['degree'], start_date=data['start_date'],
            end_date=data['end_date'], diploma_no=data.get('diploma_no', ''),
        )
        return JsonResponse(model_to_dict(edu))
    return JsonResponse({'error': 'invalid method'}, status=405)


@admin_login_required
@csrf_exempt
def emergency_contact_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ec = EmergencyContact.objects.create(
            employee_id=data['employee_id'],
            name=data['name'], relation=data['relation'],
            phone=data['phone'], address=data.get('address', ''),
        )
        return JsonResponse(model_to_dict(ec))
    return JsonResponse({'error': 'invalid method'}, status=405)


@admin_login_required
@csrf_exempt
def contract_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        con = Contract.objects.create(
            employee_id=data['employee_id'],
            contract_type=data['contract_type'],
            contract_no=data['contract_no'],
            start_date=data['start_date'], end_date=data['end_date'],
            salary=data['salary'], status=data.get('status', 'ACTIVE'),
            remark=data.get('remark', ''),
        )
        return JsonResponse(model_to_dict(con, exclude=['created_at']))
    return JsonResponse({'error': 'invalid method'}, status=405)


@admin_login_required
@csrf_exempt
def salary_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sal = Salary.objects.create(
            employee_id=data['employee_id'], pay_month=data['pay_month'],
            base_salary=data['base_salary'], post_salary=data.get('post_salary', 0),
            traffic_subsidy=data.get('traffic_subsidy', 0),
            communication_subsidy=data.get('communication_subsidy', 0),
            meal_subsidy=data.get('meal_subsidy', 0),
            overtime_pay=data.get('overtime_pay', 0),
            performance_bonus=data.get('performance_bonus', 0),
            social_security=data.get('social_security', 0),
            housing_fund=data.get('housing_fund', 0),
            income_tax=data.get('income_tax', 0),
            other_deduction=data.get('other_deduction', 0),
            net_salary=data['net_salary'],
            pay_date=data.get('pay_date'), remark=data.get('remark', ''),
        )
        return JsonResponse(model_to_dict(sal, exclude=['created_at']))
    return JsonResponse({'error': 'invalid method'}, status=405)


@admin_login_required
def salary_list(request):
    salaries = Salary.objects.select_related('employee').all().order_by('-pay_month')[:100]
    return render(request, 'StaffManage/salary_list.html', {'salaries': salaries})


@admin_login_required
def salary_export(request):
    import csv
    from django.http import HttpResponse
    from urllib.parse import quote
    
    salaries = Salary.objects.select_related('employee').all().order_by('-pay_month')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{quote("薪资记录.csv")}"'
    response.write('\ufeff')
    
    writer = csv.writer(response)
    writer.writerow([
        '员工姓名', '工号', '发放月份', '基本工资', '岗位工资', '加班费',
        '绩效奖金', '交通补贴', '餐补', '通讯补贴',
        '社保扣款', '公积金扣款', '个人所得税', '其他扣款', '实发工资',
        '发放日期', '备注'
    ])
    
    for sal in salaries:
        writer.writerow([
            sal.employee.name, sal.employee.emp_no, sal.pay_month,
            sal.base_salary, sal.post_salary, sal.overtime_pay,
            sal.performance_bonus, sal.traffic_subsidy, sal.meal_subsidy,
            sal.communication_subsidy,
            sal.social_security, sal.housing_fund, sal.income_tax,
            sal.other_deduction, sal.net_salary,
            sal.pay_date if sal.pay_date else '', sal.remark
        ])
    
    return response


@admin_login_required
def contract_list(request):
    contracts = Contract.objects.select_related('employee').filter(
        status='ACTIVE'
    ).order_by('end_date')
    return render(request, 'StaffManage/contract_list.html', {'contracts': contracts})


@admin_login_required
def get_departments_api(request):
    departments = Department.objects.all().values('id', 'name', 'code')
    return JsonResponse({'data': list(departments)})


@admin_login_required
def get_positions_api(request):
    dept_id = request.GET.get('department_id')
    if dept_id:
        positions = Position.objects.filter(department_id=dept_id).values('id', 'name', 'level')
    else:
        positions = Position.objects.select_related('department').all().values('id', 'name', 'level', 'department__name')
    return JsonResponse({'data': list(positions)})
