import os
import sys
# DON'T CHANGE THIS LINE
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.exchange_rate import Company, ExchangeRate
from src.routes.user import user_bp
from src.routes.exchange_rate import exchange_rate_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# 启用CORS支持
CORS(app, origins="*")

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(exchange_rate_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exchange_rate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 在应用上下文中导入所有模型以确保表创建
with app.app_context():
    # 导入所有模型
    from src.models.fee_config import FeeConfig
    from src.models.historical_rate import HistoricalRate
    db.create_all()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

