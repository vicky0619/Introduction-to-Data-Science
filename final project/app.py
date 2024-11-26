from flask import Flask, request, jsonify
from analysis import calculate_bmr, calculate_tdee, generate_optimized_suggestions

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        weight = data['weight']
        height = data['height']
        age = data['age']
        gender = data['gender']
        activity_level = data['activity']

        # 計算 BMR 和 TDEE
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity_level)

        return jsonify({"BMR": bmr, "TDEE": tdee})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/recommendation', methods=['POST'])
def recommendation():
    try:
        data = request.json
        print("Received data:", data)  # 打印接收到的數據，檢查格式

        foods = data['foods']
        goal = data['goal']
        tdee = data['tdee']  # 用戶端應該提供 TDEE

        # 生成健康建議
        recommendations = generate_optimized_suggestions(foods, tdee, goal)

        return jsonify({"recommendations": recommendations})
    except Exception as e:
        print("Error occurred:", e)  # 打印錯誤堆棧
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, port=8080)
