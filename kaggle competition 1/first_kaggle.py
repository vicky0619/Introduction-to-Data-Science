import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import lightgbm as lgb
import xgboost as xgb

train_data = pd.read_csv('train.csv')
train_data
train_data.isna().sum()
X = train_data.drop(columns=['data_ID', 'player_ID', 'gender', 'play years', 'hold racket handed', 'level'])
y_gender = train_data['gender']
y_play_years = train_data['play years']
y_racket_handed = train_data['hold racket handed']
y_level = train_data['level']

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_train, X_test, y_train_gender, y_test_gender = train_test_split(X, y_gender, test_size=0.2, random_state=0)
_, _, y_train_play_years, y_test_play_years = train_test_split(X, y_play_years, test_size=0.2, random_state=0)
_, _, y_train_racket_handed, y_test_racket_handed = train_test_split(X, y_racket_handed, test_size=0.2, random_state=0)
_, _, y_train_level, y_test_level = train_test_split(X, y_level, test_size=0.2, random_state=0)


params_multiclass = {
    'objective': 'multiclass',
    'metric': 'multi_logloss',
    'learning_rate': 0.06,  # 调整学习率
    'max_depth': 2,         # 增加树的深度
    'num_leaves': 4,        # 增加叶子数
    'num_class': 3,         # 类别数
    'reg_alpha': 2.0,      #5 -> 2 變高一點 2->0.5 沒有比較好
    'reg_lambda': 2.0, #5 -> 2
    'feature_fraction': 0.8,  # 降低特征采样比例
    'bagging_fraction': 0.8,  # 降低样本采样比例
    'bagging_freq': 5,       # 增加采样频率
    'random_state': 0
}

params_binary = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'learning_rate': 0.06,  # 调整学习率
    'max_depth': 2,
    'num_leaves': 4,
    'reg_alpha': 2.0, #5 -> 2
    'reg_lambda': 2.0, #5 -> 2
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'random_state': 0
}



# 訓練 gender 的模型
lgb_train_gender = lgb.Dataset(X_train, label=y_train_gender)
model_gender = lgb.train(params_binary, lgb_train_gender, num_boost_round=800)

# 訓練 play years 的模型
lgb_train_play_years = lgb.Dataset(X_train, label=y_train_play_years)
model_play_years = lgb.train(params_multiclass, lgb_train_play_years, num_boost_round=800)

# 訓練 hold racket handed 的模型
lgb_train_racket_handed = lgb.Dataset(X_train, label=y_train_racket_handed)
model_racket_handed = lgb.train(params_binary, lgb_train_racket_handed, num_boost_round=800)


# 訓練 level 的模型
lgb_train_level = lgb.Dataset(X_train, label=y_train_level)
model_level = lgb.train(params_multiclass, lgb_train_level, num_boost_round=800)

# 預測 Gender（二分類）
y_pred_gender = (model_gender.predict(X_test) > 0.5).astype(int)  # 二分類結果 > 0.5 視為 1
gender_accuracy = accuracy_score(y_test_gender, y_pred_gender)
gender_precision = precision_score(y_test_gender, y_pred_gender)
gender_recall = recall_score(y_test_gender, y_pred_gender)
gender_f1 = f1_score(y_test_gender, y_pred_gender)

# 預測 Play Years（多分類）
y_pred_play_years = model_play_years.predict(X_test).argmax(axis=1)  # 取機率最高的類別
play_years_accuracy = accuracy_score(y_test_play_years, y_pred_play_years)
play_years_precision = precision_score(y_test_play_years, y_pred_play_years, average='macro')
play_years_recall = recall_score(y_test_play_years, y_pred_play_years, average='macro')
play_years_f1 = f1_score(y_test_play_years, y_pred_play_years, average='macro')

# 預測 Racket Handed（二分類）
y_pred_racket_handed = (model_racket_handed.predict(X_test) > 0.5).astype(int)  # 二分類結果 > 0.5 視為 1
racket_handed_accuracy = accuracy_score(y_test_racket_handed, y_pred_racket_handed)
racket_handed_precision = precision_score(y_test_racket_handed, y_pred_racket_handed)
racket_handed_recall = recall_score(y_test_racket_handed, y_pred_racket_handed)
racket_handed_f1 = f1_score(y_test_racket_handed, y_pred_racket_handed)

# 預測 Level（多分類）
y_pred_level = model_level.predict(X_test).argmax(axis=1)  # 取機率最高的類別
level_accuracy = accuracy_score(y_test_level, y_pred_level)
level_precision = precision_score(y_test_level, y_pred_level, average='macro')
level_recall = recall_score(y_test_level, y_pred_level, average='macro')
level_f1 = f1_score(y_test_level, y_pred_level, average='macro')

# 總結各模型的準確率
print(f"Gender Precision: {gender_precision:.4f}, Recall: {gender_recall:.4f}, F1-Score: {gender_f1:.4f}")
print(f"Play Years Precision: {play_years_precision:.4f}, Recall: {play_years_recall:.4f}, F1-Score: {play_years_f1:.4f}")
print(f"Racket Handed Precision: {racket_handed_precision:.4f}, Recall: {racket_handed_recall:.4f}, F1-Score: {racket_handed_f1:.4f}")
print(f"Level Precision: {level_precision:.4f}, Recall: {level_recall:.4f}, F1-Score: {level_f1:.4f}")

"""
model_gender_xgb = xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss')
model_gender_xgb.fit(X_train, y_train_gender)

model_racket_handed_xgb = xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss')
model_racket_handed_xgb.fit(X_train, y_train_racket_handed)

model_play_years_xgb = xgb.XGBClassifier(objective='multi:softmax', num_class=3)
model_play_years_xgb.fit(X_train, y_train_play_years)

model_level_xgb = xgb.XGBClassifier(objective='multi:softmax', num_class=3)
model_level_xgb.fit(X_train, y_train_level)

# 預測 Gender（二分類）
y_pred_gender = (model_gender_xgb.predict(X_test) > 0.5).astype(int)  # 二分類結果 > 0.5 視為 1
gender_accuracy = accuracy_score(y_test_gender, y_pred_gender)
gender_precision = precision_score(y_test_gender, y_pred_gender)
gender_recall = recall_score(y_test_gender, y_pred_gender)
gender_f1 = f1_score(y_test_gender, y_pred_gender)

# 預測 Play Years（多分類）
y_pred_play_years = model_play_years_xgb.predict(X_test) 
play_years_accuracy = accuracy_score(y_test_play_years, y_pred_play_years)
play_years_precision = precision_score(y_test_play_years, y_pred_play_years, average='macro')
play_years_recall = recall_score(y_test_play_years, y_pred_play_years, average='macro')
play_years_f1 = f1_score(y_test_play_years, y_pred_play_years, average='macro')

# 預測 Racket Handed（二分類）
y_pred_racket_handed = (model_racket_handed_xgb.predict(X_test) > 0.5).astype(int)  # 二分類結果 > 0.5 視為 1
racket_handed_accuracy = accuracy_score(y_test_racket_handed, y_pred_racket_handed)
racket_handed_precision = precision_score(y_test_racket_handed, y_pred_racket_handed)
racket_handed_recall = recall_score(y_test_racket_handed, y_pred_racket_handed)
racket_handed_f1 = f1_score(y_test_racket_handed, y_pred_racket_handed)

# 預測 Level（多分類）
y_pred_level = model_level_xgb.predict(X_test) 
level_accuracy = accuracy_score(y_test_level, y_pred_level)
level_precision = precision_score(y_test_level, y_pred_level, average='macro')
level_recall = recall_score(y_test_level, y_pred_level, average='macro')
level_f1 = f1_score(y_test_level, y_pred_level, average='macro')

# 總結各模型的準確率
print(f"Gender Precision: {gender_precision:.4f}, Recall: {gender_recall:.4f}, F1-Score: {gender_f1:.4f}")
print(f"Play Years Precision: {play_years_precision:.4f}, Recall: {play_years_recall:.4f}, F1-Score: {play_years_f1:.4f}")
print(f"Racket Handed Precision: {racket_handed_precision:.4f}, Recall: {racket_handed_recall:.4f}, F1-Score: {racket_handed_f1:.4f}")
print(f"Level Precision: {level_precision:.4f}, Recall: {level_recall:.4f}, F1-Score: {level_f1:.4f}")
"""

test_data = pd.read_csv('test.csv')
X = test_data.drop('data_ID', axis=1)
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 預測 Gender（二分類）
y_pred_gender = model_gender.predict(X)

# 預測 Play Years（多分類）
y_pred_play_years = model_play_years.predict(X)

# 預測 Racket Handed（二分類）
y_pred_racket_handed = model_racket_handed.predict(X)

# 預測 Level（多分類）
y_pred_level = model_level.predict(X)

predicted = pd.DataFrame({
    'data_ID': test_data['data_ID'],
    'gender': y_pred_gender,
    'hold racket handed': y_pred_racket_handed,
    'play years_0': y_pred_play_years[:,0],
    'play years_1': y_pred_play_years[:,1],
    'play years_2': y_pred_play_years[:,2],
    'level_0': y_pred_level[:,0],
    'level_1': y_pred_level[:,1],
    'level_2': y_pred_level[:,2],
})

predicted.to_csv('submission_lgb.csv', index=False)
"""
# 預測 Gender（二分類）
y_pred_gender = model_gender_xgb.predict_proba(X)[:, 1]

# 預測 Play Years（多分類）
y_pred_play_years = model_play_years_xgb.predict_proba(X)

# 預測 Racket Handed（二分類）
y_pred_racket_handed = model_racket_handed_xgb.predict_proba(X)[:, 1]

# 預測 Level（多分類）
y_pred_level = model_level_xgb.predict_proba(X)

predicted = pd.DataFrame({
    'data_ID': test_data['data_ID'],
    'gender': y_pred_gender,
    'hold racket handed': y_pred_racket_handed,
    'play years_0': y_pred_play_years[:,0],
    'play years_1': y_pred_play_years[:,1],
    'play years_2': y_pred_play_years[:,2],
    'level_0': y_pred_level[:,0],
    'level_1': y_pred_level[:,1],
    'level_2': y_pred_level[:,2],
})

predicted.to_csv('submission_xgb.csv', index=False)
"""