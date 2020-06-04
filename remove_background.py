import os
from PIL import Image


def remove_background(img_path, img_dir, img_name):
    img = Image.open(img_path)
    img = img.convert('RGBA')
    datas = img.getdata()

    new_data = []
    cut_off = 100  # 높을 수록 배경 제거가 잘 됨

    for item in datas:
        if item[0] >= cut_off and item[1] >= cut_off and item[2] >= cut_off:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(f'data/korea/remove_background_data/{img_dir}/{img_name}', 'PNG')


def change_background():
    dst = Image.open('background/dst.jpg')
    new = Image.open('qwe.png')

    dst.paste(new, (100, 100), new)
    dst.save('test10.png')


if __name__ == '__main__':
    path = 'data/korea/crop_data/'
    dir_list = list(filter(lambda x: os.path.isdir(path + x), os.listdir(path)))

    for img_dir in dir_list:
        print(f'Dir name : {img_dir}')

        try:
            if not os.path.exists(f'data/korea/remove_background_data/{img_dir}'):
                # crop_data 폴더에 같은 폴더명 생성
                os.mkdir(f'data/korea/remove_background_data/{img_dir}')
                for img_file in os.listdir(path + img_dir):
                    if not img_file == '.DS_Store':
                        img_path = f'{path}{img_dir}/{img_file}'
                        remove_background(img_path, img_dir, img_file)

        except OSError:
            print('존재하는 디렉토리')
