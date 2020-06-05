import os
import random

path = ''

image_data = list(filter(lambda x: x.endswith('jpg'), os.listdir(path)))

random.seed(42)

random.shuffle(image_data)

train_test_ratio = 0.8  # train, test 분리 비율

train = image_data[:round(len(image_data) * train_test_ratio)]
test = image_data[round(len(image_data) * train_test_ratio):]

with open(f'train.txt', 'w') as f:
    for data in train:
        f.write(f'x64/data/obj/image/{data}\n')

with open(f'test.txt', 'w') as f:
    for data in test:
        f.write(f'x64/data/obj/image/{data}')
