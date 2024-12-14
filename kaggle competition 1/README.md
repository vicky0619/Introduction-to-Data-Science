# README File

## **Kaggle Competition: Multi-Classification and Binary Classification using LightGBM and XGBoost**

This repository contains code for training and evaluating models for predicting various attributes of players based on sensor data. The models are built using **LightGBM** and **XGBoost** frameworks.

---

### **Installation Requirements**
To run this project, install the following Python packages:
- `numpy`
- `pandas`
- `scikit-learn`
- `lightgbm`
- `xgboost`

Use the following command to install the required packages:
```bash
pip install numpy pandas scikit-learn lightgbm xgboost
```

---

### **Running the Code**
1. **Input Files:**
   - Ensure the following input files are in the same directory as the code:
     - `train.csv` - Training dataset with player attributes and sensor data.
     - `test.csv` - Testing dataset with player sensor data.
   
2. **Execution:**
   - Run the script directly using:
     ```bash
     python your_script_name.py
     ```

3. **Output Files:**
   - The predictions will be saved to the following CSV files:
     - `submission_lgb.csv` - Predictions using LightGBM.
     - `submission_xgb.csv` (if uncommented) - Predictions using XGBoost.

---

### **Steps in the Code**

#### **1. Data Preprocessing**
   - The training data (`train.csv`) is read and split into:
     - `X` - Features (sensor data).
     - `y_gender`, `y_play_years`, `y_racket_handed`, `y_level` - Target labels.
   - Features are scaled using `StandardScaler` for better convergence.
   - Data is split into training and testing sets with an 80/20 ratio.

#### **2. Model Training**
   - **LightGBM Models:**
     - **Binary Classification:** 
       - `model_gender` for `gender`.
       - `model_racket_handed` for `hold racket handed`.
     - **Multi-Class Classification:**
       - `model_play_years` for `play years`.
       - `model_level` for `level`.
     - Parameters are tuned for optimal performance.
   - **XGBoost Models (Optional):**
     - Uncomment the XGBoost training section to train models using XGBoost.

#### **3. Predictions**
   - Predictions are made for both LightGBM and XGBoost models.
   - Results include:
     - `gender` - Binary predictions (0 or 1).
     - `play years` - Probabilities for each of 3 classes.
     - `hold racket handed` - Binary predictions (0 or 1).
     - `level` - Probabilities for each of 3 classes.

#### **4. Evaluation Metrics**
   - **Metrics Used:**
     - Accuracy
     - Precision
     - Recall
     - F1-Score
   - These metrics are calculated and printed for all models.

---

### **Post-Processing**
- No manual adjustments are required. However, if you want to switch between LightGBM and XGBoost predictions:
  - Use the `submission_lgb.csv` or `submission_xgb.csv` files based on the desired model.

---

### **Notes**
- Adjust parameters like `learning_rate`, `max_depth`, and `num_leaves` in `params_binary` and `params_multiclass` to improve model performance.
- To use XGBoost, uncomment the respective sections in the script and run again.
