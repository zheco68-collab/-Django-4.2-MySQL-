# 智慧交通员工信息管理系统

基于 Django 框架开发的员工信息管理系统，提供员工管理、投保公司管理、供应商管理和保费查询等功能。

### 在线预览

### 访问地址：https://jnj.zheco68.asia/

**测试账号：**
- 用户名：admin
- 密码：admin123

## 功能特性

### 员工管理
- ✅ 员工信息的增删改查
- ✅ 身份证号查询（隐私保护，列表不显示）
- ✅ 按姓名、工种、投保公司、供应商、状态筛选
- ✅ 批量导入员工（CSV格式）
- ✅ 导出员工信息（CSV格式）

### 投保公司管理
- ✅ 投保公司的增删改查

### 供应商管理
- ✅ 供应商的增删改查

### 保费查询
- ✅ 按时间范围查询保费
- ✅ 按投保公司筛选
- ✅ 导出保费信息（CSV格式）

### 数据可视化
- ✅ 员工状态分布饼图
- ✅ 工种分布柱状图
- ✅ 投保公司统计图表

## 技术栈

- **框架**: Django 3.2+
- **数据库**: MySQL
- **前端**: Bootstrap 3 + Chart.js
- **图标**: Font Awesome

## 项目结构

```
DjangoWebDemo-master/
├── DjangoWebDemo/           # 项目配置
│   ├── settings.py          # 配置文件
│   ├── urls.py              # URL路由
│   └── wsgi.py              # WSGI入口
├── StaffManage/             # 核心应用
│   ├── migrations/          # 数据库迁移
│   ├── admin.py             # 后台管理
│   ├── models.py            # 数据模型
│   └── views.py             # 视图函数
├── templates/
│   └── StaffManage/         # 模板文件
├── manage.py                # 管理命令
└── requirements.txt         # 依赖清单
```

## 数据模型

### 员工表 (Employee)
| 字段 | 类型 | 说明 |
|------|------|------|
| name | CharField | 姓名 |
| id_card | CharField | 身份证号 |
| work_type | CharField | 工种（一类/二类/三类） |
| premium_standard | DecimalField | 保费标准(每天) |
| real_time_premium | DecimalField | 实时保费 |
| hire_date | DateField | 入职时间 |
| leave_date | DateField | 离职时间 |
| status | CharField | 在职状态 |
| department | ForeignKey | 所属部门 |
| insurance_company | ForeignKey | 投保公司 |
| supplier | ForeignKey | 供应商 |

### 部门表 (Department)
| 字段 | 类型 | 说明 |
|------|------|------|
| name | CharField | 部门名称 |

### 投保公司表 (InsuranceCompany)
| 字段 | 类型 | 说明 |
|------|------|------|
| name | CharField | 公司名称 |

### 供应商表 (Supplier)
| 字段 | 类型 | 说明 |
|------|------|------|
| name | CharField | 供应商名称 |

## 安装运行

### 环境要求
- Python 3.8+
- MySQL 5.7+

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd DjangoWebDemo-master
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置数据库**
```bash
# 修改 DjangoWebDemo/settings.py 中的数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

4. **数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **创建管理员**
```bash
python manage.py createsuperuser
```

6. **启动开发服务器**
```bash
python manage.py runserver
```

## 使用说明

### CSV导入格式

导入员工时，CSV文件需包含以下列（顺序固定）：

```csv
姓名,身份证号,工种,投保公司,供应商,部门,保费标准(每天),入职时间,状态,联系电话,离职时间
张三,110101199001011234,一类,公司A,供应商A,人事部,18.00,2024-01-15,在职,13800138001,
```

### 字段说明
- 工种：一类/二类/三类
- 状态：在职/离职
- 投保公司、供应商、部门需预先在系统中创建

