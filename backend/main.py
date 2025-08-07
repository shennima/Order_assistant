"""
交互式订单创建程序
允许用户手动输入订单信息
"""
from backend.models import create_tables, SessionLocal
from backend.database import create_order, get_order_by_number
from datetime import datetime

def validate_date(date_str):
    """验证日期格式是否正确"""
    if not date_str:
        return None
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        return None

def get_user_input(prompt, required=False, validator=None):
    """获取用户输入并进行验证"""
    while True:
        value = input(prompt).strip()
        if not value and not required:
            return None
        if not value and required:
            print("此字段为必填项，请重新输入。")
            continue
        if validator and not validator(value):
            print("输入格式不正确，请重新输入。")
            continue
        return value

def create_order_interactively():
    """交互式创建订单"""
    print("=== 订单创建系统 ===")
    print("请按照提示输入订单信息：")

    # 获取数据库会话
    db = SessionLocal()

    try:
        # 收集订单信息
        order_data = {}

        # 必填字段
        order_data['order_number'] = get_user_input("订单号 (必填): ", required=True)

        # 检查订单号是否已存在
        existing_order = get_order_by_number(db, order_data['order_number'])
        if existing_order:
            print(f"错误：订单号 '{order_data['order_number']}' 已存在，请使用不同的订单号。")
            return

        order_data['customer_name'] = get_user_input("客户名称 (必填): ", required=True)
        order_data['product_name'] = get_user_input("产品名称 (必填): ", required=True)
        order_data['quantity'] = float(get_user_input("数量 (必填): ", required=True))
        order_data['sale_price'] = float(get_user_input("销售价格 (必填): ", required=True))

        # 可选字段
        order_data['specification'] = get_user_input("规格: ")
        order_data['sale_type'] = get_user_input("销售类型: ")
        order_data['contract_number'] = get_user_input("合同号: ")

        # 日期字段
        date_fields = [
            ('expected_delivery_date', '预计交货日期 (YYYY-MM-DD): '),
            ('input_date', '录入日期 (YYYY-MM-DD): '),
            ('audit_date', '审核日期 (YYYY-MM-DD): '),
            ('production_date', '生产日期 (YYYY-MM-DD): '),
            ('delivery_date', '实际交货日期 (YYYY-MM-DD): ')
        ]

        for field, prompt in date_fields:
            date_value = get_user_input(prompt)
            if date_value and validate_date(date_value):
                order_data[field] = date_value
            elif date_value:
                print(f"日期格式不正确，将跳过 {field} 字段。")

        # 其他可选字段
        order_data['finished_weight'] = get_user_input("成品重量: ")
        if order_data['finished_weight']:
            order_data['finished_weight'] = float(order_data['finished_weight'])

        order_data['transport_method'] = get_user_input("运输方式: ")
        order_data['destination'] = get_user_input("目的地: ")
        order_data['payment_method'] = get_user_input("付款方式: ")
        order_data['remark'] = get_user_input("备注: ")

        # 创建订单
        new_order = create_order(db, order_data)
        print(f"\n订单创建成功！")
        print(f"订单ID: {new_order.id}")
        print(f"订单号: {new_order.order_number}")
        print(f"创建时间: {new_order.created_at}")

    except ValueError as ve:
        print(f"输入数据有误: {ve}")
    except Exception as e:
        print(f"创建订单时出错: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """主函数"""
    create_tables()  # 确保表已创建
    while True:
        create_order_interactively()
        continue_choice = input("\n是否继续创建订单？(y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes', '是']:
            break
    print("感谢使用订单创建系统！")

if __name__ == "__main__":
    main()
