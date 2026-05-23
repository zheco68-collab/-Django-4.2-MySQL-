import json
import csv
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from functools import wraps
from StaffManage.models import (
    Department, InsuranceCompany, Supplier, Employee, Premium, AdminUser
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
def index_view(request):
    employee_count = Employee.objects.count()
    on_job_count = Employee.objects.filter(status='ON').count()
    off_job_count = Employee.objects.filter(status='OFF').count()
    company_count = InsuranceCompany.objects.count()
    supplier_count = Supplier.objects.count()
    
    import json
    
    # 工种分布数据
    work_type_data = json.dumps([
        Employee.objects.filter(work_type='TYPE1').count(),
        Employee.objects.filter(work_type='TYPE2').count(),
        Employee.objects.filter(work_type='TYPE3').count(),
    ])
    
    # 投保公司统计数据
    companies = InsuranceCompany.objects.all()
    company_labels = json.dumps([c.name for c in companies])
    company_data = json.dumps([Employee.objects.filter(insurance_company=c).count() for c in companies])
    
    context = {
        'employee_count': employee_count,
        'on_job_count': on_job_count,
        'off_job_count': off_job_count,
        'company_count': company_count,
        'supplier_count': supplier_count,
        'work_type_data': work_type_data,
        'company_labels': company_labels,
        'company_data': company_data,
    }
    return render(request, 'StaffManage/index.html', context)


@admin_login_required
def employee_list(request):
    employees = Employee.objects.select_related('insurance_company', 'supplier', 'department').all()
    
    name = request.GET.get('name', '')
    id_card = request.GET.get('id_card', '')
    company = request.GET.get('company', '')
    supplier = request.GET.get('supplier', '')
    work_type = request.GET.get('work_type', '')
    status = request.GET.get('status', '')
    
    if name:
        employees = employees.filter(name__icontains=name)
    if id_card:
        employees = employees.filter(id_card__icontains=id_card)
    if company:
        employees = employees.filter(insurance_company_id=company)
    if supplier:
        employees = employees.filter(supplier_id=supplier)
    if work_type:
        employees = employees.filter(work_type=work_type)
    if status:
        employees = employees.filter(status=status)
    
    companies = InsuranceCompany.objects.all()
    suppliers = Supplier.objects.all()
    departments = Department.objects.all()
    
    context = {
        'employees': employees,
        'companies': companies,
        'suppliers': suppliers,
        'departments': departments,
        'name': name,
        'id_card': id_card,
        'company': company,
        'supplier': supplier,
        'work_type': work_type,
        'status': status,
    }
    return render(request, 'StaffManage/employee_list.html', context)


@admin_login_required
def employee_import(request):
    if request.method == 'GET':
        return render(request, 'StaffManage/employee_import.html')
    
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            return JsonResponse({'success': False, 'message': '请选择CSV文件'})
        
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'success': False, 'message': '请上传CSV格式文件'})
        
        try:
            import codecs
            decoded_file = codecs.iterdecode(csv_file, 'utf-8-sig')
            reader = csv.reader(decoded_file)
            next(reader)  # 跳过表头
            
            success_count = 0
            fail_count = 0
            errors = []
            
            for row_num, row in enumerate(reader, start=2):
                if len(row) < 9:
                    fail_count += 1
                    errors.append(f"第{row_num}行：数据列数不足")
                    continue
                
                try:
                    name = row[0].strip()
                    id_card = row[1].strip()
                    work_type = row[2].strip()
                    company_name = row[3].strip()
                    supplier_name = row[4].strip()
                    department_name = row[5].strip()
                    premium_standard = row[6].strip()
                    hire_date = row[7].strip()
                    status = row[8].strip()
                    phone = row[9].strip() if len(row) > 9 else ''
                    leave_date = row[10].strip() if len(row) > 10 else ''
                    
                    # 获取外键对象
                    company = InsuranceCompany.objects.filter(name=company_name).first()
                    supplier = Supplier.objects.filter(name=supplier_name).first()
                    department = Department.objects.filter(name=department_name).first()
                    
                    if not company:
                        fail_count += 1
                        errors.append(f"第{row_num}行：投保公司 '{company_name}' 不存在")
                        continue
                    if not supplier:
                        fail_count += 1
                        errors.append(f"第{row_num}行：供应商 '{supplier_name}' 不存在")
                        continue
                    if not department:
                        fail_count += 1
                        errors.append(f"第{row_num}行：部门 '{department_name}' 不存在")
                        continue
                    
                    # 转换工种
                    work_type_map = {'一类': 'TYPE1', '二类': 'TYPE2', '三类': 'TYPE3'}
                    if work_type not in work_type_map:
                        fail_count += 1
                        errors.append(f"第{row_num}行：工种 '{work_type}' 无效，应为：一类/二类/三类")
                        continue
                    work_type_code = work_type_map[work_type]
                    
                    # 转换状态
                    status_code = 'ON' if status == '在职' else 'OFF'
                    
                    # 检查身份证是否已存在
                    if Employee.objects.filter(id_card=id_card).exists():
                        fail_count += 1
                        errors.append(f"第{row_num}行：身份证号 '{id_card}' 已存在")
                        continue
                    
                    employee = Employee(
                        name=name,
                        id_card=id_card,
                        work_type=work_type_code,
                        insurance_company=company,
                        supplier=supplier,
                        department=department,
                        premium_standard=float(premium_standard),
                        hire_date=datetime.strptime(hire_date, '%Y-%m-%d').date(),
                        leave_date=datetime.strptime(leave_date, '%Y-%m-%d').date() if leave_date else None,
                        status=status_code,
                        phone=phone,
                    )
                    employee.save()
                    success_count += 1
                except Exception as e:
                    fail_count += 1
                    errors.append(f"第{row_num}行：导入失败 - {str(e)}")
            
            return JsonResponse({
                'success': True,
                'message': f'导入完成！成功：{success_count}条，失败：{fail_count}条',
                'success_count': success_count,
                'fail_count': fail_count,
                'errors': errors
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'导入失败：{str(e)}'})


@admin_login_required
def employee_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            employee = Employee(
                name=data['name'],
                work_type=data['work_type'],
                insurance_company_id=data['insurance_company'],
                supplier_id=data['supplier'],
                premium_standard=data['premium_standard'],
                hire_date=datetime.strptime(data['hire_date'], '%Y-%m-%d').date(),
                leave_date=datetime.strptime(data['leave_date'], '%Y-%m-%d').date() if data.get('leave_date') else None,
                status=data['status'],
                department_id=data['department'],
                id_card=data['id_card'],
                phone=data.get('phone', ''),
            )
            employee.save()
            return JsonResponse({'success': True, 'message': '添加成功'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    companies = InsuranceCompany.objects.all()
    suppliers = Supplier.objects.all()
    departments = Department.objects.all()
    return render(request, 'StaffManage/employee_form.html', {'companies': companies, 'suppliers': suppliers, 'departments': departments})


@admin_login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            employee.name = data['name']
            employee.work_type = data['work_type']
            employee.insurance_company_id = data['insurance_company']
            employee.supplier_id = data['supplier']
            employee.premium_standard = data['premium_standard']
            employee.hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
            employee.leave_date = datetime.strptime(data['leave_date'], '%Y-%m-%d').date() if data.get('leave_date') else None
            employee.status = data['status']
            employee.department_id = data['department']
            employee.id_card = data['id_card']
            employee.phone = data.get('phone', '')
            employee.save()
            return JsonResponse({'success': True, 'message': '更新成功'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    companies = InsuranceCompany.objects.all()
    suppliers = Supplier.objects.all()
    departments = Department.objects.all()
    return render(request, 'StaffManage/employee_form.html', {
        'employee': employee,
        'companies': companies,
        'suppliers': suppliers,
        'departments': departments,
    })


@admin_login_required
def employee_delete(request, pk):
    try:
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return JsonResponse({'success': True, 'message': '删除成功'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_login_required
def employee_export(request):
    employees = Employee.objects.select_related('insurance_company', 'supplier', 'department').all()
    
    name = request.GET.get('name', '')
    id_card = request.GET.get('id_card', '')
    company = request.GET.get('company', '')
    supplier = request.GET.get('supplier', '')
    work_type = request.GET.get('work_type', '')
    status = request.GET.get('status', '')
    
    if name:
        employees = employees.filter(name__icontains=name)
    if id_card:
        employees = employees.filter(id_card__icontains=id_card)
    if company:
        employees = employees.filter(insurance_company_id=company)
    if supplier:
        employees = employees.filter(supplier_id=supplier)
    if work_type:
        employees = employees.filter(work_type=work_type)
    if status:
        employees = employees.filter(status=status)
    
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response.write('\ufeff')
    response['Content-Disposition'] = 'attachment; filename=employees.csv'
    
    writer = csv.writer(response)
    writer.writerow(['序号', '姓名', '工种', '投保公司', '供应商', '保费标准(每天)', '实时保费', '入职时间', '离职时间'])
    
    for i, emp in enumerate(employees, 1):
        writer.writerow([
            i,
            emp.name,
            emp.get_work_type_display(),
            emp.insurance_company.name,
            emp.supplier.name,
            emp.premium_standard,
            emp.real_time_premium,
            emp.hire_date,
            emp.leave_date if emp.leave_date else '',
        ])
    
    return response


@admin_login_required
def premium_query(request):
    premiums = Premium.objects.select_related('insurance_company').all()
    
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    company = request.GET.get('company', '')
    
    if start_date:
        premiums = premiums.filter(start_date__gte=start_date)
    if end_date:
        premiums = premiums.filter(end_date__lte=end_date)
    if company and company != 'all':
        premiums = premiums.filter(insurance_company_id=company)
    
    companies = InsuranceCompany.objects.all()
    
    context = {
        'premiums': premiums,
        'companies': companies,
        'start_date': start_date,
        'end_date': end_date,
        'company': company,
    }
    return render(request, 'StaffManage/premium_query.html', context)


@admin_login_required
def premium_export(request):
    premiums = Premium.objects.select_related('insurance_company').all()
    
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    company = request.GET.get('company', '')
    
    if start_date:
        premiums = premiums.filter(start_date__gte=start_date)
    if end_date:
        premiums = premiums.filter(end_date__lte=end_date)
    if company and company != 'all':
        premiums = premiums.filter(insurance_company_id=company)
    
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response.write('\ufeff')
    response['Content-Disposition'] = 'attachment; filename=premiums.csv'
    
    writer = csv.writer(response)
    writer.writerow(['序号', '开始时间', '截止时间', '投保公司', '保费总额(元)'])
    
    for i, p in enumerate(premiums, 1):
        writer.writerow([
            i,
            p.start_date,
            p.end_date,
            p.insurance_company.name,
            p.total_amount,
        ])
    
    return response


@admin_login_required
def company_list(request):
    companies = InsuranceCompany.objects.all()
    return render(request, 'StaffManage/company_list.html', {'companies': companies})


@admin_login_required
def company_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            company = InsuranceCompany(
                name=data['name'],
                code=data['code'],
                contact=data.get('contact', ''),
                phone=data.get('phone', ''),
            )
            company.save()
            return JsonResponse({'success': True, 'message': '添加成功'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return render(request, 'StaffManage/company_form.html')


@admin_login_required
def company_update(request, pk):
    company = get_object_or_404(InsuranceCompany, pk=pk)
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            company.name = data['name']
            company.code = data['code']
            company.contact = data.get('contact', '')
            company.phone = data.get('phone', '')
            company.save()
            return JsonResponse({'success': True, 'message': '更新成功'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return render(request, 'StaffManage/company_form.html', {'company': company})


@admin_login_required
def company_delete(request, pk):
    try:
        company = get_object_or_404(InsuranceCompany, pk=pk)
        company.delete()
        return JsonResponse({'success': True, 'message': '删除成功'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@admin_login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'StaffManage/supplier_list.html', {'suppliers': suppliers})


@admin_login_required
def supplier_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            supplier = Supplier(
                name=data['name'],
                code=data['code'],
                contact=data.get('contact', ''),
                phone=data.get('phone', ''),
            )
            supplier.save()
            return JsonResponse({'success': True, 'message': '添加成功'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return render(request, 'StaffManage/supplier_form.html')


@admin_login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            supplier.name = data['name']
            supplier.code = data['code']
            supplier.contact = data.get('contact', '')
            supplier.phone = data.get('phone', '')
            supplier.save()
            return JsonResponse({'success': True, 'message': '更新成功'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return render(request, 'StaffManage/supplier_form.html', {'supplier': supplier})


@admin_login_required
def supplier_delete(request, pk):
    try:
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.delete()
        return JsonResponse({'success': True, 'message': '删除成功'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
