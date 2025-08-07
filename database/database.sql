-- 创建数据库
CREATE DATABASE IF NOT EXISTS order_management_system
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE order_management_system;

-- 创建订单表
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '订单ID',
    order_number VARCHAR(50) NOT NULL UNIQUE COMMENT '订单号',
    customer_name VARCHAR(100) NOT NULL COMMENT '客户名称',
    product_name VARCHAR(100) NOT NULL COMMENT '货品名',
    specification VARCHAR(200) COMMENT '规格',
    quantity DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '数量',
    sale_price DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '销售价',
    sale_type VARCHAR(50) COMMENT '销售类型',
    contract_number VARCHAR(50) COMMENT '合同号',
    expected_delivery_date DATE COMMENT '预定交期',
    input_date DATE COMMENT '输单日期',
    audit_date DATE COMMENT '审核日期',
    production_date DATE COMMENT '生产日期',
    delivery_date DATE COMMENT '交货日期',
    finished_weight DECIMAL(10,2) COMMENT '成品重',
    transport_method VARCHAR(50) COMMENT '运输方式',
    destination TEXT COMMENT '目的地',
    payment_method VARCHAR(100) COMMENT '付款方式',
    remark TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    INDEX idx_customer_name (customer_name),
    INDEX idx_order_number (order_number),
    INDEX idx_input_date (input_date),
    INDEX idx_contract_number (contract_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 创建客户表
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '客户ID',
    customer_name VARCHAR(100) NOT NULL UNIQUE COMMENT '客户名称',
    trademark VARCHAR(100) COMMENT '商标',
    address1 TEXT COMMENT '地址1',
    address2 TEXT COMMENT '地址2',
    industry VARCHAR(50) COMMENT '所在行业',
    statement_date VARCHAR(50) COMMENT '对账日期',
    business_license TEXT COMMENT '客户营业执照信息',
    order_frequency INT DEFAULT 0 COMMENT '订单频率',
    total_orders INT DEFAULT 0 COMMENT '客户累计订单量',
    total_amount DECIMAL(15,2) DEFAULT 0.00 COMMENT '总金额',
    preferred_products JSON COMMENT '偏好品类',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日期',

    INDEX idx_customer_name (customer_name),
    INDEX idx_industry (industry)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户表';

-- 创建客户联系人表
CREATE TABLE customer_contacts (
    contact_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '联系人ID',
    customer_id INT NOT NULL COMMENT '客户ID',
    position VARCHAR(50) COMMENT '职位',
    mobile VARCHAR(20) COMMENT '手机',
    phone VARCHAR(20) COMMENT '电话',
    email VARCHAR(100) COMMENT '邮箱',
    wechat VARCHAR(50) COMMENT '微信',
    other TEXT COMMENT '其他联系方式',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    INDEX idx_customer_id (customer_id),
    INDEX idx_mobile (mobile),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户联系人表';

-- 创建合同文件表（存储合同扫描件信息）
CREATE TABLE contract_files (
    contract_id INT PRIMARY KEY AUTO_INCREMENT COMMENT '合同ID',
    contract_number VARCHAR(50) NOT NULL UNIQUE COMMENT '合同号',
    file_name VARCHAR(200) COMMENT '文件名',
    file_path VARCHAR(500) COMMENT '文件路径',
    file_size INT COMMENT '文件大小(字节)',
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',

    INDEX idx_contract_number (contract_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='合同文件表';

-- 插入一些示例数据

-- 示例客户数据
INSERT INTO customers (customer_name, trademark, address1, industry, statement_date) VALUES
('张三贸易公司', '张三商标', '上海市浦东新区张江路123号', '贸易', '每月5号'),
('李四工业有限公司', '李四工业', '深圳市南山区科技园456号', '制造业', '每月10号'),
('王五进出口公司', '王五进出口', '广州市天河区商务区789号', '进出口', '每月15号');

-- 示例联系人数据
INSERT INTO customer_contacts (customer_id, position, mobile, email, wechat) VALUES
(1, '采购经理', '13800138000', 'zhangsan@example.com', 'zhangsan123'),
(2, '总经理', '13900139000', 'lisi@example.com', 'lisi456'),
(3, '业务主管', '13700137000', 'wangwu@example.com', 'wangwu789');

-- 示例订单数据
INSERT INTO orders (order_number, customer_name, product_name, specification, quantity, sale_price, sale_type, contract_number, expected_delivery_date, input_date) VALUES
('DD20240101001', '张三贸易公司', '不锈钢板材', '304/2mm*1220mm*2440mm', 100, 150.50, '批发', 'HT20240101', '2024-02-01', '2024-01-01'),
('DD20240102001', '李四工业有限公司', '铝合金型材', '6061-T6/50mm*50mm', 200, 85.00, '批发', 'HT20240102', '2024-02-15', '2024-01-02'),
('DD20240103001', '王五进出口公司', '铜管', 'TP2/Φ10mm*1mm', 500, 45.80, '零售', 'HT20240103', '2024-01-30', '2024-01-03');

-- 示例合同文件数据
INSERT INTO contract_files (contract_number, file_name, file_path) VALUES
('HT20240101', '张三贸易合同.pdf', '/uploads/contracts/ht20240101.pdf'),
('HT20240102', '李四工业合同.pdf', '/uploads/contracts/ht20240102.pdf'),
('HT20240103', '王五进出口合同.pdf', '/uploads/contracts/ht20240103.pdf');

-- 创建视图：订单状态视图
CREATE VIEW order_status_view AS
SELECT
    order_id,
    order_number,
    customer_name,
    CASE
        WHEN audit_date IS NULL THEN '待审核'
        WHEN production_date IS NULL THEN '待生产'
        WHEN delivery_date IS NULL THEN '待交货'
        WHEN delivery_date IS NOT NULL THEN '已完成'
        ELSE '未知状态'
    END as order_status,
    input_date,
    audit_date,
    production_date,
    delivery_date
FROM orders;

-- 创建视图：客户统计视图
CREATE VIEW customer_statistics_view AS
SELECT
    c.customer_id,
    c.customer_name,
    c.order_frequency,
    c.total_orders,
    c.total_amount,
    COUNT(o.order_id) as actual_order_count,
    COALESCE(SUM(o.quantity * o.sale_price), 0) as actual_total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_name = o.customer_name
GROUP BY c.customer_id, c.customer_name, c.order_frequency, c.total_orders, c.total_amount;

-- 显示创建成功信息
SELECT '数据库创建完成！' as message;