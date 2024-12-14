import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import tensorflow as tf
from tensorflow.keras import layers, models, initializers, regularizers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy, BinaryCrossentropy

# ==============================
# Constants and Setup
# ==============================
SEED = 30
np.random.seed(SEED)
tf.random.set_seed(SEED)
os.environ['TF_DETERMINISTIC_OPS'] = '1'
os.environ['PYTHONHASHSEED'] = str(SEED)
os.environ['OMP_NUM_THREADS'] = '1'

# ==============================
# Data Loading and Preprocessing
# ==============================
train_features = pd.read_csv('train_data.csv')
train_labels = pd.read_csv('train_info.csv')
test_features = pd.read_csv('test_data.csv')

# Standardization
feature_cols = ["Ax", "Ay", "Az", "Gx", "Gy", "Gz"]
scaler = StandardScaler()
train_features[feature_cols] = scaler.fit_transform(train_features[feature_cols])
test_features[feature_cols] = scaler.transform(test_features[feature_cols])

# Grouping Data by data_id
def group_data(data):
    return data.groupby('data_id')[feature_cols].apply(lambda x: x.values)

train_grouped = group_data(train_features)
test_grouped = group_data(test_features)

# Padding and Truncation
def preprocess_sequences(data, fixed_length):
    processed = []
    for seq in data:
        seq_len = len(seq)
        if seq_len < fixed_length:
            pad_len = fixed_length - seq_len
            left_pad, right_pad = pad_len // 2, pad_len - (pad_len // 2)
            seq = np.pad(seq, ((left_pad, right_pad), (0, 0)), mode='constant', constant_values=-999999)
        else:
            start_idx = (seq_len - fixed_length) // 2
            seq = seq[start_idx:start_idx + fixed_length]
        processed.append(seq)
    return np.array(processed)

fixed_length = 1000
X_train = preprocess_sequences(train_grouped, fixed_length)
X_test = preprocess_sequences(test_grouped, fixed_length)
Y = train_labels.iloc[:, 1:].values

# Train-Test Split
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y, test_size=0.2, random_state=SEED, shuffle=True)

# ==============================
# Model Definition
# ==============================
def create_cnn_model(input_shape, num_classes, name):
    initializer = initializers.GlorotUniform(seed=SEED)
    model = models.Sequential(name=name)
    model.add(layers.Masking(mask_value=-999999, input_shape=input_shape))
    model.add(layers.Conv1D(64, kernel_size=3, kernel_initializer=initializer))
    model.add(layers.LeakyReLU(0.1))
    model.add(layers.MaxPooling1D(pool_size=3))
    model.add(layers.Conv1D(128, kernel_size=3, kernel_initializer=initializer))
    model.add(layers.LeakyReLU(0.1))
    model.add(layers.MaxPooling1D(pool_size=3))
    model.add(layers.Conv1D(256, kernel_size=3, kernel_initializer=initializer))
    model.add(layers.LeakyReLU(0.1))
    model.add(layers.MaxPooling1D(pool_size=3))
    model.add(layers.Conv1D(512, kernel_size=5, kernel_initializer=initializer))
    model.add(layers.LeakyReLU(0.1))
    model.add(layers.MaxPooling1D(pool_size=3))
    model.add(layers.Conv1D(1024, kernel_size=3, kernel_initializer=initializer))
    model.add(layers.LeakyReLU(0.1))
    model.add(layers.MaxPooling1D(pool_size=3))
    model.add(layers.GlobalAveragePooling1D())
    model.add(layers.Dense(64, kernel_initializer=initializer, kernel_regularizer=regularizers.L1(0.1)))
    model.add(layers.LeakyReLU(0.1))
    model.add(layers.Dense(num_classes, activation='softmax' if num_classes > 2 else 'sigmoid', kernel_initializer=initializer))
    return model

# ==============================
# Training and Evaluation
# ==============================
def train_and_evaluate(name, model, X_train, X_val, Y_train, Y_val, num_classes, epochs=100, batch_size=32, patience=10):
    early_stopping = EarlyStopping(monitor='val_loss', patience=patience, restore_best_weights=True, verbose=1)
    lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, verbose=1)
    loss_fn = CategoricalCrossentropy(label_smoothing=0.1) if num_classes > 2 else BinaryCrossentropy(label_smoothing=0.1)
    model.compile(optimizer=Adam(learning_rate=0.001), loss=loss_fn, metrics=['accuracy'])
    history = model.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=epochs, batch_size=batch_size, callbacks=[early_stopping, lr_scheduler], verbose=1)
    Y_pred = model.predict(X_val)
    auc_score = roc_auc_score(Y_val, Y_pred, average='micro', multi_class='ovr') if num_classes > 2 else roc_auc_score(Y_val, Y_pred)
    print(f"{name} Validation ROC-AUC: {auc_score:.4f}")
    return history, auc_score

# ==============================
# Model Training
# ==============================
models_and_tasks = [
    ("Gender_Model", 1, Y_train[:, 0].reshape(-1, 1), Y_val[:, 0].reshape(-1, 1)),
    ("Experience_Model", 3, tf.keras.utils.to_categorical(Y_train[:, 1], 3), tf.keras.utils.to_categorical(Y_val[:, 1], 3)),
    ("Hand_Model", 1, Y_train[:, 2].reshape(-1, 1), Y_val[:, 2].reshape(-1, 1)),
    ("Level_Model", 3, tf.keras.utils.to_categorical(Y_train[:, 3], 3), tf.keras.utils.to_categorical(Y_val[:, 3], 3)),
]

for name, num_classes, Y_task_train, Y_task_val in models_and_tasks:
    print(f"\nTraining {name}...")
    model = create_cnn_model((X_train.shape[1], X_train.shape[2]), num_classes, name)
    history, auc = train_and_evaluate(name, model, X_train, X_val, Y_task_train, Y_task_val, num_classes)

# ==============================
# Summary
# ==============================
print("\nTraining Completed. Models and AUC scores are printed above.")
