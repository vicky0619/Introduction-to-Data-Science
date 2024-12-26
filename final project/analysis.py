import pandas as pd
import pickle
import os

# 載入模型和數據
model_path = "xgboost_recommendation_model.pkl"
recipes_path = "processed_recipes.csv"
food_data_path = "cleaned_food_data.csv"
cleaned_food_data = pd.read_csv(food_data_path)

if os.path.exists(model_path) and os.path.exists(recipes_path):
    with open(model_path, 'rb') as f:
        xgboost_model = pickle.load(f)
    recipes_df = pd.read_csv(recipes_path)
else:
    raise FileNotFoundError("模型或推薦菜餚數據檔案未找到！")

base_dri = {
    'Calories': 2000,
    'Protein': 50,
    'Fats': 70,
    'Carbs': 300,
    'Fiber': 25,
    'Sugar': 50
}

# 計算 BMR
def calculate_bmr(weight, height, age, gender):
    if gender == "男":
        return (13.7 * weight) + (5.0 * height) - (6.8 * age) + 66
    else:
        return (9.6 * weight) + (1.8 * height) - (4.7 * age) + 655

# 計算 TDEE
def calculate_tdee(bmr, activity_level):
    activity_factor = {
        "無活動（久坐）": 1.2,
        "輕量活動（每周運動1-3天）": 1.375,
        "中度活動量（每周運動3-5天）": 1.55,
        "高度活動量（每周運動6-7天）": 1.725,
        "非常高度活動量（勞力型工作）": 1.9
    }
    return bmr * activity_factor.get(activity_level, 1.2)

# 生成健康建議
def generate_optimized_suggestions(input_foods, tdee, health_goal):
    # 調整後的每日推薦攝取量 (DRI)
    goal_factor = {'weight_loss': 0.8, 'maintain': 1.0, 'muscle_gain': 1.2}
    
    adjusted_dri = {k: v * (tdee / 2000) * goal_factor[health_goal] for k, v in base_dri.items()}
    
    # 計算營養結果
    total_nutrition = calculate_total_nutrition(input_foods)

    # 比較攝取量與 DRI，生成建議
    recommendations = {}
    for nutrient, value in total_nutrition.items():
        if value > adjusted_dri[nutrient]:
            recommendations[nutrient] = f"Your {nutrient} intake is too high ({value:.1f} vs {adjusted_dri[nutrient]:.1f})."
        elif value < adjusted_dri[nutrient]:
            recommendations[nutrient] = f"Your {nutrient} intake is too low ({value:.1f} vs {adjusted_dri[nutrient]:.1f})."
        else:
            recommendations[nutrient] = f"Your {nutrient} intake is within the recommended range ({value:.1f})."

    return recommendations

def calculate_total_nutrition(input_foods):
    # 查找並合併營養數據
    food_nutrition = []
    for food in input_foods:
        # 從 cleaned_food_data 中查找 Food Name
        food_info = cleaned_food_data[cleaned_food_data['Food Name'] == food['Food Name']]

        if not food_info.empty:
            food_info = food_info.iloc[0]  # 取出匹配的第一行數據
            quantity = food['Quantity']  # 使用 input_foods 中的 Quantity(g)
            food_nutrition.append({
                "Food Name": food['Food Name'],
                "Calories": food_info['Calories'] * quantity / 100,
                "Protein": food_info['Protein'] * quantity / 100,
                "Fats": food_info['Fats'] * quantity / 100,
                "Fiber": food_info['Fiber'] * quantity / 100,
                "Carbs": food_info['Carbs'] * quantity / 100,
                "Sugar": food_info['Sugar'] * quantity / 100
            })

    # 計算總營養
    total_nutrition = {"Calories": 0, "Protein": 0, "Fiber": 0, "Fats": 0, "Carbs": 0, "Sugar": 0}

    for food in food_nutrition:
        total_nutrition["Calories"] += food["Calories"]
        total_nutrition["Protein"] += food["Protein"]
        total_nutrition["Fats"] += food["Fats"]
        total_nutrition["Fiber"] += food["Fiber"]
        total_nutrition["Carbs"] += food["Carbs"]
        total_nutrition["Sugar"] += food["Sugar"]

    return total_nutrition


def calculate_recom_nutrition(eat_total, tdee, health_goal):
    goal_factor = {'weight_loss': 0.8, 'maintain': 1.0, 'muscle_gain': 1.2}

    total_dri = {k: v * (tdee / 2000) * goal_factor[health_goal] for k, v in base_dri.items()}
    
    recom_nutrition = {"Calories": 0, "Protein": 0, "Fiber": 0, "Fats": 0, "Carbs": 0, "Sugar": 0}

    recom_nutrition["Calories"] = total_dri["Calories"] - eat_total["Calories"]
    recom_nutrition["Protein"] = total_dri["Protein"] - eat_total["Protein"]
    recom_nutrition["Fats"] = total_dri["Fats"] - eat_total["Fats"]
    recom_nutrition["Fiber"] = total_dri["Fiber"] - eat_total["Fiber"]
    recom_nutrition["Carbs"] = total_dri["Carbs"] - eat_total["Carbs"]
    recom_nutrition["Sugar"] = total_dri["Sugar"] - eat_total["Sugar"]

    return recom_nutrition