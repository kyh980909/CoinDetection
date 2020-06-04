import os

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    fill_mode='nearest')

img = load_img('data/korea/crop_data/won_500_f/won_500_f_0.jpg')

x = img_to_array(img)
x = x.reshape((1,) + x.shape)

i = 0

for batch in datagen.flow(x, batch_size=1, save_to_dir='data', save_prefix='yen_1_b',
                          save_format='jpg'):
    if i > 1:
        break
    i += 1
