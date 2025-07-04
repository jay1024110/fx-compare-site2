from src.models.user import db
from datetime import datetime

class FeeConfig(db.Model):
    """手续费配置模型"""
    __tablename__ = 'fee_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)  # 移除外键约束
    currency_pair = db.Column(db.String(10), nullable=False)  # 如 USD/CNY
    
    # 手续费配置
    fixed_fee_from = db.Column(db.Float, default=0.0)  # 汇出货币固定手续费
    fixed_fee_to = db.Column(db.Float, default=0.0)    # 汇入货币固定手续费
    percentage_fee = db.Column(db.Float, default=0.0)  # 百分比手续费 (0.01 = 1%)
    min_fee = db.Column(db.Float, default=0.0)         # 最低手续费
    max_fee = db.Column(db.Float, default=0.0)         # 最高手续费 (0表示无上限)
    
    # 其他配置
    min_amount = db.Column(db.Float, default=0.0)      # 最低汇款金额
    max_amount = db.Column(db.Float, default=0.0)      # 最高汇款金额 (0表示无上限)
    
    # 新增字段
    notes = db.Column(db.Text, default='')             # 备注信息
    is_active = db.Column(db.Boolean, default=True)    # 是否启用
    created_by = db.Column(db.String(100), default='system')  # 创建者
    updated_by = db.Column(db.String(100), default='system')  # 最后修改者
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<FeeConfig Company{self.company_id} - {self.currency_pair}>'
    
    def calculate_fee(self, amount):
        """计算手续费"""
        if not self.is_active:
            return 0.0
            
        # 百分比手续费
        percentage_fee = amount * self.percentage_fee
        
        # 总手续费 = 固定手续费 + 百分比手续费
        total_fee = self.fixed_fee_from + percentage_fee
        
        # 应用最低和最高手续费限制
        if self.min_fee > 0:
            total_fee = max(total_fee, self.min_fee)
        if self.max_fee > 0:
            total_fee = min(total_fee, self.max_fee)
            
        return round(total_fee, 2)
    
    def calculate_received_amount(self, amount, exchange_rate):
        """计算到账金额"""
        if not self.is_active:
            return 0.0
            
        # 扣除汇出货币手续费后的金额
        amount_after_fee = amount - self.calculate_fee(amount)
        
        # 按汇率转换
        converted_amount = amount_after_fee * exchange_rate
        
        # 扣除汇入货币固定手续费
        final_amount = converted_amount - self.fixed_fee_to
        
        return round(max(final_amount, 0), 2)
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'currency_pair': self.currency_pair,
            'fixed_fee_from': self.fixed_fee_from,
            'fixed_fee_to': self.fixed_fee_to,
            'percentage_fee': self.percentage_fee,
            'min_fee': self.min_fee,
            'max_fee': self.max_fee,
            'min_amount': self.min_amount,
            'max_amount': self.max_amount,
            'notes': self.notes,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

