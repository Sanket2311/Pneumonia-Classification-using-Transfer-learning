# -*- coding: utf-8 -*-
"""Pneumonia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dazjLZ3jlahU2Pd7_0aGYnNVbOTuigZK

**Importing Dependencies**
"""

from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

"""**Initializing Image size**"""

IMAGE_SIZE = [224, 224]

"""**Adding Dataset to our Colab environment**"""

pip install -U -q kaggle

mkdir -p ~/.kaggle

from google.colab import files
files.upload()

!cp kaggle.json ~/.kaggle/

!kaggle datasets download -d paultimothymooney/chest-xray-pneumonia

pwd

"""**Unzipping the dataset**"""

!unzip chest-xray-pneumonia.zip

ls

!unzip chest_xray.zip

ls

"""**Initializing Training and test dataset path**"""

train_path = '/content/chest_xray/train'
valid_path = '/content/chest_xray/test'

pwd

"""**Downloading Weights for transfer learning from VGG16**"""

# add preprocessing layer to the front of VGG
vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# don't train existing weights
for layer in vgg.layers:
  layer.trainable = False

# useful for getting number of classes
folders = glob('/content/chest_xray/train/*')

"""**Now, Let's add our own layer at the end of the model**"""

# our layers - you can add more if you want
x = Flatten()(vgg.output)
# x = Dense(1000, activation='relu')(x)
prediction = Dense(len(folders), activation='softmax')(x)

# create a model object
model = Model(inputs=vgg.input, outputs=prediction)

# view the structure of the model
model.summary()

# tell the model what cost and optimization method to use
model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

"""**Specifying the image path to the model.**"""

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('/content/chest_xray/train',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('/content/chest_xray/test',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')

"""**Fitting tha model with dataset**"""

# fit the model
r = model.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=5,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)
# loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()
plt.savefig('LossVal_loss')

# accuracies
plt.plot(r.history['acc'], label='train acc')
plt.plot(r.history['val_acc'], label='val acc')
plt.legend()
plt.show()
plt.savefig('AccVal_acc')

"""**As We can see, We have achieved a pretty good Acuuracy score of 96.7% and Validation accuracy score of 91.5%**

**Saving the model**
"""

import tensorflow as tf

from keras.models import load_model

model.save('my_first_model_vgg16.h5')

"""**Now. Let's Predict on some new images whether a person has Pneumonia**

**First, Let's pass a normal Xray image to our model.**
"""

## Predicitng on New Data


from keras.models import load_model
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np
model = load_model('my_first_model_vgg16.h5')
img = image.load_img('/content/chest_xray/val/NORMAL/NORMAL2-IM-1427-0001.jpeg', target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
img_data = preprocess_input(x)
classes = model.predict(img_data)

print(classes)

"""**As we can see here, returned array has '1' as first value and the second value is near to zero. This means that a passed image is of a person having normal xray**

**Now, Let's pass chest xray image of a person having pneumonia to see what our model predicts.**
"""

## Predicitng on New Data


from keras.models import load_model
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np
model = load_model('my_first_model_vgg16.h5')
img = image.load_img('/content/chest_xray/val/PNEUMONIA/person1951_bacteria_4882.jpeg', target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
img_data = preprocess_input(x)
classes = model.predict(img_data)
print(classes)

"""**Value at index 1 is "1". This means that person is having Pneumonia for this image.**"""

