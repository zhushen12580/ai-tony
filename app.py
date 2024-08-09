from flask import Flask, request, jsonify,render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用CORS以允许从不同域的前端发送请求

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-email', methods=['GET','POST'])
def submit_email():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        
        if email:
            # 将邮箱地址保存到文本文件
            with open('waitlist_emails.txt', 'a') as f:
                f.write(email + '\n')
            return jsonify({"message": "邮箱地址已成功添加到等候名单"}), 200
        else:
            return jsonify({"error": "未提供有效的邮箱地址"}), 400
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)