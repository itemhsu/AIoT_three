# -*- coding: utf-8 -*-
"""CNN_Cifar_10_TFLite.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17GHe6SkTQ34N_ae7Ps38wZZBHTt9joJ5

# CNN to classify Cifar-10 dataset (Images)

So far, we saw how to build a Dense Neural Network (DNN) that classified images of digits (MNIST) or even fashion images (Fashion-MNIST). Here we will instead, recognize the 10 classes of CIFAR ('airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship' and 'truck'). There are some key differences between these two image datasets that we need to take into account.

First, while MNIST were 28x28 monochrome images (1 color channel), CIFAR is 32x32 color images (3 color channels).

Second, MNIST images are simple, containing just the object centered in the image, with no background. Conversely, CIFAR ones are not centered and can have the object with a background, such as airplanes that might have a cloudy sky behind them! Those differences are the main reason to use a CNN instead of a DNN.

## Import Libraries
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten
from tensorflow.keras.callbacks import EarlyStopping

"""## Import and Inspect Dataset

Cifar-10 repository: https://www.cs.toronto.edu/~kriz/cifar.html
"""

cifar10 = tf.keras.datasets.cifar10
(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()

print(train_images.shape, train_labels.shape)
print(test_images.shape, test_labels.shape)

"""- The image data shape is: `(#images, img_heigth, img_width, #channels)`, where channels are in RGB format (red, green, blue).
- The labels shape is `(#images, label)`, where label goes from 0 to 9.

"""

train_images[0]

plt.imshow(train_images[1]);

train_labels[1][0]

"""The CIFAR labels happen to be arrays, which is why you need the extra index."""

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

class_names[9] # The List's index is the label

idx = train_labels[1][0]
class_names[idx]

print("\t", class_names[train_labels[1][0]])
plt.imshow(train_images[1])
plt.axis('off');

def plot_train_img(img, size=2):
    label = train_labels[img][0]
    plt.figure(figsize=(size,size))
    print("Label {} - {}".format(label, class_names[label]))
    plt.imshow(train_images[img])
    plt.axis('off')
    plt.show()

plot_train_img(1)

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i])
    plt.xlabel(class_names[train_labels[i][0]])
plt.show()

"""Note that images are in color, not centered and with different backgrounds

## Preprocessing dataset
"""

test_images.max()

# Normalize pixel values to be between 0 and 1
train_images = train_images / 255.0
test_images = test_images / 255.0

test_images.max()

plt.hist(train_labels[:5000]);

val_images = train_images[:5000]
val_labels = train_labels[:5000]
print(val_images.shape, val_labels.shape)

train_images = train_images[5000:]
train_labels = train_labels[5000:]
print(train_images.shape, train_labels.shape)

plt.hist(train_labels, alpha=0.5)
plt.hist(val_labels, alpha=0.5)
plt.hist(test_labels, alpha=0.5);

"""## Create Model Architecture and Compile

On [Convolution layers](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Conv2D),
- strides is an integer or tuple/list of 2 integers, specifying the strides of the convolution along the height and width. Default (1,1).
- padding: one of "valid" or "same" (case-insensitive). Default = 'valid'.
  - "valid" means no padding.  
  - "same" results in padding with zeros evenly
to the left/right or up/down of the input such that output has the same
"""

model = Sequential()


model.add(Conv2D(
    filters=32,
    kernel_size=(3,3),
    activation='relu',
    input_shape=(32, 32, 3))
)
model.add(MaxPool2D(2, 2))

model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPool2D())

model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.summary()

LOSS = 'sparse_categorical_crossentropy'
OPTIMIZER = 'adam'

# Compile the model
model.compile(optimizer=OPTIMIZER,
              loss=LOSS,
              metrics=['accuracy'])

"""## Training"""

NUM_EPOCHS = 10

early_stop = EarlyStopping(monitor='val_loss', patience=3)

# Fit the model
history = model.fit(train_images,
                    train_labels,
                    epochs=NUM_EPOCHS,
                    validation_data=(val_images, val_labels),
                    callbacks=[early_stop]
)

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
#plt.xlim([0,NUM_EPOCHS])
plt.ylim([0.4,1.0])
plt.show()

"""## Evaluate Model"""

model.evaluate(test_images, test_labels)

"""**Accuracy**
- Train: 85% - 90%;
- Validation: 68%-70%
- Test: 66%-68%
"""

predictions = np.argmax(model.predict(test_images), axis=-1)
predictions.shape

from sklearn.metrics import classification_report,confusion_matrix

print(classification_report(test_labels, predictions, target_names=class_names))

confusion_matrix(test_labels,predictions)

class_names

import seaborn as sns
plt.figure(figsize=(15,8))
sns.heatmap(confusion_matrix(test_labels,predictions), cmap='Blues', annot=True, fmt='g');

"""## Testing Model (Predicting)"""

plt.imshow(test_images[15]);

test_labels[15][0]

class_names[8]

test_images[15].shape

"""The input Tensor shape should be: (num_images, width, height, color_channels)"""

my_image = test_images[15]
my_image = my_image.reshape(1,32,32,3)
my_image.shape

img_pred = np.argmax(model.predict(my_image))
class_names[img_pred]

img_pred

pred_prob = model.predict(my_image)[0][img_pred]
pred_prob

def img_pred(img, size=4):
    label = test_labels[img][0]
    my_image = test_images[img]
    plt.figure(figsize=(size,size))
    plt.imshow(my_image)
    my_image = my_image.reshape(1,32,32,3)
    img_pred = np.argmax(model.predict(my_image))
    pred_label = class_names[img_pred]
    pred_prob = model.predict(my_image)[0][img_pred]
    print(" Label {} <=> Pred: {} with prob {:.2}".format(
        class_names[label],
        pred_label,
        pred_prob))
    plt.grid(False)
    plt.axis('off')
    plt.show()

img_pred(0)

for i in range (5):
  img_pred(i)

"""## Saving the model

Take now some time and read more about saving models. Things have changed a bit recently. Read here:

https://www.tensorflow.org/guide/keras/serialization_and_saving

You can save a model with model.save() or keras.models.save_model() (which is equivalent).

You can load it back with keras.models.load_model().

The recommended format is the "Keras v3" format, which uses the .keras extension.

There are, however, **two legacy formats** that are available: the **TensorFlow SavedModel** format and the older **Keras H5** format.

You can switch to the SavedModel format by:

    Passing save_format='tf' to save()
    Passing a filename without an extension

You can switch to the H5 format by:

    Passing save_format='h5' to save()
    Passing a filename that ends in .h5
"""

!pwd # Linux command, shows where we are in CoLab's folders

"""1) Save model as in **Keras V3** format:"""

model.save('cifar_10_model.keras')

!du -sh /content/cifar_10_model.keras

"""2) Save model as in **TensorFlow SavedModel** format:"""

model.save('cifar_10_model')

!ls /content/cifar_10_model
!du -sh /content/cifar_10_model

"""3) Save model as in **Keras H5** format:"""

model.save('cifar_10_model.h5')

!du -sh /content/cifar_10_model.h5

"""NOTE 1:

If you save your model like just discussed and would like to have them for later - before closing your Colab session **you should download them to your own computer**. Later, you will then only need to upload the saved model back into your othrr Colab session and start from it, without the need to retrain!

NOTE 2:

Use [Netron](https://netron.app) to visualize the model, hyperparameters, tensor shapes, etc. Netron is a viewer for neural network, deep learning and machine learning models (See [GitHub](https://github.com/lutzroeder/netron) for instructions about instalation in your desktop).

# Converting to TensorFlow Lite

You can convert the TF trained model using:  `TFLiteConverter.from_keras_model(model)`

Read more about converting models here:

https://www.tensorflow.org/lite/models/convert/convert_models
"""

converter = tf.lite.TFLiteConverter.from_keras_model(model)

"""Alternativally, **we can do that from a previously saved model, to avoid doing retraining**:

1) From a Keras V3 (recommended) saved model: `tf.lite.TFLiteConverter.from_keras_model(model_cifar10.keras)`

2) From a TF saved model: `tf.lite.TFLiteConverter.from_saved_model(model_cifar10)`

3) From a Keras H5 saved model: `tf.lite.TFLiteConverter.from_keras_model(model_cifar10.h5)`

Uncomment and run any of these options below - if you want to do that:
"""

# 1) From Keras V3
#model2_path = '/content/cifar_10_model.keras'
#model2 = tf.keras.models.load_model(model2_path)
#converter = tf.lite.TFLiteConverter.from_keras_model(model2)

# 2) From TF saved
#model3_path = '/content/cifar_10_model'
#converter = tf.lite.TFLiteConverter.from_saved_model(model3_path)

# 3) From Keras H5 saved
#model4_path = '/content/cifar_10_model.h5'
#model4 = tf.keras.models.load_model(model4_path)
#converter = tf.lite.TFLiteConverter.from_keras_model(model4)

tflite_model = converter.convert()

# Save .tflite model
tflite_model_size = open("/content/cifar10_model.tflite","wb").write(tflite_model)
print("TFLite model is {:,} bytes".format(tflite_model_size))

"""## Dynamic Range Quantization - DEFAULT Options
The simplest form of **post-training** quantization statically **quantizes only the weights from floating point to integer**, which has 8-bits of precision. Dynamic Range Quantization often provides a good balance between model size reduction and accuracy preservation. Read more at:

https://www.tensorflow.org/lite/performance/post_training_quantization

`optimizations` is an xperimental flag, subject to change. Set of optimizations to apply. e.g {tf.lite.Optimize.DEFAULT}. (default None, must be None or a set of values of type tf.lite.Optimize). Read more at:

https://www.tensorflow.org/api_docs/python/tf/lite/TFLiteConverter

DEFAULT The default optimization strategy that enables post-training quantization. The type of post-training quantization that will be used is dependent on the other converter options supplied. Read more at:

https://www.tensorflow.org/api_docs/python/tf/lite/Optimize


"""

converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model_quant = converter.convert()

# Save .tflite model and print its size on disk:
tflite_model_quant_size = open("/content/cifar10_model_quant.tflite","wb").write(tflite_model_quant)
print("TFLite Quantized model (with DEFAULT optimizations) is {:,} bytes".format(tflite_model_quant_size))

"""NOTE:

Use [Netron](https://netron.app) to visualize the quantized model. Pay attention that now the weights are int8.

## Testing TFLite Model

Interpreter is an interface for running TensorFlow Lite models.
"""

interpreter = tf.lite.Interpreter("/content/cifar10_model_quant.tflite")

interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_details

output_details

def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image

image = test_images[0]
plt.imshow(image);

set_input_tensor(interpreter, image)
interpreter.invoke()
output_details = interpreter.get_output_details()[0]

interpreter.get_tensor(output_details['index'])

"""The squeeze() function in NumPy is used to remove an axis of length 1 from an input array. This will remove one set of [] from above array. Read some more info at:

https://www.geeksforgeeks.org/numpy-squeeze-in-python/
"""

np.squeeze(interpreter.get_tensor(output_details['index']))

output = np.squeeze(interpreter.get_tensor(output_details['index']))
output

img_pred = np.argmax(output)
class_names[img_pred]

img_pred

output[img_pred]

def classify_image(image):
    set_input_tensor(interpreter, image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))
    img_pred = np.argmax(output)
    pred_label = class_names[img_pred]
    pred_prob = output[img_pred]
    plt.imshow(image)
    print(" Pred: {} with prob {:.2}".format(pred_label, pred_prob))
    plt.grid(False)
    plt.axis('off')
    plt.show()

classify_image(test_images[0])

for i in range (5):
  classify_image(test_images[i])

"""# TensorFlow Lite Micro

### Generate a TensorFlow Lite for Microcontrollers Model
To convert the **TensorFlow Lite (TFL)** quantized model into a C source file that can be loaded by TensorFlow Lite for Microcontrollers on MCUs, we simply need to use the ```xxd``` tool to convert the ```.tflite``` file into a ```.cc``` file. But, first, install xxd:
"""

!apt-get update && apt-get -qq install xxd

"""Now, convert and save the .cc converted model"""

MODEL_TFLITE = 'cifar10_model_quant.tflite'
MODEL_TFLITE_MICRO = 'cifar10_model_quant.cc'
!xxd -i {MODEL_TFLITE} > {MODEL_TFLITE_MICRO}
REPLACE_TEXT = MODEL_TFLITE.replace('/', '_').replace('.', '_')
!sed -i 's/'{REPLACE_TEXT}'/g_model/g' {MODEL_TFLITE_MICRO}

"""If you'd like to download your model for safekeeping:
1. On the left of the UI click on the folder icon
2. Click on the three dots to the right of the ```cifar10_model_quant.cc``` file and select download
"""

!cat {MODEL_TFLITE_MICRO}