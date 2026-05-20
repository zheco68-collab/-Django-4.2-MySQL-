# 智慧交通员工信息管理系统

基于 **Django 4.2 + MySQL** 的企业员工信息管理系统，专为智慧交通行业设计，提供完整的员工档案、合同、薪资管理功能。

##  项目亮点

| 亮点             | 说明                                                 |
| ---------------- | ---------------------------------------------------- |
| **智慧交通主题** | 采用深蓝、青绿、金黄配色方案，契合智慧交通行业特性   |
| **安全可靠**     | PBKDF2-SHA256 密码哈希、CSRF防护、完整的登录认证体系 |
| **完整数据模型** | 8张数据表，员工档案35个字段，涵盖人事管理全流程      |
| **数据导出**     | 员工档案、薪资记录支持CSV导出，Excel直接打开无乱码   |
| **响应式设计**   | Bootstrap前端框架，支持桌面和移动设备访问            |
| **高效查询**     | 多条件筛选、部门/职位联动、实时搜索                  |
| **数据完整性**   | 外键约束保护，防止数据不一致                         |
| **快速部署**     | 一键启动，内置测试数据，开箱即用                     |

## 技术栈

| 类别     | 技术                            |
| -------- | ------------------------------- |
| 后端框架 | Django 4.2.14                   |
| 数据库   | MySQL 8.0 (端口 3306)           |
| 前端框架 | Bootstrap 3.4.1 + jQuery 1.12.4 |
| 图标库   | Font Awesome 6.5                |
| 密码加密 | PBKDF2-SHA256                   |

## 快速启动

```bash
# 1. 安装依赖
pip install Django==4.2.14 mysqlclient django-crispy-forms

# 2. 进入项目目录
cd DjangoWebDemo-master

# 3. 启动服务器
python manage.py runserver
```

访问 **http://127.0.0.1:8000/login**

默认账号：`admin` / `admin123`

## 数据库表结构

### 1. department（部门表）

| 字段       | 类型         | 说明               |
| ---------- | ------------ | ------------------ |
| id         | INT (PK)     | 主键，自增         |
| name       | VARCHAR(100) | 部门名称，唯一     |
| code       | VARCHAR(20)  | 部门编码，唯一     |
| parent_id  | INT (FK)     | 上级部门ID，可为空 |
| leader     | VARCHAR(50)  | 部门负责人         |
| phone      | VARCHAR(20)  | 部门电话           |
| remark     | TEXT         | 备注               |
| created_at | DATETIME     | 创建时间           |
| updated_at | DATETIME     | 更新时间           |

### 2. position（职位表）

| 字段          | 类型         | 说明           |
| ------------- | ------------ | -------------- |
| id            | INT (PK)     | 主键，自增     |
| name          | VARCHAR(100) | 职位名称，唯一 |
| code          | VARCHAR(20)  | 职位编码，唯一 |
| department_id | INT (FK)     | 所属部门ID     |
| level         | VARCHAR(10)  | 职级（L1-L7）  |
| remark        | TEXT         | 职位说明       |
| created_at    | DATETIME     | 创建时间       |

**职级选项**：L1-基层员工 / L2-骨干员工 / L3-主管级 / L4-经理级 / L5-总监级 / L6-副总经理级 / L7-总经理级

### 3. employee（员工档案表）

| 字段               | 类型         | 说明                |
| ------------------ | ------------ | ------------------- |
| id                 | INT (PK)     | 主键，自增          |
| emp_no             | VARCHAR(20)  | 工号，唯一          |
| name               | VARCHAR(50)  | 姓名                |
| gender             | VARCHAR(1)   | 性别（M=男，F=女）  |
| id_card            | VARCHAR(18)  | 身份证号，唯一      |
| birth_date         | DATE         | 出生日期            |
| marital_status     | VARCHAR(1)   | 婚姻状况（S/M/D/W） |
| blood_type         | VARCHAR(3)   | 血型（A/B/O/AB）    |
| phone              | VARCHAR(20)  | 手机号码            |
| email              | VARCHAR(254) | 电子邮箱            |
| native_place       | VARCHAR(200) | 籍贯                |
| address            | VARCHAR(255) | 现住地址            |
| emergency_contact  | VARCHAR(50)  | 紧急联系人          |
| emergency_phone    | VARCHAR(20)  | 紧急联系电话        |
| department_id      | INT (FK)     | 所属部门            |
| position_id        | INT (FK)     | 职位                |
| status             | VARCHAR(20)  | 员工状态            |
| hire_date          | DATE         | 入职日期            |
| contract_start     | DATE         | 合同起始日期        |
| contract_end       | DATE         | 合同结束日期        |
| social_security_no | VARCHAR(30)  | 社保账号            |
| bank_card_no       | VARCHAR(30)  | 工资卡号            |
| bank_name          | VARCHAR(100) | 开户银行            |
| photo              | IMAGE        | 照片                |
| remark             | TEXT         | 备注                |
| created_at         | DATETIME     | 创建时间            |
| updated_at         | DATETIME     | 更新时间            |

**员工状态**：PROBATION（试用期）/ ONBOARD（在职）/ LEAVE（离职）/ RETIRED（退休）

### 4. education（学历信息表）

| 字段        | 类型         | 说明       |
| ----------- | ------------ | ---------- |
| id          | INT (PK)     | 主键，自增 |
| employee_id | INT (FK)     | 员工ID     |
| school      | VARCHAR(200) | 毕业学校   |
| major       | VARCHAR(100) | 专业       |
| degree      | VARCHAR(10)  | 学历       |
| start_date  | DATE         | 入学日期   |
| end_date    | DATE         | 毕业日期   |
| diploma_no  | VARCHAR(50)  | 毕业证号   |

**学历选项**：HS（高中/中专）/ CJ（大专）/ BK（本科）/ SS（硕士）/ BS（博士）

### 5. emergency_contact（紧急联系人表）

| 字段        | 类型         | 说明       |
| ----------- | ------------ | ---------- |
| id          | INT (PK)     | 主键，自增 |
| employee_id | INT (FK)     | 员工ID     |
| name        | VARCHAR(50)  | 联系人姓名 |
| relation    | VARCHAR(20)  | 关系       |
| phone       | VARCHAR(20)  | 联系电话   |
| address     | VARCHAR(255) | 住址       |

**关系选项**：SPOUSE（配偶）/ CHILD（子女）/ PARENT（父母）/ SIBLING（兄弟姐妹）/ OTHER（其他）

### 6. contract（劳动合同表）

| 字段          | 类型          | 说明           |
| ------------- | ------------- | -------------- |
| id            | INT (PK)      | 主键，自增     |
| employee_id   | INT (FK)      | 员工ID         |
| contract_type | VARCHAR(20)   | 合同类型       |
| contract_no   | VARCHAR(50)   | 合同编号，唯一 |
| start_date    | DATE          | 合同起始日     |
| end_date      | DATE          | 合同终止日     |
| salary        | DECIMAL(12,2) | 合同月薪       |
| status        | VARCHAR(20)   | 合同状态       |
| file_path     | VARCHAR(255)  | 合同文件路径   |
| created_at    | DATETIME      | 创建时间       |

**合同类型**：FIXED（固定期限）/ OPEN（无固定期限）/ PART_TIME（非全日制）/ OUTSOURCE（劳务派遣）
**合同状态**：DRAFT（草稿）/ ACTIVE（生效中）/ EXPIRED（已过期）/ TERMINATED（已终止）

### 7. salary（薪资记录表）

| 字段                  | 类型          | 说明                |
| --------------------- | ------------- | ------------------- |
| id                    | INT (PK)      | 主键，自增          |
| employee_id           | INT (FK)      | 员工ID              |
| pay_month             | VARCHAR(7)    | 发放月份（YYYY-MM） |
| base_salary           | DECIMAL(12,2) | 基本工资            |
| post_salary           | DECIMAL(12,2) | 岗位工资            |
| traffic_subsidy       | DECIMAL(12,2) | 交通补贴            |
| communication_subsidy | DECIMAL(12,2) | 通讯补贴            |
| meal_subsidy          | DECIMAL(12,2) | 餐补                |
| overtime_pay          | DECIMAL(12,2) | 加班费              |
| performance_bonus     | DECIMAL(12,2) | 绩效奖金            |
| social_security       | DECIMAL(12,2) | 社保扣款            |
| housing_fund          | DECIMAL(12,2) | 公积金扣款          |
| income_tax            | DECIMAL(12,2) | 个人所得税          |
| other_deduction       | DECIMAL(12,2) | 其他扣款            |
| net_salary            | DECIMAL(12,2) | 实发工资            |
| pay_date              | DATE          | 发放日期            |
| remark                | VARCHAR(255)  | 备注                |
| created_at            | DATETIME      | 创建时间            |

**唯一约束**：(employee_id, pay_month)

### 8. admin_user（管理员表）

| 字段       | 类型         | 说明                   |
| ---------- | ------------ | ---------------------- |
| id         | INT (PK)     | 主键，自增             |
| username   | VARCHAR(50)  | 用户名，唯一           |
| password   | VARCHAR(255) | PBKDF2-SHA256 哈希密码 |
| real_name  | VARCHAR(50)  | 真实姓名               |
| phone      | VARCHAR(20)  | 联系电话               |
| is_active  | BOOL         | 是否启用               |
| last_login | DATETIME     | 最后登录时间           |
| created_at | DATETIME     | 创建时间               |

## 系统功能

| 模块       | 功能                                                         |
| ---------- | ------------------------------------------------------------ |
| 首页仪表盘 | 统计员工总数、在职人数、试用期、离职人数、部门数量、合同到期预警 |
| 部门管理   | 部门的增删，支持层级结构（上级部门）                         |
| 职位管理   | 职位增删，关联部门，支持7级职级                              |
| 员工档案   | 完整档案管理（35个字段），支持多条件筛选查询、CSV导出        |
| 合同管理   | 劳动合同记录，到期时间显示                                   |
| 薪资管理   | 月度薪资明细，含各项补贴和扣款、CSV导出                      |
| 登录认证   | PBKDF2-SHA256 密码哈希存储                                   |
| 数据导出   | 员工档案、薪资记录支持CSV格式导出（UTF-8编码，支持Excel打开） |

## 数据库配置

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

## 项目目录结构

```
DjangoWebDemo-master/
├── DjangoWebDemo/           # Django 项目配置
│   ├── settings.py          # 项目配置
│   └── urls.py              # URL 路由
├── StaffManage/             # 员工管理应用
│   ├── models.py            # 数据模型（8张表）
│   ├── views.py             # 视图函数
│   ├── admin.py             # Django 后台注册
│   └── migrations/          # 数据库迁移文件
├── templates/StaffManage/   # HTML 模板
│   ├── base.html            # 基础模板
│   ├── index.html           # 首页仪表盘
│   ├── login.html           # 登录页
│   ├── employee_list.html   # 员工管理
│   ├── department_list.html # 部门管理
│   ├── position_list.html   # 职位管理
│   ├── contract_list.html   # 合同管理
│   └── salary_list.html     # 薪资管理
├── static/                  # 静态文件
├── db.sqlite3               # SQLite 数据库（旧）
└── manage.py                # Django 管理脚本
```

## 数据库迁移

```bash
# 创建迁移文件
python manage.py makemigrations StaffManage

# 执行迁移
python manage.py migrate

# 创建管理员账号
python manage.py shell -c "from StaffManage.models import AdminUser; from django.contrib.auth.hashers import make_password; AdminUser.objects.create(username='admin', password=make_password('admin123'), real_name='系统管理员')"
```
