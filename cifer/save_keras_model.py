# 📄 save_keras_model.py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# สร้างโมเดลง่าย ๆ
model = Sequential([
    Dense(64, input_shape=(10,), activation='relu'),
    Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy')

# สร้างข้อมูลปลอมเพื่อให้ model.fit ผ่าน
X = np.random.rand(100, 10)
y = np.random.randint(0, 2, size=100)
model.fit(X, y, epochs=1)

# บันทึก
model.save("models/my_model.h5")
