import pandas as pd
import matplotlib.pyplot as plt

# 加載清理後的數據集
try:
    df_selected = pd.read_csv("/Users/vickyt/Desktop/University/大三/資料科學導論/final project/cleaned_food_data.csv")
    # 確保所有列名一致
    df_selected.columns = df_selected.columns.str.strip()
except FileNotFoundError:
    raise FileNotFoundError("Could not find the 'cleaned_food_data.csv' file.")

# 基本參數
base_dri = {
    'Calories': 2000,
    'Protein': 50,
    'Fats': 70,
    'Carbs': 300,
    'Fiber': 25,
    'Sugar': 50
}

goal_factor = {'weight_loss': 0.8, 'maintain': 1.0, 'muscle_gain': 1.2}
# 活動水平對應轉換字典
activity_mapping = {
    "無活動（久坐）": "sedentary",
    "輕量活動（每周運動1-3天）": "light",
    "中度活動量（每周運動3-5天）": "moderate",
    "高度活動量（每周運動6-7天）": "active",
    "非常高度活動量（勞力型工作）": "very_active"
}

# 活動水平對應的 TDEE 係數
activity_factor = {
    "sedentary": 1.2,      # 無活動（久坐）
    "light": 1.375,        # 輕量活動
    "moderate": 1.55,      # 中度活動
    "active": 1.725,       # 高度活動
    "very_active": 1.9     # 非常高度活動
}



# 計算 BMR
def calculate_bmr(weight, height, age, gender):
    if gender == "男":
        return (13.7 * weight) + (5.0 * height) - (6.8 * age) + 66
    else:  # 女
        return (9.6 * weight) + (1.8 * height) - (4.7 * age) + 655


# 計算 TDEE
def calculate_tdee(bmr, activity_level):
    activity_level = activity_mapping[activity_level]  # 轉換活動水平
    return bmr * activity_factor[activity_level]


# 生成健康建議（基於 TDEE）
def generate_optimized_suggestions(input_foods, tdee, health_goal):
    # 根據 TDEE 和健康目標調整 DRI
    adjusted_dri = {nutrient: base_dri[nutrient] * (tdee / 2000) * goal_factor[health_goal]
                    for nutrient in base_dri}

    # 確保列名一致
    if 'Food' in input_foods:
        input_foods['Food Name'] = input_foods.pop('Food')

    user_data = pd.DataFrame(input_foods)

    # 合併數據
    try:
        merged_data = user_data.merge(df_selected, on='Food Name', how='left')
    except KeyError:
        raise KeyError("Column 'Food Name' not found in dataset or input data.")

    # 計算營養攝取總量
    for col in ['Calories', 'Protein', 'Fats', 'Carbs', 'Fiber', 'Sugar']:
        merged_data[col] = merged_data[col] * merged_data['Quantity'] / 100

    total_nutrition = merged_data[['Calories', 'Protein', 'Fats', 'Carbs', 'Fiber', 'Sugar']].sum()

    # 比較用戶攝取量與調整後的 DRI 值
    suggestions = {}
    for nutrient, dri_value in adjusted_dri.items():
        intake = total_nutrition[nutrient]
        if intake > dri_value:
            suggestions[nutrient] = f"Your {nutrient} intake is too high ({intake:.1f} vs {dri_value:.1f}). Reduce foods like Bread, Apple, Chicken Breast."
        elif intake < dri_value * 0.8:
            suggestions[nutrient] = f"Your {nutrient} intake is too low ({intake:.1f} vs {dri_value:.1f}). Increase foods like Chicken Breast, Bread, Apple."
        else:
            suggestions[nutrient] = f"Your {nutrient} intake is within the recommended range ({intake:.1f} vs {dri_value:.1f})."

    return suggestions

def plot_nutrition_trends(data):
    """
    繪製營養攝取趨勢圖
    :param data: pandas DataFrame，包含用戶的營養數據
    """
    data["date"] = pd.to_datetime(data["date"])
    data.set_index("date", inplace=True)

    # 繪製每種營養素的趨勢
    data[["calories", "protein", "fats", "carbs"]].plot(figsize=(10, 6))
    plt.title("營養攝取趨勢")
    plt.xlabel("日期")
    plt.ylabel("攝取量")
    plt.legend(["卡路里", "蛋白質", "脂肪", "碳水化合物"])
    plt.grid(True)
    plt.show()