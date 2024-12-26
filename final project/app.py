from flask import Flask, request, jsonify
import pandas as pd
import os
import pickle
from analysis import calculate_bmr, calculate_tdee, generate_optimized_suggestions,calculate_total_nutrition , calculate_recom_nutrition
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from IPython.display import Image, display, HTML

app = Flask(__name__)

# 加載推薦模型和菜餚數據
model_path = "xgboost_recommendation_model.pkl"
recipes_path = "processed_recipes.csv"

# 進行特徵縮放 (使用已經 fit 過的 scaler)
scaler = MinMaxScaler()

# 檢查模型與資料檔案
if os.path.exists(model_path) and os.path.exists(recipes_path):
    with open(model_path, 'rb') as f:
        xgboost_model = pickle.load(f)
    recipes_df = pd.read_csv(recipes_path)

    recipes_df = recipes_df.drop_duplicates(subset='name', keep='first')
    features = ['Calories_Kcal', 'Carbs_g', 'Fats_g', 'Fiber_g', 'Protein_g', 'Sugars_g']
    X = recipes_df[features]
    X_scaled = scaler.fit_transform(X)
    all_scores = xgboost_model.predict(X_scaled)  # 預測所有餐點分數

else:
    raise FileNotFoundError("模型或推薦菜餚數據檔案未找到！")

# 路由：計算 BMR 和 TDEE
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


def recommend_recipes(nutrient_needs):
    # 準備模型輸入，將 nutrient_needs 轉換為 np.array
    input_features = np.array([[  # 確保順序與模型訓練時相同
        nutrient_needs["Calories"],   # 熱量
        nutrient_needs["Carbs"],      # 碳水化合物
        nutrient_needs["Fats"],       # 脂肪
        nutrient_needs["Fiber"],      # 纖維
        nutrient_needs["Protein"],    # 蛋白質
        nutrient_needs["Sugar"]       # 糖分
    ]])

    input_scaled = scaler.transform(input_features)

    # 計算與使用者輸入的相似度分數
    similarity_scores = abs(xgboost_model.predict(input_scaled) - all_scores)

    # 將分數加入到數據集中
    # 確保 'match_score' 欄位不存在
    if 'match_score' in recipes_df.columns:
        recipes_df.drop(columns=['match_score'], inplace=True)

    # 新增 'match_score' 欄位
    recipes_df['match_score'] = similarity_scores

    # 找出匹配度最高的 Top 5 菜餚
    top_5 = recipes_df.nsmallest(5, "match_score")


    # 輸出推薦結果：名稱、圖片和超連結
    recommended_recipes = []

    for index, row in top_5.iterrows():
        recipe_info = {
            "name": row['name'],        # 菜餚名稱
            "image_url": row['img_src'],  # 菜餚圖片 URL
            "url": row['url'],           # 完整食譜超連結
            # "match_score": row['match_score'],           # 完整食譜超連結
            # "nutrient_needs": nutrient_needs
        }
        recommended_recipes.append(recipe_info)

    # 使用 IPython display 輸出推薦結果
    # print("推薦的 Top 5 菜餚：")
    # for recipe in recommended_recipes:
    #     display(HTML(f"<h3>{recipe['name']}</h3>"))   # 顯示菜餚名稱
    #     display(Image(url=recipe['image_url'], width=300))  # 顯示圖片
    #     display(HTML(f"<a href='{recipe['url']}' target='_blank'>查看完整食譜</a>"))  # 超連結

    return recommended_recipes



# 路由：生成健康建議和推薦菜餚
@app.route('/recommendation', methods=['POST'])
def recommendation():
    try:
        data = request.json
        analysis_date = data['analysis_date']
        tdee = data['tdee']
        goal = data['goal']

        # 加載 CSV 文件中的數據
        csv_file_path = "user_food_log.csv"
        if not os.path.exists(csv_file_path):
            return jsonify({"error": "No food log data found."}), 400

        # 讀取用戶輸入的飲食日誌
        food_log = pd.read_csv(csv_file_path)
        food_log['Date'] = pd.to_datetime(food_log['Date'])
        analysis_date = pd.to_datetime(analysis_date)

        # 篩選指定日期的數據
        filtered_data = food_log[food_log['Date'] == analysis_date]

        if filtered_data.empty:
            return jsonify({"error": f"No data found for the date {analysis_date.date()}."}), 404

        # 格式化數據為函數所需結構
        input_foods = filtered_data[['Food Name', 'Quantity']].to_dict(orient='records')

        # 生成健康建議
        recommendations = generate_optimized_suggestions(input_foods, tdee, goal)

        # 根據需求推薦菜餚
        
        total_nutrients = calculate_total_nutrition(input_foods)
        recom_total = calculate_recom_nutrition(total_nutrients, tdee, goal)
        # recom_total = {"Calories": 0, "Protein": 0, "Carbs": 0, "Fiber": 0, "Fats": 0, "Sugar":0}
        recommended_recipes = recommend_recipes(recom_total)

        return jsonify({
            "recommendations": recommendations,
            "recommended_recipes": recommended_recipes
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)
