import os
from PIL import Image

# path = 'data/korea/original_data/'

src = 'images'
dst = 'background'

data_dir = list(filter(lambda x: os.path.isdir(f'{src}/{x}'), os.listdir(src)))

for dir_name in data_dir:
    print(dir_name)
    for data in os.listdir(f'{src}/{dir_name}'):
        print(data)
        if data.endswith('.jpg'):
            image = Image.open(f'{src}/{dir_name}/{data}')
            image = image.convert('RGBA')  # png 이미지에 알파채널 추가
            image.save(f'{dst}/{data.replace("jpg", "png")}')
            # if data.endswith('jpg'):
            #     os.remove(f'{src}{dir_name}/{data}')
