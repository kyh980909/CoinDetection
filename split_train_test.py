import os
import random
import shutil

path = 'data/korea/train/'

dir_list = list(filter(lambda x: os.path.isdir(path+x), os.listdir(path)))

for folder in dir_list:
    data = os.listdir(path + folder)

    test_data = random.sample(data, 20)

    os.mkdir('data/korea/test/' + folder)

    for filename in test_data:
        shutil.move(path + folder + '/' + filename,
                    "data/korea/test/" + folder + '/' + filename)
