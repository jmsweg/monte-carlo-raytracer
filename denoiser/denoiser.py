"""Kernel Predicting Convolutional Networks for Denoising Monte Carlo Renderings

Implementation based on this paper:
http://drz.disneyresearch.com/~jnovak/publications/KPCN/KPCN.pdf

This module implements a kernel predicting network to denoise monte carlo
renderings. The aim is to produce high quality renderings at fast speeds by
rendering lowl quality, noisy images from the monte carlo renderer, and then
running the image through the model to remove the noise, producing images at a
much higher quality.
"""


import tensorflow as tf
import data

# Global flags
FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_integer ("patchSize", 64,
                            "The size of the input patches")

#tf.app.flags.DEFINE_integer ("reconstructionKernelSize", 21,
#                            "The size of the reconstruction kernel")

tf.app.flags.DEFINE_integer ("inputChannels", 3,
                            "The number of channels in an input patch")

tf.app.flags.DEFINE_integer ("outputChannels", 3,
                            "The number of channels in an output patch")

tf.app.flags.DEFINE_float   ("learningRate", 0.00001,
                            "The learning rate for ADAM")

tf.app.flags.DEFINE_integer ("numEpochs", 200,
                            "Number of training epochs")

# First convolutional layer (must define input shape)
def firstConvLayer():
    return tf.keras.layers.Conv2D(
        input_shape=(FLAGS.patchSize, FLAGS.patchSize, FLAGS.inputChannels),
        filters=100,
        kernel_size=(5, 5),
        use_bias=True,
        strides=[1, 1],
        padding="VALID",
        activation=tf.keras.activations.relu,
        kernel_initializer=tf.keras.initializers.glorot_uniform
    )

# Convolutional layer (not final)
def convLayer():
    return tf.keras.layers.Conv2D(
        filters=100,
        kernel_size=(5, 5),
        use_bias=True,
        strides=[1, 1],
        padding="VALID",
        activation=tf.keras.activations.relu,
        kernel_initializer=tf.keras.initializers.glorot_uniform
    )

# Final convolutional layer - no activation function
def finalConvLayer():
    return tf.keras.layers.Conv2D(
        filters=FLAGS.outputChannels,
        kernel_size=(5, 5),
        use_bias=True,
        strides=(1, 1),
        padding="VALID",
        activation=None,
        kernel_initializer=tf.keras.initializers.glorot_uniform
    )

reference_train = data.data["train"]["colour"]["reference"]
noisy_train = data.data["train"]["colour"]["noisy"]

model = tf.keras.models.Sequential([

    # Conv layer 1
    firstConvLayer(),

    # Conv layer 2
    convLayer(),

    # Conv layer 3
    convLayer(),

    # Conv layer 4
    convLayer(),

    # Conv layer 5
    convLayer(),

    # Conv layer 6
    convLayer(),

    # Conv layer 7
    convLayer(),

    # Conv layer 8
    convLayer(),

    # Conv layer 9
    finalConvLayer()
])

model.compile(
    optimizer="adam",
    loss="mean_absolute_error",
    metrics=["accuracy"]
)

model.fit(
    noisy_train,
    reference_train,
    epochs=5
)



#model.compile(optimizer='adam',
#              loss='sparse_categorical_crossentropy',
#              metrics=['accuracy'])

#model.fit(x_train, y_train, epochs=5)
#model.evaluate(x_test, y_test)

