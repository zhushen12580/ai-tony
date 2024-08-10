from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 启用CORS以允许从不同域的前端发送请求

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Zhushen@01@120.79.81.153/ai_tony'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义模型
class WaitlistEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<WaitlistEmail {self.email}>'

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-email', methods=['POST'])
def submit_email():
    data = request.json
    email = data.get('email')
    
    if email:
        try:
            new_email = WaitlistEmail(email=email)
            db.session.add(new_email)
            db.session.commit()
            return jsonify({"message": "邮箱地址已成功添加到等候名单"}), 200
        except Exception as e:
            db.session.rollback()
            if 'Duplicate entry' in str(e):
                return jsonify({"error": "该邮箱地址已经在等候名单中"}), 400
            else:
                return jsonify({"error": "添加邮箱地址时发生错误"}), 500
    else:
        return jsonify({"error": "未提供有效的邮箱地址"}), 400
        
if __name__ == '__main__':
    app.run(debug=True)
