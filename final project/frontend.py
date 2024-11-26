import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

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

# 輸入飲食內容
st.header("🍴 輸入您的飲食內容進行分析")
food_names = st.text_input("食物名稱（以逗號分隔）:", placeholder="例如：Apple, Chicken Breast")
quantities = st.text_input("食物數量（以逗號分隔，單位為克）:", placeholder="例如：150, 200")
goal = st.selectbox("健康目標:", ["weight_loss", "maintain", "muscle_gain"])

if st.button("📊 生成健康建議"):
    if st.session_state.tdee:  # 確保 TDEE 已計算
        food_list = [{"Food Name": name.strip(), "Quantity": int(qty.strip())} for name, qty in zip(food_names.split(","), quantities.split(","))]
        response = requests.post(
            "http://127.0.0.1:8080/recommendation",
            json={"foods": food_list, "goal": goal, "tdee": st.session_state.tdee}
        )
        if response.status_code == 200:
            result = response.json()
            recommendations = result["recommendations"]

            # 顯示健康建議
            st.markdown("### 🥗 個性化健康建議")
            for nutrient, suggestion in recommendations.items():
                if "too high" in suggestion:
                    st.error(f"🔴 **{nutrient}:** {suggestion}")
                elif "too low" in suggestion:
                    st.warning(f"🟡 **{nutrient}:** {suggestion}")
                else:
                    st.success(f"🟢 **{nutrient}:** {suggestion}")

            # 繪製條形圖
            nutrient_labels = []
            nutrient_values = []
            nutrient_colors = []

            for nutrient, suggestion in recommendations.items():
                if "too high" in suggestion:
                    nutrient_labels.append(nutrient)
                    nutrient_values.append(-1)  # 過高為負數
                    nutrient_colors.append("red")
                elif "too low" in suggestion:
                    nutrient_labels.append(nutrient)
                    nutrient_values.append(1)  # 過低為正數
                    nutrient_colors.append("orange")
                else:
                    nutrient_labels.append(nutrient)
                    nutrient_values.append(0)  # 正常為 0
                    nutrient_colors.append("green")

            fig, ax = plt.subplots(figsize=(8, 5))
            bars = ax.barh(nutrient_labels, nutrient_values, color=nutrient_colors)
            ax.set_xlabel("Recommendation Status")
            ax.set_ylabel("Nutrients")
            ax.set_title("Nutrient Recommendation Overview")
            ax.set_xlim(-1.5, 1.5)
            ax.set_xticks([-1, 0, 1])
            ax.set_xticklabels(["Too High", "Optimal", "Too Low"])
            st.pyplot(fig)

        else:
            st.error("生成健康建議出錯！")
    else:
        st.error("請先計算 BMR 和 TDEE！")
