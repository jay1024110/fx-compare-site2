#!/usr/bin/env python3
"""
初始化数据库并添加示例数据
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from src.models.user import db
from src.models.exchange_rate import Company, ExchangeRate
from src.main import app

def init_sample_data():
    """初始化示例数据"""
    with app.app_context():
        # 清空现有数据
        ExchangeRate.query.delete()
        Company.query.delete()
        
        # 创建示例公司
        companies = [
            Company(name="中国银行", website="https://www.boc.cn", contact="95566"),
            Company(name="工商银行", website="https://www.icbc.com.cn", contact="95588"),
            Company(name="建设银行", website="https://www.ccb.com", contact="95533"),
            Company(name="招商银行", website="https://www.cmbchina.com", contact="95555"),
            Company(name="中信银行", website="https://www.citicbank.com", contact="95558")
        ]
        
        for company in companies:
            db.session.add(company)
        
        db.session.commit()
        
        # 创建示例汇率数据
        currency_pairs = ["USD/CNY", "EUR/CNY", "JPY/CNY", "GBP/CNY", "HKD/CNY"]
        base_rates = {
            "USD/CNY": {"buy": 7.25, "sell": 7.30},
            "EUR/CNY": {"buy": 7.85, "sell": 7.92},
            "JPY/CNY": {"buy": 0.048, "sell": 0.052},
            "GBP/CNY": {"buy": 9.15, "sell": 9.25},
            "HKD/CNY": {"buy": 0.92, "sell": 0.95}
        }
        
        for i, company in enumerate(companies):
            for pair in currency_pairs:
                # 为每个公司添加略有不同的汇率
                variation = (i - 2) * 0.01  # -0.02 到 +0.02 的变化
                buy_rate = base_rates[pair]["buy"] + variation
                sell_rate = base_rates[pair]["sell"] + variation
                
                rate = ExchangeRate(
                    company_id=company.id,
                    currency_pair=pair,
                    buy_rate=round(buy_rate, 4),
                    sell_rate=round(sell_rate, 4)
                )
                db.session.add(rate)
        
        db.session.commit()
        print("示例数据初始化完成！")
        
        # 显示创建的数据
        print(f"创建了 {len(companies)} 家公司")
        print(f"创建了 {ExchangeRate.query.count()} 条汇率记录")

if __name__ == "__main__":
    init_sample_data()

