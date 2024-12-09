import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

MODEL_FILE = "recommendation_model.pkl"

def train_model(data):
    """
    使用用戶數據訓練模型
    :param data: pandas DataFrame，包含用戶的飲食數據
    """
    # 特徵和標籤
    X = data[["calories", "protein", "fats", "carbs"]]
    y = data["goal"]  # 標籤: 減重、增肌或維持

    # 訓練集和測試集拆分
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 訓練模型
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # 評估模型
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"模型準確率: {accuracy:.2f}")

    # 保存模型
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

def load_model():
    """加載已訓練的模型"""
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)
    return model
