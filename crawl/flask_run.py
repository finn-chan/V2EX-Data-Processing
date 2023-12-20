import json

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/receive_cookies', methods=['POST'])
def receive_cookies():
    data = request.get_json()
    cookies = data.get('cookies')
    if cookies:
        print("Received cookies:", cookies)
        # 更新config.json文件
        try:
            with open('../config.json', 'r+') as file:
                config = json.load(file)
                config['cookie'] = cookies
                file.seek(0)  # 重置文件指针到文件开头
                json.dump(config, file, indent=4)
                file.truncate()  # 删除文件指针后的内容
            return jsonify({"message": "Cookies received and updated"}), 200
        except Exception as e:
            print(f"Error updating config.json: {e}")
            return jsonify({"message": "Failed to update cookies in config.json"}), 500
    else:
        return jsonify({"message": "No cookies received"}), 400


def run():
    app.run(debug=True, port=5000)  # 运行在5000端口
