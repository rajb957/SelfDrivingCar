import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np

data = keras.datasets.fashion_mnist
(train_images, train_labels),(test_images, test_labels) = data.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
plt.imshow(test_images[0],cmap=plt.cm.binary)

train_images = train_images / 255.0
test_images = test_images / 255.0
print(train_images.shape)
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

model.fit(train_images,train_labels,epochs=5)

test_loss, test_acc= model.evaluate(test_images,test_labels)
predictions = model.predict(test_images)
print("Tested Acc. ", test_acc)
print(class_names[np.argmax(predictions[0])])
plt.show()