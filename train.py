from s3_image_generator import S3ImageGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Flatten, Dense
from s3_fetch_images import df1
import os
import pickle


# Load ResNet50 without the top layer
resnet = ResNet50(include_top=False, input_shape=(200, 200, 3))
resnet.trainable = False


x = Flatten()(resnet.output)

# Age tower
dense1 = Dense(512, activation='relu')(x)
dense3 = Dense(512, activation='relu')(dense1)
output1 = Dense(1, activation='linear', name='age')(dense3)

# Gender tower
dense2 = Dense(512, activation='relu')(x)
dense4 = Dense(512, activation='relu')(dense2)
output2 = Dense(1, activation='sigmoid', name='gender')(dense4)

model = Model(inputs=resnet.input, outputs=[output1, output2])

model.compile(
    optimizer='adam',
    loss={'age': 'mse', 'gender': 'binary_crossentropy'},
    metrics={'age': 'mae', 'gender': 'accuracy'}
)

# Generator
train_gen = S3ImageGenerator(df1, batch_size=32)

# Training
model.fit(train_gen, epochs=20)

model.save('model.h5')  # Save the model to the SageMaker output directory
