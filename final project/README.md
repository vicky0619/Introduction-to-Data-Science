# Personalized Nutrition Assistant

This project presents a **Personalized Nutrition Assistant** system that integrates nutritional data, user profiles, and dietary records to offer customized dietary recommendations. By leveraging machine learning (XGBoost), the system provides health scores, recipe recommendations, and dietary insights tailored to individual needs.

---

## 📄 **Introduction**

This project leverages nutritional data to provide precise dietary recommendations:
- **Motivation**: Rising global health issues such as obesity and cardiovascular diseases highlight the importance of nutrition management. Many lack a comprehensive understanding of nutritional values, leading to imbalanced diets.
- **Goal**: Analyze dietary habits combined with nutritional data to generate personalized recommendations and recipes.

---

## 📊 **Dataset**

1. **[Food Nutritional Facts](https://www.kaggle.com/datasets/beridzeg45/food-nutritional-facts)**:
   - Nutritional data for 1,174 food items.
   - Includes calories, protein, fats, carbs, fiber, sugar, vitamins, and minerals.
   - Used for dietary analysis and nutrient gap identification.

2. **[EpiRecipes Dataset](https://www.kaggle.com/datasets/hugodarwood/epirecipes)**:
   - Recipes with ingredients, preparation steps, and nutritional details.
   - Used to recommend recipes tailored to users’ nutritional needs.

---

## 🛠 **System Architecture**

![System Architecture](https://hackmd.io/_uploads/r1Kw87uBJe.png)

The system consists of:
1. **Input Layer**: Users provide personal data (age, weight, height, gender) and dietary records.
2. **Analysis Layer**: Calculates **BMR** and **TDEE**, evaluates nutritional intake, and identifies deficiencies/excesses.
3. **Recommendation Layer**: Uses XGBoost to suggest the top 5 recipes, including detailed cooking instructions.

---

## 📋 **How to Reproduce**

### Prerequisites
1. Python 3.9 or higher.
2. Install the required Python libraries listed in `requirements.txt`.

### Steps to Run
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vicky0619/Introduction-to-Data-Science.git
   cd Introduction-to-Data-Science/final\ project
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate  # For Windows: env\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Backend (Flask)**:
   - Navigate to the backend directory and start the API:
     ```bash
     python app.py
     ```

5. **Run the Frontend (Streamlit)**:
   - Launch the interactive user interface:
     ```bash
     streamlit run frontend.py
     ```

6. **Access the Application**:
   - Open the Streamlit interface in your browser (e.g., `http://localhost:8501`).

---

## 📂 **File Structure**

1. **`app.py`**:
   - Backend Flask API for processing user data, calculating BMR/TDEE, and generating recommendations.

2. **`frontend.py`**:
   - Streamlit-based frontend for user input and displaying results.

3. **`analysis.py`**:
   - Core analysis logic, including calculations for nutritional gaps, BMR, TDEE, and recipe recommendations using XGBoost.

4. **`requirements.txt`**:
   - List of required Python libraries for the project.

5. **`cleaned_food_data.csv`**:
   - Preprocessed dataset for nutritional analysis.

---

## 🚀 **Features**

1. **User Input**:
   - Age, gender, height, weight, activity level.
   - Records daily dietary intake.

2. **Nutritional Analysis**:
   - Calculates BMR and TDEE.
   - Evaluates nutritional gaps and provides health recommendations.

3. **Machine Learning**:
   - **XGBoost** predicts health scores for food items.
   - Suggests top 5 recipes based on nutritional needs.

4. **Recipe Recommendations**:
   - Detailed recipes with preparation steps.

5. **Data Visualization**:
   - Displays nutritional trends and deficiencies through charts.

---

## 📈 **Model Description**

1. **Model Selection**:
   - **XGBoost** was chosen for its regularization and sparse data optimization capabilities.

2. **Training**:
   - Data preprocessed using `LabelEncoder` and `MinMaxScaler`.
   - 80-20 train-test split to evaluate performance.

3. **Prediction**:
   - Predicts health scores for recipes based on key nutritional features.
   - Generates similarity scores to match user needs with recipes.

4. **Recommendation**:
   - Top 5 recipes suggested based on similarity scores.

---

## 📧 **Contact**
For questions or contributions, feel free to reach out:
- Wen-Chi Tsai: [vicky46586038@gmail.com](mailto:vicky46586038@gmail.com)
- Si-Ying Chen: [d0915708@gmail.com](mailto:d0915708@gmail.com)
- Yun-Sheng Chen: [yunsheng1223@gmail.com](mailto:yunsheng1223@gmail.com)

---

## 📝 **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.