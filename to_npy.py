import os, glob, numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split

data_dir = 'data/korea/train'
categories = ['won_10_f_0','won_10_b_0', 'won_50_f', 'won_50_b', 'won_100_f_0', 'won_100_b_0', 'won_100_f_1', 'won_100_b_1', 'won_500_f', 'won_500_b']
nb_classes = len(categories)

image_w = 64
image_h = 64

pixels = image_h * image_w * 3

X = []
y = []

for idx, cate in enumerate(categories):
    label = [0 for i in range(nb_classes)]
    label[idx] = 1

    image_dir = data_dir + "/" + cate
    files = glob.glob(image_dir+"/*.jpg")
    print(cate, " 파일 길이 : ", len(files))

    for i, f in enumerate(files):
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.resize((image_w, image_h))
        data = np.asarray(img)

        X.append(data)
        y.append(label)

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y)
xy = (X_train, X_test, y_train, y_test)
np.save('data/korea/won_image_data.npy', xy)

print("ok", len(y))