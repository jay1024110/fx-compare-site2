from src.models.user import db
from datetime import datetime

class HistoricalRate(db.Model):
    """历史汇率数据模型"""
    __tablename__ = 'historical_rates'
    
    id = db.Column(db.Integer, primary_key=True)
    currency_pair = db.Column(db.String(10), nullable=False)  # 如 CNY/USD
    date = db.Column(db.Date, nullable=False)
    
    # OHLC数据 (开盘、最高、最低、收盘)
    open_rate = db.Column(db.Float, nullable=False)
    high_rate = db.Column(db.Float, nullable=False)
    low_rate = db.Column(db.Float, nullable=False)
    close_rate = db.Column(db.Float, nullable=False)
    
    # 交易量 (可选)
    volume = db.Column(db.Integer, default=0)
    
    # 数据来源和备注
    source = db.Column(db.String(100), default='system')  # 数据来源
    notes = db.Column(db.Text, default='')                # 备注信息
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 创建复合索引以提高查询性能
    __table_args__ = (
        db.Index('idx_currency_pair_date', 'currency_pair', 'date'),
    )
    
    def __repr__(self):
        return f'<HistoricalRate {self.currency_pair} - {self.date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'currency_pair': self.currency_pair,
            'date': self.date.isoformat() if self.date else None,
            'open_rate': self.open_rate,
            'high_rate': self.high_rate,
            'low_rate': self.low_rate,
            'close_rate': self.close_rate,
            'volume': self.volume,
            'source': self.source,
            'notes': self.notes
        }
    
    def to_candlestick_data(self):
        """转换为K线图数据格式"""
        return {
            'x': self.date.isoformat(),
            'o': self.open_rate,
            'h': self.high_rate,
            'l': self.low_rate,
            'c': self.close_rate,
            'v': self.volume
        }
    
    @classmethod
    def get_currency_pairs(cls):
        """获取所有可用的货币对"""
        pairs = db.session.query(cls.currency_pair).distinct().all()
        return [pair[0] for pair in pairs]
    
    @classmethod
    def get_latest_rate(cls, currency_pair):
        """获取指定货币对的最新汇率"""
        return cls.query.filter_by(currency_pair=currency_pair)\
                      .order_by(cls.date.desc())\
                      .first()
    
    @classmethod
    def get_rate_range(cls, currency_pair, start_date, end_date, limit=None):
        """获取指定时间范围内的汇率数据"""
        query = cls.query.filter(
            cls.currency_pair == currency_pair,
            cls.date >= start_date,
            cls.date <= end_date
        ).order_by(cls.date.asc())
        
        if limit:
            query = query.limit(limit)
            
        return query.all()

