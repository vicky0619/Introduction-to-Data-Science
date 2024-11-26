# 健康與營養建議系統 (Health and Nutrition Recommendation System)

## 中文說明

### 🌟 簡介
健康與營養建議系統是一個基於 BMR 和 TDEE 的飲食健康建議工具，通過用戶輸入的基本信息（性別、年齡、體重、身高、活動水平）計算每日消耗的熱量 (TDEE)，並根據用戶的健康目標（減重、維持體重、增肌）和飲食內容生成個性化的健康建議。

該系統的目的是幫助用戶更好地管理每日營養攝取，實現健康目標。

---

### 🖥️ 功能
1. **BMR 和 TDEE 計算**：  
   根據用戶的輸入計算基礎代謝率 (BMR) 和每日消耗熱量 (TDEE)。  

2. **個性化健康建議生成**：  
   使用 TDEE 和用戶提供的飲食內容，分析用戶的營養攝取是否平衡，並給出具體建議（例如，增加蛋白質或減少碳水化合物攝取）。  

3. **圖表可視化**：  
   系統使用圖表展示用戶的營養攝取狀況，幫助用戶更直觀地了解自己的飲食問題。

---

### 🖼️ 網頁示意圖

1. **TDEE 和 BMR 計算頁面**  
   ![TDEE 和 BMR 計算](https://i.imgur.com/3IGrrV8.png)

2. **飲食建議分析頁面**  
   ![飲食建議分析](https://i.imgur.com/cIgsdfh.png)

---

### 📦 系統架構
- **前端**：使用 [Streamlit](https://streamlit.io) 構建，用戶可以通過瀏覽器輸入數據並查看分析結果。
- **後端**：使用 [Flask](https://flask.palletsprojects.com/) 提供 API，負責計算 TDEE 和生成營養建議。
- **數據集**：來自 Kaggle 的食品營養數據集，經過清理後提供詳細的營養成分信息。

---

### 🔧 安裝與使用

#### 1. 克隆專案
```bash
git clone git clone https://github.com/vicky0619/Introduction-to-Data-Science.git
cd Introduction-to-Data-Science/final\ project
```

#### 2. 安裝依賴
確保已安裝 Python 3.8 或以上版本，然後執行：
```bash
pip install -r requirements.txt
```

#### 3. 啟動後端 Flask API
```bash
python app.py
```

#### 4. 啟動前端 Streamlit 應用
```bash
streamlit run frontend.py
```

#### 5. 打開瀏覽器
在瀏覽器中輸入 `http://localhost:8501`，即可使用本系統。

---

### 貢獻指南

歡迎對本專案進行改進！請按照以下步驟發起 Pull Request：

1. **Fork 專案**：點擊右上角 **Fork**，並將專案克隆到您的本地環境。
   ```bash
   git clone https://github.com/your-username/Introduction-to-Data-Science.git
   cd Introduction-to-Data-Science/final\ project
   ```

2. **創建分支**：為您的功能或修復創建新分支。
   ```bash
   git checkout -b your-feature-branch
   ```

3. **提交更改**：進行修改後，提交代碼並推送到您的遠端儲存庫。
   ```bash
   git add .
   git commit -m "描述您的更改"
   git push origin your-feature-branch
   ```

4. **發起 Pull Request**：返回 GitHub，點擊 **Compare & pull request**，提交您的更改描述。

---

## English

### 🌟 Introduction
The Health and Nutrition Recommendation System is a dietary health tool that provides personalized recommendations based on BMR (Basal Metabolic Rate) and TDEE (Total Daily Energy Expenditure). Users input their basic information (gender, age, weight, height, and activity level), and the system calculates their daily energy expenditure (TDEE). Based on the user’s health goals (weight loss, maintenance, or muscle gain) and dietary intake, the system generates tailored nutritional advice.

This system aims to help users manage their daily nutritional intake and achieve their health goals more effectively.

---

### 🖥️ Features
1. **BMR and TDEE Calculation**:  
   Calculate the user’s Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) based on their input.  

2. **Personalized Health Recommendations**:  
   Analyze the user’s dietary intake using TDEE and provide suggestions, such as increasing protein or reducing carbohydrate intake.  

3. **Visualized Insights**:  
   Display the user’s nutritional balance with charts to help them better understand their dietary habits.

---

### 🖼️ Website Demo

1. **TDEE and BMR Calculation Page**  
   ![TDEE and BMR Calculation](https://i.imgur.com/3IGrrV8.png)

2. **Diet Analysis and Recommendations Page**  
   ![Diet Analysis](https://i.imgur.com/cIgsdfh.png)

---

### 📦 System Architecture
- **Frontend**: Built with [Streamlit](https://streamlit.io), allowing users to input data and view results through a browser.
- **Backend**: Provides APIs using [Flask](https://flask.palletsprojects.com/) to calculate TDEE and generate nutritional recommendations.
- **Dataset**: Uses a Kaggle food nutrition dataset that provides detailed nutritional information after data cleaning.

---

### 🔧 Installation and Usage

#### 1. Clone the repository
```bash
git clone git clone https://github.com/vicky0619/Introduction-to-Data-Science.git
cd Introduction-to-Data-Science/final\ project
```

#### 2. Install dependencies
Make sure Python 3.8 or above is installed, then run:
```bash
pip install -r requirements.txt
```

#### 3. Start the Flask backend
```bash
python app.py
```

#### 4. Start the Streamlit frontend
```bash
streamlit run frontend.py
```

#### 5. Open the browser
Visit `http://localhost:8501` in your browser to use the system.

---

### 🛠️ Developer
- **Developer**: Your Name or Team Name
- **Contact**: Your Contact Info

