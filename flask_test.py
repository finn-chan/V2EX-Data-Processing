from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/receive_cookies', methods=['POST'])
def receive_cookies():
    data = request.get_json()
    cookies = data.get('cookies')
    if cookies:
        print("Received cookies:", cookies)
        return jsonify({"message": "Cookies received"}), 200
    else:
        return jsonify({"message": "No cookies received"}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # 运行在5000端口
