import cv2
import os
import time
import random
import shutil


def image_blending(background_img, foreground_img, alpha_img, save_path, label_file):
    try:
        # 이미지 불러오기
        foreground = cv2.imread(foreground_img, -1)
        background = cv2.imread(background_img, -1)
        alpha = cv2.imread(alpha_img, -1)

        foreground = foreground.astype(float)
        background = background.astype(float)
        background = cv2.resize(background, dsize=(1920, 1080), interpolation=cv2.INTER_AREA)  # 배경 크기 리사이징
        alpha = alpha.astype(float) / 255

        foreground = cv2.multiply(alpha, foreground)
        background = cv2.multiply(1.0 - alpha, background)
        out_image = cv2.add(foreground, background)

        cv2.imwrite(save_path, out_image)

        shutil.copy(label_file, save_path.replace('png', 'txt'))

    except Exception as e:
        print(f'Error: {e}')
        print(foreground_img)
        print(alpha_img)
        print(background_img)
        print(f'{save_path}')


if __name__ == '__main__':
    background_path = 'background/'
    foreground_path = 'data/korea/original_data/'
    alpha_path = 'data/korea/alpha_data/'

    random_seed = [42, 44, 46, 48, 50]

    background_list = list(filter(lambda x: x.endswith('.png'), os.listdir(background_path)))
    foreground_list = list(filter(lambda x: os.path.isdir(foreground_path + x), os.listdir(foreground_path)))
    alpha_list = list(filter(lambda x: os.path.isdir(alpha_path + x), os.listdir(alpha_path)))

    for img_dir in alpha_list:
        try:
            if not os.path.exists(f'data/korea/blend_data/{img_dir}'):
                # blend_data 폴더에 같은 폴더명 생성
                os.mkdir(f'data/korea/blend_data/{img_dir}')
                start = time.time()
                for seed in random_seed:
                    random.seed(seed)  # 난수 시드 설정
                    for alpha_img in list(filter(lambda x: x.endswith('png'), os.listdir(f'{alpha_path}{img_dir}'))):
                        background_img = random.choice(background_list)  # 랜덤한 배경 추출
                        image_blending(f'{background_path}{background_img}',
                                       f'{foreground_path}{img_dir}/{alpha_img}',
                                       f'{alpha_path}{img_dir}/{alpha_img}',
                                       f'data/korea/blend_data/{img_dir}/{alpha_img.replace(".png", "")}_{background_img}',
                                       f'{alpha_path}{img_dir}/{alpha_img.replace("png", "txt")}')

                print(time.time() - start)
                print('=' * 20)

        except OSError:
            print('존재하는 디렉토리')
