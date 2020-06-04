import cv2
import numpy as np
import time
import os


def extract_alpha(img_path, img_dir, img_name, label):
    try:
        # 이미지 불러오기
        img = cv2.imread(img_path, 0)

        k = 5

        img = cv2.GaussianBlur(img, (k, k), 0)
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 1000, param1=20, param2=150, minRadius=150,
                                   maxRadius=350)
        # circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100, param1=20, param2=100, minRadius=150, maxRadius=500)
        circles = np.uint16(np.around(circles))

        # 원이 한개일 때
        x, y, r = circles[0][0]
        mask = np.zeros((1080, 1920), dtype=np.uint8)
        mask = cv2.circle(mask, (x, y), r, (255, 255, 255), -1, 8, 0)
        cv2.imwrite(f'data/korea/alpha_data/{img_dir}/{img_name}', cv2.cvtColor(mask, cv2.COLOR_GRAY2RGBA))
        with open(f'data/korea/alpha_data/{img_dir}/{img_name.replace(".png", "")}.txt', 'w') as f:
            f.write(f'{label} {x - r} {y - r} {x + r} {y + r}')

    except Exception as e:
        print(f'Error: {e}')
        print(f'{img_name}')
        print('원이 검출되지 않음')


if __name__ == '__main__':
    path = 'data/korea/original_data/'
    dir_list = list(filter(lambda x: os.path.isdir(path + x), os.listdir(path)))

    for img_dir in dir_list:
        print(f'Dir name : {img_dir}')

        if img_dir == 'won_500_f':
            index = 0
        elif img_dir == 'won_500_b':
            index = 1
        elif img_dir == 'won_100_f_0':
            index = 2
        elif img_dir == 'won_100_b_0':
            index = 3
        elif img_dir == 'won_100_f_1':
            index = 4
        elif img_dir == 'won_100_b_1':
            index = 5
        elif img_dir == 'won_50_f':
            index = 6
        elif img_dir == 'won_50_b':
            index = 7
        elif img_dir == 'won_10_f_0':
            index = 8
        elif img_dir == 'won_10_b_0':
            index = 9
        elif img_dir == 'won_10_f_1':
            index = 10
        elif img_dir == 'won_10_b_1':
            index = 11

        with open('data/korea/data_label.txt', 'a') as f:
            f.write(f'{index} : {img_dir}\n')

        try:
            if not os.path.exists(f'data/korea/alpha_data/{img_dir}'):
                # alpha_data 폴더에 같은 폴더명 생성
                os.mkdir(f'data/korea/alpha_data/{img_dir}')
                start = time.time()
                for img_file in os.listdir(path + img_dir):
                    img_path = f'{path}{img_dir}/{img_file}'
                    extract_alpha(img_path, img_dir, img_file, index)

                print(time.time() - start)
                print('=' * 20)

        except OSError:
            print('존재하는 디렉토리')

# ['won_100_b_0', 'won_100_b_1', 'won_100_f_0', 'won_100_f_1', 'won_10_b_0', 'won_10_b_1', 'won_10_f_0', 'won_10_f_1', 'won_500_b', 'won_500_f', 'won_50_b', 'won_50_f']
