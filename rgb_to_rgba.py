import os
from PIL import Image

path = 'data/korea/original_data/'

data_dir = list(filter(lambda x: os.path.isdir(path + x), os.listdir(path)))

# for dir_name in data_dir:
#     for data in os.listdir(f'{path}/{dir_name}'):
#         if not data == '.DS_Store':
#             img = Image.open(f'{path}{dir_name}/{data}')
#             img = img.convert('RGBA') # png 이미지에 알파채널 추가
#             img.save(f'{path}{dir_name}/{data}')


for data in os.listdir('background'):
    print(data)
    img = Image.open(f'background/{data}')
    img = img.convert('RGBA')  # png 이미지에 알파채널 추가
    img.save(f'background/{data}.png')
