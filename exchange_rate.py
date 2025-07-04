from src.models.user import db
from datetime import datetime

class Company(db.Model):
    """换汇公司模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200))
    contact = db.Column(db.String(100))
    
    # 新增字段
    notes = db.Column(db.Text, default='')              # 备注信息
    contact_info = db.Column(db.Text, default='')       # 详细联系信息
    business_hours = db.Column(db.String(200), default='') # 营业时间
    is_active = db.Column(db.Boolean, default=True)     # 是否启用
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联汇率数据
    exchange_rates = db.relationship('ExchangeRate', backref='company', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Company {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
            'contact': self.contact,
            'notes': self.notes,
            'contact_info': self.contact_info,
            'business_hours': self.business_hours,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ExchangeRate(db.Model):
    """汇率数据模型"""
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    currency_pair = db.Column(db.String(10), nullable=False)  # 例如: USD/CNY
    buy_rate = db.Column(db.Float, nullable=False)  # 买入价
    sell_rate = db.Column(db.Float, nullable=False)  # 卖出价
    
    # 新增字段
    notes = db.Column(db.Text, default='')              # 备注信息
    is_active = db.Column(db.Boolean, default=True)     # 是否启用
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ExchangeRate {self.currency_pair} - {self.company.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'company_id': self.company_id,
            'company_name': self.company.name if self.company else None,
            'currency_pair': self.currency_pair,
            'buy_rate': self.buy_rate,
            'sell_rate': self.sell_rate,
            'notes': self.notes,
            'is_active': self.is_active,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

