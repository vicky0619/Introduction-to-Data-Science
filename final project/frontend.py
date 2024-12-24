import os
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(
    page_title="Health and Nutrition Recommendation System",
    page_icon="🔥",
    layout="centered"
)

# 設置應用標題
st.title("🔥 健康飲食推薦與熱量計算")

# 初始化 session_state
if "bmr" not in st.session_state:
    st.session_state.bmr = None
if "tdee" not in st.session_state:
    st.session_state.tdee = None

# 計算 BMR 和 TDEE
st.header("📋 計算 BMR 和 TDEE")
gender = st.selectbox("性別:", ["男", "女"])
age = st.number_input("年齡:", min_value=1, max_value=120, value=25, step=1)
weight = st.number_input("體重（公斤）:", min_value=20.0, max_value=300.0, value=70.0, step=0.1)
height = st.number_input("身高（公分）:", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
activity_level = st.selectbox(
    "活動水平:",
    ["無活動（久坐）", "輕量活動（每周運動1-3天）", "中度活動量（每周運動3-5天）", "高度活動量（每周運動6-7天）", "非常高度活動量（勞力型工作）"]
)

if st.button("💡 計算 BMR 和 TDEE"):
    response = requests.post(
        "http://127.0.0.1:8080/calculate",
        json={"weight": weight, "height": height, "age": age, "gender": gender, "activity": activity_level}
    )
    if response.status_code == 200:
        result = response.json()
        st.session_state.bmr = result["BMR"]
        st.session_state.tdee = result["TDEE"]
        st.success(f"BMR: {result['BMR']:.1f}, TDEE: {result['TDEE']:.1f}")
    else:
        st.error("計算出錯！")

# 顯示 BMR 和 TDEE 結果（如果已計算）
if st.session_state.bmr and st.session_state.tdee:
    st.info(f"💡 **BMR:** {st.session_state.bmr:.1f} kcal/day, **TDEE:** {st.session_state.tdee:.1f} kcal/day")

# 修改的標題
st.header("🍴 輸入您的飲食內容")

# 新增日期欄位，預設為今天日期
date = st.date_input("日期:", value=datetime.today().date())

food_names = st.text_input("食物名稱（以逗號分隔）:", placeholder="例如：Apple, Chicken Breast")
quantities = st.text_input("食物數量（以逗號分隔，單位為克）:", placeholder="例如：150, 200")

# ✅新增輸入按鈕
if st.button("✅輸入"):
    try:
        # 加載合法食物名稱
        cleaned_data_path = "cleaned_food_data.csv"
        if not os.path.exists(cleaned_data_path):
            st.error("系統無法找到基礎食品數據庫！請聯繫管理員。")
        else:
            valid_foods = pd.read_csv(cleaned_data_path)['Food Name'].str.strip().tolist()

        # 獲取輸入數據
        input_date = str(date)  # 日期
        input_food_names = [name.strip() for name in food_names.split(",")]  # 食物名稱列表
        input_quantities = [qty.strip() for qty in quantities.split(",")]  # 食物數量列表

        # 檢查食物名稱是否合法
        invalid_foods = [name for name in input_food_names if name not in valid_foods]

        if invalid_foods:
            st.error(f"以下食物無法識別，請檢查後重新輸入: {', '.join(invalid_foods)}")
        else:
            # 構建輸入數據的 DataFrame
            new_data = pd.DataFrame({
                "Date": [input_date] * len(input_food_names),
                "Food Name": input_food_names,
                "Quantity": [int(qty) for qty in input_quantities]
            })

            # 定義 CSV 文件路徑
            csv_file_path = "user_food_log.csv"

            # 檢查 CSV 是否存在
            if not os.path.exists(csv_file_path):
                new_data.to_csv(csv_file_path, index=False)
            else:
                new_data.to_csv(csv_file_path, mode='a', header=False, index=False)

            st.success("已成功保存輸入的飲食記錄！")
    except Exception as e:
        st.error(f"保存飲食記錄時發生錯誤: {e}")

# 新增「輸入分析日期」欄位及標題
st.subheader("🍴 輸入您要進行分析飲食內容的日期")
analysis_date = st.date_input("選擇分析日期:", value=datetime.today().date())

# 健康目標部分
goal = st.selectbox("健康目標:", ["weight_loss", "maintain", "muscle_gain"])

# 生成健康建議按鈕
if st.button("📊 生成健康建議"):
    if st.session_state.tdee:
        response = requests.post(
            "http://127.0.0.1:8080/recommendation",
            json={"analysis_date": str(analysis_date), "tdee": st.session_state.tdee, "goal": goal}
        )
        if response.status_code == 200:
            result = response.json()
            recommendations = result["recommendations"]
            suggested_recipes = result.get("recommended_recipes", [])

            # 顯示健康建議
            st.markdown("### 🥗 個性化健康建議")
            for nutrient, suggestion in recommendations.items():
                if "too high" in suggestion:
                    st.error(f"🔴 **{nutrient}:** {suggestion}")
                elif "too low" in suggestion:
                    st.warning(f"🟡 **{nutrient}:** {suggestion}")
                else:
                    st.success(f"🟢 **{nutrient}:** {suggestion}")

            # 顯示推薦菜餚
            st.markdown("### 🍽️ 推薦菜餚")
            if suggested_recipes:
                for index, recipe in enumerate(suggested_recipes):
                    st.markdown(
                        f"""
                        **Top {index + 1} 推薦：**  
                        **{recipe['name']}**  
                        食譜網址： [點擊這裡]({recipe['url']})
                        """,
                        unsafe_allow_html=True
                    )
                    st.image(recipe['image_url'])

            else:
                st.warning("未找到推薦的菜餚。")
        else:
            st.error("生成健康建議出錯！！" + response.text)
    else:
        st.error("請先計算 BMR 和 TDEE！")
